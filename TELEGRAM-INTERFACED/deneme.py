import json
jsonFile = open("users/{}/userJson.json".format("whilefalse27"), "r")
jsonText = jsonFile.read()
print(jsonText)
jsonFile.close()
convertedDict = json.loads(jsonText)

folderData = convertedDict["folder-data"]["folder1"]
print(folderData)
