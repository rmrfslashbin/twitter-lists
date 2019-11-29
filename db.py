import os
from pathlib import Path
import json


class JSON:
    def __init__(self, cfgFile="./data.json"):
        self.path = Path(cfgFile)

    def create(self):
        self.path.touch()
        return (True)

    def load(self):
        if not self.path.resolve().exists():
            self.create()
        dataSource = self.path.resolve()

        with dataSource.open() as f:
            try:
                self.data = json.loads(f.read())
            except json.decoder.JSONDecodeError:
                self.data = {}

        return(self.data)

    def save(self, data):
        self.path.resolve().exists()

        dataSource = self.path.resolve()

        with dataSource.open("w") as f:
            f.write(
                json.dumps(
                    data,
                    sort_keys=True,
                    indent=2,
                    separators=(',', ': ')
                )
            )
        return (True)


class DBFunctions(JSON):
    def __init__(self, cfgFile="./data.json"):
        super().__init__(cfgFile)
        self.users = {}
        self.lists = {}
        self.reverse = {}
        self.usersReverse = {}
        self.listsReverseOwnerID = {}
        self.data = self.load()

    def _setupUser(self, userID):
        self.users[userID] = {}
        self.users[userID]["follower"] = None
        self.users[userID]["screen_name"] = None
        self.users[userID]["in_lists"] = []
        self.users[userID]["blocked"] = False
        self.users[userID]["following"] = False

    def _setupList(self, listID):
        self.lists[listID] = {}
        self.lists[listID]["full_name"] = None
        self.lists[listID]["ownerID"] = None
        self.lists[listID]["owner_screen_name"] = None
        self.lists[listID]["slug"] = None

    def _reverse(self, uid, screen_name):
        self.usersReverse[screen_name] = uid

    def _blockedUsers(self):
        for u in self.data["blocks"]["data"]:
            self._reverse(u["id"], u["screen_name"])
            while True:
                try:
                    self.users[u["id"]]["blocked"] = True
                except KeyError:
                    self._setupUser(u["id"])
                    continue
                self.users[u["id"]]["screen_name"] = u["screen_name"]
                break

    def _followers(self):
        for u in self.data["followers"]["data"]:
            self._reverse(u["id"], u["screen_name"])
            while True:
                try:
                    self.users[u["id"]]["follower"] = True
                except KeyError:
                    self._setupUser(u["id"])
                    continue
                self.users[u["id"]]["screen_name"] = u["screen_name"]
                break

    def _following(self):
        for u in self.data["following"]["data"]:
            self._reverse(u["id"], u["screen_name"])
            while True:
                try:
                    self.users[u["id"]]["following"] = True
                except KeyError:
                    self._setupUser(u["id"])
                    continue
                self.users[u["id"]]["screen_name"] = u["screen_name"]
                break

    def _memberOfLists(self):
        for l in self.data["member_of_lists"]["data"]:
            listFullName = l["full_name"]
            listID = l["list_id"]
            owner_id = l["owner_id"]
            owner_screen_name = l["owner_screen_name"]
            slug = l["slug"]

            while True:
                try:
                    self.lists[listID]["full_name"] = listFullName
                except KeyError:
                    self._setupList(listID)
                    continue
                self.lists[listID]["owner_id"] = owner_id
                self.lists[listID]["owner_screen_name"] = owner_screen_name
                self.lists[listID]["slug"] = slug
                break

            for u in l["members"]:
                self._reverse(u["id"], u["screen_name"])
                while True:
                    try:
                        self.users[u["id"]]["in_lists"].append({
                            "list_id": listID, "listFullName": listFullName})
                    except KeyError:
                        self._setupUser(u["id"])
                        continue
                    self.users[u["id"]]["screen_name"] = u["screen_name"]
                    break

    def _usersLists(self):
        for l in self.data["users_lists"]["data"]:
            listFullName = l["full_name"]
            listID = l["list_id"]
            owner_id = l["owner_id"]
            owner_screen_name = l["owner_screen_name"]
            slug = l["slug"]

            while True:
                try:
                    self.lists[listID]["full_name"] = listFullName
                except KeyError:
                    self._setupList(listID)
                    continue
                self.lists[listID]["owner_id"] = owner_id
                self.lists[listID]["owner_screen_name"] = owner_screen_name
                self.lists[listID]["slug"] = slug
                break

            for u in l["members"]:
                self._reverse(u["id"], u["screen_name"])
                while True:
                    try:
                        self.users[u["id"]]["in_lists"].append({
                            "list_id": listID, "listFullName": listFullName})
                    except KeyError:
                        self._setupUser(u["id"])
                        continue
                    self.users[u["id"]]["screen_name"] = u["screen_name"]
                    break

    def _listSlugToOwnerID(self):
        for l in self.data["lists"]:
            listID = l
            slug = self.data["lists"][listID]["slug"]
            ownerID = self.data["lists"][listID]["owner_id"]

            self.listsReverseOwnerID[slug] = ownerID

    def commit(self):
        try:
            self.data["users"] = self.users
            self.data["lists"] = self.lists
            self.data["usersReverseLookup"] = self.usersReverse
            self.data["listsReverseLookupOwnerID"] = self.listsReverseOwnerID
            self.save(self.data)
        except BaseException:
            raise

        return(True)

    def process(self):
        try:
            self._blockedUsers()
            self._followers()
            self._following()
            self._memberOfLists()
            self._usersLists()
            # self._listSlugToOwnerID()
        except BaseException:
            raise

        return(True)
