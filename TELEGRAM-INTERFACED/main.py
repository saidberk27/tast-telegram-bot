# -*- coding: utf-8 -*-
import time

from threading import Timer
import requests
from telegram import *
from telegram.ext import *
from requests import *
import send_message
import os
import ast
import json
import STRINGS_EN
import STRINGS_HW

def updateCommand(update: Updater,context: CallbackContext,mode = "updateData"):
    global currentUser
    global inputMode
    global selectedGroup
    global selectedPost
    global addButtonsList
    global buttonDatas

    inputMode = "None"
    selectedGroup = "None"
    selectedPost = "None"
    addButtonsList = []
    buttonDatas = []
    selectedFolder = "None"
    # SIFIRLAMALAR-------------
    keyboard = [
        [
            InlineKeyboardButton(botTexts.string_channels, callback_data='channels'),
            InlineKeyboardButton("💥 POSTS", callback_data='posts'),
        ],
        [InlineKeyboardButton("💬 PUBLISHING ADS", callback_data='publishingads')],
        [InlineKeyboardButton("CHANGE LANGUAGE 🇮🇱/🇬🇧", callback_data='changelanguage')],
        [InlineKeyboardButton("✅ BOT IS ACTIVE", callback_data='botisactive')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    if(mode == "updateData"):
        context.bot.send_message(chat_id=update.effective_chat.id, text=(botTexts.string_botUpdated), reply_markup=reply_markup)

    elif(mode == "backTap"):
        context.bot.send_message(chat_id=update.effective_chat.id, text=("Please Select"),reply_markup=reply_markup)

def startCommand(update: Update, context: CallbackContext) -> None:
    global currentUser
    global inputMode
    global selectedGroup
    global selectedPost
    global addButtonsList
    global buttonDatas


    inputMode = "None"
    selectedGroup = "None"
    selectedPost = "None"
    addButtonsList = []
    buttonDatas = []

    #SIFIRLAMALAR-------------
    user = update.message.from_user
    username = user['username']

    currentUser = username

    if (userCheck(username)):
        keyboard = [
            [
                InlineKeyboardButton("🔥 CHANNELS", callback_data='channels'),
                InlineKeyboardButton("💥 POSTS", callback_data='posts'),
            ],
            [InlineKeyboardButton("💬 PUBLISHING ADS", callback_data='publishingads')],
            [InlineKeyboardButton("CHANGE LANGUAGE 🇮🇱/🇬🇧", callback_data='changelanguage')],
            [InlineKeyboardButton("✅ BOT IS ACTIVE", callback_data='botisactive')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id,text="Hello {} Welcome to bot!".format(user['username']),reply_markup=reply_markup)

    else:
        keyboard = [[InlineKeyboardButton("Tap to Contact", url='https://t.me/BenjaminPost')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id,text="❌ You Are Not Allowed to Use This Bot! Please Contact Admin",reply_markup = reply_markup)


def languageSelectionQueryListener(update: Update, context: CallbackContext):
    global botTexts
    query = update.callback_query
    query.answer()

    if(query.data == "changelanguage"):
        languageOptions = [[InlineKeyboardButton("English 🇬🇧", callback_data="english")],[InlineKeyboardButton("Hebrew 🇮🇱", callback_data="hebrew")]]
        reply_markup = InlineKeyboardMarkup(languageOptions)
        context.bot.send_message(chat_id=update.effective_chat.id, text="PLease Select a Language",reply_markup=reply_markup)

    if (query.data == "english"):
        print("English Selected")
        botTexts = STRINGS_EN
        updateCommand(update, context)

    elif (query.data == "hebrew"):
        print("Hebrew Selected")
        botTexts = STRINGS_HW
        updateCommand(update, context)

def mainQueryHandler(update: Update, context: CallbackContext) -> None:
    global inputMode
    global timer
    query = update.callback_query
    query.answer()

    print(query.data,inputMode)
    jsonFile = open("users/{}/userJson.json".format(currentUser), "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)

    channel_lists = convertedDict['channel-data'].keys()

    if(query.data == "channels"):
        listChannels(update,context)

    if(query.data == "posts"):
        listFolders(update, context)
        inputMode = "postEdit"


    if(query.data == "back"):
        updateCommand(update,context,mode="backTap")

    if(query.data == "add_channel"):
        addChannel(update,context,showMessage=True)

    if(query.data == "add_post"):
        addPost(update,context,showMessage=True)
    if(query.data == "add post to folder"):
        listAllPosts(update,context)
    if(query.data == "remove post from folder"):
        removePostFromFolder(update,context)
    if(query.data == "publishingads"):
        inputMode = "jobEdit"
        publishingAds(update,context)

    if(query.data == "add button ok"):
        saveJob(update,context)
        inputMode = None

    if(query.data in channel_lists and inputMode == "channelEdit"):
        global selectedGroup
        selectedGroup = query.data
        editButton = [[InlineKeyboardButton("⛔ REMOVE CHANNEL", callback_data="remove channel")],[InlineKeyboardButton("⬅️ BACK", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(editButton)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Edit Channel", reply_markup=reply_markup)

    if(query.data == "remove channel"):
        removeSelectedChannel(update,context)

    if(query.data == "start publishing"):
        global runData
        runData = True
        startPublishing(update,context)


    if(query.data == "NO"):
        updateCommand(update,context,mode="backTap")

    if(query.data == "add new job"):
        addNewJob(update,context)

    if(inputMode == "groupSelection"):
        if(query.data != "add new job"):
            selectedGroup = query.data
            groupSelection(update, context, selectedGroup)
            inputMode = "postSelection"
        else:
            print("await for input")

    if(inputMode == "postSelection"):
        try:
            global selectedPost
            selectedPost = query.data
            postSelection(update, context, selectedPost)
            inputMode = "addButton"
        except KeyError as ke:
            print("await for input",selectedPost)

    if(inputMode == "addButton"):
        addButtons(update,context,mod="first")

def editPosts(update: Update, context: CallbackContext):
    global inputMode
    query = update.callback_query
    query.answer()
    editButton = [[InlineKeyboardButton("✏️ EDIT POST",callback_data="edit post")],[InlineKeyboardButton("➕ ADD TO FOLDER",callback_data="addtofolder")],[InlineKeyboardButton("⛔ REMOVE POST FROM FOLDER", callback_data='remove post from folder')],[InlineKeyboardButton("⬅️ BACK",callback_data='back')]]
    reply_markup_edit = InlineKeyboardMarkup(editButton)

    jsonFile = open("users/{}/userJson.json".format(currentUser), "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)
    adList = convertedDict["post-data"].keys()

    if(inputMode == "postEdit" and query.data in adList):
        global postWillBeEdited
        postWillBeEdited = query.data
        currentAdText = convertedDict["post-data"][postWillBeEdited]
        context.bot.send_message(chat_id=update.effective_chat.id, text="Current Ad Text = {}".format(currentAdText), reply_markup=reply_markup_edit)

    if(query.data == "edit post"):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please Type New Text")
        inputMode = "waitForNewAdText"

    if (query.data == "addtofolder"):
        inputMode = "addPostFolder"
        addPostFolder(update,context)

def editSelectedPost(update,context,newText):
    print(newText)
    jsonFile = open("users/{}/userJson.json".format(currentUser), "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)
    convertedDict["post-data"][postWillBeEdited] = newText

    userJsonWrite = open("users/{}/userJson.json".format(currentUser), "w")
    userJsonWrite.write(json.dumps(convertedDict))
    userJsonWrite.close()

    updateCommand(update,context)

def removeSelectedChannel(update,context):
    jsonFile = open("users/{}/userJson.json".format(currentUser), "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)
    willRemoveDict = convertedDict["channel-data"]
    willRemoveDict.pop(selectedGroup)
    convertedDict["channel-data"] = willRemoveDict

    jsonFileWrite = open("users/{}/userJson.json".format(currentUser), "w")
    jsonFileWrite.write(json.dumps(convertedDict))
    jsonFile.close()

    updateCommand(update,context)

def editSelectedPost(update,context,newText):
    print(newText)
    jsonFile = open("users/{}/userJson.json".format(currentUser), "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)
    convertedDict["post-data"][postWillBeEdited] = newText

    userJsonWrite = open("users/{}/userJson.json".format(currentUser), "w")
    userJsonWrite.write(json.dumps(convertedDict))
    userJsonWrite.close()

    updateCommand(update,context)

def editJobs(update: Update, context: CallbackContext):
    global inputMode
    global jobFile
    query = update.callback_query
    query.answer()

    editButton = [[InlineKeyboardButton("⏲️ ADD TIMER", callback_data="add timer")],
                  [InlineKeyboardButton("🛑 STOP PUBLISHING AND REMOVE ❌", callback_data="stop publishing and remove")],
                  [InlineKeyboardButton("⬅️ BACK", callback_data='back')]]
    reply_markup_edit = InlineKeyboardMarkup(editButton)


    jobs = os.listdir("users/{}/jobs/".format(currentUser)) # returns list
    dotJsonAdded = query.data + ".json" #Job Name



    if(dotJsonAdded in jobs and inputMode == "jobEdit"):

        job_group = dotJsonAdded.split("-")[0]
        job_post = dotJsonAdded.split("-")[1]
        context.bot.send_message(chat_id=update.effective_chat.id, text="Group: {} Post: {}".format(job_group,job_post), reply_markup=reply_markup_edit)
        jobFile = "users/{}/jobs/{}".format(currentUser, dotJsonAdded)
    else:
        pass

    if(query.data == "add timer"):
        addTimer(update,context)

    if(query.data == "stop publishing and remove"):
        global runData
        os.remove(jobFile)
        runData = False
        time.sleep(3)
        runData = True
        startPublishing(update,context) # Bastan Baslat
        updateCommand(update,context)

    if(query.data == "1 Minute"):
        with open(jobFile,"r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "1 Minute"
        jobWrite = open(jobFile,"w")
        jobWrite.write(str(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if(query.data == "10 Minutes"):
        with open(jobFile,"r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "10 Minutes"
        jobWrite = open(jobFile,"w")
        jobWrite.write(str(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if(query.data == "30 Minutes"):
        with open(jobFile,"r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "30 Minutes"
        jobWrite = open(jobFile,"w")
        jobWrite.write(str(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if(query.data == "1 Hour"):
        with open(jobFile,"r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "1 Hour"
        jobWrite = open(jobFile,"w")
        jobWrite.write(str(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if(query.data == "3 Hours"):
        with open(jobFile,"r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "3 Hours"
        jobWrite = open(jobFile,"w")
        jobWrite.write(str(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if(query.data == "6 Hours"):
        with open(jobFile,"r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "6 Hours"
        jobWrite = open(jobFile,"w")
        jobWrite.write(str(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if(query.data == "12 Hours"):
        with open(jobFile,"r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "12 Hours"
        jobWrite = open(jobFile,"w")
        jobWrite.write(str(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if (query.data == "1 Day"):
        with open(jobFile, "r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "1 Day"
        jobWrite = open(jobFile, "w")
        jobWrite.write(str(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if (query.data == "3 Days"):
        with open(jobFile, "r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "3 Days"
        jobWrite = open(jobFile, "w")
        jobWrite.write(str(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if (query.data == "1 Week"):
        with open(jobFile, "r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "1 Week"
        jobWrite = open(jobFile, "w")
        jobWrite.write(str(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update,context)


def addTimer(update,context):
    timerButtons = [[InlineKeyboardButton("1 Minute", callback_data="1 Minute"), InlineKeyboardButton("10 Minutes", callback_data="10 Minutes"),InlineKeyboardButton("30 Minutes", callback_data="30 Minutes")], [InlineKeyboardButton("1 Hour", callback_data="1 Hour"),InlineKeyboardButton("3 Hours", callback_data="3 Hours"),InlineKeyboardButton("6 Hours", callback_data="6 Hours")],[InlineKeyboardButton("12 Hours", callback_data="12 Hours"),InlineKeyboardButton("1 Day", callback_data="1 Day")],[InlineKeyboardButton("3 Days", callback_data="3 Days"),InlineKeyboardButton("1 Week", callback_data="1 Week")]]

    reply_markup = InlineKeyboardMarkup(timerButtons)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please Select",reply_markup=reply_markup)


def userCheck(username):
    print(type(username))
    path = "users"
    usernameChecked = getCheckedUserName(username)
    userList = os.listdir(path=path)

    return usernameChecked in userList

def getCheckedUserName(username):
    illegal_chars = ["<",">","/","*","?"," ","'",'"',":","|","\\"]
    letterUpdated = ""

    for letter in username:
        if letter in illegal_chars:
            print("Illegal Char Detected")
            letter = ""
        letterUpdated = letterUpdated + letter

    return letterUpdated


def logTut(update):
    try:
        logFile = open("logs.txt", "a")
        logFile.write(update.message.text + "\n")
        logFile.close()
    except UnicodeEncodeError:
        logFile.write(update.message.text[2:] + "\n")
        logFile.close()



def listChannels(update,context):
    global currentUser
    buttons = []
    jsonFile = open("users/{}/userJson.json".format(currentUser), "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)

    channel_lists = convertedDict['channel-data'].keys()
    for channelNames in channel_lists:
        buttons.append([InlineKeyboardButton(channelNames,callback_data=channelNames)])


    staticsOfList = [InlineKeyboardButton(botTexts.string_addChannel, callback_data='add_channel')], [InlineKeyboardButton("⬅️ BACK", callback_data='back')]
    buttons = buttons + list(staticsOfList)
    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text="List:",reply_markup=reply_markup)

    global inputMode
    inputMode = "channelEdit"
def listFolderPosts(update, context, folder = None):
    buttons = []
    jsonFile = open("users/{}/userJson.json".format(currentUser), "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)

    folderData = convertedDict["folder-data"][folder]

    for adNames in folderData:
        buttons.append([InlineKeyboardButton(adNames,callback_data=adNames)])

    staticsOfList = [InlineKeyboardButton("➕ ADD POST TO FOLDER", callback_data='add post to folder')], [InlineKeyboardButton("⬅️ BACK", callback_data='back')]
    buttons = buttons + list(staticsOfList)
    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please Select a Post", reply_markup=reply_markup)
    inputMode = "postEdit"
def listAllPosts(update,context):
    global currentUser

    buttons = []
    jsonFile = open("users/{}/userJson.json".format(currentUser), "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)

    adList = convertedDict["post-data"].keys()

    for adNames in adList:
        buttons.append([InlineKeyboardButton(adNames, callback_data=adNames)])

    staticsOfList = [[InlineKeyboardButton(botTexts.string_addPost, callback_data='add_post')], [InlineKeyboardButton("⬅️ BACK", callback_data='back')]]
    buttons = buttons + list(staticsOfList)
    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text="All of Your Posts:", reply_markup=reply_markup)

def listFolders(update: Update, context: CallbackContext):
    jsonFile = open("users/{}/userJson.json".format(currentUser), "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)

    folderData = convertedDict["folder-data"]
    folderList = folderData.keys()

    buttons = []
    for folder in folderList:
        buttons.append([InlineKeyboardButton(folder,callback_data=folder)])
    staticsOfList = [InlineKeyboardButton("➕ ADD NEW FOLDER", callback_data='add folder')], [InlineKeyboardButton("⛔ REMOVE POST", callback_data='remove_post')], [InlineKeyboardButton("⬅️ BACK", callback_data='back')]
    buttons = buttons + list(staticsOfList)
    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Select a Folder", reply_markup=reply_markup)

    global inputMode
    inputMode = "postEdit"

def folderSelection(update: Updater, context: CallbackContext):
    jsonFile = open("users/{}/userJson.json".format(currentUser), "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)

    folderData = convertedDict["folder-data"]
    folderList = folderData.keys()

    query = update.callback_query
    query.answer()
    global selectedFolder

    if (query.data in folderList):
        global inputMode
        inputMode = "postEdit"
        selectedFolder = query.data
        listFolderPosts(update, context, query.data)

    if(query.data == "add folder"):
        addNewFolder(update,context)

def addNewFolder(update,context):
    global inputMode
    inputMode = "folderName"
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please Type Folder Name")


def awaitForInput(update: Updater, context: CallbackContext):
    global inputMode
    print("Tetiklendi",inputMode)
    if(inputMode == "group"):
        try:
            addChannel(update, context, ekleme=True, groupInfo=update.message.text)
            inputMode = "None"
        except IndexError: #ADD CHANNEL'I YAKALAYIP INDEXERROR VERMEMESI ICIN
            pass

    elif(inputMode == "folderName"):
        global folderName
        folderName = update.message.text

        jsonFile = open("users/{}/userJson.json".format(currentUser), "r")
        jsonText = jsonFile.read()
        jsonFile.close()
        convertedDict = json.loads(jsonText)

        folderData = convertedDict["folder-data"]
        folderData.update({folderName:[]})
        convertedDict["folder-data"] = folderData

        jsonFileWrite = open("users/{}/userJson.json".format(currentUser), "w")
        jsonFileWrite.write(json.dumps(convertedDict))
        jsonFile.close()
        updateCommand(update,context)

    elif(inputMode == "post"):
        try:
            addPost(update,context,ekleme=True,groupInfo=update.message.text)
            inputMode = None
        except IndexError: #ADD CHANNEL'I YAKALAYIP INDEXERROR VERMEMESI ICIN
            pass

    elif(inputMode == "groupSelection"):
        global selectedGroup

        selectedGroup = getCurrentQuery(update,context)
        groupSelection(update,context,selectedGroup)
        inputMode = "postSelection"

    elif(inputMode == "postSelection"):
        postSelection(update,context,selectedPost=update.message.text)
        inputMode = "publishAreYouSure"

    elif(inputMode == "waitForNewAdText"):
        newContent = update.message.text
        editSelectedPost(update,context,newContent)
    elif(inputMode == "addButton"):
        userInput = update.message.text
        buttonText = userInput.split(",")[0]
        buttonURL = userInput.split(",")[1]

        addButtons(update,context,buttonText,buttonURL,mod="inputici")

    else:
        print("yazmam")

def addChannel(update, context, ekleme=False, groupInfo = None,showMessage=False):
    global inputMode
    inputMode = "group"
    if(showMessage):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please Enter the (Group Name,Group ID)")
    print("ADD CHANNEL")
    if(ekleme):
        groupInfoList = groupInfo.split(",")

        channelNameInput = groupInfoList[0]
        channelIdInput = groupInfoList[1]

        global currentUser
        jsonFile = open("users/{}/userJson.json".format(currentUser), "r")
        jsonText = jsonFile.read()
        jsonFile.close()
        convertedDict = json.loads(jsonText)


        channelNameDict = convertedDict['channel-data'] #Dict'ten channelnamesi al
        channelNameDict.update({"{}".format(channelNameInput):"{}".format(channelIdInput)}) #NAME,SELECTION BOOL VE ID ATA selection=false cunku aktiflestirme olmayacak eklenir eklenmez.
        convertedDict['channel-data'] = channelNameDict #Guncelleyip geri ver

        print(type(convertedDict))

        userJsonWrite = open("users/{}/userJson.json".format(currentUser), "w")
        userJsonWrite.write(json.dumps(convertedDict))
        userJsonWrite.close()

        updateCommand(update,context)

    else:
        print("Input Bekle")

def addPost(update, context, ekleme=False, groupInfo = None,showMessage=False):
    global inputMode
    inputMode = "post"
    buttons = [[InlineKeyboardButton("Add Media",callback_data='add_media')],[InlineKeyboardButton("Skip Media",callback_data='skip_media')],[InlineKeyboardButton("⬅️ BACK",callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(buttons)

    if(showMessage):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please Enter the (Ad Name,Ad Text)",reply_markup=reply_markup)
    if(ekleme):
        groupInfoList = groupInfo.split(",")

        postNameInput = groupInfoList[0]
        postIdInput = groupInfoList[1]

        global currentUser
        jsonFile = open("users/{}/userJson.json".format(currentUser), "r")
        jsonText = jsonFile.read()
        jsonFile.close()
        convertedDict = json.loads(jsonText)

        postData = convertedDict['post-data']  # Dict'ten post-data al
        postData.update({"{}".format(postNameInput): "{}".format(postIdInput)})  # NAME,SELECTION BOOL VE ID ATA
        convertedDict['post-data'] = postData  # Guncelleyip geri ver

        userJsonWrite = open("users/{}/userJson.json".format(currentUser), "w")
        userJsonWrite.write(json.dumps(convertedDict))
        userJsonWrite.close()

        updateCommand(update,context)

    else:
        print("Input Bekle")

def addPostFolder(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    print(query.data)
    if(inputMode == "addPostFolder" and query.data == "addtofolder"):
        jsonFile = open("users/{}/userJson.json".format(currentUser), "r")
        jsonText = jsonFile.read()
        jsonFile.close()

        convertedDict = json.loads(jsonText)
        folderData = convertedDict["folder-data"][selectedFolder]
        folderData.append(postWillBeEdited)
        convertedDict["folder-data"][selectedFolder] = folderData

        jsonFileWrite = open("users/{}/userJson.json".format(currentUser), "w")
        jsonFileWrite.write(json.dumps(convertedDict))
        jsonFileWrite.close()

        updateCommand(update,context)

def removePostFromFolder(update,context):
    jsonFile = open("users/{}/userJson.json".format(currentUser), "r")
    jsonText = jsonFile.read()
    jsonFile.close()

    convertedDict = json.loads(jsonText)
    folderData = convertedDict["folder-data"][selectedFolder]
    folderData.remove(postWillBeEdited)
    convertedDict["folder-data"][selectedFolder] = folderData

    jsonFileWrite = open("users/{}/userJson.json".format(currentUser), "w")
    jsonFileWrite.write(json.dumps(convertedDict))
    jsonFileWrite.close()

    updateCommand(update, context)

def publishingAds(update,context):
    global currentUser
    buttons = []
    last_buttons = [[InlineKeyboardButton("ADD NEW JOB ➕",callback_data="add new job")],[InlineKeyboardButton("REMOVE JOB ⛔",callback_data="remove job")],[InlineKeyboardButton("START PUBLISHING👍",callback_data="start publishing")],[InlineKeyboardButton("⬅️ BACK",callback_data="back")]]
    jobs = os.listdir("users/{}/jobs/".format(currentUser)) # returns list
    for job in jobs:
        buttons.append([InlineKeyboardButton(job[:-5],callback_data=job[:-5])])
    reply_markup = InlineKeyboardMarkup(buttons + last_buttons)
    context.bot.send_message(chat_id=update.effective_chat.id,text="Your Saved Jobs:",reply_markup=reply_markup)

def addNewJob(update,context):
     idList = []

     print("publishing")
     jsonFile = open("users/{}/userJson.json".format(currentUser), "r")

     jsonText = jsonFile.read()
     jsonFile.close()
     convertedDict = json.loads(jsonText)

     channelNames = list(convertedDict['channel-data'].keys())
     channelNamesStatus = convertedDict['channel-data'].values()

     channelNamesStr = str(channelNames)
     for channelStatus in channelNamesStatus:
         idList.append(channelStatus)

     context.bot.send_message(chat_id=update.effective_chat.id,
                              text="Your Active Groups: {}".format(channelNamesStr[1:-1]))
     listChannels(update, context)
     global inputMode
     inputMode = "groupSelection"


def groupSelection(update,context,selectedGroup):
    activeWork = open("users/{}/active-works.json".format(currentUser),"r")

    activeWorkText = activeWork.read()
    activeWork.close()

    convertedDict = json.loads(activeWorkText)

    convertedDict.update({selectedGroup:""})

    userJsonWrite = open("users/{}/active-works.json".format(currentUser), "w")
    userJsonWrite.write(json.dumps(convertedDict))
    userJsonWrite.close()

    context.bot.send_message(chat_id=update.effective_chat.id,text="Group Succesfully Selected and Saved! Now Please Pick Post For Your Group:")
    listAllPosts(update,context)


def postSelection(update,context,selectedPost):
    global currentUser

    activeWork = open("users/{}/active-works.json".format(currentUser), "r")
    postFile = open("users/{}/userJson.json".format(currentUser),"r")

    postText = postFile.read()
    activeWorkText = activeWork.read()
    activeWork.close()
    postFile.close()

    convertedDictActiveWorks = json.loads(activeWorkText)
    convertedDictPosts = json.loads(postText)

    postData = convertedDictPosts['post-data']
    adText = postData["{}".format(selectedPost)]

    convertedDictActiveWorks[selectedGroup] = adText #selectedGroup Global Var
    print(convertedDictActiveWorks)
    userJsonWrite = open("users/{}/active-works.json".format(currentUser), "w")
    userJsonWrite.write(json.dumps(convertedDictActiveWorks))
    userJsonWrite.close()

    #context.bot.send_message(chat_id=update.effective_chat.id,text="{}".format(convertedDictActiveWorks))
    context.bot.send_message(chat_id=update.effective_chat.id,text="Post Selected.")


def publishYesorNo(update,context):
    buttons = [[InlineKeyboardButton("YES",callback_data='YES')],[InlineKeyboardButton("NO",callback_data='NO')]]
    context.bot.send_message(chat_id=update.effective_chat.id,text="ARE YOU SURE?",reply_markup=InlineKeyboardMarkup(buttons))


def publishPosts(update, context, jobData, timer):
    global currentUser

    jobGroupName = jobData['GroupName']
    jobPostName = jobData['PostName']
    jobButtons = jobData['Buttons']
    userFile = open("users/{}/userJson.json".format(currentUser), "r")

    userData = userFile.read()
    userFile.close()
    convertedDictUsers = json.loads(userData)

    channel_id = convertedDictUsers["channel-data"][jobGroupName]
    ad_text = convertedDictUsers["post-data"][jobPostName]
    if(timer == "1 Minute"):
        def Interval():
            run = runData
            publish(update,context,channelID=channel_id, adText=ad_text,buttons = jobButtons)
            if run:
                Timer(60, Interval).start()
        Interval()

    if (timer == "10 Minutes"):
        def Interval():
            run = runData
            publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons)
            if run:
                Timer(600, Interval).start()

        Interval()

    if (timer == "30 Minutes"):
        def Interval():
            run = runData
            publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons)
            if run:
                Timer(1800, Interval).start()

        Interval()

    if (timer == "1 Hour"):
        def Interval():
            run = runData
            publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons)
            if run:
                Timer(3600, Interval).start()

        Interval()

    if (timer == "3 Hours"):
        def Interval():
            run = runData
            publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons)
            if run:
                Timer(10.800, Interval).start()

        Interval()

    if (timer == "6 Hours"):
        def Interval():
            run = runData
            publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons)
            if run:
                Timer(21.600, Interval).start()

        Interval()

    if (timer == "12 Hours"):
        def Interval():
            run = runData
            publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons)
            if run:
                Timer(43.200, Interval).start()

        Interval()

    if (timer == "1 Day"):
        def Interval():
            run = runData
            publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons)
            if run:
                Timer(86.400, Interval).start()

        Interval()

    if (timer == "3 Days"):
        def Interval():
            run = runData
            publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons)
            if run:
                Timer(259.200, Interval).start()

        Interval()

    if (timer == "1 Week"):
        def Interval():
            run = runData
            publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons)
            if run:
                Timer(259.200, Interval).start()

        Interval()


def publish(update,context,channelID,adText,buttons):
    buttonsFinal = []

    for button in buttons:
        buttonsFinal.append([InlineKeyboardButton("{}".format(button[0]), url="{}".format(button[1]))])

    context.bot.send_message(chat_id=channelID, text=adText ,reply_markup=InlineKeyboardMarkup(buttonsFinal))

    global inputMode


def deactivateBot():
    print("Bot Is Deactivating")


def fileListener(update,context):
    print("image handler")
    context.bot.get_file(update.message.document).download()

def addButtons(update,context,buttonText = None,buttonURL = None,mod = None):
    global inputMode
    global buttonDatas
    global addButtonsList

    lastItem = [[InlineKeyboardButton(botTexts.string_addButton, callback_data="add button")], [InlineKeyboardButton("OK 👌", callback_data="add button ok")]]
    if(mod == "first"):
        context.bot.send_message(chat_id=update.effective_chat.id,text="Add Buttons",reply_markup=InlineKeyboardMarkup(lastItem))
    else:
        try:
            if(buttonText == None or buttonURL == None):
                raise ValueError
            addButtonsList.append([InlineKeyboardButton(buttonText,url=buttonURL)])
            buttonsFinal = addButtonsList + lastItem
            context.bot.send_message(chat_id=update.effective_chat.id,text="Button Succesfully Added!",reply_markup=InlineKeyboardMarkup(buttonsFinal))

            buttonDatasLocal = [buttonText, buttonURL]
            buttonDatas.append(buttonDatasLocal)

        except ValueError:
            context.bot.send_message(chat_id=update.effective_chat.id,text="URL OR BUTTON TEXT IS UNDEFINED")
            updateCommand(update,context,mode="backTap")
            inputMode = None


def saveJob(update,context):
    global buttonDatas
    global timer
    jobData = {"GroupName":selectedGroup,"PostName":selectedPost,"Buttons":buttonDatas}
    jobFile = open("users/{}/jobs/{}-job.json".format(currentUser,selectedGroup + "-" + selectedPost),"w")
    jobFile.write(str(jobData))

    updateCommand(update,context)

def startPublishing(update,context):
    jobsList = os.listdir("users/{}/jobs/".format(currentUser))

    for job in jobsList:
        fullFileName = "users/{}/jobs/{}".format(currentUser,job)
        with open(fullFileName) as jobFile:
            jobText = jobFile.read()
            jobTextDict = ast.literal_eval(jobText)
            try:
                timer = jobTextDict['Timer']
                publishPosts(update, context, jobTextDict, timer)
            except KeyError:
                context.bot.send_message(chat_id=update.effective_chat.id, text=("Please Arrange Timer!"))
                updateCommand(update,context,mode="backTap")



if __name__ == '__main__':
    from threading import Timer

    updater = Updater(token="5149901305:AAFBvwD3N1UCCkBDmNlRE9nH5YMa6fFAYtM")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", startCommand))
    dispatcher.add_handler(CommandHandler("update",updateCommand))
    dispatcher.add_handler(MessageHandler(Filters.text, awaitForInput), group=1)#GROUP=1 DIYEREK DAHA FAZLA HANDLER KYOABILIYORUZ, https://github.com/python-telegram-bot/python-telegram-bot/issues/1133

    updater.dispatcher.add_handler(CallbackQueryHandler(mainQueryHandler))

    updater.dispatcher.add_handler(CallbackQueryHandler(editPosts),group=1)
    updater.dispatcher.add_handler(CallbackQueryHandler(editJobs),group=2)
    updater.dispatcher.add_handler(CallbackQueryHandler(folderSelection), group=3)
    updater.dispatcher.add_handler(CallbackQueryHandler(addPostFolder), group=4)
    updater.dispatcher.add_handler(CallbackQueryHandler(languageSelectionQueryListener), group=5)

    dispatcher.add_handler(MessageHandler(Filters.document,fileListener))

    botTexts = STRINGS_EN
    runData = True
    currentUser = None
    inputMode = "None"
    selectedGroup = "None"
    selectedPost = "None"
    selectedFolder = "None"
    timer = "None"
    postWillBeEdited = "None"
    jobFile = "None"
    folderName = "None"
    buttonDatas = []
    addButtonsList = []
    updater.start_polling()
    updater.idle()