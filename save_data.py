# -*- coding: utf-8 -*-
import json
class SaveData:
    def __init__(self, adTitle=None, adContent=None, adTimer=None):
        self.adTitle = adTitle
        self.adContent = adContent
        self.adTimer = adTimer

    def _createAdDict(self):
        adJson = {"Ad Title":"{}".format(self.adTitle),
                  "Ad Content":"{}".format(self.adContent),
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

if __name__ == '__main__':
    SaveData(adTitle="qwqwq", adContent="qwqeqe!", adTimer=5).saveAdToJson()
