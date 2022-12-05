    with open("./user.json", "r+") as file:
        userList = json.load(file)
        if(username == userList["username"] and password == userList["password"]):
            return(userList["username"], userList["password"], userList["ip"], userList["online"], userList["friend"])
        else:
            return(-1, -1, -1, -1, -1)