from datetime import datetime
import twitter
from settings import Settings
from db import JSON


class TwitterUtils:

    def __init__(self):
        self.config = Settings()
        self.settings = self.config.load()

        self.jsonDB = JSON()
        self.load()

        self.api = twitter.Api(
            consumer_key=self.settings["consumer"]["key"],
            consumer_secret=self.settings["consumer"]["secret"],
            access_token_key=self.settings["access"]["token"],
            access_token_secret=self.settings["access"]["secret"])

    def save(self):
        self.jsonDB.save(self.data)

    def load(self):
        self.data = self.jsonDB.load()


class Fetch(TwitterUtils):

    def __init__(self):
        super().__init__()

    def _makeDataObj(self, contents, data):
        dataObj = {
            "contents": contents,
            "timestamp": str(datetime.now()),
            "forUser": {
                "name": self.settings["owner"]["accountName"],
                "id": self.settings["owner"]["id"]
            },
            "data": data
        }
        return(dataObj)

    def _getListMembers(self, list_id):
        l = []
        nextC = -1
        while nextC != 0:
            # members of a list
            nextC, previousC, listData = self.api.GetListMembersPaged(
                list_id=list_id, cursor=nextC)
            for i in listData:
                l.append({"id": i.id, "screen_name": i.screen_name})
        return(l)

    def getFriends(self):
        l = []
        nextC = -1
        while nextC != 0:
            # Who is the user following
            nextC, previousC, listData = self.api.GetFriendsPaged(cursor=nextC)
            for i in listData:
                l.append({"id": i.id, "screen_name": i.screen_name})

        self.data["following"] = self._makeDataObj("following", l)

    def getFollowers(self):
        l = []
        nextC = -1
        while nextC != 0:
            # Who is following the user
            nextC, previousC, listData = self.api.GetFollowersPaged(
                cursor=nextC)
            for i in listData:
                l.append({"id": i.id, "screen_name": i.screen_name})

        self.data["followers"] = self._makeDataObj("followers", l)

    def getBlocks(self):
        l = []
        nextC = -1
        while nextC != 0:
            ## Who is blocked
            nextC, previousC, listData = self.api.GetBlocksPaged(cursor=nextC)
            for i in listData:
                l.append({"id": i.id, "screen_name": i.screen_name})

        self.data["blocks"] = self._makeDataObj("blocks", l)

    def getLists(self):
        l = []
        # All list a users subscribes to AND their created lists
        listData = self.api.GetListsList(user_id=self.settings["owner"]["id"])
        for i in listData:
            l.append({
                "list_id": i.id,
                "full_name": i.full_name,
                "slug": i.slug,
                "owner_screen_name": i.user.screen_name,
                "owner_id": i.user.id,
                "members": self._getListMembers(i.id)})

        self.data["users_lists"] = self._makeDataObj("users_lists", l)

    def getListMemberships(self):
        l = []
        # lists user is a member of
        listData = self.api.GetMemberships(count=1000)
        for i in listData:
            l.append({
                "list_id": i.id,
                "full_name": i.full_name,
                "slug": i.slug,
                "owner_screen_name": i.user.screen_name,
                "owner_id": i.user.id,
                "members": self._getListMembers(i.id)})

        self.data["member_of_lists"] = self._makeDataObj("member_of_lists", l)

    def getListTimeline(self, lid, slug, ownerID, since_id=None, count=5):
        return (
            self.api.GetListTimeline(
                list_id=lid,
                slug=slug,
                owner_id=ownerID,
                since_id=since_id,
                count=count))

    def searchUser(self, uid=None, screen_name=None):
        return True
