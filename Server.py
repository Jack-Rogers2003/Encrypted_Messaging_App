import _thread
import rsa
import socket
import threading
import sqlite3
import random
import sys
import os.path
global lock
global online
Flag = True
online = []
temp = []
connections = []
i = 0
lock = threading.Lock()
array = []

#Connects to the users database

with sqlite3.connect("users.db",  check_same_thread=False) as db:
    cursor = db.cursor()


#Checks if the table exists, and if it doesn't creates the table

cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
Username VARCHAR(20) NOT NULL,
User_ID VARCHAR(20) NOT NULL,
Password VARCHAR(20) NOT NULL,
Password_Check VARCHAR(20) NOT NULL,
Public_Key VARCHAR(20),
Identity VARCHAR(20) NOT NULL);
''')


#Creats a socket to connect to

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# piece of code to allow IP address & Port
host="127.0.0.1"
port=5000
s.bind((host,port))
print("success!")
s.listen(5)
i = 0
array = []

#Shows users within the database

for row in cursor.execute('SELECT * FROM users'):
        array.append(row)
print(array)

#login function


def handle_message(conn):
        message = conn.recv(1024).decode()
        print("message recieved")
        print(message)
        check = message.split(",")
        print(check)
        if check[0] == "login" and check[1] == "!£$%qwert":
                _thread.start_new_thread(login,(message,conn,check,))
                sys.exit()
        if check[0] == "logout" and check[1] == ":;@'~#":
                _thread.start_new_thread(logout,(conn,check,))
                sys.exit()
        if check[0] == "name change" and check[1] == "change_name+=-_":
                _thread.start_new_thread(name_change,(check,conn,message,))
                sys.exit()
        if check[0] == "password change" and check[1] == "changePas@/?#:;":
                _thread.start_new_thread(password_change, (check,conn,))
                sys.exit()
        if check[0] == "add user" and check[1] == "useradd_+':;*":
                _thread.start_new_thread(add_user,(conn,check))
                sys.exit()
        if check[0] == "delete user" and check[1] == "userdelt[{!£&^87":
                _thread.start_new_thread(delete_user,(message,conn,check,))
                sys.exit()
        if check[0] == "list of users" and check[1] == "getlist*&^%$£{}":
                _thread.start_new_thread(user_list, (conn,check,))
                sys.exit()
        if check[0] == "message_handler" and check[1] == "messagehandle647&^%$":
                _thread.start_new_thread(message_handler,(conn,check,))
                sys.exit()
        if check[0] == "username change" and check[1] == "UserChange56£$%^&26":
                _thread.start_new_thread(user_name_change,(conn,check,))
                sys.exit()
        check = message.split("!")
        if check[0] == "keys" and check[1] == "key%^&*()":
                _thread.start_new_thread(key_handler,(message,conn,check,))
                sys.exit()
                
                
def login(message,conn,check):
    global lock
    q = ""
    pass_array = []
    password_check_array = []
    array2 = []
    identity_array = []
    username = (check[2])
    final_hash = ""
    real_password = ""
    role = ""
    print(username)
    #Searches for where the username sent is the same as one in the database, and then select the password it is associated with
    try:
            lock.acquire(True)
            for row in cursor.execute('SELECT Password FROM users WHERE Username = ?', (username,)):
                print(row)
                password = str(row)
                array2 = password.split("'")
                print(array2)
                pass_array.append(array2[1])
                print(pass_array)
                print("passarray")
    finally:
            lock.release()
    try:
            lock.acquire(True)
            for row in cursor.execute('SELECT Identity FROM users WHERE Username = ?', (username,)):
                print(row)
                role = str(row)
                array2 = role.split("'")
                print(array2)
                identity = array2[1]
                identity_array.append(identity)
    finally:
            lock.release()
    try:
            lock.acquire(True)
            for row in cursor.execute('SELECT Password_Check FROM users WHERE Username = ?', (username,)):
                print(row)
                pass2 = str(row)
                array2 = pass2.split("'")
                print(array2)
                password_check_array.append(array2[1])
                print(password_check_array)
    finally:
            lock.release()

    if len(array2) != 0:
        print("not 0")
        for i in range(0,len(pass_array)):
                real_password = pass_array[i]
                role = identity_array[i]
                password = check[3]
                pass1 = list(password)
                pass2 = list(password_check_array[i])
                print(pass1)
                print(pass2)
                if len(pass1) == len(pass2):
                        hashed_array = []
                        for i in range(0,len(pass2)):
                                hashed_array.append(int(pass1[i])*int(pass2[i]))
                        print(hashed_array)
                        final_hash = ""
                        for i in range(0,len(hashed_array)):
                                final_hash = str(final_hash) + str(hashed_array[i])
                        print(final_hash)
                        print("here is the final hash")
                if final_hash == real_password:
                    try:
                            lock.acquire(True)
                            for row in cursor.execute('SELECT User_ID FROM users WHERE Username = ? AND PASSWORD = ?', (username,final_hash)):
                                row = str(row)
                                array2 = row.split("'")
                                ID = array2[1]
                                message = "found," + role + "," + str(ID)
                            break
                    finally:
                            lock.release()
                if final_hash != real_password:
                        print("no here!")
                        message = "not-found"
                else:
                        message = "not-found"
        for i in range(0,len(online)):
                if online[i][0] == username and online[i][2] == ID:
                        message = "logged in"
                        break
        print(message)
    if len(array2) == 0:
        message = "not-found"
        print(message)
    send(message,conn)
    _thread.start_new_thread(handle_message,(conn,))
    print("hello I am here")
    sys.exit()
    print("Thread is ended now")


def logout(conn,check):
        disconnect = ""
        global online
        print(online)
        for i in range(0,len(online)):
                print("here")
                disconnect = online[i][1]
                print(disconnect)
                if online[i][0] == check[2]:
                        online.pop(i)
        sys.exit()
        conn.close()
        
def name_change(check,conn,message):
        global lock
        global online
        print("At name change")
        print(online)
        print(check)
        for i in range(0,len(temp)):
                s = temp[i][1]
                n = check[3]
                if str(temp[i][0]) == str(check[2]):
                        if check[4] == "Client":
                                ID = check[5]
                                online.append([n,s,ID])
                        else:
                                online.append([n,s])
                        print(online)
                        num = len(online)-1
                        print("name changing")
                        print(message)
                        send(message,conn)
                        break
                if temp[i][0] != check[2]:
                        print("not found")
        _thread.start_new_thread(handle_message,(conn,))
        sys.exit()

def password_change(check,conn):
        global lock
        array = []
        print("at pass change")
        print(check)
        if check[6] == "Client" or check[6] == "Admin: own pass":
                username = check[2]
                password = check[3]
                ID = check[7]
                full_password = []
                code = []
                pass1 = []
                try:
                        lock.acquire(True)
                        for row in cursor.execute("SELECT Password_Check FROM users WHERE Username = ? AND User_ID = ?", (username,ID,)):
                                print(row)
                                row = str(row)
                                row_split = row.split("'")
                                print(row_split)
                                code.append(row_split[1])
                        for row in cursor.execute("SELECT Password FROM users WHERE Username = ? AND User_ID = ?", (username,ID,)):
                                row = str(row)
                                row_split = row.split("'")
                                pass1.append(row_split[1])
                        for i in range(0,len(pass1)):
                                        num1 = list(password)
                                        print(num1)
                                        num2 = list(code[i])
                                        print(num2)
                                        for j in range(0,len(num1)):
                                                full_password.append(int(num1[j])*int(num2[j]))
                                        final_hash = ""
                                        for j in range(0,len(num1)):
                                                final_hash = final_hash + str(full_password[j])
                        for i in range(0,len(pass1)):
                                print("hey!")
                                print(final_hash)
                                if pass1[i] == final_hash:
                                        print(pass1[i])
                                        new_password = check[4]
                                        num = check[5]
                                        cursor.execute('UPDATE users SET Password = ? WHERE Username = ? AND User_ID = ?', (new_password,username,ID,))
                                        db.commit()
                                        cursor.execute('UPDATE users SET Password_Check = ? WHERE Username = ? AND User_ID = ?', (num,username,ID,))
                                        db.commit()
                                        print("complete")
                                        message = "Done"
                                        break
                                if pass1[i] != final_hash:
                                        message = "not-found"
                        send(message,conn)
                finally:
                        lock.release()
        if check[6] == "Admin: other user":
                username = check[4]
                ID = check[5]
                password = check[2]
                second_pass = check[3]
                for i in range(0,len(online)):
                        if online[i][0] == username and online[i][2] == ID:
                                message = "logged in"
                                break
                        else:
                                message = "Fine"
                if message == "Fine":
                        try:
                                lock.acquire(True)
                                cursor.execute('UPDATE users SET Password = ? WHERE Username = ? AND User_ID = ?', (password,username,ID))
                                db.commit()
                                cursor.execute('UPDATE users SET Password_Check = ? WHERE Username = ? AND User_ID = ?', (second_pass,username,ID))
                                db.commit()
                        finally:
                                lock.release()
                        print("finished pass change")
                for row in cursor.execute('SELECT * FROM users'):
                        array.append(row)
        print(array)
        send(message,conn)
        _thread.start_new_thread(handle_message,(conn,))
        sys.exit()
        
                

def add_user(conn,check):
        global lock
        print("at add user")
        username = check[2]
        password = check[3]
        password2 = check[4]
        identity = check[5]
        ID = random.randint(0,10000)
        try:
                lock.acquire(True)
                cursor.execute("INSERT INTO users (Username, User_ID, Password, Password_Check, Identity) VALUES (?,?,?,?,?)", (str(username),str(ID), str(password),str(password2),str(identity)))
                db.commit()
        finally:
                lock.release()
        print("added")
        _thread.start_new_thread(handle_message,(conn,))
        sys.exit()

def delete_user(message,conn,check):
        global lock
        global online
        userID = check[3]
        user = check[2]
        for i in range(0,len(online)):
                if online[i][0] == user and online[i][2] == userID:
                        message = "logged in"
                        break
                else:
                        message = "Fine"
        if message == "Fine":
                try:
                        lock.acquire(True)
                        cursor.execute("DELETE FROM users WHERE Username = ? AND User_ID = ?", (user,userID,))
                        db.commit()
                finally:
                        lock.release()
        send(message,conn)
        _thread.start_new_thread(handle_message,(conn,))
        sys.exit()

def user_list(conn,check):
        global lock
        print("at user list")
        list_of_users = ""
        list_of_userIDs = ""
        role = "Client"
        try:
                lock.acquire(True)
                for row in cursor.execute("SELECT Username FROM users WHERE identity = ?", (role,)):
                        row = str(row)
                        row = row.split("'")
                        list_of_users += row[1] + ","
                for row in cursor.execute("SELECT User_ID FROM users WHERE identity = ?", (role,)):
                        row = str(row)
                        row = row.split("'")
                        list_of_userIDs += row[1] + ","
        finally:
                lock.release()
        message = str(list_of_users)
        send(message,conn)
        message = str(list_of_userIDs)
        send(message,conn)
        _thread.start_new_thread(handle_message,(conn,))
        sys.exit()

def user_name_change(conn,check):
        global lock
        new_username = check[2]
        old_username = check[3]
        user_id = check[4]
        print(new_username)
        print(user_id)
        print(old_username)
        print("I am here")
        for i in range(0,len(online)):
                if online[i][0] == old_username and online[i][2] == user_id:
                        message = "logged in"
                        break
                else:
                        message = "Fine"
        if message == "Fine":
                try:
                        lock.acquire(True)
                        cursor.execute('UPDATE users SET Username = ? WHERE Username = ? AND User_ID = ?', (new_username,old_username,user_id))
                        db.commit()
                finally:
                        lock.release()
        send(message,conn)
        _thread.start_new_thread(handle_message,(conn,))
        sys.exit()

def message_handler(conn,check,):
        global online
        global lock
        row = ""
        if check[7] == "checking":
                print("at check")
                ID = check[3]
                try:
                        lock.acquire(True)
                        with sqlite3.connect("messages_to_send.db",  check_same_thread=False) as db:
                                cursor = db.cursor()
                        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS messages_to_send(
                        sender VARCHAR(20) NOT NULL,
                        sender_ID VARCHAR(20) NOT NULL,
                        recipient VARCHAR(20) NOT NULL,
                        recipient_ID VARCHAR(20) NOT NULL,
                        number_of_messages VARCHAR(20));
                        ''')
                        for row in cursor.execute('SELECT number_of_messages FROM messages_to_send WHERE sender = ? AND sender_ID = ? AND recipient = ? AND recipient_ID = ?', (check[4],check[5],check[2],ID)):
                                row = str(row)
                                print(row)
                                print("HERE ROW")
                                row = row.split("'")
                                row = row[1]
                        print("here is row")
                        print(row)
                        if row != "":
                                conn.send(row.encode())
                                file = open(check[4] + check[5] + check[2] + ID, "rb")
                                for i in range(0,int(row)):
                                        sending = file.readline()
                                        conn.send(sending)
                                        
                                cursor.execute('DELETE FROM  messages_to_send WHERE sender = ? AND sender_ID = ? AND recipient = ? AND recipient_ID = ?', (check[4],check[5],check[2],ID))
                                db.commit()
                        if row == "":
                                message = "False"
                                send(message,conn)
                        with sqlite3.connect("users.db",  check_same_thread=False) as db:
                            cursor = db.cursor()
                finally:
                        lock.release()
                print("here is the message being sent")
                _thread.start_new_thread(handle_message,(conn,))
                sys.exit()
        if check[6] == "sending":
                print("at sending")
                ID = check[5]
                try:
                        with sqlite3.connect("messages_to_send.db",  check_same_thread=False) as db:
                                cursor = db.cursor()
                        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS messages_to_send(
                        sender VARCHAR(20) NOT NULL,
                        sender_ID VARCHAR(20) NOT NULL,
                        recipient VARCHAR(20) NOT NULL,
                        recipient_ID VARCHAR(20) NOT NULL,
                        number_of_messages VARCHAR(20));
                        ''')
                        lock.acquire(True)
                        print("R ID")
                        print(check[6])
                        for row in cursor.execute('SELECT number_of_messages FROM messages_to_send WHERE sender = ? AND sender_ID = ? AND recipient = ? AND recipient_ID = ?', (check[3],check[4],check[5],ID)):
                                row = str(row)
                                row = row.split("'")
                                row = row[1]
                        print("here is the row")
                        print(row)
                        message = conn.recv(1024)
                        if row != "":
                                row = int(row)
                                print(row)
                                file = open(check[2] + check[3] + check[4] + check[5], "wb")
                                file.write(message)
                                file.close()
                                file = open(check[2] + check[3] + check[4] + check[5], "a")
                                file.write("\n")
                                num = row + 1
                                cursor.execute("UPDATE messages_to_send SET number_of_messages = ? WHERE sender = ? AND sender_ID = ? AND recipient = ? AND recipient_ID = ?", (num,check[3],check[4],check[5],ID))
                                db.commit()
                        if row == "":
                                file = open(check[2] + check[3] + check[4] + check[5], "wb")
                                file.write(message)
                                file.close()
                                cursor.execute("INSERT INTO messages_to_send (sender, sender_ID, recipient, recipient_ID, number_of_messages) VALUES (?,?,?,?,?)", (check[2],check[3],check[4],ID,str("1")))
                                db.commit()
                                print("Inserted")
                        with sqlite3.connect("users.db",  check_same_thread=False) as db:
                            cursor = db.cursor()
                finally:
                        lock.release()
                _thread.start_new_thread(handle_message,(conn,))
                sys.exit()

def key_handler(message,conn,check):
        global lock
        if check[4] == "key insert":
                try:
                        lock.acquire(True)
                        key = conn.recv(1024)
                        print(key)
                        file = open ("public" + check[2] + check[3], "wb")
                        file.write(key)
                        file.close()
                        print("complete")
                finally:
                        lock.release()
        if check[4] == "get key":
                try:
                        lock.acquire(True)
                        file = open ("public" +check[2] + check[3], "rb")
                        key = file.read()
                        file.close()
                        print("sending key")
                        print(key)
                        print(type(key))
                        conn.send(key)
                finally:
                        lock.release()
                
        _thread.start_new_thread(handle_message,(conn,))
        



def send(message,conn):
     #sends a message to a user as specified by the recipient
     print(message)
     conn.send(message.encode())
     print("here is conn: " + str(conn))
    
def listening(i):
    conn, addr = s.accept()
    Flag = False
    print("Hello")
    print(conn)
    connections.append(conn)
    print(connections)
    user = ("user" + str(i))
    temp.append([i,conn])
    message = str(i)
    send(message, conn)
    print(temp)
    i += 1
    # Display message when user connects
    print('*Server Connected ')
    _thread.start_new_thread(handle_message,(conn,))
    _thread.start_new_thread(listening,(i,))
    sys.exit()

print("Hey there")
_thread.start_new_thread(listening,(i,))

