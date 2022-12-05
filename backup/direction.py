import googlemaps, json, os, fnmatch

map = googlemaps.Client(key="AIzaSyCT9dShISsjp0qie6WvIMUAEuSCEPlG1vo")
counter = len(fnmatch.filter(os.listdir("./result"), '*.json*'))

# Calculating shortest path
chosen_mcp_list = ["M4", "M1", "M3"]
chosen_mcp_list.insert(0, "M0")
id_list, coord_list = [], []
with open("./data/mcp.json", "r") as mcp_file:
    mcp_list = json.load(mcp_file)
    for chosen_mcp in chosen_mcp_list:
        for mcp in mcp_list["mcp_list"]:
            if(chosen_mcp == mcp['mcp_id']):
                id_list.append(mcp['mcp_id'])
                coord_list.append(mcp['mcp_coord'])
direction = map.directions(origin=coord_list[0], destination=coord_list[0], waypoints=coord_list[1:], optimize_waypoints = True, mode='driving')
center_lat = (direction[0]["bounds"]["northeast"]["lat"] + direction[0]["bounds"]["southwest"]["lat"]) / 2 # Find center of 2 bounds
center_lng = (direction[0]["bounds"]["northeast"]["lng"] + direction[0]["bounds"]["southwest"]["lng"]) / 2

# Write into json file
with open(f"./result/R{counter}.json", "w") as route_file:
    route_file.write(json.dumps(direction, indent=4))
    
with open("./data/route.json", "r+") as route_file:
    route_list = json.load(route_file)
    route_id = len(route_list["route_list"])
    route_ord = direction[0]["waypoint_order"]
    route_direction = "M0 -> "
    for idx in route_ord:
        route_direction += id_list[int(idx)] + " -> "
    route_direction += " -> M0"
    route_length, route_time = 0, 0
    for idx in direction[0]["legs"]:
        route_length += idx["distance"]["value"]
        route_time += idx["duration"]["value"]
    new_route = {
                    "route_id": f"R{route_id}",
                    "route_direction": route_direction,
                    "route_length": f"{route_length} m",
                    "route_time": f"{route_time} mins",
                    "route_status": "Unassigned"
                }
    route_list["route_list"].append(new_route)
    route_file.seek(0)
    json.dump(route_list, route_file, indent = 4)
    
# Plot map as an image
marker_list, waypoint_list = [], []
for leg in direction[0]["legs"]:
    leg_start_loc = leg["start_location"]
    marker_list.append(f'{leg_start_loc["lat"]},{leg_start_loc["lng"]}')
    for step in leg["steps"]:
        end_loc = step["end_location"]
        waypoint_list.append(f'{end_loc["lat"]},{end_loc["lng"]}')
last_stop = direction[0]["legs"][-1]["end_location"]
marker_list.append(f'{last_stop["lat"]},{last_stop["lng"]}')
markers = ["color:blue|size:mid|label:" + chr(65 + i) + "|" + r for i, r in enumerate(marker_list)]
map_direction = map.static_map( center = f"{center_lat},{center_lng}",
                                scale=2, 
                                zoom=13,
                                size=[1024, 1024], 
                                format="jpg", 
                                maptype="roadmap",
                                markers=markers,
                                path="color:0x0000ee|weight:2|" + "|".join(waypoint_list))

with open(f"./Result/R{counter}.jpg", "wb") as img:
    for chunk in map_direction:
        img.write(chunk)


    
    