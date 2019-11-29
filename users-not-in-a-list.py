#!/usr/bin/env python3

from datetime import datetime
from db import JSON
from utils import jsonPrint

j = JSON()
data = j.load()

print("Non blocked users, not in a list:\n")
for user in data["users"]:
    if len(data["users"][user]["in_lists"]
           ) < 1 and not data["users"][user]["blocked"]:
        print(user, data["users"][user]["screen_name"])
        # jsonPrint(data["users"][user])
