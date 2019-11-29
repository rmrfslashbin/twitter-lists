#!/usr/bin/env python3

from twitterUtils import TwitterUtils, Fetch
from db import DBFunctions


#t = TwitterUtils()
f = Fetch()

#raise SystemExit

print("Getting friends/follows")
f.getFriends()

print("Getting followers")
f.getFollowers()

print("Getting blocked users")
f.getBlocks()

print("Getting user's lists and lists to which user subscribes")
f.getLists()

print("Getting list of which the user is a member")
f.getListMemberships()

print("Saving data...")
f.save()

print("Generating list data and user maps")
j = DBFunctions()
try:
    j.process()
except BaseException:
    raise
j.commit()

print("Done!")
