import socket, json
from tkinter import *
from threading import Thread
from datetime import datetime

HOST = socket.gethostname()
IP = socket.gethostbyname(HOST)
PORT = 5002

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

def acceptClient():
    while True:
        sktFromClient, addrFromClient = sktServer.accept()
        sktList.add(sktFromClient)
        currentTime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        print("\033[1;32m" + f"\n[{currentTime}] *Received connection from {addrFromClient[0]} : {addrFromClient[1]}*" + "\033[1;37m")
        t = Thread(target=listenToClient, args=(sktFromClient, addrFromClient[0]), daemon=True)
        t.start()

def listenToClient(sktFunc, addrFunc):
    while True:
        rcommand = sktFunc.recv(1024).decode()
        rcommandArr = rcommand.split()
        if(rcommandArr[0] == '!login' and len(rcommandArr) == 4): # !login <Username> <Password> <Port>
            (username, password, ip, port, online, friend) = cmdSearch(rcommandArr[1], rcommandArr[2])
            if(username == -1):
                message = "Login failed\n"
                sktFunc.send(message.encode())
            else:
                ip = addrFunc
                online = 1
                port = rcommandArr[3]
                cmdUpdate(username, password, ip, port, online, friend)
                message = "!loginOK"
                sktFunc.send(message.encode())
        elif(rcommandArr[0] == '!logout' and len(rcommandArr) == 2): # !logout <Username>
            sktFunc.close()
            (username, password, ip, port, online, friend) = cmdSearch(rcommandArr[1], "!NA")
            online = 0
            cmdUpdate(username, password, ip, port, online, friend)
            print(f"{addrFunc} disconnected\n")
            break
        elif(rcommandArr[0] == "!connect" and len(rcommandArr) == 3): # !connect <Friend username> <Username>            
            (username, password, ip, port, online, friend) = cmdSearch(rcommandArr[1], "!NA")
            if(username == -1):
                message = f"User {rcommandArr[1]} not found\n"
                sktFunc.send(message.encode())
            else:
                if(online == 0):
                    message = f"{username} is not online\n"
                    sktFunc.send(message.encode())
                else:
                    message = "!connectOK"
                    sktFunc.send(message.encode())
                    toSend = f"{username} {ip} {port}"
                    sktFunc.send(toSend.encode())
        elif(rcommandArr[0] == "!info" and len(rcommandArr) == 2): # !info <Username>
            (username, password, ip, port, online, friend) = cmdSearch(rcommandArr[1], "!NA")
            message = f"Username: {username}\nPassword: {password}\nIP: {ip}\nOnline: {online}\nFriend: {friend}\n"
            sktFunc.send(message.encode())
        elif(rcommandArr[0] == "!change_p" and len(rcommandArr) == 3): # !change_p <Password> <Username>
            (username, password, ip, port, online, friend) = cmdSearch(rcommandArr[2], "!NA")
            password = rcommandArr[1]
            cmdUpdate(username, password, ip, port, online, friend)
            message = "Password changed successfully\n"
            sktFunc.send(message.encode())
        elif(rcommandArr[0] == "!list" and len(rcommandArr) == 2): # !list <Username>
            message = "<Username> <Online> <Friend>\n" + cmdListClient()
            sktFunc.send(message.encode())
        elif(rcommandArr[0] == "!add" and len(rcommandArr) == 3): # !add <Friend username> <Username>
            (fusername, fpassword, fip, fport, fonline, ffriend) = cmdSearch(rcommandArr[1], "!NA")
            if(fusername == -1):
                message = f"User {rcommandArr[1]} not found\n"
                sktFunc.send(message.encode())
            else:
                friendExist = False
                (username, password, ip, port, online, friend) = cmdSearch(rcommandArr[2], "!NA")
                friendList = friend.split(":")
                for frd in friendList:
                    if(frd == fusername):
                        friendExist = True
                        break
                if(friendExist):
                    message = f"User {fusername} is already in the friend list\n"
                    sktFunc.send(message.encode())
                else:
                    friendList.append(fusername)
                    friend = ":".join(friendList)
                    cmdUpdate(username, password, ip, port, online, friend)
                    message = f"User {fusername} added to the friend list\n"
                    sktFunc.send(message.encode())
        elif(rcommandArr[0] == "!remove" and len(rcommandArr) == 3): # !remove <Friend username> <Username>
            (fusername, fpassword, fip, fonline, ffriend) = cmdSearch(rcommandArr[1], "!NA")
            if(fusername == -1):
                message = f"User {rcommandArr[1]} not found\n"
                sktFunc.send(message.encode())
            else:
                friendExist = False
                (username, password, ip, port, online, friend) = cmdSearch(rcommandArr[2], "!NA")
                if(username == fusername):
                    message = f"You can't remove yourself from the friend list\n"
                    sktFunc.send(message.encode())
                else:
                    friendList = friend.split(":")
                    for frd in friendList:
                        if(frd == fusername):
                            friendExist = True
                            break
                    if(friendExist):
                        friendList.remove(fusername)
                        friend = ":".join(friendList)
                        cmdUpdate(username, password, ip, port, online, friend)
                        message = f"User {fusername} is removed from the friend list\n"
                        sktFunc.send(message.encode())
                    else:
                        message = f"User {fusername} is not in the friend list\n"
                        sktFunc.send(message.encode())
        else:
            message = "Invalid command\n"
            sktFunc.send(message.encode())

