#!/usr/bin/env python3

from datetime import datetime
from db import JSON
from utils import jsonPrint

j = JSON()
data = j.load()

print("Non blocked users their assigned list(s):\n")
for user in data["users"]:
    if len(data["users"][user]["in_lists"]
           ) > 0 and not data["users"][user]["blocked"]:
        inLists = []
        for l in data["users"][user]["in_lists"]:
            inLists.append(l["listFullName"])
        print(f"{data['users'][user]['screen_name']} : {' :: '.join(inLists)}")
