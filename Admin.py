import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from tkinter import *
import socket
import sys
import os
import time
import _thread
import threading
import sqlite3
import random
import time
start = True


with sqlite3.connect("users.db") as db:
    cursor = db.cursor()

def SendMessage():
    print(s)
    print(message)
    s.send(message.encode())
    
def RecieveMessage():
    while True :
        global message
        print("I am here")
        message = s.recv(1024).decode()
        print("After decode")
        print(message)
        if not message :
            print("not recieved")
            RecieveMessage()
        print("recieved")
        print(message)
        return message
        break

#connects to the server
s = socket.socket()   
host = '127.0.0.1'
port = 5000
s.connect((host,port))
file = open("username.txt", "r")
user_info = file.readline()
user_info = user_info.split(",")
username = user_info[0]
ID = user_info[1]
print(username)
file.close()
RecieveMessage()
print(message)
to_send = "name change," + "change_name+=-_," + str(message) + "," + str(username) + ",Admin"
s.send(to_send.encode())
RecieveMessage()


class add_user(tk.Toplevel):
    def insert_user(self):
        global message
        #obtains the username and password from the label entries
        add_username = entered_username.get()
        add_password = entered_password.get()

        #this program hashes and salts the password
        password_character_list = list(add_password)
        ascii_password = []
        for i in range(0,len(password_character_list)):
            asci = ord(password_character_list[i])
            asci = asci*8+9*12-4
            ascii_password.append(asci)
            
        word = ""
        for i in range(0,len(ascii_password)):
            word = word + str(ascii_password[i])
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

        final_hash = ""
        for i in range(0,len(hashed_array)):
            final_hash = final_hash + str(hashed_array[i])
        
        role = response.get()
        if role == 0:
            identity = "Client"
        if role == 1:
            identity = "Admin"
        message = "add user," + "useradd_+':;*," + add_username + "," + str(final_hash) + "," + str(num) + "," + identity
        SendMessage()
        self.destroy()
    def __init__(self, parent):
        #sets up a window to add  a new user
        global entered_username
        global entered_password
        global response
        super().__init__(parent)
        self.geometry('300x200')
        self.title('Add a New user')
        entered_username = tk.StringVar()
        entered_password = tk.StringVar()
        response = tk.IntVar()
        username = ttk.Label(self, text= "New User's Username:")
        username.pack(fill='x', expand = True)
        username_entry = ttk.Entry(self, textvariable=entered_username)
        username_entry.pack(fill='x', expand = True)

        password = ttk.Label(self, text="New User's Password:")
        password.pack(fill='x', expand = True)
        password_entry = ttk.Entry(self, textvariable=entered_password)
        password_entry.pack(fill='x', expand = True)

        check_box = ttk.Checkbutton(self, text = "Admin?", variable=response)
        check_box.pack()

        enter_button = ttk.Button(self, text="Enter", command = self.insert_user)
        enter_button.pack(fill='x', expand=True, pady=10)

        exit_button = ttk.Button(self, text = "Exit", command=self.destroy)
        exit_button.pack(fill='x', expand = True, pady=10)

