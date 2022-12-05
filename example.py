import json, os, fnmatch

jan_arr = []
mcp_arr = []

with open("./example/janitor.json") as file: # with open se tu file.close() khi thao tac xong
    lst = json.load(file)
    for item in lst['jan_list']:
        if(item['jan_status'] == 'Available'):
	        jan_arr.append(item['jan_id'])

print(jan_arr) #Array bao gom cac janitor available
     
with open("./example/mcp.json") as file: # MCP id = 000 duoc coi la diem khoi hanh nen ko co value cua cap va janitor
    lst = json.load(file)
    for item in lst['mcp_list']:
        if(item['mcp_janitor'] == ''):
	        mcp_arr.append(item['mcp_id'])
         
print(mcp_arr) #Array bao gom cac MCP chua co janitor

# TODO: 1. Cap nhat id cua janitor duoc chon vao file json cua MCP tuong ung
# TODO: 2. Cap nhat id cua MCP duoc chon va janitor status vao file json cua janitor tuong ung
# Tren cai table janitor tren web, vi du o janitor 008 thi chon trong cai dropbox cai MCP 009 roi nhan assign thi se tuong tu nhu 2 cai input o duoi
# Khi nhan nut assign thi se load file python de process viec gan mcp vao janitor cap nhat vo file json cua mcp va jan
# Quan Bui se dung cai table va su dung noi dung cua file json de dien vo cai table do

# Vi du 1 function can implement
# jan_id = str(input()) #1 Chon 1 janitor nao d
# mcp_id = str(input()) #2 Chon 1 MCP nao do

# Append vao file json
with open("./example/route.json", "r+") as file:
    route_list = json.load(file)
    route_id = len(route_list["route_list"])
    route_direction = "M0 -> M1 -> M2 -> M0"
    route_length = 0
    route_time = 0
    new_route = {
                    "route_id": f"R{route_id}",
                    "route_direction": route_direction,
                    "route_length": f"{route_length} m",
                    "route_time": f"{route_time} mins",
                    "route_status": "Unassigned"
                }
    route_list["route_list"].append(new_route)
    file.seek(0)
    json.dump(route_list, file, indent = 4)