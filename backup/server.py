import time, socket, os
from threading import Thread
from datetime import datetime

HOST = socket.gethostname()
IP = socket.gethostbyname(HOST)
PORT = 5002
print(f"\n{HOST} : {IP} : {PORT}")

def accept_peer():
    while True:
        skt_from_client, addr_from_client = server_skt.accept()
        sktlist.add(skt_from_client)
        time_now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        print("\033[1;32m" + f"\n[{time_now}] *Received connection from {addr_from_client[0]} : {addr_from_client[1]}*" + "\033[1;37m")
        t = Thread(target=listen_to_peer, args=(skt_from_client, addr_from_client[0]), daemon=True)
        t.start()

def listen_to_peer(func_skt, func_addr):
    while True:
        rcommand = func_skt.recv(1024).decode()
        rcommandArr = rcommand.split()
        if(rcommandArr[0] == '!login'): # !login <Username> <Password>
            print()
        elif(rcommandArr[0] == '!logout'):
            file_exist = cmd_search_file("$NA", "$NA", func_addr)
            if(file_exist == "-1"):
                func_skt.send("\nNot logged in!".encode())
            else:
                if(cmd_search_infile(file_exist, 3) == "0"):
                    func_skt.send("\nNot logged in!".encode())
                else:
                    cmd_change_infile(file_exist, 3, "0", 0)
                    func_skt.send("\nLogout successfully!".encode())
        elif(rcommandArr[0] == "!register"):
            file_exist = cmd_search_file("$NA", "$NA", func_addr) 
            if(file_exist == "-1"):
                file_exist = cmd_search_file(rcommandArr[1], "$NA", "$NA")
                if(file_exist == "-1"): 
                    cmd_add_file(rcommandArr[1], rcommandArr[2], func_addr, "1")
                    # func_skt.send("Account successfully registered!".encode())
                    func_skt.send("!regok".encode())
                    func_skt.send(f"{rcommandArr[1]}".encode())
                else:
                    func_skt.send("\nAccount already registered! (1 account is bound to only 1 IP and vice versa)".encode())
            else:
                func_skt.send("\nIP is already registered! (1 account is bound to only 1 IP and vice versa)".encode())
        elif(rcommandArr[0] == "!connect"):            
            file_exist = cmd_search_file("$NA", "$NA", func_addr)
            if(file_exist == "-1"):
                func_skt.send("\nNot logged in!".encode())
            else:
                if(cmd_search_infile(file_exist, 3) == "0"):
                    func_skt.send("\nNot logged in!".encode())
                else:
                    file_exist = cmd_search_file(rcommandArr[1], "$NA", "$NA")
                    if(file_exist == "-1"):
                        func_skt.send(f"No account named {rcommandArr[1]}".encode())
                    else:
                        friend_ip = cmd_search_infile(file_exist, 2)
                        func_skt.send("!conok".encode())
                        func_skt.send(friend_ip.encode())
        elif(rcommandArr[0] == "!info"):
            file_exist = cmd_search_file("$NA", "$NA", func_addr)
            if(file_exist == "-1"):
                func_skt.send("\nNot logged in!".encode())
            else:
                if(cmd_search_infile(file_exist, 3) == "0"):
                    func_skt.send("\nNot logged in!".encode())
                else:
                    to_send = "\n<Username> <Password> <IP> <Online> <Busy> <Friends>\n" + cmd_search_infile(file_exist, -1)
                    func_skt.send(to_send.encode())
        elif(rcommandArr[0] == "!change_p"):
            file_exist = cmd_search_file("$NA", "$NA", func_addr)
            if(file_exist == "-1"):
                func_skt.send("\nNot logged in!".encode())
            else:
                if(cmd_search_infile(file_exist, 3) == "0"):
                    func_skt.send("\nNot logged in!".encode())
                else:
                    cmd_change_infile(file_exist, 1, rcommandArr[1], 0)
                    func_skt.send("\nPassword changed successfully!".encode())
        elif(rcommandArr[0] == "!user_list"):
            to_send = "\n<Username> <Password> <IP> <Online> <Busy> <Friends>" + cmd_search_infile("$all", -1)
            func_skt.send(to_send.encode())
        elif(rcommandArr[0] == "!add"):
            file_exist = cmd_search_file("$NA", "$NA", func_addr)
            if(file_exist == "-1"):
                func_skt.send("\nNot logged in!".encode())
            else:
                if(cmd_search_infile(file_exist, 3) == "0"):
                    func_skt.send("\nNot logged in!".encode())
                else:
                    if(cmd_search_file(rcommandArr[1], "$NA", "$NA") == "-1"):
                        func_skt.send(f"\nUser {rcommandArr[1]} not found!".encode())
                    else:
                        if(cmd_change_infile(file_exist, 5, rcommandArr[1], 1)):
                            func_skt.send(f"\n{rcommandArr[1]} is already a friend!".encode())
                        else:
                            func_skt.send("\nFriend added successfully!".encode())
        elif(rcommandArr[0] == "!remove"):
            file_exist = cmd_search_file("$NA", "$NA", func_addr)
            if(file_exist == "-1"):
                func_skt.send("\nNot logged in!".encode())
            else:
                if(cmd_search_infile(file_exist, 3) == "0"):
                    func_skt.send("\nNot logged in!".encode())
                else:
                    temp_friend_list = cmd_search_infile(file_exist, 5)
                    if(len(temp_friend_list) == 1):
                        func_skt.send("\nYou don't have any friend!".encode())
                    else:
                        if(cmd_change_infile(file_exist, 5, rcommandArr[1], -1)):
                            func_skt.send("\nFriend removed successfully!".encode())
                        else:
                            func_skt.send(f"\n{rcommandArr[1]} is not in your friend list!".encode())
        elif(rcommandArr[0] == "!busy"):
            file_exist = cmd_search_file("$NA", "$NA", func_addr)
            cmd_change_infile(file_exist, 4, "1", 0)
            

