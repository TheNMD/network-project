import time, socket
from threading import Thread
from datetime import datetime

HOST = socket.gethostname()
IP = socket.gethostbyname(HOST)
PORT = 5002
SERVER_IP = "192.168.1.10"
print(f"\n{HOST} : {IP} : {PORT}")

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
        sktToPeer.connect((ip, 5003))
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
    print("\n1.  Enter !logout to logout."   
        + "\n2.  Enter !connect <Username> to connect to a friend."
        + "\n3.  Enter !info to see your info. (Name, Password, IP, Online, Friends)"
        + "\n4.  Enter !change_p <New password> to change password."
        + "\n5.  Enter !list to see all users."
        + "\n6.  Enter !help to see instructions.\n")

if __name__ == '__main__':
    sktList = set()
    sktServer, sktToServer = socket.socket(), socket.socket()

    try:
        sktToServer.connect((SERVER_IP, PORT))
    except Exception as e:
        print(e)

    while True:
        username = input("Username: ")
        password = input("Password: ")
        sktToServer.send(f"!login {username} {password}".encode())
        result = sktToServer.recv(1024).decode()
        if(result == "!loginOK"):
            break
        print(result)

    sktServer.bind((IP, PORT))
    sktServer.listen()
    t = Thread(target=listenToPeer, daemon=True)
    t.start()

    cmdInstruction()

    while True:
        command = str(input())
        if(command == "help"):
            cmdInstruction()
            continue
        sktToServer.send(command.encode())
        result = sktToServer.recv(1024).decode()
        if(result == "!logoutOK"):
            print()
            break
        elif(result == "!connectOK"):
            result = sktToServer.recv(1024).decode()
            
            #TODO
            
            continue
        print(result)




    
    