class delete_user(tk.Toplevel):
    def send_delete_clicked(self):
        #Handles request to delete a user
        global username
        global message
        global list_box
        user = ""
        name= ""
        name = list_box.get(ANCHOR)
        name_list = name.split(" ")
        #checks if name has any spaces in it and then accounts for it when getting the user name
        if name != ""
            if len(name_list) > 2:
                for i in range(0,len(name_list)-1):
                    user = user + str(name_list[i]) + ""
            if len(name_list) == 2:
                user = name_list[0]
            userID = name_list[len(name_list)-1]
            print(user)
            print(userID)
            message = "delete user," + "userdelt[{!£&^87," + user + "," + userID
            SendMessage()
            RecieveMessage()
            #Recieves a message to check that the deletion took place or if the user is currently logged in
            if message == "logged in":
                tkinter.messagebox.showinfo(title="Error", message="This user is currently logged in")
            else:
                tkinter.messagebox.showinfo(title="Complete", message="Succesfully deleted")
            message = "list of users," + "getlist*&^%$£{}," + username
            SendMessage()
            RecieveMessage()
            #obtians the updated user list and modiefies the current list
            user_list = message.split(",")
            RecieveMessage()
            IDs = message.split(",")
            list_box.delete(0, END)
            print(user_list)
            for i in range(0,len(user_list)-1):
                if user_list[i] == username and IDs[i] == ID:
                    print("Nope")
                else:
                    insert = (user_list[i]) + " " + (IDs[i])
                    list_box.insert(END, insert)


    def search_clicked(self):
        global entered_username
        global IDs
        global user_list
        global list_box
        print("Here are the IDS")
        print(IDs)
        search_letters = [[]]
        search = str(entered_username.get())
        if search != "":
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
        print("here")
        global message
        global list_box
        global IDs
        global user_list
        global entered_username
        super().__init__(parent)
        entered_username = tk.StringVar()
        self.geometry('300x200')
        self.title('Delete a User')
        message = "list of users," + "getlist*&^%$£{}," + username
        SendMessage()
        RecieveMessage()
        print(message)
        self.geometry('400x500')
        self.title('Delete User')
        list_box = tk.Listbox(self)
        scroll = Scrollbar(self, orient=VERTICAL)
        list_box = Listbox(self, width=50, yscrollcommand=scroll.set)
        scroll.config(command = list_box.yview)
        scroll.pack(side=RIGHT, fill = Y)
        list_box.pack(pady=10)
        user_list = message.split(",")
        RecieveMessage()
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
                
        enter_button = ttk.Button(self, text="Select", command=self.send_delete_clicked)
        enter_button.pack(fill='x', expand=True, pady=10)

        search_button = ttk.Button(self, text="Search for a user", command=self.search_clicked)
        search_button.pack(fill='x', expand=True, pady=10)

        exit_button = ttk.Button(self, text = "Exit", command=self.destroy)
        exit_button.pack(fill='x', expand = True, pady=10)


