import time, socket, random, re
from threading import Thread
from datetime import datetime

HOST = socket.gethostname()
IP = socket.gethostbyname(HOST)
PORT = 5002
SERVER_IP = "192.168.1.10"
name = "Anon"
busy = False
print(f"\n{HOST} : {IP} : {PORT}")

def pserver():
    while busy == False:
        skt_from_client, addr_from_client = server_skt.accept()
        busy = True
        # skt_to_server.send("!busy".encode())
        time_now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        print("\033[1;32m" + f"\n[{time_now}] *Received connection from {addr_from_client[0]} : {addr_from_client[1]}*" + "\033[1;37m")
        t = Thread(target=pserver_listen, args=(skt_from_client,), daemon=True)
        t.start()

def pserver_listen(func_skt):
    while True:
        receive_message = func_skt.recv(1024).decode()
        if(receive_message == "!quit"):
            skt_to_client.send(receive_message.encode())
            time.sleep(2) 
            break
        print(receive_message)
    func_skt.close()

def pserver_listen_mserver():
    while True:
        result = skt_to_server.recv(1024).decode()
        if(result == "!logok" or result == "!regok"):
            result = skt_to_server.recv(1024).decode()
            name = result
            result = f"\n*Welcome to the server {name}*"
        elif(result == "!conok"):
            result = skt_to_server.recv(1024).decode()
            try:
                skt_to_client.connect((result, PORT))
                skt_to_server.send("!busy".encode())
            except Exception as e:
                print(e)
            result = "\n*Connection established*"
        print(result)

def outer_instruction():
    print("\n1.  Enter !login <Username> <Password> to login." 
        + "\n2.  Enter !logout to logout." 
        + "\n3.  Enter !register <Username> <Password> to register an account."
        + "\n4.  Enter !connect <Friend_username> to connect to a friend."
        + "\n---------------------------"
        + "\n5.  Enter !info to see your info. (Name, Password, Online status, Friends)"
        + "\n6.  Enter !change_p <New_password> to change password."
        + "\n---------------------------"
        + "\n7.  Enter !user_list to see all users."
        + "\n8.  Enter !add <Friend_username> to add a friend."
        + "\n9.  Enter !remove <Friend_username> to remove a friend."
        + "\n---------------------------"
        + "\n10. Enter !help to see instructions."
        + "\n11. ...\n")
    
def inner_instruction():
    print("\n1.  Enter !quit to quit chatting." 
        + "\n2.  Press !info to see your info."
        + "\n3.  Press !user_list to see all users."
        + "\n5.  Press !help to see instructions."
        + "\n6.  ..."
        + "\n*Note: For to access other features you need to quit chatting first.*\n")


if __name__ == '__main__':
    skt_list = set()
    server_skt, skt_to_server, skt_to_client = socket.socket(), socket.socket(), socket.socket()

    # try:
    #     skt_to_server.connect((SERVER_IP, PORT))
    #     t = Thread(target=pserver_listen, daemon=True)
    #     t.start()
    # except Exception as e:
    #     print(e)

    server_skt.bind((IP, PORT))
    server_skt.listen()
    t = Thread(target=pserver, daemon=True)
    t.start()

    outer_instruction()
    while True:
        command = str(input())
        command_arr = command.split()
        if(command_arr[0] == "!login" and len(command_arr) == 3):
            skt_to_server.send(command.encode())
        elif(command_arr[0] == "!logout" and len(command_arr) == 1):
            skt_to_server.send(command.encode())
        elif(command_arr[0] == "!register" and len(command_arr) == 3):
            skt_to_server.send(command.encode())
        elif(command_arr[0] == "!connect" and len(command_arr) == 2):
            # skt_to_server.send(command.encode())
            try:
                skt_to_client.connect((command_arr[1], PORT))
            except Exception as e:
                print(e)
                result = "\n*Connection established*"
            # skt_to_server.send("!busy".encode())
            busy = True
            inner_instruction()
            while True:
                message = str(input())
                if(message == '!quit'):
                    if(busy):
                        skt_to_client.send(message.encode())
                    skt_to_client.close()
                    skt_to_client = socket.socket()
                    t = Thread(target=pserver, daemon=True)
                    t.start()
                    break
                elif(message == '!info'):
                    skt_to_server.send(message.encode())
                elif(message == '!user_list'):
                    skt_to_server.send(message.encode())
                elif(message == '!help'):
                    inner_instruction()
                else:
                    time_now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                    skt_to_client.send(f"[{time_now}] {name} : {message}".encode()) 
        elif(command_arr[0] == '!info' and len(command_arr) == 1):
            skt_to_server.send(command.encode())
        elif(command_arr[0] == '!change_n' and len(command_arr) == 2):
            skt_to_server.send(command.encode())
        elif(command_arr[0] == '!change_p' and len(command_arr) == 2):
            skt_to_server.send(command.encode())
        elif(command_arr[0] == '!user_list' and len(command_arr) == 1):
            skt_to_server.send(command.encode())
        elif(command_arr[0] == '!friend_list' and len(command_arr) == 1):
            skt_to_server.send(command.encode())
        elif(command_arr[0] == '!add' and len(command_arr) == 2):
            skt_to_server.send(command.encode())
        elif(command_arr[0] == '!remove' and len(command_arr) == 2):
            skt_to_server.send(command.encode())
        elif(command_arr[0] == '!help' and len(command_arr) == 1):
            outer_instruction()
        else:
            print("\nUnknown command")




    
    
