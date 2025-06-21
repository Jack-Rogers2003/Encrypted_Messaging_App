import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import socket
import sys
import os
import _thread
import threading
import sqlite3
import random
import time
import tkinter.messagebox 
start = True


with sqlite3.connect("users.db") as db:
    cursor = db.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS client(
Username INTERGER PRIMARY KEY,
Password VARCHAR(20) NOT NULL,
Private_Key VARCHAR(20) NOT NULL);
''')

def RecieveMessage():
    global message
    while True :
        global message
        message = s.recv(1024).decode()
        if not message :
            print("not recieved")
            RecieveMessage()
        print("recieved")
        print(message)
        return message

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
print("trying to connect")
print(s)
host = '127.0.0.1'
port = 5000
s.connect((host,port))
name = "server"
ID = str(random.randint(0,1000000))
name = name+str(ID)
print(name)
to_send = "name change," + "change_name+=-_," + "," + str(name) + "," + "nothing"
s.send(to_send.encode())

root = tk.Tk()
root.geometry("400x220")
root.resizable(False, False)
root.title('Sign In')

username = tk.StringVar()
password = tk.StringVar()
RecieveMessage()


def login_clicked():
    global s
    global message
    u = username.get()
    p1 = password.get()
    print(p1)
    words = list(p1)
    values = []
    for i in range(0,len(words)):
        asci = ord(words[i])
        asci = asci*8+9*12-4
        values.append(asci)
    word = ""
    for i in range(0,len(values)):
        word = word + str(values[i])
    login_request = "login," + "!£$%qwert," + u + "," + word
    s.send(login_request.encode())
    RecieveMessage()
    recieved = message.split(",")
    if recieved[0] == "found":
        message = "logout," + ":;@'~#," + name
        s.send(message.encode())
        s.close()
        time.sleep(1)
        root.destroy()
        ID = recieved[2]
        if recieved[1] == "Client":
            file = open("username.txt", "w")
            to_write = u + "," + ID
            print(to_write)
            file.write(to_write)
            file.close()
            import Client
        if recieved[1] == "Admin":
            file = open("username.txt", "w")
            to_write = u +"," + ID
            print(to_write)
            file.write(to_write)
            file.close()
            import Admin
    if recieved[0] == "not-found":
        tkinter.messagebox.showinfo(title="Error", message="Either the usernme or password is inccorect")
    if recieved[0] == "logged in":
        tkinter.messagebox.showinfo(title="Error", message="This user is already logged in")
        

def exit_clicked():
    message = "logout," + ":;@'~#," + name
    s.send(message.encode())
    s.close()
    root.destroy()

signin = ttk.Frame(root)
signin.pack(padx=10, pady=10, fill='x', expand=True)

welcome_label = ttk.Label(signin, text = "Enter your log in details:")
welcome_label.pack(fill='x', expand=True)

username_label = ttk.Label(signin, text = "Username:")
username_label.pack(fill='x', expand=True)
username_entry = ttk.Entry(signin, textvariable=username)
username_entry.pack(fill='x', expand=True)

password_label = ttk.Label(signin, text="Password:")
password_label.pack(fill='x', expand=True)
password_entry = ttk.Entry(signin, textvariable=password, show="*")
password_entry.pack(fill='x', expand=True)

login_button = ttk.Button(signin, text="Login", command=login_clicked)
login_button.pack(fill='x', expand=True, pady=10)

exit_button = ttk.Button(signin, text="Exit", command=exit_clicked)
exit_button.pack(fill='x', expand=True, pady=10)

root.mainloop()


