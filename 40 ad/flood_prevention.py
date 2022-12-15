import json
class FloodPrevention:
    def __init__(self, timer):
        self.timer = timer

    def checkTimers(self):
        timerList = []
        with open("userData.json","r") as userfile:
            data = json.load(userfile)
            ads = data["Ads"]
            for ad in ads:
                timerList.append(ad["Ad Timer"])

        numberOfTimer10Secs = timerList.count(10)
        numberOfTimer30Secs = timerList.count(30)


        if((self.timer == 10 and numberOfTimer10Secs > 1) or (self.timer == 30 and numberOfTimer30Secs > 2)):
            return False
        else:
            return True

    def calculateAdsPerMinute(self):
        timerList = []
        limit = 20
        with open("userData.json","r") as userfile:
            data = json.load(userfile)
            ads = data["Ads"]
            for ad in ads:
                timerList.append(ad["Ad Timer"])

            for timer in timerList:
                timerPostPerMinute = 60/timer
                limit = limit - timerPostPerMinute


        currentTimerPostPerMinute = 60/self.timer
        limit = limit - currentTimerPostPerMinute

        print(limit)
        print(currentTimerPostPerMinute)

        if(limit >= 0):
            return True
        else:
            return False

if __name__ == '__main__':
    FloodPrevention(20).calculateAdsPerMinute()