import os
import json
import time


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

    userName = input("Please Type Username of User of This Bot: ")
    botToken = input("Please Enter Bot Token: ")
    print("DISCLAIMER! MAKE SURE YOUR BOT HAS BEEN ADDED TO EVERY GROUP YOU WANT TO PUBLISH ADVERTISEMENTS (BEING ADMIN IS NOT REQUIRED)")
    try:
        createFolders(userName,botToken)
        time.sleep(5)
    except FileExistsError:
        print("User Already Saved")
        time.sleep(5)