def cmdListServer():
    toPrint = ""
    with open("./user.json", "r+") as file:
        userList = json.load(file)
        for idx in range(len(userList["userList"])):
            toPrint += f"{userList['userList'][idx]}\n"
    return toPrint

def cmdListClient():
    toPrint = ""
    with open("./user.json", "r+") as file:
        userList = json.load(file)
        for idx in range(len(userList["userList"])):
            toPrint += f"{userList['userList'][idx]['username']} {userList['userList'][idx]['online']} {userList['userList'][idx]['friend']}\n"
    return toPrint

def cmdSearch(username, password):
    with open("./user.json", "r+") as file:
        userList = json.load(file)
        for idx in range(len(userList["userList"])):
            if(username == userList["userList"][idx]["username"] and (password == userList["userList"][idx]["password"] or password == "!NA")):
                return(userList["userList"][idx]["username"], 
                    userList["userList"][idx]["password"], 
                    userList["userList"][idx]["ip"],
                    userList["userList"][idx]["port"], 
                    userList["userList"][idx]["online"],
                    userList["userList"][idx]["friend"])
        return(-1, -1, -1, -1, -1, -1)

def cmdUpdate(username, password, ip, port, online, friend):
    file = open("./user.json", "r+")
    userList = json.load(file)
    for idx in range(len(userList["userList"])):
        if(username == userList["userList"][idx]["username"]):
            userList["userList"][idx]["password"] = password
            userList["userList"][idx]["ip"] = ip
            userList["userList"][idx]["ip"] = port 
            userList["userList"][idx]["online"] = online
            userList["userList"][idx]["friend"] = friend
    file.close()
    with open("./user.json", "w+") as file:
        json.dump(userList, file, indent = 4)
    
def cmdInstruction():
    toPrint = ("\n1. Enter !list to show all user list."
             + "\n2. Enter !add <Username> <Password> to add a user."
             + "\n3. Enter !remove <Username> to remove a user."
             + "\n4. Enter !help to see instructions.\n")
    return toPrint

def cmdInput():
    command = inputText.get()
    commandArr = command.split()
    outputText.insert(END, "\n" + f"Command: {command}")
    if(commandArr[0] == "!list" and len(commandArr) == 1): # !list
        outputText.insert(END, "\n" + cmdListServer())
    elif(commandArr[0] == "!add" and len(commandArr) == 3): # !add <Username> <Password>
        (username, password, ip, port, online, friend) = cmdSearch(commandArr[1], "!NA")
        if(username == -1):
            with open("./user.json", "r+") as file:
                userList = json.load(file)
                newUser = {
                    "username": commandArr[1],
                    "password": commandArr[2],
                    "ip": "0.0.0.0",
                    "port": 0,
                    "online": 0,
                    "friend": f"{commandArr[1]}"
                }
                userList["userList"].append(newUser)
                file.seek(0)
                json.dump(userList, file, indent = 4)
            message = f"User {commandArr[1]} added successfully\n"
            outputText.insert(END, "\n" + message)
        else:
            message = f"User {commandArr[1]} already existed\n"
            outputText.insert(END, "\n" + message)
    elif(commandArr[0] == "!remove" and len(commandArr) == 2): # !remove <Username>
        (username, password, ip, port, online, friend) = cmdSearch(commandArr[1], "!NA")
        if(username == -1):
            message = f"User {commandArr[1]} not found\n"
            outputText.insert(END, "\n" + message)
        else:
            file = open("./user.json", "r+")
            userList = json.load(file)
            for idx in range(len(userList["userList"])):
                if(username == userList["userList"][idx]["username"]):
                    del userList["userList"][idx]
            file.close()
            with open("./user.json", "w+") as file:
                json.dump(userList, file, indent = 4)
            message = f"User {commandArr[1]} deleted successfully\n"
            outputText.insert(END, "\n" + message)
    elif(commandArr[0] == "!help" and len(commandArr) == 1): # !help
        message = cmdInstruction()
        outputText.insert(END, "\n" + message)     
    else:
        message = "Invalid command\n"
        outputText.insert(END, "\n" + message)
    inputText.delete(0, END)
    
if __name__ == '__main__':
    sktList = set()
    sktServer = socket.socket()

    sktServer.bind((IP, PORT))
    sktServer.listen()
    t = Thread(target=acceptClient, daemon=True)
    t.start()
    
    root = Tk()
    root.title("Server - Menu")
    outputText = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    outputText.grid(row=1, column=0, columnspan=2)
    scrollbar = Scrollbar(outputText)
    scrollbar.place(relheight=1, relx=0.974)
    inputText = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
    inputText.grid(row=2, column=0)
    Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=cmdInput).grid(row=2, column=1)
    outputText.insert(END, "\n" + f"{HOST} : {IP} : {PORT}")
    outputText.insert(END, "\n" + cmdInstruction())
    
    root.mainloop()
    