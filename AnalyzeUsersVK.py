import requests
import time


class AnalyzeUsersVK(object):

    def __init__(self, token, version):
        self.token = token
        self.version = version

    def getUserInfo(self, userId):
        fields = "sex,bdate,city,country,contacts,site,education,occupation,interests,activities,career"
        return requests.post("https://api.vk.com/method/users.get?user_ids=" + str(userId) + "&fields=" + fields + "&access_token=" + self.token + "&v=" + self.version).json()

    def getUsersInfo(self, usersList):
        users = []
        for i in usersList:
            try:
                users.append(self.getUserInfo(i["id"])["response"][0])
                time.sleep(0.4)
            except:
                print(self.getUserInfo(i["id"]))
                continue
        return users
    
    def getUsersWithInterests(self, usersInfo):
        users = []
        for i in usersInfo:
            if "interests" in i.keys() and i["interests"] != "":
                users.append(i)
        return users

    def getUsersWithCareer(self, usersInfo):
        users = []
        for i in usersInfo:
            if "career" in i.keys() and  len(i["career"]) != 0:
                users.append(i)
        return users
