# -*- coding: utf-8 -*-
import json
class SaveData:
    def __init__(self, adTitle=None, adContent=None, channelList=None, adTimer=None, channelName = None,  channelID = None):
        self.adTitle = adTitle
        self.adContent = adContent
        self.adTimer = adTimer
        self.channelList = channelList
        self.channelName = channelName
        self.channelID = channelID

    def _createAdDict(self):
        adJson = {"Ad Title":"{}".format(self.adTitle),
                  "Ad Content":"{}".format(self.adContent),
                  "Ad Channels":self.channelList,
                  "Ad Timer":self.adTimer
                   }

        return adJson

    def saveAdToJson(self):
        with open("userData.json","r+") as jsonFile:
            data = json.load(jsonFile)
            adDict = self._createAdDict()
            data["Ads"].append(adDict)
            print(data)
            convertedData = json.dumps(data)

            jsonFile.seek(0)
            jsonFile.write(convertedData) #once yaziyoruz, cursor sona geliyor
            jsonFile.truncate()#sonra yazdigimiz veriden once ne varsa siliyoruz. OVERWRITE
            #https://stackoverflow.com/questions/2424000/read-and-overwrite-a-file-in-python

    def saveChanneltoJson(self):
        with open("userData.json","r+") as jsonFile:
            data = json.load(jsonFile)
            channelDict = {"{}".format(self.channelName):"{}".format(self.channelID)}
            data["channels"].update(channelDict)

            convertedData = json.dumps(data)

            jsonFile.seek(0)
            jsonFile.write(convertedData)
            jsonFile.truncate()

if __name__ == '__main__':
    SaveData(adTitle="qwqwq", adContent="qwqeqe!", adTimer=5).saveAdToJson()
