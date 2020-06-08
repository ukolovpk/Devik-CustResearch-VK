import requests
import datetime
from utils.Commons import Commons


class AnalyzeCommunitiesVK(object):

    def __init__(self, token, version):
        self.token = token
        self.version = version
        self.commons = Commons()

    def getSubscribers(self, groupId):
        offset = 0
        countItems = requests.post("https://api.vk.com/method/groups.getMembers?group_id=" + groupId + "&sort=id_asc" + \
            "&count=1000&fields=sex,bdate,country&access_token=" + self.token + "&v=" + self.version).json()["response"]["count"]
        count = int(countItems / 1000) + 1
        subscribers = []
        for i in range(count):
            url = "https://api.vk.com/method/groups.getMembers?group_id=" + groupId + "&sort=id_asc&offset=" + \
                str(offset) + "&count=1000&fields=sex,bdate,country&access_token=" + \
                self.token + "&v=" + self.version
            response = requests.post(url)
            offset += 1000
            if response.status_code == 200 and not("error" in response.json().keys()):
                for i in response.json()["response"]["items"]:
                    subscribers.append(i)
            else:
                print(response.json())
                raise NameError(
                    "Status code or response is wrong: " + str(response.status_code))
        return subscribers


    def getParents(self, subscribers):
        parents = []
        for i in subscribers:
            try:
                bdate = [int(i) for i in i["bdate"].split(".")]
            except:
                continue
            if len(bdate) == 3:
                bdateDate = datetime.date(bdate[2], bdate[1], bdate[0])
                age = self.commons.calculateAge(bdateDate)
                if age >= 26:
                    parents.append(i)
            else:
                continue
        return parents


    def getKids(self, subscribers):
        kids = []
        for i in subscribers:
            try:
                bdate = [int(i) for i in i["bdate"].split(".")]
            except:
                continue
            if len(bdate) == 3:
                bdateDate = datetime.date(bdate[2], bdate[1], bdate[0])
                age = self.commons.calculateAge(bdateDate)
                if age <= 14:
                    kids.append(i)
            else:
                continue
        return kids


    def calculateAverAge(self, subs):
        years = 0
        subscribersWithAge = 0
        for i in subs:
            try:
                bdate = [int(i) for i in i["bdate"].split(".")]
            except:
                continue
            if len(bdate) == 3:
                bdateDate = datetime.date(bdate[2], bdate[1], bdate[0])
                age = self.commons.calculateAge(bdateDate)
                subscribersWithAge += 1
            else:
                continue
            years += age
        return years / subscribersWithAge


    def calculateSex(self, subs):
        subscribersWithSex = 0
        male = 0
        female = 0
        for i in subs:
            try:
                sex = i["sex"]
                subscribersWithSex += 1
            except:
                continue
            if sex == 1:
                female += 1
            elif sex == 2:
                male += 1
        return {"male": male / subscribersWithSex * 100, "female": female / subscribersWithSex * 100}
