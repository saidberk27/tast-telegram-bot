import json
jsonFile = open("users/{}/userJson.json".format("whilefalse27"), "r")
jsonText = jsonFile.read()
jsonFile.close()
convertedDict = json.loads(jsonText)

channelNameDict = convertedDict['channel-names']  # Dict'ten channelnamesi al
channelNameDict.update({"{}".format("tost"): "False,{}".format("32")})

print(channelNameDict)