def cmd_search_file(name, pwd, ip):
    for file in os.listdir():
        if(file.endswith(".txt")):
            user = open(f"{file}", "r")
            line = user.readline()
            user.close()
            user_info = line.split()
            if((user_info[0] == name or name == "$NA") 
            and (user_info[1] == pwd or pwd == "$NA") 
            and (user_info[2] == ip or ip == "$NA")):
                return file
    return "-1"

def cmd_search_infile(file, index):
    if(file == "$all"):
        friend_list = ""
        for file in os.listdir():
            if(file.endswith(".txt")):
                user = open(f"{file}", "r")
                line = user.readline()
                user.close()
                friend_list += "\n" + line
        return friend_list
    else:
        user = open(f"{file}", "r")
        line = user.readline()
        user.close()
        user_info = line.split()
        if(index == -1):
            return line
        else:
            return user_info[index]

def cmd_add_file(file, pwd, ip, online):
    user = open(f"{file}.txt", "w")
    user.write(f"{file} {pwd} {ip} {online} 0 {file}")
    user.close()
    
def cmd_change_infile(file, index, change, opt):
    user = open(f"{file}", "r")
    line = user.readline()
    user.close()
    user_info = line.split()
    data = user_info[index].split(":")
    data_exist = False
    if(opt == -1):
        for item in data:
            if(item == change):
                data.remove(item)
                data_exist = True
                break
        if(data_exist):    
            user_info[index] = ":".join(data)      
    elif(opt == 0):
        user_info[index] = change
    else:
        for item in data:
            if(item == change):
                data_exist = True
                break
        if(data_exist == False):
            user_info[index] += ":" + change
    user = open(f"{file}", "w")
    user.write(f"{user_info[0]} {user_info[1]} {user_info[2]} {user_info[3]} {user_info[4]} {user_info[5]}")
    user.close()
    return data_exist
    
def cmdInstruction():
    print("\n1. Press !user_list to show all user list."
        + "\n2. Enter !add <Username> <Password> <IP> to add a user."
        + "\n3. Enter !remove <Username> <Password> to remove a user."
        + "\n4. Enter !help to see instructions."
        + "\n5. ...\n")

if __name__ == '__main__':
    sktlist = set()
    server_skt = socket.socket()
    
    server_skt.bind((IP, PORT))
    server_skt.listen()
    t = Thread(target=accept_peer, daemon=True)
    t.start()
    
    cmd_instruction()
    while True:
        command = str(input())
        commandArr = command.split()
        if(commandArr[0] == "!user_list" and len(commandArr) == 1):
            print("\n<Username> <Password> <IP> <Online> <Busy> <Friends>" + cmd_search_infile("$all", -1))
        elif(commandArr[0] == "!add" and len(commandArr) == 4):
            file_exist = cmd_search_file("$NA", "$NA", commandArr[3]) 
            if(file_exist == "-1"):
                file_exist = cmd_search_file(commandArr[1], "$NA", "$NA")
                if(file_exist == "-1"): 
                    cmd_add_file(commandArr[1], commandArr[2], commandArr[3], "0")
                    print("\nAccount successfully registered!")
                else:
                    print("\nAccount already registered!")
            else:
                print("\IP already registered!")
        elif(commandArr[0] == "!remove" and len(commandArr) == 2):
            file_exist = cmd_search_file(commandArr[1], "$NA", "$NA")
            if(file_exist == "-1"):
                print(f"\nAccount {commandArr[1]} not found!")
            else:
                os.remove(f"{file_exist}")
                print(f"\nAccount {commandArr[1]} successfully removed!") 
        elif(commandArr[0] == "!help" and len(commandArr) == 1):
            cmd_instruction()
        elif(commandArr[0] == "!reset" and len(commandArr) == 1):
            for file in os.listdir():
                if(file.endswith(".txt")):
                    user = open(f"{file}", "r")
                    line = user.readline()
                    user.close()
                    user_info = line.split()
                    user = open(f"{file}", "w")
                    user.write(f"{user_info[0]} {user_info[1]} {user_info[2]} 0 0 {user_info[5]}")
                    user.close()
            print(f"\n*Reset all accounts*")           
        else:
            print("\nUnknown command")