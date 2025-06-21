import socket
import rsa
import _thread
import threading
import random
import sys
import os
import tkinter as tk
from tkinter import *
import time
from tkinter import ttk
import tkinter.messagebox 
import time
import sqlite3
global Flag
Flag = True
global privatekey


start = True
def SendMessage(message):
    s.send(message.encode())

def RecieveMessage():
    check = []
    checker = 0
    #listens for messages from the server
    global message
    global text_widget
    message = s.recv(1024).decode()
    while message == "":
        RecieveMessage()
    else:
        return message

            
global s
global username
#connects to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
host = '127.0.0.1'
port = 5000
s.connect((host,port))
time.sleep(1)
file = open("username.txt", "r")
user_info = file.read()
user_info = user_info.split(",")
username = user_info[0]
ID = user_info[1]
print(username)
print(ID)
file.close()
RecieveMessage()
print(message)
to_send = "name change," + "change_name+=-_," + str(message) + "," + str(username) + "," + "Client," + str(ID)
print(to_send)
s.send(to_send.encode())
print("success!")
Flag = True
RecieveMessage()

privatekey = ""


file_exists = os.path.exists("private" + username + ID)
print(file_exists)

if file_exists == True:
    file = open("private" + username + ID, "rb")
    privatekey = file.read()
    print(privatekey)
    privatekey = rsa.key.PrivateKey.load_pkcs1(privatekey, format='PEM')
    print(type(privatekey))
    file.close()

if file_exists == False:
    print("at keys")
    public, privatekey = rsa.newkeys(1024)
    print(public)
    print(privatekey)
    print("HERE ARE KEYS")
    test = "test"
    encoded = rsa.encrypt(test.encode(), public)
    decoded = rsa.decrypt(encoded, privatekey).decode()

    print(test)
    print(encoded)
    print(decoded)
    a = privatekey.save_pkcs1(format='PEM')
    print(public)
    print(type(privatekey))
    public = public.save_pkcs1(format='PEM')
    print(public)
    print(type(public))
    message = "keys!" + "key%^&*()!" + username + "!" + str(ID) + "!" + "key insert"
    SendMessage(message)
    s.send(public)
    file = open("private" + username + ID, "wb")
    file.write(a)
    print(privatekey)
    print(type(privatekey))
    file.close()



    

with sqlite3.connect("Messages.db",  check_same_thread=False) as db:
    cursor = db.cursor()
#Checks if the table exists, and if it doesn't creates the table

cursor.execute('''
CREATE TABLE IF NOT EXISTS Messages(
Main_user VARCHAR(20) NOT NULL,
Main_user_ID VARCHAR(20) NOT NULL,
recipient VARCHAR(20) NOT NULL,
recipientID VARCHAR(20) NOT NULL,
messages VARCHAR(20) NOT NULL);
''')


