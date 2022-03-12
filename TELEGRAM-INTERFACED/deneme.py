import json

activeWork = open("active-works.json", "r")

activeWorkText = activeWork.read()
activeWork.close()

convertedDict = json.loads(activeWorkText)
print(convertedDict)
postSaveLocation = convertedDict["testchannel"]  # selectedGroup Global Var
postSaveLocation = "ASDF"
convertedDict["testchannel"] = postSaveLocation
print(convertedDict)