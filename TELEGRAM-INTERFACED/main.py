# -*- coding: utf-8 -*-
import time
from telegram import *
from telegram.ext import *
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
    global addMedia
    global selectedFile

    addMedia = False
    selectedFile = None
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
            InlineKeyboardButton(botTexts.string_posts, callback_data='posts'),
        ],
        [InlineKeyboardButton(botTexts.string_publishingAds, callback_data='publishingads')],
        [InlineKeyboardButton(botTexts.string_changeLanguage, callback_data='changelanguage')],
        [InlineKeyboardButton(botTexts.string_addManager, callback_data='add manager')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    if(mode == "updateData"):
        context.bot.send_message(chat_id=update.effective_chat.id, text=(botTexts.string_botUpdated), reply_markup=reply_markup)

    elif(mode == "backTap"):
        context.bot.send_message(chat_id=update.effective_chat.id, text=(botTexts.string_pleaseSelect),reply_markup=reply_markup)

def sendMistake(update: Updater,context: CallbackContext,message = "Something Went Wrong"):
    global currentUser
    global inputMode
    global selectedGroup
    global selectedPost
    global addButtonsList
    global buttonDatas
    global addMedia
    global selectedFile

    addMedia = False
    selectedFile = None
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
            InlineKeyboardButton(botTexts.string_posts, callback_data='posts'),
        ],
        [InlineKeyboardButton(botTexts.string_publishingAds, callback_data='publishingads')],
        [InlineKeyboardButton(botTexts.string_changeLanguage, callback_data='changelanguage')],
        [InlineKeyboardButton(botTexts.string_addManager, callback_data='add manager')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)