class change_password(tk.Toplevel):
    global message
    global username
    def send_new_password(self):
        global message
        global ID
        current = current_password.get()
        new_pass_1 = new_password_1.get()
        new_pass_2 = new_password_2.get()
        if new_pass_1 != new_pass_2:
            tkinter.messagebox.showinfo(title="Error", message="Passwords are not correct, please make sure you've entered the new password in correctly")

        if new_pass_1 == new_pass_2:
            new_pass_list = list(new_pass_1)
            values = []
            for i in range(0,len(new_pass_list)):
                asci = ord(new_pass_list[i])
                asci = asci*8+9*12-4
                values.append(asci)
            word = ""
            for i in range(0,len(values)):
                word = word + str(values[i])
            length = list(word)
            number = 1
            for i in range(0,len(word)-1):
                number = number*10
            second_number = (number*10)-1

            num = random.randint(number,second_number)
            numbers = list(str(num))
            hashed_array = []
            for i in range(0,len(numbers)):
                hashed_array.append(int(length[i])*int(numbers[i]))
            new_pass_1 = ""
            for i in range(0,len(hashed_array)):
                new_pass_1 = new_pass_1 + str(hashed_array[i])

            values = []
            word = ""
            current_pass_list = list(current)
            for i in range(0,len(current_pass_list)):
                asci = ord(current_pass_list[i])
                asci = asci*8+9*12-4
                values.append(asci)
                
            for i in range(0,len(values)):
                word = word + str(values[i])
            current = word
            print(current)
            print(num)
            message = "password change," + "changePas@/?#:;," + str(username) + "," + str(current) + "," + str(new_pass_1) + "," + str(num) + "," + "Client" + "," + str(ID)
            print(message)
            SendMessage(message)
            RecieveMessage()
            print(message)
            if message == "Done":
                tkinter.messagebox.showinfo(title="Finished", message="Password has been successfuly changed")
            if message == "not-found":
                tkinter.messagebox.showinfo(title="Error", message="Current password is uncorrect, make sure it was entered correctly")
            self.destroy()
            
    def __init__(self, parent):
        global current_password
        global new_password_1
        global new_password_2
        super().__init__(parent)
        self.geometry('300x220')
        self.title('Change Password')
        current_password = tk.StringVar()
        new_password_1 = tk.StringVar()
        new_password_2 = tk.StringVar()
        
        currentpassword = ttk.Label(self, text = "Current Password:")
        currentpassword.pack(fill='x', expand = True)
        currentpassword_entry = ttk.Entry(self, textvariable=current_password)
        currentpassword_entry.pack(fill='x', expand=True)

        newpassword_1 = ttk.Label(self, text = "New Password:")
        newpassword_1.pack(fill='x', expand = True)
        newpassword_1_entry = ttk.Entry(self, textvariable=new_password_1)
        newpassword_1_entry.pack(fill='x', expand=True)

        newpassword_2 = ttk.Label(self, text = "New Password Again:")
        newpassword_2.pack(fill='x', expand = True)
        newpassword_2_entry = ttk.Entry(self, textvariable=new_password_2)
        newpassword_2_entry.pack(fill='x', expand=True)
        
        enter2_button = ttk.Button(self, text="Enter", command=self.send_new_password)
        enter2_button.pack(fill='x', expand=True, pady=10)
        exit_button = ttk.Button(self, text="Back", command=self.destroy)
        exit_button.pack(fill='x', expand = True, pady=10)

def check_for_messages():
    global recipient
    global recipientID
    global text_widget
    global username
    global list_all_messages
    global ID
    global message
    global Flag
    global privatekey
    if Flag == True:
        print("working")
        sending = "message_handler," + "messagehandle647&^%$," + username + "," + ID + "," + recipient + "," + recipientID + ",Ignore" + ",checking"
        s.send(sending.encode())
        RecieveMessage()
        print("here is the recieved message")
        print(message)
        if message != "False":
            for i in range(0,int(message)):
                message = s.recv(1024)
                print(message)
                print(type(message))
                print("decrypting")
                print(privatekey)
                print(type(privatekey))
                text_widget.config(state=NORMAL)
                while True:
                    try:
                        recieved = rsa.decrypt(message, privatekey).decode()
                        break
                    except:
                        _thread.start_new_thread(check_for_messages,())
                        sys.exit()
                insert = recipient + str(recipientID) + ": " + str(recieved)
                list_all_messages = str(list_all_messages) + "newmessage$%^&*()" + insert
                text_widget.insert(tk.END, insert + '\n')
                text_widget.config(state=DISABLED)
                print(list_all_messages)
            if list_all_messages == "":
                cursor.execute('INSERT INTO Messages (Main_user, Main_user_ID, recipient, recipientID, messages) VALUES (?,?,?,?,?)', (username,ID, recipient, recipientID, str(list_all_messages)))
                db.commit()
            else:
                cursor.execute("UPDATE Messages SET messages = ? WHERE Main_user = ? AND Main_user_ID = ? AND recipient = ? AND recipientID = ?", (str(list_all_messages),username, ID, recipient, recipientID))
                db.commit()
            _thread.start_new_thread(check_for_messages,())
            sys.exit()
        else:
            _thread.start_new_thread(check_for_messages,())
            sys.exit()
    if Flag == False:
        sys.exit()
        

    

