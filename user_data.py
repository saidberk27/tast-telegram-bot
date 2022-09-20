import json

class UserData:
    _jsonFile = open("userData.json", "r")
    _jsonText = _jsonFile.read()
    _jsonFile.close()
    _convertedDict = json.loads(_jsonText)

    def getChannelNames(self):
        return list(self._convertedDict['channels'].keys())

    def getChannelIds(self):
        return list(self._convertedDict['channels'].values())

    def getChannelIdFromChannelName(self, channelName):
        try:
            return self._convertedDict['channels'][channelName]
        except KeyError:
            return "Invalid Channel"

    def getPostTitles(self):
        return list(self._convertedDict['posts'].keys())

    def getPostContents(self):
        return list(self._convertedDict['channels'].values())

    def getPostContentFromPostTitle(self, postName):
        try:
            return self._convertedDict['posts'][postName]
        except KeyError:
            return "Invalid Post"

    def isActive(self):
        return self._convertedDict['isActive'] == "true" #is string equals to true then bool also equals to true too.

    def addNewChannel(self, channelName, channelID):
        pass
        #POSTS