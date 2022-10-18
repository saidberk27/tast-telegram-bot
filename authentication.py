import json
class Auth:
    def __init__(self, username):
        self.username = username

    def initializeFirstManager(self):
        with open("managerlist.json", "r+") as managerfile:
            data = json.load(managerfile)
            data["manager_list"].append(self.username)
            convertedData = json.dumps(data)
            managerfile.seek(0)
            managerfile.write(convertedData)  # once yaziyoruz, cursor sona geliyor
            managerfile.truncate()

    def isManager(self):
        with open("managerlist.json", "r+") as jsonFile:
            data = json.load(jsonFile)
            return self.username in data["manager_list"]


    def addManager(self):
        with open("managerlist.json", "r+") as managerfile:
            data = json.load(managerfile)
            if(len(data["manager_list"]) > 3): #limit ekliyoruz
                return False
            else:
                data["manager_list"].append(self.username)
                convertedData = json.dumps(data)

                managerfile.seek(0)
                managerfile.write(convertedData)  # once yaziyoruz, cursor sona geliyor
                managerfile.truncate()  # sonra yazdigimiz veriden once ne varsa siliyoruz. OVERWRITE
                # https://stackoverflow.com/questions/2424000/read-and-overwrite-a-file-in-python
                return True