class message_users(tk.Toplevel):
    def enter_clicked(self):
        global entered_message
        global message_window
        global text_widget
        global recipient
        global username
        global ID
        global recipientID
        global list_all_messages
        global messages
        global message
        global Flag
        global recipientkey
        Flag = False
        print("here")
        recipient = ""
        messages = ""
        row = ""
        messages_array = ""
        name = ""
        list_all_messages = ""
        name = list_box.get(ANCHOR)
        if name != "":
            name_list = name.split(" ")
            recipient = name_list[0]
            if len(name_list) > 2:
                for i in range(1,len(name_list)-1):
                    recipient = recipient + str(name_list[i]) + " "
            if len(name_list) == 2:
                recipient = name_list[0]
            recipientID = name_list[len(name_list)-1]
            messages_array = []
            message = "keys!" + "key%^&*()!" + recipient + "!" + recipientID + "!get key" + "!ignore"
            SendMessage(message)
            message = s.recv(1024)
            print(message)
            print(type(message))
            recipientkey = rsa.key.PublicKey.load_pkcs1(message, format='PEM')
            print("recipientkey")
            print(type(recipientkey))
            print(recipientkey)
            print(message)
            
            message_window = tk.Toplevel(self)
            entered_message = tk.StringVar()
            message_window.title('Messaging')
            message_window.geometry('300x300')

            text_widget = tk.Text(message_window, height = 10, width = 60)
            text_widget.pack()
            text_widget.config(state=DISABLED)
            
            message_label = ttk.Label(message_window, text = "")
            message_label.pack(fill='x', expand=True)
            message_entry = ttk.Entry(message_window, textvariable=entered_message)
            message_entry.pack(fill='x', expand=True)

            enter_button = ttk.Button(message_window, text="Message", command=self.message_enter_clicked)
            enter_button.pack(fill='x', expand=True, pady=10)

            exit_button = ttk.Button(message_window, text="Exit", command=self.message_window_destroy)
            exit_button.pack(fill='x', expand=True, pady=10)
            message = ""
            for row in cursor.execute('SELECT messages FROM Messages WHERE Main_user = ? AND Main_user_ID = ? AND recipient = ? AND recipientID = ?', (username, ID, recipient,recipientID,)):
                row = str(row)
                print("here is row")
                print(row)
                row_list_1 = row.rsplit("'", 1)
                print(row_list_1)
                row_list_1 = str(row_list_1[0])
                row_list = row_list_1.split("'", 1)
                print(row_list)
                while True:
                    try:
                        print("here is row list")
                        print(row_list)
                        list_all_messages = row_list[1]
                        break
                    except:
                        print("here is exception")
                        row_list_1 = row.rsplit('"', 1)
                        print(row_list_1)
                        row_list_1 = str(row_list_1[0])
                        print(row_list_1)
                        row_list = row_list_1.split('"', 1)
                        print(row_list)
                    
            print(row)
            print("existstance")
            print(list_all_messages)
            if row != "":
                messages_list = list_all_messages.split("newmessage$%^&*()")
                if len(messages_list) > 0:
                    print(messages_list)
                    text_widget.config(state=NORMAL)
                    for i in range(0,len(messages_list)):
                        text = messages_list[i]
                        text_widget.insert(tk.END, text + '\n')
                    text_widget.config(state=DISABLED)
                    
            Flag = True
            _thread.start_new_thread(check_for_messages,())

    def message_window_destroy(self):
        global message_window
        global Flag
        Flag = False
        message_window.destroy()
                   
        
    def message_enter_clicked(self):
        global entered_message
        global message
        global Flag
        global recipient
        global recipientID
        global messages
        global text_widget
        global username
        global ID
        global recipientkey
        global list_all_messages
        row = ""
        Flag = False
        original = str(entered_message.get())
        print(list_all_messages)
        if original != "":
            print(type(recipientkey))
            to_send = rsa.encrypt(original.encode(), recipientkey) 
            print("here is the recipient ID " + recipientID)
            to_another_user = "message_handler," + "messagehandle647&^%$," + username + "," + ID + "," + str(recipient) + "," + str(recipientID) + "," + "sending" + ",ignore"
            print(to_another_user)
            print("Check here please at send")
            s.send(to_another_user.encode())
            time.sleep(0.3)
            s.send(to_send)
            original = username + ID + ": " + str(original)
            if list_all_messages == "":
                list_all_messages = original
            else:
                list_all_messages = list_all_messages + "newmessage$%^&*()" + original
            print(list_all_messages)
            text_widget.config(state=NORMAL)
            print(to_send)
            text_widget.insert(tk.END, original + '\n')
            text_widget.config(state=DISABLED)
            if row == "":
                cursor.execute('INSERT INTO Messages (Main_user, Main_user_ID, recipient, recipientID, messages) VALUES (?,?,?,?,?)', (username,ID, recipient, recipientID, str(list_all_messages)))
                db.commit()
            else:
                cursor.execute("UPDATE Messages SET messages = ? WHERE Main_user = ? AND Main_user_ID = ? AND recipient = ? AND recipientID = ?", (str(list_all_messages), username, ID, recipient, recipientID,))
                db.commit()
        Flag = True
        _thread.start_new_thread(check_for_messages,())
        
        
    
    def search_clicked(self):
        global entered_username
        global IDs
        global user_list
        global list_box
        print("Here are the IDS")
        print(IDs)
        search_letters = [[]]
        search = str(entered_username.get())
        search_list = list(search)
        for i in range(0,len(user_list)-1):
            put_in = list(user_list[i])
            for j in range(0,len(put_in)):
                search_letters[i].append(put_in[j])
            search_letters.append([])
        numbers = []
        not_numbers = []
        for i in range(0,len(search_letters)-1):
            k = 0
            for j in range(0,len(search_list)):
                if search_letters[i][j] == search_list[k] and i not in numbers:
                    numbers.append(i)
                if search_letters[i][j] != search_list[k] and i not in not_numbers:
                    not_numbers.append(i)
                    break
        list_box.delete(0, END)
        for i in range(0,len(numbers)):
            num = numbers[i]
            if user_list[num] == username and IDs[num] == ID:
                print("Nope")
            else:
                insert = user_list[num] + " " + IDs[num]
                list_box.insert(END,insert)
            
                
    def __init__(self, parent):
        global username
        global IDs
        global entered_username
        global message
        global user_list
        global list_box
        user_list = ""
        entered_username = tk.StringVar()
        message = "list of users," + "getlist*&^%$£{}," + username
        SendMessage(message)
        RecieveMessage()
        print(message)
        print("here")
        super().__init__(parent)
        self.geometry('400x500')
        self.title('Message')
        list_box = tk.Listbox(self)
        scroll = Scrollbar(self, orient=VERTICAL)
        list_box = Listbox(self, width=50, yscrollcommand=scroll.set)
        scroll.config(command = list_box.yview)
        scroll.pack(side=RIGHT, fill = Y)
        list_box.pack(pady=10)
        user_list = message.split(",")
        print("now ehere")
        RecieveMessage()
        print("and here")
        IDs = message.split(",")
        print(user_list)
        for i in range(0,len(user_list)):
            if user_list[i] == username and IDs[i] == ID:
                print("Nope")
            else:
                insert = (user_list[i]) + " " + (IDs[i])
                list_box.insert(END, insert)
            
        username_label = ttk.Label(self, text = "Username:")
        username_label.pack(fill='x', expand=True)
        username_entry = ttk.Entry(self, textvariable=entered_username)
        username_entry.pack(fill='x', expand=True)
        
        enter_button = ttk.Button(self, text="Select", command=self.enter_clicked)
        enter_button.pack(fill='x', expand=True, pady=10)

        search_button = ttk.Button(self, text="Search for a user", command=self.search_clicked)
        search_button.pack(fill='x', expand=True, pady=10)

        exit_button = ttk.Button(self, text="Exit", command=self.destroy)
        exit_button.pack(fill='x', expand=True, pady=10)



class main(tk.Tk):
    def logout_clicked(self):
        message = "logout," + ":;@'~#," + username
        s.send(message.encode())
        time.sleep(1)
        s.close()
        root.destroy()

    def change_password_clicked(self):
        window = change_password(self)
        window.grab_set()
        print("I'm working too!")

    def message_clicked(self):
        window = message_users(self)
        window.grab_set()
        print("I'm working too!")
            
    def __init__(self):
        print("hello")
        super().__init__()
        self.geometry('300x200')
        self.title('Main Page')

        message_button = ttk.Button(self, text="Send a Message", command=self.message_clicked)
        message_button.pack(fill='x', expand=True, pady=10)

        change_password_button = ttk.Button(self, text="Change Password", command=self.change_password_clicked)
        change_password_button.pack(fill='x', expand=True, pady=10)

        logout_button = ttk.Button(self, text="Log out", command=self.logout_clicked)
        logout_button.pack(fill='x', expand=True, pady=10)
        print("All the way here")


__name__ = "__main__"
if __name__ == "__main__":
    print("currently here")
    root = main()
    root.mainloop()
