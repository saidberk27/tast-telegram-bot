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

def updateCommand(update: Updater,context: CallbackContext,mode = "updateData"):
    global inputMode
    inputMode = None
    keyboard = [
        [
            InlineKeyboardButton("🔥 CHANNELS", callback_data='channels'),
            InlineKeyboardButton("💥 POSTS", callback_data='posts'),
        ],
        [InlineKeyboardButton("💬 PUBLISHING ADS", callback_data='publishingads')],
        [InlineKeyboardButton("✅ BOT IS ACTIVE", callback_data='botisactive')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    if(mode == "updateData"):
        context.bot.send_message(chat_id=update.effective_chat.id, text=("Bot Succesfully Updated! 🔥🔥🔥"),reply_markup=reply_markup)

    elif(mode == "backTap"):
        context.bot.send_message(chat_id=update.effective_chat.id, text=("Please Select"),reply_markup=reply_markup)

def startCommand(update: Update, context: CallbackContext) -> None:
    global currentUser

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
            [InlineKeyboardButton("✅ BOT IS ACTIVE", callback_data='botisactive')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id,text="Hello {} Welcome to bot!".format(user['username']),reply_markup=reply_markup)

    else:
        keyboard = [[InlineKeyboardButton("Tap to Contact", url='https://t.me/BenjaminPost')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id,text="❌ You Are Not Allowed to Use This Bot! Please Contact Admin",reply_markup = reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    global inputMode

    query = update.callback_query
    query.answer()

    if(query.data == "channels"):
        listChannels(update,context)

    if(query.data == "posts"):
        listPosts(update,context)

    if(query.data == "back"):
        updateCommand(update,context,mode="backTap")
        
    if(query.data == "add_channel"):
        addChannel(update,context,showMessage=True)

    if(query.data == "add_post"):
        addPost(update,context,showMessage=True)

    if(query.data == "publishingads"):
        publishingAds(update,context)

    if(query.data == "add button ok"):
        publishYesorNo(update,context)
    if(query.data == "YES"):
        publishPosts(update, context)
    if(query.data == "NO"):
        updateCommand(update,context,mode="backTap")
    if(inputMode == "groupSelection"):
        if(query.data != "publishingads"):
            inputMode = "postSelection"
            global selectedGroup
            selectedGroup = query.data
            print(selectedGroup)
            groupSelection(update, context, selectedGroup)
        else:
            print("await for input")

    if(inputMode == "postSelection"):
        try:
            postSelection(update, context, selectedPost=query.data)
            inputMode = "addButton"
        except KeyError:
            print("await for input")

    if(inputMode == "addButton"):
        addButtons(update,context,mod="first")
        inputMode = None
    if(inputMode == "publishAreYouSure"):
        if(query.data == "YES" or query.data == "NO"):
            publishPosts(update, context, message=query.data)
            inputMode = None


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


    staticsOfList = [InlineKeyboardButton("➕ ADD CHANNEL",callback_data='add_channel')], [InlineKeyboardButton("⛔ REMOVE CHANNEL",callback_data='remove_channel')], [InlineKeyboardButton("⬅️ BACK",callback_data='back')]
    buttons = buttons + list(staticsOfList)
    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text="List:",reply_markup=reply_markup)

def listPosts(update,context):
    global currentUser

    buttons = []
    jsonFile = open("users/{}/userJson.json".format(currentUser), "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)

    adList = convertedDict["post-data"].keys()

    for adNames in adList:
        buttons.append([InlineKeyboardButton(adNames,callback_data=adNames)])

    staticsOfList = [InlineKeyboardButton("➕ ADD POST", callback_data='add_post')], [InlineKeyboardButton("⛔ REMOVE POST", callback_data='remove_post')], [InlineKeyboardButton("⬅️ BACK", callback_data='back')]
    buttons = buttons + list(staticsOfList)
    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello", reply_markup=reply_markup)

def awaitForInput(update: Updater, context: CallbackContext):
    global inputMode
    print("Tetiklendi",inputMode)
    if(inputMode == "group"):
        try:
            addChannel(update, context, ekleme=True, groupInfo=update.message.text)
            inputMode = "None"
        except IndexError: #ADD CHANNEL'I YAKALAYIP INDEXERROR VERMEMESI ICIN
            pass

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

    elif(inputMode == "publishAreYouSure"):
        publishPosts(update, context, message=update.message.text)
        inputMode = None

    elif(inputMode == "addButton"):
        userInput = update.message.text
        buttonText = userInput.split(",")[0]
        buttonURL = userInput.split(",")[1]

        addButtons(update,context,buttonText,buttonURL,mod="addButtonInputIcı")
        inputMode = None
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

        user = update.message.from_user
        currentUser = user['username']
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

        user = update.message.from_user
        currentUser = user['username']
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

def publishingAds(update,context):
    global currentUser
    idList = []

    print("publishing")
    jsonFile = open("users/{}/userJson.json".format(currentUser), "r")

    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)

    channelNames = list(convertedDict['channel-data'].keys())
    channelNamesStatus=convertedDict['channel-data'].values()

    channelNamesStr = str(channelNames)
    for channelStatus in channelNamesStatus:
        idList.append(channelStatus)


    context.bot.send_message(chat_id=update.effective_chat.id,text="Your Active Groups: {}".format(channelNamesStr[1:-1]))
    listChannels(update,context)
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
    listPosts(update,context)


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


def publishPosts(update, context):

    global currentUser

    activeWork = open("users/{}/active-works.json".format(currentUser), "r")
    userFile = open("users/{}/userJson.json".format(currentUser), "r")

    userData = userFile.read()
    activeWorkText = activeWork.read()
    activeWork.close()
    userFile.close()

    convertedDictActiveWorks = json.loads(activeWorkText)
    convertedDictUsers = json.loads(userData)

    activeGroupsNames = list(convertedDictActiveWorks.keys())

    for groupName in activeGroupsNames:
        channel_id = convertedDictUsers["channel-data"][groupName]
        post_data = convertedDictActiveWorks[groupName]
        publish(update,context,channelID=channel_id,adText=post_data)



def publish(update,context,channelID,adText):
    print("publish")
    baseUrl = "https://api.telegram.org/bot5149901305:AAFBvwD3N1UCCkBDmNlRE9nH5YMa6fFAYtM/sendMessage?chat_id={}&text={}".format(channelID, adText)
    requests.get(baseUrl)
    updateCommand(update,context)
    global inputMode
    inputMode = None

def deactivateBot():
    print("Bot Is Deactivating")


def fileListener(update,context):
    print("image handler")
    context.bot.get_file(update.message.document).download()

def addButtons(update,context,buttonText = None,buttonURL = None,mod = None):
    global inputMode
    buttons = []
    lastItem = [[InlineKeyboardButton("➕ TAP TO ADD BUTTON",callback_data="add button")],[InlineKeyboardButton("OK 👌",callback_data="add button ok")]]
    if(mod == "first"):
        context.bot.send_message(chat_id=update.effective_chat.id,text="Add Buttons",reply_markup=InlineKeyboardMarkup(lastItem))
    else:
        try:
            if(buttonText == None or buttonURL == None):
                raise ValueError
            buttons.append([InlineKeyboardButton(buttonText,url=buttonURL)])
            buttonsOK = buttons + lastItem
            context.bot.send_message(chat_id=update.effective_chat.id,text="Button Succesfully Added!",reply_markup=InlineKeyboardMarkup(button))

        except ValueError:
            context.bot.send_message(chat_id=update.effective_chat.id,text="URL OR BUTTON TEXT IS UNDEFINED")
            updateCommand(update,context,mode="backTap")
            inputMode = None



if __name__ == '__main__':

    updater = Updater(token="5149901305:AAFBvwD3N1UCCkBDmNlRE9nH5YMa6fFAYtM")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start",startCommand))
    dispatcher.add_handler(CommandHandler("update",updateCommand))
    dispatcher.add_handler(MessageHandler(Filters.text, awaitForInput), group=1)#GROUP=1 DIYEREK DAHA FAZLA HANDLER KYOABILIYORUZ, https://github.com/python-telegram-bot/python-telegram-bot/issues/1133

    updater.dispatcher.add_handler(CallbackQueryHandler(button))


    dispatcher.add_handler(MessageHandler(Filters.document,fileListener))

    currentUser = None

    inputMode = "None"
    selectedGroup = "None"
    updater.start_polling()
    updater.idle()

    #ADD GRUPTA 2 HANDLER KULLANDIM, BIRISI GENERAL HANDLER ILK BASISI ALGILAMAK ICIN (OZEL HANDLER ADD GRUP MESAJINA TEPKI VERMIYOR) DIGERI DE ADD GRUP MESAJINDAN SONRAKI INPUTU YAKALAMASI ICIN