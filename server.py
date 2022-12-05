import socket, json, time
from threading import Thread
from datetime import datetime

HOST = socket.gethostname()
IP = socket.gethostbyname(HOST)
PORT = 5002
print(f"\n{HOST} : {IP} : {PORT}")

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
        if(rcommandArr[0] == '!login' and len(rcommandArr) == 3): # !login <Username> <Password>
            (username, password, ip, online) = cmdSearch(rcommandArr[1], rcommandArr[2], "!NA")
            if(username == -1):
                message = "Login failed\n"
                sktFunc.send(message.encode())
            else:
                ip = addrFunc
                online = 1
                cmdUpdate(username, password, ip, online)
                message = "!loginOK"
                sktFunc.send(message.encode())
        elif(rcommandArr[0] == '!logout' and len(rcommandArr) == 1): # !logout
            (username, password, ip, online) = cmdSearch("!NA", "!NA", addrFunc)
            online = 0
            cmdUpdate(username, password, ip, online)
            message = "!logoutOK"
            sktFunc.send(message.encode())
        elif(rcommandArr[0] == "!connect" and len(rcommandArr) == 2): # !connect <Username>            
            (username, password, ip, online) = cmdSearch(rcommandArr[1], "!NA", "!NA")
            if(username == -1):
                message = f"User {rcommandArr[1]} not found\n"
                sktFunc.send(message.encode())
            else:
                message = "connectOK"
                sktFunc.send(message.encode())
                message = ip
                sktFunc.send(message.encode())
        elif(rcommandArr[0] == "!info" and len(rcommandArr) == 1): # !info
            (username, password, ip, online) = cmdSearch("!NA", "!NA", addrFunc)
            message = f"Username: {username}\n Password:{password}\n IP: {ip}\n Online: {online}\n"
            sktFunc.send(message.encode())
        elif(rcommandArr[0] == "!change_p" and len(rcommandArr) == 2): # !change_p <Password>
            (username, password, ip, online) = cmdSearch("NA", "!NA", addrFunc)
            password = rcommandArr[1]
            cmdUpdate(username, password, ip, online)
            message = "Password changed successfully\n"
            sktFunc.send(message.encode())
        elif(rcommandArr[0] == "!list" and len(rcommandArr) == 1):
            message = cmdList()
            sktFunc.send(message.encode())
        else:
            message = "Invalid command\n"
            sktFunc.send(message.encode())

def cmdList():
    toPrint = ""
    with open("./user.json", "r+") as file:
        userList = json.load(file)
        for idx in range(len(userList["userList"])):
            toPrint += f"{userList['userList'][idx]}\n"
    return toPrint

def cmdSearch(username, password, ip):
    with open("./user.json", "r+") as file:
        userList = json.load(file)
        for idx in range(len(userList["userList"])):
            if((username == userList["userList"][idx]["username"] or username == "!NA") and (password == userList["userList"][idx]["password"] or password == "!NA") and (password == userList["userList"][idx]["ip"] or ip == "!NA")):
                return(userList["userList"][idx]["username"], 
                       userList["userList"][idx]["password"], 
                       userList["userList"][idx]["ip"], 
                       userList["userList"][idx]["online"])
        return(-1, -1, -1, -1)

def cmdUpdate(username, password, ip, online):
    file = open("./user.json", "r+")
    userList = json.load(file)
    for idx in range(len(userList["userList"])):
        if(username == userList["userList"][idx]["username"]):
            userList["userList"][idx]["password"] = password
            userList["userList"][idx]["ip"] = ip 
            userList["userList"][idx]["online"] = online 
    file.close()
    with open("./user.json", "w+") as file:
        json.dump(userList, file, indent = 4)
    
def cmdInstruction():
    print("\n1. Press !list to show all user list."
        + "\n2. Enter !add <Username> <Password> to add a user."
        + "\n3. Enter !remove <Username> to remove a user."
        + "\n4. Enter !help to see instructions.\n")

if __name__ == '__main__':
    sktList = set()
    sktServer = socket.socket()
    
    sktServer.bind((IP, PORT))
    sktServer.listen()
    t = Thread(target=acceptClient, daemon=True)
    t.start()
    
    cmdInstruction()
    
    while True:
        command = str(input())
        commandArr = command.split()
        if(commandArr[0] == "!list" and len(commandArr) == 1): # !list
            print(cmdList())
        elif(commandArr[0] == "!add" and len(commandArr) == 3): # !add <Username> <Password>
            (username, password, ip, online) = cmdSearch(commandArr[1], "!NA", "!NA")
            if(username == -1):
                with open("./user.json", "r+") as file:
                    userList = json.load(file)
                    newUser = {
                        "username": commandArr[1],
                        "password": commandArr[2],
                        "ip": "0.0.0.0",
                        "online": 0
                    }
                    userList["userList"].append(newUser)
                    file.seek(0)
                    json.dump(userList, file, indent = 4)
                message = f"User {commandArr[1]} added successfully\n"
                print(message)
            else:
                message = f"User {commandArr[1]} already existed\n"
                print(message)
        elif(commandArr[0] == "!remove" and len(commandArr) == 2): # !remove <Username>
            (username, password, ip, online) = cmdSearch(commandArr[1], "!NA", "!NA")
            if(username == -1):
                message = f"User {commandArr[1]} not found\n"
                print(message)
            else:
                file = open("./user.json", "r+")
                userList = json.load(file)
                for idx in range(len(userList["userList"])):
                    if(commandArr[1] == userList["userList"][idx]["username"]):
                        del userList["userList"][idx]
                file.close()
                with open("./user.json", "w+") as file:
                    json.dump(userList, file, indent = 4)
                message = f"User {commandArr[1]} deleted successfully\n"
                print(message)
        elif(commandArr[0] == "!help" and len(commandArr) == 1): # !help
            cmdInstruction()        
        else:
            print("Invalid command\n")