def startCommand(update: Update, context: CallbackContext) -> None:
    global currentUser
    global inputMode
    global selectedGroup
    global selectedPost
    global addButtonsList
    global buttonDatas

    print("BOT IS ACTIVE")

    languageLoader()

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
                InlineKeyboardButton(botTexts.string_channels, callback_data='channels'),
                InlineKeyboardButton(botTexts.string_posts , callback_data='posts'),
            ],
            [InlineKeyboardButton(botTexts.string_publishingAds, callback_data='publishingads')],
            [InlineKeyboardButton(botTexts.string_changeLanguage, callback_data='changelanguage')],
            [InlineKeyboardButton(botTexts.string_addManager, callback_data='add manager')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        context.bot.send_message(chat_id=update.effective_chat.id,text=botTexts.string_helloMessage.format(user['username']),reply_markup=reply_markup)

    else:
        keyboard = [[InlineKeyboardButton("Tap to Contact", url='https://t.me/BenjaminPost')],[InlineKeyboardButton("הקש כדי ליצור קשר", url='https://t.me/BenjaminPost')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id,text="❌ You Are Not Allowed to Use This Bot! Please Contact Admin",reply_markup = reply_markup)


def languageSelectionQueryListener(update: Update, context: CallbackContext):
    global botTexts
    query = update.callback_query
    query.answer()
    query.message.delete() # SINGLE-CALL YAPTIM ( TEK BALON CIKIYOR BUTONA BASINCA )
    if(query.data == "changelanguage"):
        languageOptions = [[InlineKeyboardButton("English 🇬🇧", callback_data="english")],[InlineKeyboardButton("Hebrew 🇮🇱", callback_data="hebrew")]]
        reply_markup = InlineKeyboardMarkup(languageOptions)
        context.bot.send_message(chat_id=update.effective_chat.id, text="PLease Select a Language",reply_markup=reply_markup)

    if (query.data == "english"):
        print("English Selected")
        botTexts = STRINGS_EN

        jsonFile = open("userJson.json", "r")
        jsonText = jsonFile.read()
        jsonFile.close()

        convertedDict = json.loads(jsonText)
        convertedDict.update({"language":"en"})

        userJsonWrite = open("userJson.json", "w")
        userJsonWrite.write(json.dumps(convertedDict))
        userJsonWrite.close()

        updateCommand(update, context)
    elif (query.data == "hebrew"):
        print("Hebrew Selected")
        botTexts = STRINGS_HW

        jsonFile = open("userJson.json", "r")
        jsonText = jsonFile.read()
        jsonFile.close()

        convertedDict = json.loads(jsonText)
        convertedDict.update({"language":"hw"})

        userJsonWrite = open("userJson.json", "w")
        userJsonWrite.write(json.dumps(convertedDict))
        userJsonWrite.close()

        updateCommand(update, context)

def mainQueryHandler(update: Update, context: CallbackContext) -> None:
    global inputMode
    global timer
    query = update.callback_query
    query.answer()

    print(query.data,inputMode)
    jsonFile = open("userJson.json", "r")
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

    if(query.data == "add manager"):
        addManager(update,context)

    if(query.data == "add_channel"):
        addChannel(update,context,showMessage=True)

    if(query.data == "add_post"):
        addPostShowButtons(update,context)
    if(query.data == "add post to folder"):
        listAllPosts(update,context)
    if(query.data == "remove post from folder"):
        removePostFromFolder(update,context)
    if(query.data == "publishingads"):
        inputMode = "jobEdit"
        publishingAds(update,context)

    if(query.data == "remove media"):
        global selectedFile
        os.remove("medias/{}".format(selectedFile))
        updateCommand(update,context)

    if(query.data == "add to post"):
        inputMode = "PostName"
        global botTexts
        context.bot.send_message(chat_id=update.effective_chat.id,text=botTexts.string_postName)

    if(query.data == "add button ok"):
        saveJob(update,context)
        inputMode = None

    if(query.data in channel_lists and inputMode == "channelEdit"):
        global selectedGroup
        selectedGroup = query.data
        editButton = [[InlineKeyboardButton(botTexts.string_removeChannel, callback_data="remove channel")],[InlineKeyboardButton(botTexts.string_back, callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(editButton)
        context.bot.send_message(chat_id=update.effective_chat.id, text=botTexts.string_editChannel, reply_markup=reply_markup)

    if(query.data == "remove channel"):
        removeSelectedChannel(update,context)

    if(query.data == "start publishing"):
        startPublishing(update,context)
        updateCommand(update,context)

    if(query.data == "remove job"):
        removeJob(update,context)

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
            inputMode = "addButtonText"
        except KeyError as ke:
            print("await for input",selectedPost)

    if(inputMode == "addButtonText"):
        addButtons(update,context,mod="first")

def editPosts(update: Update, context: CallbackContext):
    global inputMode
    query = update.callback_query
    query.answer()
    editButton = [[InlineKeyboardButton(botTexts.string_editPost,callback_data="edit post")],[InlineKeyboardButton(botTexts.string_addToFolder,callback_data="addtofolder")],[InlineKeyboardButton(botTexts.string_removePostFromFolder, callback_data='remove post from folder')],[InlineKeyboardButton(botTexts.string_back,callback_data='back')]]
    reply_markup_edit = InlineKeyboardMarkup(editButton)

    jsonFile = open("userJson.json", "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)
    adList = convertedDict["post-data"].keys()

    if(inputMode == "postEdit" and query.data in adList):
        global postWillBeEdited
        postWillBeEdited = query.data
        currentAdText = convertedDict["post-data"][postWillBeEdited]
        context.bot.send_message(chat_id=update.effective_chat.id, text=botTexts.string_currentAdText.format(currentAdText), reply_markup=reply_markup_edit)

    if(query.data == "edit post"):
        context.bot.send_message(chat_id=update.effective_chat.id, text=botTexts.string_pleaseTypeNewText)
        inputMode = "waitForNewAdText"

    if (query.data == "addtofolder"):
        inputMode = "addPostFolder"
        addPostFolder(update,context)

def editSelectedPost(update,context,newText):
    print(newText)
    jsonFile = open("userJson.json", "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)
    convertedDict["post-data"][postWillBeEdited] = newText

    userJsonWrite = open("userJson.json", "w")
    userJsonWrite.write(json.dumps(convertedDict))
    userJsonWrite.close()

    updateCommand(update,context)

def removeSelectedChannel(update,context):
    jsonFile = open("userJson.json", "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)
    willRemoveDict = convertedDict["channel-data"]
    willRemoveDict.pop(selectedGroup)
    convertedDict["channel-data"] = willRemoveDict

    jsonFileWrite = open("userJson.json", "w")
    jsonFileWrite.write(json.dumps(convertedDict))
    jsonFile.close()

    updateCommand(update,context)

def editSelectedPost(update,context,newText):
    print(newText)
    jsonFile = open("userJson.json", "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)
    convertedDict["post-data"][postWillBeEdited] = newText

    userJsonWrite = open("userJson.json", "w")
    userJsonWrite.write(json.dumps(convertedDict))
    userJsonWrite.close()

    updateCommand(update,context)

def editJobs(update: Update, context: CallbackContext):
    global inputMode
    global jobFile
    query = update.callback_query
    query.answer()

    editButton = [[InlineKeyboardButton(botTexts.string_addTimer, callback_data="add timer")],
                  [InlineKeyboardButton(botTexts.string_startPublishing, callback_data="start publishing")],
                  [InlineKeyboardButton(botTexts.string_removeJob, callback_data="remove job")],
                  [InlineKeyboardButton(botTexts.string_back, callback_data='back')]]
    reply_markup_edit = InlineKeyboardMarkup(editButton)

    jobs = os.listdir("jobs/") # returns list
    dotJsonAdded = query.data + ".json" #Job Name

    if(dotJsonAdded in jobs and inputMode == "jobEdit"):
        global selectedJob
        selectedJob = dotJsonAdded
        job_group = dotJsonAdded.split("-")[0]
        job_post = dotJsonAdded.split("-")[1]
        context.bot.send_message(chat_id=update.effective_chat.id, text=botTexts.string_GroupFormatPostFormat.format(job_group,job_post), reply_markup=reply_markup_edit)
        jobFile = "jobs/{}".format(dotJsonAdded)
    else:
        pass

    if(query.data == "add timer"):
        addTimer(update,context)

    if(query.data == "stop publishing"):
        jobFile = open("jobs/{}".format(selectedJob), "r")
        jobText = jobFile.read()
        jobFile.close()

        JobFileConvertedDict = json.loads(jobText)
        JobFileConvertedDict['isRun'] = 'False'
        jobFileWrite = open("jobs/{}".format(selectedJob), "w")
        jobFileWrite.write(json.dumps(JobFileConvertedDict))
        jobFileWrite.close()

        updateCommand(update,context)

    if (query.data == "1 Second"):
        with open(jobFile, "r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "1 Second"
        jobWrite = open(jobFile, "w")
        jobWrite.write(json.dumps(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if (query.data == "10 Seconds"):
        with open(jobFile, "r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "10 Seconds"
        jobWrite = open(jobFile, "w")
        jobWrite.write(json.dumps(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if (query.data == "30 Seconds"):
        with open(jobFile, "r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "30 Seconds"
        jobWrite = open(jobFile, "w")
        jobWrite.write(json.dumps(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if (query.data == "45 Seconds"):
        with open(jobFile, "r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "45 Seconds"
        jobWrite = open(jobFile, "w")
        jobWrite.write(json.dumps(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if(query.data == "1 Minute"):
        with open(jobFile,"r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "1 Minute"
        jobWrite = open(jobFile,"w")
        jobWrite.write(json.dumps(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if(query.data == "10 Minutes"):
        with open(jobFile,"r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "10 Minutes"
        jobWrite = open(jobFile,"w")
        jobWrite.write(json.dumps(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if(query.data == "30 Minutes"):
        with open(jobFile,"r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "30 Minutes"
        jobWrite = open(jobFile,"w")
        jobWrite.write(json.dumps(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if(query.data == "1 Hour"):
        with open(jobFile,"r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "1 Hour"
        jobWrite = open(jobFile,"w")
        jobWrite.write(json.dumps(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if(query.data == "3 Hours"):
        with open(jobFile,"r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "3 Hours"
        jobWrite = open(jobFile,"w")
        jobWrite.write(json.dumps(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if(query.data == "6 Hours"):
        with open(jobFile,"r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "6 Hours"
        jobWrite = open(jobFile,"w")
        jobWrite.write(json.dumps(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if(query.data == "12 Hours"):
        with open(jobFile,"r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "12 Hours"
        jobWrite = open(jobFile,"w")
        jobWrite.write(json.dumps(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if (query.data == "1 Day"):
        with open(jobFile, "r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "1 Day"
        jobWrite = open(jobFile, "w")
        jobWrite.write(json.dumps(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if (query.data == "3 Days"):
        with open(jobFile, "r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "3 Days"
        jobWrite = open(jobFile, "w")
        jobWrite.write(json.dumps(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update, context)

    if (query.data == "1 Week"):
        with open(jobFile, "r") as JobFile:
            JobFileConvertedDict = ast.literal_eval(JobFile.read())
            JobFileConvertedDict['Timer'] = "1 Week"
        jobWrite = open(jobFile, "w")
        jobWrite.write(json.dumps(JobFileConvertedDict))
        jobWrite.close()
        updateCommand(update,context)


def addTimer(update,context):
    timerButtons = [[InlineKeyboardButton(botTexts.string_1second, callback_data="1 Second"), InlineKeyboardButton(botTexts.string_10seconds, callback_data="10 Seconds"),InlineKeyboardButton(botTexts.string_30seconds, callback_data="30 Seconds"),InlineKeyboardButton(botTexts.string_45seconds, callback_data="45 Seconds")],[InlineKeyboardButton(botTexts.string_1minute, callback_data="1 Minute"), InlineKeyboardButton(botTexts.string_10minutes, callback_data="10 Minutes"),InlineKeyboardButton(botTexts.string_30minutes, callback_data="30 Minutes")], [InlineKeyboardButton(botTexts.string_1hour, callback_data="1 Hour"),InlineKeyboardButton(botTexts.string_3hours, callback_data="3 Hours"),InlineKeyboardButton(botTexts.string_6hours, callback_data="6 Hours")],[InlineKeyboardButton(botTexts.string_12hours, callback_data="12 Hours"),InlineKeyboardButton(botTexts.string_1day, callback_data="1 Day")],[InlineKeyboardButton(botTexts.string_3days, callback_data="3 Days"),InlineKeyboardButton(botTexts.string_1week, callback_data="1 Week")]]

    reply_markup = InlineKeyboardMarkup(timerButtons)
    context.bot.send_message(chat_id=update.effective_chat.id, text=botTexts.string_pleaseSelect,reply_markup=reply_markup)


def userCheck(username):
    usernameChecked = getCheckedUserName(username)
    with open("userList.txt","r") as userFile:
        userList = userFile.readlines()

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
    jsonFile = open("userJson.json", "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)

    channel_lists = convertedDict['channel-data'].keys()
    for channelNames in channel_lists:
        buttons.append([InlineKeyboardButton(channelNames,callback_data=channelNames)])


    staticsOfList = [InlineKeyboardButton(botTexts.string_addChannel, callback_data='add_channel')], [InlineKeyboardButton(botTexts.string_back, callback_data='back')]
    buttons = buttons + list(staticsOfList)
    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text=botTexts.string_list,reply_markup=reply_markup)

    global inputMode
    inputMode = "channelEdit"
def listFolderPosts(update, context, folder = None):
    buttons = []
    jsonFile = open("userJson.json", "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)

    folderData = convertedDict["folder-data"][folder]

    for adNames in folderData:
        buttons.append([InlineKeyboardButton(adNames,callback_data=adNames)])

    staticsOfList = [InlineKeyboardButton(botTexts.string_addPostToFolder, callback_data='add post to folder')], [InlineKeyboardButton(botTexts.string_back, callback_data='back')]
    buttons = buttons + list(staticsOfList)
    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text=botTexts.string_pleaseSelectPost, reply_markup=reply_markup)
    inputMode = "postEdit"
def listAllPosts(update,context):
    global currentUser

    buttons = []
    jsonFile = open("userJson.json", "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)

    adList = convertedDict["post-data"].keys()

    for adNames in adList:
        buttons.append([InlineKeyboardButton(adNames, callback_data=adNames)])

    staticsOfList = [[InlineKeyboardButton(botTexts.string_addPost, callback_data='add_post')], [InlineKeyboardButton(botTexts.string_back, callback_data='back')]]
    buttons = buttons + list(staticsOfList)
    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text=botTexts.string_allOfYourPosts, reply_markup=reply_markup)

def listFolders(update: Update, context: CallbackContext):
    jsonFile = open("userJson.json", "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)

    folderData = convertedDict["folder-data"]
    folderList = folderData.keys()

    buttons = []
    for folder in folderList:
        buttons.append([InlineKeyboardButton(folder,callback_data=folder)])
    staticsOfList = [InlineKeyboardButton(botTexts.string_addNewFolder, callback_data='add folder')],[InlineKeyboardButton(botTexts.string_back, callback_data='back')]
    buttons = buttons + list(staticsOfList)
    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text=botTexts.string_selectAFolder, reply_markup=reply_markup)

    global inputMode
    inputMode = "postEdit"

def folderSelection(update: Updater, context: CallbackContext):
    jsonFile = open("userJson.json", "r")
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
    global botTexts
    context.bot.send_message(chat_id=update.effective_chat.id, text=botTexts.string_pleaseTypeFolderName)


def awaitForInput(update: Updater, context: CallbackContext):
    global inputMode
    print("Trigerred",inputMode)


    if(inputMode == "GroupName"):
        try:
            global groupWillBeSaved
            groupWillBeSaved = update.message.text
            inputMode = "groupId"
            global botTexts
            context.bot.send_message(chat_id=update.effective_chat.id, text=botTexts.string_pleaseTypeGroupId)
        except IndexError: #ADD CHANNEL'I YAKALAYIP INDEXERROR VERMEMESI ICIN
            pass

    elif(inputMode == "groupId"):
        try:
            groupId = update.message.text
            channelInfo = groupWillBeSaved + "," + groupId
            addChannel(update, context, ekleme=True, groupInfo=channelInfo)
        except IndexError:  # ADD CHANNEL'I YAKALAYIP INDEXERROR VERMEMESI ICIN
            pass

    elif(inputMode == "folderName"):
        global folderName
        folderName = update.message.text

        jsonFile = open("userJson.json", "r")
        jsonText = jsonFile.read()
        jsonFile.close()
        convertedDict = json.loads(jsonText)

        folderData = convertedDict["folder-data"]
        folderData.update({folderName:[]})
        convertedDict["folder-data"] = folderData

        jsonFileWrite = open("userJson.json", "w")
        jsonFileWrite.write(json.dumps(convertedDict))
        jsonFile.close()
        updateCommand(update,context)

    if (inputMode == "image name"):
        os.rename("medias/nameless.jpg", "medias/{}.jpg".format(update.message.text))
        updateCommand(update, context)

    elif(inputMode == "PostName"):
        try:
            global postWillBeSaved
            postWillBeSaved = update.message.text
            inputMode = "PostContent"
            context.bot.send_message(chat_id=update.effective_chat.id, text=botTexts.string_postContent)
        except IndexError:  # ADD CHANNEL'I YAKALAYIP INDEXERROR VERMEMESI ICIN
            pass

    if(inputMode == "addManager"):
        addSelectedManager(update,context,userName = update.message.text)

    elif(inputMode == "PostContent"):
        global addMedia
        try:
            postContent = update.message.text
            postInfo = postWillBeSaved + "," + postContent
            addPost(update, context, groupInfo=postInfo, skip=addMedia)
        except IndexError:  # ADD CHANNEL'I YAKALAYIP INDEXERROR VERMEMESI ICIN
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

    elif(inputMode == "addButtonText"):
        global buttonText
        buttonText = update.message.text
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please Enter The URL That Button Will Redirect")
        inputMode = "addButtonURL"

    elif(inputMode == "addButtonURL"):
        global buttonURL
        buttonURL = update.message.text

        addButtons(update,context,buttonText,buttonURL,mod="inputici")

    else:
        print("not trigerred")

def addChannel(update, context, ekleme=False, groupInfo = None,showMessage=False):
    global inputMode
    inputMode = "GroupName"
    if(showMessage):
        global botTexts
        context.bot.send_message(chat_id=update.effective_chat.id, text=botTexts.string_pleaseEnterTheGroupName)
    print("ADD CHANNEL")
    if(ekleme):
        groupInfoList = groupInfo.split(",")

        channelNameInput = groupInfoList[0]
        channelIdInput = groupInfoList[1]

        global currentUser
        jsonFile = open("userJson.json", "r")
        jsonText = jsonFile.read()
        jsonFile.close()
        convertedDict = json.loads(jsonText)


        channelNameDict = convertedDict['channel-data'] #Dict'ten channelnamesi al
        channelNameDict.update({"{}".format(channelNameInput):"{}".format(channelIdInput)}) #NAME,SELECTION BOOL VE ID ATA selection=false cunku aktiflestirme olmayacak eklenir eklenmez.
        convertedDict['channel-data'] = channelNameDict #Guncelleyip geri ver

        print(type(convertedDict))

        userJsonWrite = open("userJson.json", "w")
        userJsonWrite.write(json.dumps(convertedDict))
        userJsonWrite.close()

        updateCommand(update,context)

    else:
        print("Await Input")

def addPostShowButtons(update,context):
    global inputMode
    inputMode = "PostName"
    buttons = [[InlineKeyboardButton(botTexts.string_addMedia,callback_data='add_media')],[InlineKeyboardButton(botTexts.string_skipMedia,callback_data='skip_media')],[InlineKeyboardButton(botTexts.string_back,callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text=botTexts.string_skipAddMedia, reply_markup=reply_markup)

def listMedias(update,context):
    buttons = []
    medias = os.listdir("medias/")  # returns list
    last_buttons = [[InlineKeyboardButton(botTexts.string_addNewMedia,callback_data="add new media")],[InlineKeyboardButton(botTexts.string_back,callback_data="back")]]

    for media in medias:
        buttons.append([InlineKeyboardButton(media, callback_data=media)])
    reply_markup = InlineKeyboardMarkup(buttons + last_buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text=botTexts.string_savedMediaFiles, reply_markup=reply_markup)

def addPost(update, context, groupInfo = None,skip=True):
    groupInfoList = groupInfo.split(",")

    postNameInput = groupInfoList[0]
    postIdInput = groupInfoList[1]

    jsonFile = open("userJson.json", "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)

    userJsonWrite = open("userJson.json", "w")
    if(skip):
        postData = convertedDict['post-data']  # Dict'ten post-data al
        postData.update({"{}".format(postNameInput): "{},{}".format(postIdInput,selectedFile)})  # NAME,SELECTION BOOL VE ID ATA
        convertedDict['post-data'] = postData  # Guncelleyip geri ver

    else:
        postData = convertedDict['post-data']  # Dict'ten post-data al
        postData.update({"{}".format(postNameInput): "{}".format(postIdInput)})  # NAME,SELECTION BOOL VE ID ATA
        convertedDict['post-data'] = postData  # Guncelleyip geri ver

    userJsonWrite.write(json.dumps(convertedDict))
    userJsonWrite.close()
    updateCommand(update, context)

def addManager(update,context):
    global inputMode
    inputMode = "addManager"
    context.bot.send_message(chat_id=update.effective_chat.id, text=botTexts.string_pleaseEnterManagerUserName)



def addSelectedManager(update,context, userName):
    jsonFile = open("userJson.json", "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)

    try:
        managerList = convertedDict['managers']
        if(len(managerList) >= 2):
            raise ValueError
        managerList.append(userName)
        convertedDict['managers'] = managerList

        userJsonWrite = open("userJson.json", "w")
        userJsonWrite.write(json.dumps(convertedDict))
        userJsonWrite.close()

        userListWrite = open("userList.txt","a")
        userListWrite.write("\n{}".format(userName))
        userListWrite.close()

        updateCommand(update,context)

    except ValueError:
        sendMistake(update,context,message="You Have Maximum Number Of Managers.Can't Be Added.")




def addOrSkipMedia(update: Update, context: CallbackContext):
    global addMedia
    global inputMode

    query = update.callback_query
    query.answer()
    if(query.data == "add_media"):
        addMedia = True
        listMedias(update, context)
    elif(query.data == "skip_media"):
        addMedia = False
        context.bot.send_message(chat_id=update.effective_chat.id, text=botTexts.string_postName)
        inputMode = "PostName"

    medias = os.listdir("medias/")  # returns list
    if(query.data in medias):
        global selectedFile
        selectedFile = query.data
        editMedia(update,context)

    if(query.data == "add new media"):
        inputMode = "save img"
        context.bot.send_message(chat_id=update.effective_chat.id, text=botTexts.string_dragImage)

def editMedia(update,context):
    global inputMode
    query = update.callback_query
    query.answer()
    editButton = [[InlineKeyboardButton(botTexts.string_addToPost, callback_data='add to post')],[InlineKeyboardButton(botTexts.string_removeMedia, callback_data='remove media')],
                  [InlineKeyboardButton(botTexts.string_back, callback_data='back')]]

    reply_markup = InlineKeyboardMarkup(editButton)
    context.bot.send_message(chat_id=update.effective_chat.id, text=botTexts.string_pleaseSelect,reply_markup=reply_markup)

def addPostFolder(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    print(query.data)
    if(inputMode == "addPostFolder" and query.data == "addtofolder"):
        jsonFile = open("userJson.json", "r")
        jsonText = jsonFile.read()
        jsonFile.close()

        convertedDict = json.loads(jsonText)
        folderData = convertedDict["folder-data"][selectedFolder]
        folderData.append(postWillBeEdited)
        convertedDict["folder-data"][selectedFolder] = folderData

        jsonFileWrite = open("userJson.json", "w")
        jsonFileWrite.write(json.dumps(convertedDict))
        jsonFileWrite.close()

        updateCommand(update,context)

def removePostFromFolder(update,context):
    jsonFile = open("userJson.json", "r")
    jsonText = jsonFile.read()
    jsonFile.close()

    convertedDict = json.loads(jsonText)
    folderData = convertedDict["folder-data"][selectedFolder]
    folderData.remove(postWillBeEdited)
    convertedDict["folder-data"][selectedFolder] = folderData

    jsonFileWrite = open("userJson.json", "w")
    jsonFileWrite.write(json.dumps(convertedDict))
    jsonFileWrite.close()

    updateCommand(update, context)

def publishingAds(update,context):
    global currentUser
    buttons = []
    last_buttons = [[InlineKeyboardButton(botTexts.string_addNewJob,callback_data="add new job")],[InlineKeyboardButton(botTexts.string_stopPublishing, callback_data="stop publishing")],[InlineKeyboardButton(botTexts.string_back,callback_data="back")]]
    jobs = os.listdir("jobs/") # returns list
    for job in jobs:
        buttons.append([InlineKeyboardButton(job[:-5],callback_data=job[:-5])])
    reply_markup = InlineKeyboardMarkup(buttons + last_buttons)
    context.bot.send_message(chat_id=update.effective_chat.id,text=botTexts.string_savedJobs,reply_markup=reply_markup)

def addNewJob(update,context):
     idList = []

     print("publishing")
     jsonFile = open("userJson.json", "r")

     jsonText = jsonFile.read()
     jsonFile.close()
     convertedDict = json.loads(jsonText)

     channelNames = list(convertedDict['channel-data'].keys())
     channelNamesStatus = convertedDict['channel-data'].values()

     channelNamesStr = str(channelNames)
     for channelStatus in channelNamesStatus:
         idList.append(channelStatus)

     context.bot.send_message(chat_id=update.effective_chat.id,
                              text=botTexts.string_yourActiveGroups.format(channelNamesStr[1:-1]))
     listChannels(update, context)
     global inputMode
     inputMode = "groupSelection"


def groupSelection(update,context,selectedGroup):
    activeWork = open("active-works.json","r")

    activeWorkText = activeWork.read()
    activeWork.close()

    convertedDict = json.loads(activeWorkText)

    convertedDict.update({selectedGroup:""})

    userJsonWrite = open("active-works.json", "w")
    userJsonWrite.write(json.dumps(convertedDict))
    userJsonWrite.close()

    context.bot.send_message(chat_id=update.effective_chat.id,text=botTexts.string_groupSelected)
    listAllPosts(update,context)


def postSelection(update,context,selectedPost):
    global currentUser

    activeWork = open("active-works.json", "r")
    postFile = open("userJson.json","r")

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
    userJsonWrite = open("active-works.json", "w")
    userJsonWrite.write(json.dumps(convertedDictActiveWorks))
    userJsonWrite.close()

    #context.bot.send_message(chat_id=update.effective_chat.id,text="{}".format(convertedDictActiveWorks))
    context.bot.send_message(chat_id=update.effective_chat.id,text=botTexts.string_postSelected)


def publishYesorNo(update,context):
    buttons = [[InlineKeyboardButton(botTexts.string_yes,callback_data='YES')],[InlineKeyboardButton(botTexts.string_no,callback_data='NO')]]
    context.bot.send_message(chat_id=update.effective_chat.id,text=botTexts.string_areYouSure, reply_markup=InlineKeyboardMarkup(buttons))


def publishPosts(update, context, jobData, timer):
    global currentUser
    print("Posts are being publishing.")
    jobGroupName = jobData['GroupName']
    jobPostName = jobData['PostName']
    jobButtons = jobData['Buttons']
    userFile = open("userJson.json", "r")

    userData = userFile.read()
    userFile.close()
    convertedDictUsers = json.loads(userData)

    channel_id = convertedDictUsers["channel-data"][jobGroupName]
    ad_data = convertedDictUsers["post-data"][jobPostName]
    ad_text = ad_data.split(",")[0]
    try:
        ad_media = ad_data.split(",")[1]
    except IndexError:
        ad_media = None

    if (timer == "1 Second"):
        def Interval():
            jobFile = open("jobs/{}".format(selectedJob), "r")
            jobText = jobFile.read()
            JobFileConvertedDict = json.loads(jobText)
            isRun = JobFileConvertedDict['isRun']

            if(isRun == "False"):
                print("pass")
                jobFile.close()

            elif(isRun == "True"):
                print(isRun)
                publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons, adFile=ad_media, isRun=isRun)
                if True:
                    Timer(1, Interval).start()
                jobFile.close()

        Interval()

    if (timer == "10 Seconds"):
        def Interval():
            jobFile = open("jobs/{}".format(selectedJob), "r")
            jobText = jobFile.read()
            JobFileConvertedDict = json.loads(jobText)
            isRun = JobFileConvertedDict['isRun']

            if (isRun == "False"):
                print("pass")
                jobFile.close()

            elif (isRun == "True"):
                publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons, adFile=ad_media,
                        isRun=isRun)
                if True:
                    Timer(10, Interval).start()

                jobFile.close()

        Interval()

    if (timer == "30 Seconds"):
        def Interval():
            jobFile = open("jobs/{}".format(selectedJob), "r")
            jobText = jobFile.read()
            JobFileConvertedDict = json.loads(jobText)
            isRun = JobFileConvertedDict['isRun']

            if (isRun == "False"):
                print("pass")
                jobFile.close()

            elif (isRun == "True"):
                publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons, adFile=ad_media,
                        isRun=isRun)
                if True:
                    Timer(30, Interval).start()

                jobFile.close()

        Interval()

    if (timer == "45 Seconds"):
        def Interval():
            jobFile = open("jobs/{}".format(selectedJob), "r")
            jobText = jobFile.read()
            JobFileConvertedDict = json.loads(jobText)
            isRun = JobFileConvertedDict['isRun']

            if (isRun == "False"):
                print("pass")
                jobFile.close()

            elif (isRun == "True"):
                publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons, adFile=ad_media,
                        isRun=isRun)
                if True:
                    Timer(45, Interval).start()

                jobFile.close()

        Interval()
    if(timer == "1 Minute"):
        def Interval():
            jobFile = open("jobs/{}".format(selectedJob), "r")
            jobText = jobFile.read()
            JobFileConvertedDict = json.loads(jobText)
            isRun = JobFileConvertedDict['isRun']

            if (isRun == "False"):
                print("pass")
                jobFile.close()

            elif (isRun == "True"):
                publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons, adFile=ad_media,
                        isRun=isRun)
                if True:
                    Timer(60, Interval).start()

                jobFile.close()

        Interval()
    if (timer == "10 Minutes"):
        def Interval():
            jobFile = open("jobs/{}".format(selectedJob), "r")
            jobText = jobFile.read()
            JobFileConvertedDict = json.loads(jobText)
            isRun = JobFileConvertedDict['isRun']

            if (isRun == "False"):
                print("pass")
                jobFile.close()

            elif (isRun == "True"):
                publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons, adFile=ad_media,
                        isRun=isRun)
                if True:
                    Timer(600, Interval).start()

                jobFile.close()

        Interval()

    if (timer == "30 Minutes"):
        def Interval():
            jobFile = open("jobs/{}".format(selectedJob), "r")
            jobText = jobFile.read()
            JobFileConvertedDict = json.loads(jobText)
            isRun = JobFileConvertedDict['isRun']

            if (isRun == "False"):
                print("pass")
                jobFile.close()

            elif (isRun == "True"):
                publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons, adFile=ad_media,
                        isRun=isRun)
                if True:
                    Timer(1800, Interval).start()

                jobFile.close()

        Interval()

    if (timer == "1 Hour"):
        def Interval():
            jobFile = open("jobs/{}".format(selectedJob), "r")
            jobText = jobFile.read()
            JobFileConvertedDict = json.loads(jobText)
            isRun = JobFileConvertedDict['isRun']

            if (isRun == "False"):
                print("pass")
                jobFile.close()

            elif (isRun == "True"):
                publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons, adFile=ad_media,
                        isRun=isRun)
                if True:
                    Timer(3600, Interval).start()

                jobFile.close()

        Interval()

    if (timer == "3 Hours"):
        def Interval():
            jobFile = open("jobs/{}".format(selectedJob), "r")
            jobText = jobFile.read()
            JobFileConvertedDict = json.loads(jobText)
            isRun = JobFileConvertedDict['isRun']

            if (isRun == "False"):
                print("pass")
                jobFile.close()

            elif (isRun == "True"):
                publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons, adFile=ad_media,
                        isRun=isRun)
                if True:
                    Timer(10800, Interval).start()

                jobFile.close()

        Interval()
    if (timer == "6 Hours"):
        def Interval():
            jobFile = open("jobs/{}".format(selectedJob), "r")
            jobText = jobFile.read()
            JobFileConvertedDict = json.loads(jobText)
            isRun = JobFileConvertedDict['isRun']

            if (isRun == "False"):
                print("pass")
                jobFile.close()

            elif (isRun == "True"):
                publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons, adFile=ad_media,
                        isRun=isRun)
                if True:
                    Timer(21.600, Interval).start()

                jobFile.close()

        Interval()

    if (timer == "12 Hours"):
        def Interval():
            jobFile = open("jobs/{}".format(selectedJob), "r")
            jobText = jobFile.read()
            JobFileConvertedDict = json.loads(jobText)
            isRun = JobFileConvertedDict['isRun']

            if (isRun == "False"):
                print("pass")
                jobFile.close()

            elif (isRun == "True"):
                publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons, adFile=ad_media,
                        isRun=isRun)
                if True:
                    Timer(43.200, Interval).start()

                jobFile.close()

        Interval()

    if (timer == "1 Day"):
        def Interval():
            jobFile = open("jobs/{}".format(selectedJob), "r")
            jobText = jobFile.read()
            JobFileConvertedDict = json.loads(jobText)
            isRun = JobFileConvertedDict['isRun']

            if (isRun == "False"):
                print("pass")
                jobFile.close()

            elif (isRun == "True"):
                publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons, adFile=ad_media,
                        isRun=isRun)
                if True:
                    Timer(86.400, Interval).start()

                jobFile.close()

        Interval()
    if (timer == "3 Days"):
        def Interval():
            jobFile = open("jobs/{}".format(selectedJob), "r")
            jobText = jobFile.read()
            JobFileConvertedDict = json.loads(jobText)
            isRun = JobFileConvertedDict['isRun']

            if (isRun == "False"):
                print("pass")
                jobFile.close()

            elif (isRun == "True"):
                publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons, adFile=ad_media,
                        isRun=isRun)
                if True:
                    Timer(259.200, Interval).start()

                jobFile.close()

        Interval()

    if (timer == "1 Week"):
        def Interval():
            jobFile = open("jobs/{}".format(selectedJob), "r")
            jobText = jobFile.read()
            JobFileConvertedDict = json.loads(jobText)
            isRun = JobFileConvertedDict['isRun']

            if (isRun == "False"):
                print("pass")
                jobFile.close()

            elif (isRun == "True"):
                publish(update, context, channelID=channel_id, adText=ad_text, buttons=jobButtons, adFile=ad_media,
                        isRun=isRun)
                if True:
                    Timer(604.800, Interval).start()

                jobFile.close()

        Interval()

def publish(update,context,channelID,adText,adFile,buttons,isRun = "False"):
    buttonsFinal = []
    if(isRun == "False"):
        print("don't run")
    else:
        print("Run")
        if(adFile == None):
            for button in buttons:
                buttonsFinal.append([InlineKeyboardButton("{}".format(button[0]), url="{}".format(button[1]))])

            context.bot.send_message(chat_id=channelID, text=adText ,reply_markup=InlineKeyboardMarkup(buttonsFinal))

        else:
            for button in buttons:
                buttonsFinal.append([InlineKeyboardButton("{}".format(button[0]), url="{}".format(button[1]))])

            path = "medias/{}".format(adFile)
            context.bot.send_photo(channelID, photo=open(path, 'rb'), caption=adText,reply_markup=InlineKeyboardMarkup(buttonsFinal))

def deactivateBot():
    print("Bot Is Deactivating")


def fileListener(update,context):
    global inputMode
    print("image handler")
    if(inputMode == "save img"):
        context.bot.get_file(update.message.document).download(custom_path="medias/nameless.jpg")
        context.bot.send_message(chat_id=update.effective_chat.id, text=botTexts.string_pleaseNameYourPhoto)
        inputMode = "image name"


def addButtons(update,context,buttonText = None,buttonURL = None,mod = None):
    global inputMode
    global buttonDatas
    global addButtonsList

    lastItem = [[InlineKeyboardButton(botTexts.string_addButton, callback_data="add button")], [InlineKeyboardButton("OK 👌", callback_data="add button ok")]]
    if(mod == "first"):
        context.bot.send_message(chat_id=update.effective_chat.id,text="Please Enter Your Button's Text", reply_markup=InlineKeyboardMarkup(lastItem))
    else:
        try:
            if(buttonText == None or buttonURL == None):
                raise ValueError
            addButtonsList.append([InlineKeyboardButton(buttonText,url=buttonURL)])
            buttonsFinal = addButtonsList + lastItem
            try:
                context.bot.send_message(chat_id=update.effective_chat.id,text=botTexts.string_buttonSuccesfullyAdded, reply_markup=InlineKeyboardMarkup(buttonsFinal))
            except:
                if(buttonURL[0] == "@"):
                    buttonURL = "https://t.me/{}".format(buttonURL)
                    context.bot.send_message(chat_id=update.effective_chat.id, text=botTexts.string_buttonSuccesfullyAdded,reply_markup=InlineKeyboardMarkup(buttonsFinal))
                else:
                    sendMistake(update,context, message = botTexts.string_urlIsInvalid)

            buttonDatasLocal = [buttonText, buttonURL]
            buttonDatas.append(buttonDatasLocal)

        except ValueError:
            context.bot.send_message(chat_id=update.effective_chat.id,text=botTexts.string_urlOrButtonUndefined)
            updateCommand(update,context,mode="backTap")
            inputMode = None


def saveJob(update,context):
    print("Save Job")
    global buttonDatas
    global timer
    jobData = {"GroupName":selectedGroup,"PostName":selectedPost,"Buttons":buttonDatas}
    jobFile = open("jobs/{}-job.json".format(selectedGroup + "-" + selectedPost),"w")
    jobFile.write(json.dumps(jobData))

    updateCommand(update,context)

def startPublishing(update,context):
    print("publishing is starting")
    fullFileName = "jobs/{}".format(selectedJob)
    with open(fullFileName) as jobFile:
        jobText = jobFile.read()
        JobFileConvertedDict = json.loads(jobText)

    try:
        timer = JobFileConvertedDict['Timer']
        JobFileConvertedDict['isRun'] = 'True'
        jobFileWrite = open("jobs/{}".format(selectedJob), "w")
        jobFileWrite.write(json.dumps(JobFileConvertedDict))
        jobFileWrite.close()

        publishPosts(update, context, JobFileConvertedDict, timer)
    except KeyError:
        sendMistake(update,context,message=botTexts.string_pleaseArrangeTimer)

def removeJob(update,context):
    os.remove("jobs/{}".format(selectedJob))
    updateCommand(update,context)
def languageLoader():
    jsonFile = open("userJson.json", "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)
    global botTexts
    try:
        if(convertedDict["language"] == "en"):
            botTexts = STRINGS_EN
        elif(convertedDict["language"] == "hw"):
            botTexts = STRINGS_HW
        else:
            botTexts = STRINGS_EN
    except KeyError:
        botTexts = STRINGS_EN

if __name__ == '__main__':
    from threading import Timer

    botTokenFile = open("botToken.txt","r")
    botToken = botTokenFile.read()
    botTokenFile.close()

    updater = Updater(token=botToken)
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
    updater.dispatcher.add_handler(CallbackQueryHandler(addOrSkipMedia), group=6)

    dispatcher.add_handler(MessageHandler(Filters.document,fileListener))

    runData = False
    currentUser = None
    inputMode = "None"
    selectedGroup = "None"
    selectedPost = "None"
    selectedFolder = "None"
    timer = "None"
    postWillBeEdited = "None"
    jobFile = "None"
    folderName = "None"
    groupWillBeSaved = "None"
    addMedia = False
    selectedJob = None
    buttonDatas = []
    addButtonsList = []
    selectedFile = None
    updater.start_polling()
    updater.idle()