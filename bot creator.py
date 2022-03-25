import os
import json
import time
import shutil

def arrangeManagers(userName):
    jsonFile = open("{}/userJson.json".format(userName), "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)
    managerList = convertedDict['managers']
    print("Managers of user = {}".format(managerList))
    selection = input("PLEASE TYPE \n 1 for REMOVE MANAGER \n 2 for ADD MANAGER")

    userFile = open("{}/userList.txt".format(userName), "r")
    userFileContent = userFile.readlines()
    userFile.close()

    if(selection == "1"):
        managerWillBeRemoved = input("Please Type the UserName of the Manager You Want to Remove")
        managerList.remove(managerWillBeRemoved)
        convertedDict['managers'] = managerList

        userJsonWrite = open("{}/userJson.json".format(userName), "w")
        userJsonWrite.write(json.dumps(convertedDict))
        userJsonWrite.close()

        try:
            userFileContent.remove(managerWillBeRemoved)
        except ValueError:
            userFileContent.remove(managerWillBeRemoved + "\n")

        userFileWrite = open("{}/userList.txt".format(userName), "w")
        for user in userFileContent:
            userFileWrite.write(user + "\n")

        print("Manager Succesfully Removed")


    if (selection == "2"):
        managerWillBeAdded = input("Please Type the UserName of the Manager You Want to Add")
        managerList.append(managerWillBeAdded)
        convertedDict['managers'] = managerList

        userJsonWrite = open("{}/userJson.json".format(userName), "w")
        userJsonWrite.write(json.dumps(convertedDict))
        userJsonWrite.close()

        userFileContent.append(managerWillBeAdded)

        userFileWrite = open("{}/userList.txt".format(userName), "a")
        for user in userFileContent:
            userFileWrite.write(user + "\n")
        userFileWrite.close()

        print("Manager Succesfully Added")


def createFolders(userName,botToken):
    mainFolder = "{}".format(userName)
    os.makedirs(mainFolder)

    jobsFolder = mainFolder + "/jobs"
    os.makedirs(jobsFolder)

    mediasFolder = mainFolder + "/medias"
    os.makedirs(mediasFolder)

    userJsonDict = {"channel-data": {}, "post-data": {}, "folder-data": {}, "language": "hw", "managers": []}
    emptyUserJson = open(mainFolder + "/userJson.json","w")
    emptyUserJson.write(json.dumps(userJsonDict))
    emptyUserJson.close()
    
    activeWorksJsonDict = {}
    emptyActiveWorksJson = open(mainFolder + "/active-works.json", "w")
    emptyActiveWorksJson.write(json.dumps(activeWorksJsonDict))
    emptyUserJson.close()

    os.system("copy main.py {}".format(mainFolder))
    os.system("copy STRINGS_EN.py {}".format(mainFolder))
    os.system("copy STRINGS_HW.py {}".format(mainFolder))

    userListPath = mainFolder + "/userList.txt"
    userList = open(userListPath,"w")
    userList.write(userName)
    userList.close()

    logsFilePath = mainFolder + "/logs.txt"
    logsList = open(logsFilePath, "w")
    logsList.write("BOT CREATED")
    logsList.close()

    startBatFile = mainFolder + "/start.bat"
    logsList = open(startBatFile, "w")
    logsList.write("python3 main.py")
    logsList.close()

    botTokenFile = mainFolder + "/botToken.txt"
    botTokenWrite = open(botTokenFile, "w")
    botTokenWrite.write(botToken)
    botTokenWrite.close()

if __name__ == '__main__':
    while True:
        selection = input("PLEASE TYPE \n 1 for CREATE BOT: \n 2 for DELETE BOT: \n 3 for ARRANGE MANAGERS: \n 4 for QUIT: \n")
        if(selection == "1"):
            userName = input("Please Type Username of User of This Bot: ")
            botToken = input("Please Enter Bot Token: ")
            print("DISCLAIMER! MAKE SURE YOUR BOT HAS BEEN ADDED TO EVERY GROUP YOU WANT TO PUBLISH ADVERTISEMENTS (BEING ADMIN IS NOT REQUIRED)")
            try:
                createFolders(userName,botToken)
                time.sleep(5)
            except FileExistsError:
                print("User Already Saved")
                time.sleep(5)

        if(selection == "2"):
            try:
                userName = input("Please Type Username of User You Want To Delete")
                shutil.rmtree(userName)
            except FileNotFoundError:
                print("User Not Exist")
                continue

        if(selection == "3"):
            try:
                userName = input("Please Type Username of User You Want Arrange Managers")
                arrangeManagers(userName)
            except FileNotFoundError:
                print("User Not Exist")
                continue

        if(selection == "4"):
            break
