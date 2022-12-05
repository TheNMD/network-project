import socket, json, time
from threading import Thread
from datetime import datetime

HOST = socket.gethostname()
IP = socket.gethostbyname(HOST)
PORT = 5002
print(f"\n{HOST} : {IP} : {PORT}")

def acceptPeer():
    while True:
        sktFromClient, addrFromClient = sktServer.accept()
        sktList.add(sktFromClient)
        currentTime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        print("\033[1;32m" + f"\n[{currentTime}] *Received connection from {addrFromClient[0]} : {addrFromClient[1]}*" + "\033[1;37m")
        t = Thread(target=listenToPeer, args=(sktFromClient, addrFromClient[0]), daemon=True)
        t.start()

def listenToPeer(sktFunc, addrFunc):
    while True:
        rcommand = sktFunc.recv(1024).decode()
        rcommandArr = rcommand.split()
        if(rcommandArr[0] == '!login'): # !login <Username> <Password>
            print()
        elif(rcommandArr[0] == '!logout'):
            print()
        elif(rcommandArr[0] == "!register"):
            print()
        elif(rcommandArr[0] == "!connect"):            
            print()
        elif(rcommandArr[0] == "!info"):
            print()
        elif(rcommandArr[0] == "!change_p"):
            print()
        elif(rcommandArr[0] == "!add"):
            print()
        elif(rcommandArr[0] == "!remove"):
            print()

def cmdSearch(username, password):
    with open("./user.json", "r+") as file:
        userList = json.load(file)
        if(username == userList["username"] and password == userList["password"]):
            return(userList["username"], userList["password"], userList["ip"], userList["online"], userList["friend"])
        else:
            return(-1, -1, -1, -1, -1)

def cmdUpdate(username, password, ip, online, friend):
    with open("./user.json", "r+") as file:
        userList = json.load(file)
        update = {
            "username": username,
            "password": password,
            "ip": ip,
            "online": online,
            "friend": friend
        }
        userList.append(update)
        file.seek(0)
        json.dump(userList, file, indent = 4)
    
def cmdInstruction():
    print("\n1. Press !user_list to show all user list."
        + "\n2. Enter !add <Username> <Password> <IP> to add a user."
        + "\n3. Enter !remove <Username> <Password> to remove a user."
        + "\n4. Enter !help to see instructions."
        + "\n5. ...\n")

if __name__ == '__main__':
    sktList = set()
    sktServer = socket.socket()
    
    sktServer.bind((IP, PORT))
    sktServer.listen()
    t = Thread(target=acceptPeer, daemon=True)
    t.start()
    
    cmdInstruction()
    while True:
        command = str(input())
        commandArr = command.split()
        if(commandArr[0] == "!list" and len(commandArr) == 1):
            with open("./user.json", "r+") as file:
                userList = json.load(file)
            print("\n<Username> <Password> <IP> <Online> <Busy> <Friends>")
        elif(commandArr[0] == "!add" and len(commandArr) == 4):
            print()
        elif(commandArr[0] == "!remove" and len(commandArr) == 2):
            print()
        elif(commandArr[0] == "!help" and len(commandArr) == 1):
            cmdInstruction()
        elif(commandArr[0] == "!reset" and len(commandArr) == 1):
            print(f"\n*Reset all accounts*")           
        else:
            print("\nUnknown command")