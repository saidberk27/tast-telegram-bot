import json

class UserData:
    _jsonFile = open("userData.json", "r")
    _jsonText = _jsonFile.read()
    _jsonFile.close()
    _convertedDict = json.loads(_jsonText)
    _adList = _convertedDict["Ads"]
    def getChannelNames(self):
        return list(self._convertedDict['channels'].keys())

    def getChannelIds(self):
        return list(self._convertedDict['channels'].values())

    def getChannelIdFromChannelName(self, channelName):
        try:
            return self._convertedDict['channels'][channelName]
        except KeyError:
            return "Invalid Channel"

    def getAdTitles(self):
        _jsonFile = open("userData.json", "r")
        _jsonText = _jsonFile.read()
        _jsonFile.close()
        _convertedDict = json.loads(_jsonText)
        _adList = _convertedDict["Ads"]

        _adTitles = []
        for ad in self._adList:
            _adTitles.append(ad["Ad Title"])
        return _adTitles

    def getAdContents(self):
        _adContents = []
        for ad in self._adList:
            _adContents.append(ad["Ad Content"])
        return _adContents

    def isActive(self):
        return self._convertedDict['isActive'] == "true" #is string equals to true then bool also equals to true too.

    def addNewChannel(self, channelName, channelID):
        pass