class which_details(tk.Toplevel):
    def username_response(self):
        global j
        global new_username
        global new_username_check
        global username_window
        if j == 0:
            j += 1
            new_username = tk.StringVar()
            new_username_check = tk.StringVar()
            
            username_window = tk.Toplevel(self)
            username_window.title('Username Change')
            username_window.geometry('300x300')

            username_label = ttk.Label(username_window, text = "New Username")
            username_label.pack(fill='x', expand=True)
            username_entry = ttk.Entry(username_window, textvariable=new_username)
            username_entry.pack(fill='x', expand=True)

            username_label = ttk.Label(username_window, text = "New Username Again")
            username_label.pack(fill='x', expand=True)
            username_entry = ttk.Entry(username_window, textvariable=new_username_check)
            username_entry.pack(fill='x', expand=True)

            enter_button = ttk.Button(username_window, text="Enter", command=self.username_enter_clicked)
            enter_button.pack(fill='x', expand=True, pady=10)

            exit_button = ttk.Button(username_window, text="Exit", command=self.username_window_destroy)
            exit_button.pack(fill='x', expand=True, pady=10)
            
    def username_enter_clicked(self):
        global new_username
        global new_username_check
        global message
        global list_box
        username_1 = new_username.get()
        username_2 = new_username_check.get()
        current = list_box.get(ANCHOR)
        if username_1 != "" and username_2 != "":
            current_list = current.split(" ")
            current_username = current_list[1]
            if len(current_list) > 2:
                for i in range(1,len(current_list)-1):
                    current_username = current_username + " " + current_list[i] 
            if len(current_list) == 2:
                current_username = current_list[0]
            print(current_username)
            current_ID = current_list[len(current_list)-1]
            if username_1 != username_2:
                tkinter.messagebox.showinfo(title="Error", message="Make sure both entered usernames are the same")
            if username_1 == username_2:
                print("sending")
                message = "username change," + "UserChange56£$%^&26," + username_1 + "," + current_username + "," + current_ID
                print("message")
                SendMessage()
                RecieveMessage()
                if message == "logged in":
                    tkinter.messagebox.showinfo(title="Error", message="This user is currently logged in")
                else:
                    tkinter.messagebox.showinfo(title="Complete", message="Username changed")
            message = "list of users," + "getlist*&^%$£{}," + username
            SendMessage()
            RecieveMessage()
            user_list = message.split(",")
            RecieveMessage()
            IDs = message.split(",")
            list_box.delete(0, END)
            print(user_list)
            for i in range(0,len(user_list)-1):
                if user_list[i] == username and IDs[i] == ID:
                    print("Nope")
                else:
                    insert = (user_list[i]) + " " + (IDs[i])
                    list_box.insert(END, insert)
            j = 0
            username_window.destroy()

    def username_window_destroy(self):
        global j
        global username_window
        j = 0
        username_window.destroy()

    def password_window_destroy(self):
        global j
        global password_window
        j = 0
        password_window.destroy()

    def password_response(self):
        global j
        global new_password
        global new_password_check
        global password_window
        if j == 0:
            new_password = tk.StringVar()
            new_password_check = tk.StringVar()

            password_window = tk.Toplevel(self)
            password_window.title('Password Change')
            password_window.geometry('300x300')

            password_label = ttk.Label(password_window, text = "New Password")
            password_label.pack(fill='x', expand=True)
            password_entry = ttk.Entry(password_window, textvariable=new_password)
            password_entry.pack(fill='x', expand=True)

            password_label = ttk.Label(password_window, text = "New Password")
            password_label.pack(fill='x', expand=True)
            password_entry = ttk.Entry(password_window, textvariable=new_password_check)
            password_entry.pack(fill='x', expand=True)

            enter_button = ttk.Button(password_window, text="Enter", command=self.password_enter_clicked)
            enter_button.pack(fill='x', expand=True, pady=10)

            exit_button = ttk.Button(password_window, text="Exit", command=self.password_window_destroy)
            exit_button.pack(fill='x', expand=True, pady=10)

    def password_enter_clicked(self):
        global new_password
        global new_password_check
        global message
        global list_box
        current = list_box.get(ANCHOR)
        new_pass_1 = new_password.get()
        password_2 = new_password_check.get()
        if new_pass_1 != "" and password_2 != "":
            current_list = current.split(" ")
            username = current_list[0]
            if len(current_list) > 2:
                for i in range(1,len(current_list)-1):
                    username = username + " " + current_list[i] 
            if len(current_list) == 2:
                username = current_list[0]
            ID = current_list[len(current_list)-1]
            print(username)

            new_pass_1 = new_password.get()
            password_2 = new_password_check.get()

            if new_pass_1 != password_2:
                tkinter.messagebox.showinfo(title="Error", message="Make sure both entered passwords are the same")
                
            if new_pass_1 == password_2:
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
                    
                message = "password change," + "changePas@/?#:;," + str(new_pass_1) + "," + str(num) + "," + str(username) + "," + str(ID) + "," + "Admin: other user"
                SendMessage()
                RecieveMessage()
                if message == "logged in":
                    tkinter.messagebox.showinfo(title="Error", message="This user is currently logged in")
                else:
                    tkinter.messagebox.showinfo(title="Complete", message="Password has been changed")
                message = "list of users," + "getlist*&^%$£{}," + username
                SendMessage()
                RecieveMessage()
                user_list = message.split(",")
                RecieveMessage()
                IDs = message.split(",")
                print(user_list)
                list_box.delete(0,END)
                for i in range(0,len(user_list)-1):
                    insert = (user_list[i]) + " " + (IDs[i])
                    list_box.insert(END, insert)
                j = 0
                password_window.destroy()

    def search_clicked(self):
        global entered_username
        global IDs
        global user_list
        global list_box
        print("Here are the IDS")
        print(IDs)
        search_letters = [[]]
        search = str(entered_username.get())
        if search != "":
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
                insert = user_list[num] + " " + IDs[num]
                list_box.insert(END,insert)
                
            
           
    def __init__(self, parent):
        global j
        j = 0
        super().__init__(parent)
        global message
        global IDs
        global list_box
        global user_list
        global entered_username
        self.geometry('300x500')
        self.title('Username or Password')
        header = ttk.Label(self, text="Pick what you would like to change")
        header.pack(fill='x', expand=True)
        entered_username = tk.StringVar()
        list_box = tk.Listbox(self)
        scroll = Scrollbar(self, orient=VERTICAL)
        list_box = Listbox(self, width=50, yscrollcommand=scroll.set)
        scroll.config(command = list_box.yview)
        scroll.pack(side=RIGHT, fill = Y)
        list_box.pack(pady=10)
        message = "list of users," + "getlist*&^%$£{}," + username
        SendMessage()
        RecieveMessage()
        user_list = message.split(",")
        RecieveMessage()
        IDs = message.split(",")
        print(user_list)
        for i in range(0,len(user_list)-1):
            if user_list[i] == username and IDs[i] == ID:
                print("Nope")
            else:
                insert = (user_list[i]) + " " + (IDs[i])
                list_box.insert(END, insert)

        username_label = ttk.Label(self, text = "Username:")
        username_label.pack(fill='x', expand=True)
        username_entry = ttk.Entry(self, textvariable=entered_username)
        username_entry.pack(fill='x', expand=True)

        username_button = ttk.Button(self, text="Change Username", command =self.username_response)
        username_button.pack(fill='x', expand=True, pady=10)

        password_button = ttk.Button(self, text="Change Password", command = self.password_response)
        password_button.pack(fill='x', expand=True, pady=10)

        search_button = ttk.Button(self, text="Search for a user", command=self.search_clicked)
        search_button.pack(fill='x', expand=True, pady=10)

        exit_button = ttk.Button(self, text = "Exit", command=self.destroy)
        exit_button.pack(fill='x', expand = True, pady=10)


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
            message = "password change," + "changePas@/?#:;," + str(username) + "," + str(current) + "," + str(new_pass_1) + "," + str(num) + "," + "Admin: own pass" + "," + str(ID)
            print(message)
            SendMessage()
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
        exit_button = ttk.Button(self, text="Exit", command=self.destroy)
        exit_button.pack(fill='x', expand = True, pady=10)
                
