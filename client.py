import socket, time
from tkinter import *
from threading import Thread
from datetime import datetime

HOST = socket.gethostname()
IP = socket.gethostbyname(HOST)
PORT0 = 5002
PORT1 = 5003
PORT2 = 5004
SERVER_IP = "192.168.1.10"

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

def listenToPeer():
    sktFromPeer, addrFromPeer = sktServer.accept()
    currentTime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    print("\033[1;32m" + f"\n[{currentTime}] *Received connection from {addrFromPeer[0]} : {addrFromPeer[1]}*" + "\033[1;37m")
    
    while True:
        rmessage = sktFromPeer.recv(1024).decode()
        currentTime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        if(rmessage == "!quit"):
            print("\033[1;32m" + f"\n[{currentTime}] *{addrFromPeer[0]} disconnected*" + "\033[1;37m")
            sktFromPeer.close()
            t = Thread(target=listenToPeer, daemon=True)
            t.start()
            break
        print("\033[1;32m" + rmessage + "\033[1;37m")

def talkToPeer(ip):
    sktToPeer = socket.socket()
    
    try:
        sktToPeer.connect((ip, PORT2))
    except Exception as e:
        print(e)
    
    while True:
        message = str(input())
        if(message == '!quit'):
            sktToPeer.send(message.encode())
            time.sleep(0.1)
            sktToPeer.close()
            break
        currentTime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        sktToPeer.send(f"[{currentTime}] {username} : {message}".encode()) 

def cmdInstruction():
    toPrint = ("\n1.  Enter !logout to logout."   
             + "\n2.  Enter !connect <Username> to connect to a friend."
             + "\n3.  Enter !info to see your info. (Name, Password, IP, Online, Friends)"
             + "\n4.  Enter !change_p <New password> to change password."
             + "\n5.  Enter !list to see all users."
             + "\n6.  Enter !add <Username> to add a friend"
             + "\n7.  Enter !remove <Username> to remove a friend"
             + "\n8.  Enter !help to see instructions.\n")
    return toPrint

def cmdInput():
    command = inputText.get()
    outputText.insert(END, "\n" + f"Command: {command}")
    command = str(input())
    if(command == "!help"):
        message = cmdInstruction()
        outputText.insert(END, "\n" + message)  
    else:
        sktToServer.send(command.encode())
        message = sktToServer.recv(1024).decode()
        if(message == "!logoutOK"):
            print()
        elif(message == "!connectOK"):
            message = sktToServer.recv(1024).decode()
        else:
            outputText.insert(END, "\n" + message)  
    inputText.delete(0, END)

if __name__ == '__main__':
    sktList = set()
    sktServer, sktToServer = socket.socket(), socket.socket()

    # try:
    #     sktToServer.connect((SERVER_IP, PORT1))
    #     while True:
    #         username = input("Username: ")
    #         password = input("Password: ")
    #         sktToServer.send(f"!login {username} {password}".encode())
    #         result = sktToServer.recv(1024).decode()
    #         if(result == "!loginOK"):
    #             break
    #         print(result)
    # except Exception as e:
    #     print(e)

    sktServer.bind((IP, PORT0))
    sktServer.listen()
    t = Thread(target=listenToPeer, daemon=True)
    t.start()

    root = Tk()
    root.title("Menu")
    outputText = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    outputText.grid(row=1, column=0, columnspan=2)
    scrollbar = Scrollbar(outputText)
    scrollbar.place(relheight=1, relx=0.974)
    inputText = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
    inputText.grid(row=2, column=0)
    Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=cmdInput).grid(row=2, column=1)
    outputText.insert(END, "\n" + f"{HOST} : {IP} : {PORT0}")
    outputText.insert(END, "\n" + cmdInstruction())
    
    root.mainloop()




    
    
