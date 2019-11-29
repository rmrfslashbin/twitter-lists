#!/usr/bin/env python3

from twitterUtils import TwitterUtils, Fetch
from db import JSON
from utils import jsonPrint
import argparse
import time

parser = argparse.ArgumentParser(
    description='Lookup Twiter User by User Number')
group = parser.add_mutually_exclusive_group(required=True)
parser.add_argument(
    '--since',
    nargs=1,
    type=str,
    help="Start at status following...")
parser.add_argument('--json', action='store_true', help="Ouput data in JSON")
parser.add_argument(
    '--count',
    type=int,
    help="Number of tweets to show (defualt = 5)")
parser.add_argument('--timer', type=int, help="Loop with delay of (x) seconds")
group.add_argument('-l', '--lid', nargs=1, type=str,
                   help="Twitter list ID to stream")
group.add_argument('-n', '--name', nargs=1, type=str, help="Twitter list name")
group.add_argument(
    '-s',
    '--show',
    action='store_true',
    help="Show a listing of lists")

args = parser.parse_args()

# Load up the local cache
j = JSON()
data = j.load()

# Just show a list of lists from the cache
if args.show:
    jsonOut = []
    for l in data["lists"]:
        listID = l
        slug = data["lists"][listID]["slug"]
        owner = data["lists"][listID]["owner_screen_name"]
        if args.json:
            jsonOut.append({"list_id": listID, "slug": slug, "owner": owner})
        else:
            print(f"{listID.rjust(20, ' ')} :: {slug.rjust(25, ' ')} :: {owner}")
    if args.json:
        jsonPrint({"lists": jsonOut})

# Init list vars
lid = None
slug = None
ownerID = None
jsonOut = []
loop = True
timer = 0


# Set the list ID, if provided
if args.lid:
    lid = args.lid[0]

# Set the name, if provided
if args.name:
    # Using a list name requires the owner ID
    slug = args.name[0]
    ownerID = data["listsReverseLookupOwnerID"][slug]

# If either were actuall provided... init a new Fetch obj
if lid or slug:
    fetch = Fetch()

    # Set up the since_id. If set, fetch tweets AFTER this ID
    since_id = None
    if args.since:
        since_id = args.since[0]

    # Max number of tweets to fetch
    count = None
    if args.count:
        # for some reason... the API fetches count - 1.
        count = args.count + 1

    # Timer, if it was set
    if args.timer:
        timer = args.timer

    # Loop is set to True for the first loop... so the loop actually execs
    while loop:
        # GO!
        for s in fetch.getListTimeline(
                lid,
                slug,
                ownerID,
                since_id=since_id,
                count=count):
            # Pull out the useful bits
            created_at = s.created_at
            since_id = s.id_str
            favorite_count = s.favorite_count
            hashtags = s.hashtags
            retweet_count = s.retweet_count
            text = s.text
            url = []
            user = s.user.screen_name

            # Just get the short URLs
            for u in s.urls:
                url.append(u.url)

            # JSON output
            if args.json:
                jsonOut.append({
                    "created_at": created_at,
                    "id": since_id,
                    "favorite_count": favorite_count,
                    "hashtags": hashtags,
                    "retweet_count": retweet_count,
                    "text": text,
                    "urls": url,
                    "user": user})
            else:
                # Make the hastags pretty
                hashtagList = []
                if len(hashtags) < 1:
                    hashtagList = ["(None)"]
                else:
                    for hashtag in hashtags:
                        hashtagList.append(hashtag.text)

                # Non JSON display
                print(f"ID: {since_id}")
                print(f"Posted by: @{user} at: {created_at}")
                print(f"  {text}")
                print(f"hashtags: {' '.join(hashtagList)}")
                print(
                    f"Favorited {favorite_count} times. Retweeted {retweet_count} times.")
                print(url)
                print("\n\n")

        if args.json:
            # Actually print the JSON
            jsonPrint({"tweets": jsonOut})

        if args.timer:
            # If the timer was set...
            if not args.json:
                # Tell the non-JSON displays why we're sleeping
                print(f"(Sleeping {args.timer}) seconds.\n")
            # sleep
            time.sleep(args.timer)
        else:
            # Otherwise...
            # Disable "while" if looping was not intended (ie: 1 run only)
            loop = False


# Example of getListTimeline output
'''
{
  "created_at": "Sat Dec 22 11:08:02 +0000 2018",
  "favorite_count": 1,
  "hashtags": [],
  "id": 1076434180614037504,
  "id_str": "1076434180614037504",
  "lang": "en",
  "retweet_count": 1,
  "source": "<a href=\"http://www.socialnewsdesk.com\" rel=\"nofollow\">SocialNewsDesk</a>",
  "text": "A Canada goose and a ring-billed gull are recovering at a wildlife center after eating pills that were dumped in a\u2026 https://t.co/tWibemTXJv",
  "truncated": true,
  "urls": [{
    "expanded_url": "https://twitter.com/i/web/status/1076434180614037504",
    "url": "https://t.co/tWibemTXJv"
  }],
  "user": {"see below..."},
  "user_mentions": []
}
'''

'''
"user": {
  "created_at": "Wed Apr 11 12:50:15 +0000 2007",
  "description": "Atlanta's best source for news. You can reach our customer service team here: @AJCassist",
  "favourites_count": 495,
  "followers_count": 1038796,
  "following": true,
  "friends_count": 56451,
  "geo_enabled": true,
  "id": 4170491, "id_str": "4170491",
  "lang": "en",
  "listed_count": 5021,
  "location": "Atlanta, GA",
  "name": "AJC",
  "profile_background_color": "00539B",
  "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
  "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
  "profile_banner_url": "https://pbs.twimg.com/profile_banners/4170491/1537904419",
  "profile_image_url":
  "http://pbs.twimg.com/profile_images/952541825495166977/l4hFbA20_normal.jpg",
  "profile_image_url_https": "https://pbs.twimg.com/profile_images/952541825495166977/l4hFbA20_normal.jpg",
  "profile_link_color": "00539B",
  "profile_sidebar_border_color": "FFFFFF",
  "profile_sidebar_fill_color": "F0F5ED",
  "profile_text_color": "333333",
  "screen_name": "ajc",
  "statuses_count": 234629,
  "url": "https://t.co/jvkZJ5B2LG",
  "verified": true}
'''
