def userCheck(userName):
    path = "users"
    userList = os.listdir(path=path)
    if userName in userList:
        pass
def userNameCheck(username):
    illegal_chars = ["<",">","/","*","?"," ","'",'"',":","|","\\"]
    letterUpdated = ""

    for letter in username:
        if letter in illegal_chars:
            print("Illegal Char Detected")
            letter = ""
        letterUpdated = letterUpdated + letter

    return letterUpdated

    print(letterUpdated)
def loginAndCreateFolder(userName = "whilefalse27"):
    import os
    try:
        path = "users/{}".format(userName)
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
    except OSError:
        checked = userNameCheck(userName)
        path = "users/{}".format(checked)
        if not isExist:
            os.makedirs(path)
import os

def readJson():
    import json
    jsonFile = open("users/whilefalse27/userJson.json","r")
    jsonText = jsonFile.read()
    parseJson = json.loads(jsonText)
    print(type(parseJson["channel-names"]))

readJson()