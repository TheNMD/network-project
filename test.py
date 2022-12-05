import json
    
username = "asdas"
password = "123452"    

with open("./user.json", "r+") as file:
    userList = json.load(file)
    for idx in range(len(userList["userList"])):
        print(userList["userList"][idx], "\n")