class main(tk.Tk):
    #This sets up the initial window and the functions which will bring up the associated window for when each button is pressed
    def log_out_clicked(self):
        message = "logout," + ":;@'~#," + username
        s.send(message.encode())
        time.sleep(1)
        s.close()
        root.destroy()
    def add_user_clicked(self):
        window = add_user(self)
        window.grab_set()
    def delete_user_clicked(self):
        window = delete_user(self)
        window.grab_set()
    def change_user_details_clicked(self):
        window = which_details(self)
        window.grab_set()
    def change_password_clicked(self):
        window = change_password(self)
        window.grab_set()
        print("I'm working too!")
    def __init__(self):
        super().__init__()
        self.geometry('300x250')
        self.title('Main Page')

        add_user_button = ttk.Button(self, text="Add a user", command=self.add_user_clicked)
        add_user_button.pack(fill='x', expand= True, pady=10)

        delete_user_button = ttk.Button(self, text="Delete a User", command=self.delete_user_clicked)
        delete_user_button.pack(fill='x', expand = True, pady=10)

        change_user_details_button = ttk.Button(self, text="Change a User's Details", command=self.change_user_details_clicked)
        change_user_details_button.pack(fill='x', expand = True, pady=10)

        change_password_button = ttk.Button(self, text="Change Password", command=self.change_password_clicked)
        change_password_button.pack(fill='x', expand=True, pady=10)

        logout_button = ttk.Button(self, text="Logout", command=self.log_out_clicked)
        logout_button.pack(fill='x', expand = True, pady=10)

__name__= "__main__"
if __name__== "__main__":
    root = main()
    root.mainloop()

