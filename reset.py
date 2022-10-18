import json

def resetManagerList():
    with open("managerlist.json", "r+") as managerfile:
        data = json.load(managerfile)
        data["manager_list"] = []
        convertedData = json.dumps(data)
        managerfile.seek(0)
        managerfile.write(convertedData)  # once yaziyoruz, cursor sona geliyor
        managerfile.truncate()

def resetUserData():
    with open("userData.json", "r+") as jsonFile:
        defaultJson = {"channels": {}, "isActive": "true", "Ads": []}
        convertedData = json.dumps(defaultJson)

        jsonFile.seek(0)
        jsonFile.write(convertedData)
        jsonFile.truncate()

if __name__ == "__main__":
    print("Datas are resetting...")
    resetManagerList()
    resetUserData()