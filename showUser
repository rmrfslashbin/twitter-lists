#!/usr/bin/env python

from db import JSON
from utils import jsonPrint
from twitterUtils import Fetch
import argparse

parser = argparse.ArgumentParser(
    description='Lookup Twiter User by User Number')

mx_group = parser.add_mutually_exclusive_group()
mx_group.add_argument('-u', '--uid', nargs=1, type=str, help="Twitter user ID")
mx_group.add_argument(
    '-n',
    '--name',
    nargs=1,
    type=str,
    help="Twitter screen name")

subparsers = parser.add_subparsers(
    dest='command',
    required=True,
    help='sub-command help')
parser_list = subparsers.add_parser('list', help='List users')
parser_search = subparsers.add_parser('search', help='Search for a  user')

parser.add_argument(
    '-o',
    '--online',
    action='store_true',
    help="Search on-line, not cache")
args = parser.parse_args()

j = JSON()
data = j.load()

if args.command == "list":
    print(f"{ 'User ID'.rjust(25, ' ') } :: Screen Name")
    for u in data["users"]:
        print(f"{u.rjust(25, ' ') } :: { data['users'][u]['screen_name'] }")
elif args.command == "search":
    if args.online:
        if not args.uid or args.name:
            print("UID or name must be specified")
        else:
            f = Fetch()
            f.searchUser(args.uid, args.name)
            print("Not yet implimented")
    else:
        if args.name:
            print(f"{uid} ==> {args.name[0]}")
            jsonPrint(data["users"][uid])
        elif args.uid:
            print(f"User ID {args.uid[0]}")
            jsonPrint(data["users"][args.uid[0]])
