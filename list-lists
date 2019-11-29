#!/usr/bin/env python3

from datetime import datetime
from db import JSON
from utils import jsonPrint

j = JSON()
data = j.load()

print(f"{'list ID':20s} {'list owner':15s} list name")
for list in data["lists"]:
    listObj = data["lists"][list]
    print(f"{list:20s} {listObj['owner_screen_name']:15s} {listObj['slug']}")
