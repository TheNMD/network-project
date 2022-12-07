import socket, os
from tkinter import *
from threading import Thread
from datetime import datetime

HOST = socket.gethostname()
IP = socket.gethostbyname(HOST)
SPORT = 5002
PORT = 5002
SERVER_IP = "192.168.1.10"

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

def acceptPeer(root):
    while True:
        sktFromPeer, addrFromPeer = sktServer.accept()
        currentTime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        print("\033[1;32m" + f"\n[{currentTime}] *Received connection from {addrFromPeer[0]} : {addrFromPeer[1]}*" + "\033[1;37m")
        t = Thread(target=listenToPeer, args=(sktFromPeer, addrFromPeer[0], root), daemon=True)
        t.start()

def listenToPeer(sktFunc, addrFunc, root):
    def messageInput():
        message = inputText.get()
        messageArr = message.split()
        currentTime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        if(messageArr[0] == "!quit" and len(messageArr) == 1): # !quit
            sktFunc.send(message.encode())
            outputText.insert(END, "\n" + f"[{currentTime}] You: {message}") 
        elif(messageArr[0] == "!send" and len(messageArr) == 2): # !send <File>
            filename = f"./file/{messageArr[1]}"
            filesize = os.path.getsize(filename)
            totalRead = 0
            message += f" {filesize}"
            sktFunc.send(message.encode())
            with open(filename, "rb") as file:                
                while(totalRead < filesize):
                    byteRead = file.read(1024)
                    sktFunc.send(byteRead)
                    totalRead += len(byteRead)
                outputText.insert(END, "\n" + f"[{currentTime}] System: File sent successfully") 
        else:
            outputText.insert(END, "\n" + f"[{currentTime}] You: {message}")
            sktFunc.send(message.encode())
            inputText.delete(0, END)
    
    newWindow = Toplevel(root)
    newWindow.title("Chatbox")
    outputText = Text(newWindow, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    outputText.grid(row=1, column=0, columnspan=2)
    scrollbar = Scrollbar(outputText)
    scrollbar.place(relheight=1, relx=0.974)
    inputText = Entry(newWindow, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
    inputText.grid(row=2, column=0)
    Button(newWindow, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=messageInput).grid(row=2, column=1)
    outputText.insert(END, "\n" + f"Enter !quit to stop chatting")
    
    while True:
        rmessage = sktFunc.recv(1024).decode()
        rmessageArr = rmessage.split()
        currentTime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        if(rmessageArr[0] == "!quit"): # !quit
            sktFunc.send(rmessage.encode())
            outputText.insert(END, "\n" + f"[{currentTime}] Friend: {rmessage}")
            outputText.insert(END, "\n" + f"System: Chatbox will be closed after a few seconds")
            print("\033[1;32m" + f"\n[{currentTime}] {addrFunc} disconnected" + "\033[1;37m")
            root.after(5000)
            sktFunc.close()
            break
        elif(rmessageArr[0] == "!send"): # !send <File> <Size>
            filename = f"./file/{rmessageArr[1]}"
            filesize = int(rmessageArr[2])
            totalWrite = 0
            with open(filename, "wb") as file:
                while(totalWrite < filesize):
                    byteWrite = sktFunc.recv(1024)
                    file.write(byteWrite)
                    totalWrite += len(byteWrite)
                outputText.insert(END, "\n" + f"[{currentTime}] System: New file received") 
        else:
            outputText.insert(END, "\n" + f"[{currentTime}] Friend: {rmessage}")
        
    newWindow.destroy()

def talkToPeer(ip, root):
    def messageInput():
        message = inputText.get()
        messageArr = message.split()
        currentTime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        if(messageArr[0] == "!quit" and len(messageArr) == 1): # !quit
            sktToPeer.send(message.encode())
            outputText.insert(END, "\n" + f"[{currentTime}] You: {message}")
            inputText.delete(0, END)
        elif(messageArr[0] == "!send" and len(messageArr) == 2): # !send <File>
            filename = f"./file/{messageArr[1]}"
            filesize = os.path.getsize(filename)
            totalRead = 0
            message += f" {filesize}"
            sktToPeer.send(message.encode())
            with open(filename, "rb") as file:
                while(totalRead < filesize):
                    byteRead = file.read(1024)
                    sktToPeer.send(byteRead)
                    totalRead += len(byteRead)
                outputText.insert(END, "\n" + f"[{currentTime}] System: File sent successfully") 
            inputText.delete(0, END)
        else:
            outputText.insert(END, "\n" + f"[{currentTime}] You: {message}")
            sktToPeer.send(message.encode())
            inputText.delete(0, END)

    sktToPeer = socket.socket()
    
    try:
        sktToPeer.connect((ip, PORT))
    except Exception as e:
        print(e)
    
    newWindow = Toplevel(root)
    newWindow.title("Chatbox")
    outputText = Text(newWindow, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    outputText.grid(row=1, column=0, columnspan=2)
    scrollbar = Scrollbar(outputText)
    scrollbar.place(relheight=1, relx=0.974)
    inputText = Entry(newWindow, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
    inputText.grid(row=2, column=0)
    Button(newWindow, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=messageInput).grid(row=2, column=1)
    outputText.insert(END, "\n" + f"Enter !quit to stop chatting")
    
    while True:
        rmessage = sktToPeer.recv(1024).decode()
        rmessageArr = rmessage.split()
        currentTime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        if(rmessageArr[0] == "!quit"): # !quit
            sktToPeer.send(rmessage.encode())
            outputText.insert(END, "\n" + f"[{currentTime}] Friend: {rmessage}")
            outputText.insert(END, "\n" + f"System: Chatbox will be closed after a few seconds")
            print("\033[1;32m" + f"\n[{currentTime}] {ip} disconnected" + "\033[1;37m")
            root.after(5000)
            sktToPeer.close()
            break
        elif(rmessageArr[0] == "!send"): # !send <File> <Size>
            filename = f"./file/{rmessageArr[1]}"
            filesize = int(rmessageArr[2])
            totalWrite = 0
            with open(filename, "wb") as file:
                while(totalWrite < filesize):
                    byteWrite = sktToPeer.recv(1024)
                    file.write(byteWrite)
                    totalWrite += len(byteWrite)
                outputText.insert(END, "\n" + f"[{currentTime}] System: New file received")
        else:
            outputText.insert(END, "\n" + f"[{currentTime}] Friend: {rmessage}")
        
    newWindow.destroy()


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
    if(command == "!help"):
        message = cmdInstruction()
        outputText.insert(END, "\n" + message)
    elif(command == "!logout"):
        command += f" {username}"
        sktToServer.send(command.encode())
        root.after(1000)
        sktToServer.close()
    else:
        # command += f" {username}"
        # sktToServer.send(command.encode())
        # message = sktToServer.recv(1024).decode()
        message = "!connectOK"
        if(message == "!connectOK"):
            # ip = sktToServer.recv(1024).decode()
            ip = "192.168.1.6"
            t = Thread(target=talkToPeer, args=(ip, root), daemon=True)
            t.start()
        else:
            outputText.insert(END, "\n" + message)  
    inputText.delete(0, END)


if __name__ == '__main__':
    sktList = set()
    sktServer, sktToServer = socket.socket(), socket.socket()

    # try:
    #     sktToServer.connect((SERVER_IP, SPORT))
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

    root = Tk()
    root.title("Menu")
    outputText = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    outputText.grid(row=1, column=0, columnspan=2)
    scrollbar = Scrollbar(outputText)
    scrollbar.place(relheight=1, relx=0.974)
    inputText = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
    inputText.grid(row=2, column=0)
    Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=cmdInput).grid(row=2, column=1)
    outputText.insert(END, "\n" + f"{HOST} : {IP} : {PORT}")
    outputText.insert(END, "\n" + cmdInstruction())
    
    sktServer.bind((IP, PORT))
    sktServer.listen()
    t = Thread(target=acceptPeer, args=(root,), daemon=True)
    t.start()
    
    root.mainloop()




    
    
