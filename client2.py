import os, socket
from tkinter import *
from threading import Thread
from datetime import datetime

HOST = socket.gethostname()
IP = socket.gethostbyname(HOST)
PORT = 5005
SPORT = 5002
SIP = IP

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

def acceptPeer(root):
    while True:
        sktFromPeer, addrFromPeer = sktServer.accept()
        fname = sktFromPeer.recv(1024).decode()
        currentTime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        print("\033[1;32m" + f"\n[{currentTime}] *Received connection from {addrFromPeer[0]} : {addrFromPeer[1]}*" + "\033[1;37m")
        t = Thread(target=listenToPeer, args=(sktFromPeer, addrFromPeer[0], fname, root), daemon=True)
        t.start()

def listenToPeer(sktFunc, addrFunc, fname, root):
    def messageInput():
        message = inputText.get()
        messageArr = message.split()
        currentTime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        if(messageArr[0] == "!quit" and len(messageArr) == 1): # !quit 
            sktFunc.send(message.encode())
            outputText.insert(END, "\n" + f"[{currentTime}] You: {message}") 
        elif(messageArr[0] == "!send" and len(messageArr) == 2): # !send <File>
            filename = f"./{username}/{messageArr[1]}"
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
        elif(messageArr[0] == "!help" and len(messageArr) == 1):
             outputText.insert(END, "\n" + chatInstruction())
             inputText.delete(0, END)
        else:
            outputText.insert(END, "\n" + f"[{currentTime}] You: {message}")
            sktFunc.send(message.encode())
            inputText.delete(0, END)
    
    newWindow = Toplevel(root)
    newWindow.title(f"{fname}")
    outputText = Text(newWindow, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    outputText.grid(row=1, column=0, columnspan=2)
    scrollbar = Scrollbar(outputText)
    scrollbar.place(relheight=1, relx=0.974)
    inputText = Entry(newWindow, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
    inputText.grid(row=2, column=0)
    Button(newWindow, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=messageInput).grid(row=2, column=1)
    outputText.insert(END, "\n" + chatInstruction())
    
    while True:
        rmessage = sktFunc.recv(1024).decode()
        rmessageArr = rmessage.split()
        currentTime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        if(rmessageArr[0] == "!quit"): # !quit
            sktFunc.send(rmessage.encode())
            outputText.insert(END, "\n" + f"[{currentTime}] {fname}: {rmessage}")
            outputText.insert(END, "\n" + f"System: Chatbox will be closed after a few seconds")
            print("\033[1;32m" + f"\n[{currentTime}] {addrFunc} disconnected" + "\033[1;37m")
            root.after(5000)
            sktFunc.close()
            break
        elif(rmessageArr[0] == "!send"): # !send <File> <Size>
            filename = f"./{username}/{rmessageArr[1]}"
            filesize = int(rmessageArr[2])
            totalWrite = 0
            with open(filename, "wb") as file:
                while(totalWrite < filesize):
                    byteWrite = sktFunc.recv(1024)
                    file.write(byteWrite)
                    totalWrite += len(byteWrite)
                outputText.insert(END, "\n" + f"[{currentTime}] System: New file received") 
        else:
            outputText.insert(END, "\n" + f"[{currentTime}] {fname}: {rmessage}")
        
    newWindow.destroy()

def talkToPeer(fname, fip, fport, root):
    def messageInput():
        message = inputText.get()
        messageArr = message.split()
        currentTime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        if(messageArr[0] == "!quit" and len(messageArr) == 1): # !quit
            sktToPeer.send(message.encode())
            outputText.insert(END, "\n" + f"[{currentTime}] You: {message}")
            inputText.delete(0, END)
        elif(messageArr[0] == "!send" and len(messageArr) == 2): # !send <File>
            filename = f"./{username}/{messageArr[1]}"
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
        elif(messageArr[0] == "!help" and len(messageArr) == 1):
            outputText.insert(END, "\n" + chatInstruction())
            inputText.delete(0, END)
        else:
            outputText.insert(END, "\n" + f"[{currentTime}] You: {message}")
            sktToPeer.send(message.encode())
            inputText.delete(0, END)

    sktToPeer = socket.socket()
    
    try:
        sktToPeer.connect((fip, fport))
        root.after(1000)
        sktToPeer.send(username.encode())
    except Exception as e:
        print(e)
    
    newWindow = Toplevel(root)
    newWindow.title(f"{fname}")
    outputText = Text(newWindow, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    outputText.grid(row=1, column=0, columnspan=2)
    scrollbar = Scrollbar(outputText)
    scrollbar.place(relheight=1, relx=0.974)
    inputText = Entry(newWindow, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
    inputText.grid(row=2, column=0)
    Button(newWindow, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=messageInput).grid(row=2, column=1)
    outputText.insert(END, "\n" + chatInstruction())
    
    while True:
        rmessage = sktToPeer.recv(1024).decode()
        rmessageArr = rmessage.split()
        currentTime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        if(rmessageArr[0] == "!quit"): # !quit
            sktToPeer.send(rmessage.encode())
            outputText.insert(END, "\n" + f"[{currentTime}] {fname}: {rmessage}")
            outputText.insert(END, "\n" + f"System: Chatbox will be closed after a few seconds")
            print("\033[1;32m" + f"\n[{currentTime}] {fip} disconnected" + "\033[1;37m")
            root.after(5000)
            sktToPeer.close()
            break
        elif(rmessageArr[0] == "!send"): # !send <File> <Size>
            filename = f"./{username}/{rmessageArr[1]}"
            filesize = int(rmessageArr[2])
            totalWrite = 0
            with open(filename, "wb") as file:
                while(totalWrite < filesize):
                    byteWrite = sktToPeer.recv(1024)
                    file.write(byteWrite)
                    totalWrite += len(byteWrite)
                outputText.insert(END, "\n" + f"[{currentTime}] System: New file received")
        else:
            outputText.insert(END, "\n" + f"[{currentTime}] {fname}: {rmessage}")
        
    newWindow.destroy()

def chatInstruction():
    toPrint = ("\n1.  Enter !quit to stop chatting."   
             + "\n2.  Enter !send <File path> to connect to a friend."
             + "\n3.  Enter !help to see instructions.\n")
    return toPrint

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
        inputText.delete(0, END)
    elif(command == "!logout"):
        command += f" {username}"
        sktToServer.send(command.encode())
        root.after(1000)
        sktToServer.close()
        root.destroy()
    else:
        command += f" {username}"
        sktToServer.send(command.encode())
        message = sktToServer.recv(1024).decode()
        if(message == "!connectOK"):
            toReceive = sktToServer.recv(1024).decode()
            toReceiveArr = toReceive.split()
            fname = toReceiveArr[0]
            fip = toReceiveArr[1]
            fport = int(toReceiveArr[2])
            t = Thread(target=talkToPeer, args=(fname, fip, fport, root), daemon=True)
            t.start()
        else:
            outputText.insert(END, "\n" + message)  
        inputText.delete(0, END)


if __name__ == '__main__':
    sktList = set()
    sktServer, sktToServer = socket.socket(), socket.socket()

    try:
        sktToServer.connect((SIP, SPORT))
        while True:
            username = input("Username: ")
            password = input("Password: ")
            sktToServer.send(f"!login {username} {password} {PORT}".encode())
            result = sktToServer.recv(1024).decode()
            if(result == "!loginOK"):
                break
            print(result)
    except Exception as e:
        print(e)

    root = Tk()
    root.title(f"{username} - Menu")
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




    
    
