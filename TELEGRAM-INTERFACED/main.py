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

def updateCommand(update: Updater,context: CallbackContext):
    buttons = [[KeyboardButton("🔥 CHANNELS")], [KeyboardButton("💥 POSTS")],[KeyboardButton("💬 PUBLISHING ADS")],[KeyboardButton("✅ BOT IS ACTIVE")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot Succesfully Updated!",reply_markup=ReplyKeyboardMarkup(buttons))

def startCommand(update: Updater,context: CallbackContext):
    user = update.message.from_user
    username = user['username']

    if(userCheck(username)):
        buttons = [[KeyboardButton("🔥 CHANNELS")], [KeyboardButton("💥 POSTS")], [KeyboardButton("💬 PUBLISHING ADS")],[KeyboardButton("✅ BOT IS ACTIVE")]]
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hello {} Welcome to bot!".format(user['username']), reply_markup=ReplyKeyboardMarkup(buttons))
    else: context.bot.send_message(chat_id=update.effective_chat.id, text="❌ You Are Not Allowed to Use This Bot! Please Contact Admın")

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

def mainMenu(update,context):
    buttons = [[KeyboardButton("🔥 CHANNELS")], [KeyboardButton("💥 POSTS")], [KeyboardButton("💬 PUBLISHING ADS")],[KeyboardButton("✅ BOT IS ACTIVE")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please Select",reply_markup=ReplyKeyboardMarkup(buttons))

def logTut(update):
    try:
        logFile = open("logs.txt", "a")
        logFile.write(update.message.text + "\n")
        logFile.close()
    except UnicodeEncodeError:
        logFile.write(update.message.text[2:] + "\n")
        logFile.close()

def generalMessageHandler(update: Updater, context: CallbackContext):
    logTut(update)

#------------------------------GENERAL----------------------------#
    if("🔥 CHANNELS" in update.message.text):
        #fileListener(update,context)
        listChannels(update,context)
    if("💥 POSTS" in update.message.text):
        listPosts(update,context)

    if ("✅ BOT IS ACTIVE" in update.message.text):
        deactivateBot()

    if ("⬅️ BACK" in update.message.text):
        mainMenu(update,context)

    if("💬 PUBLISHING ADS" in update.message.text):
        publishingAds(update,context)
#------------------------------GENERAL----------------------------#
    if("➕ ADD CHANNEL" in update.message.text):
        addChannel(update,context,showMessage=True,ekleme=False) #BUTONA ILK BASIS ICIN GEREKLI BIR CAGIRMA,INPUT BEKLEMEZ

    if ("➕ ADD POST" in update.message.text):
        addPost(update, context, showMessage=True,ekleme=False)  # BUTONA ILK BASIS ICIN GEREKLI BIR CAGIRMA,INPUT BEKLEMEZ
#------------------------------LIST CHANNELS----------------------------#
    #if ("🔆 CHANNEL 1" in update.message.text):
    #    print("Channel One")
    #    userJson = open("users.txt","r")
    #    userJsonList = userJson.readlines()
    #   userData = userJsonList[0]
    #   convertedDict = ast.literal_eval(userData)
    #   print(convertedDict["username"],convertedDict["channels"][0],convertedDict["adText"])
    #   send_message.sendText(adText=convertedDict["adText"])



def listChannels(update,context):
    buttons = []

    user = update.message.from_user
    currentUser = user['username']
    jsonFile = open("users/{}/userJson.json".format(currentUser), "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)

    channel_lists = convertedDict['channel-data'].keys()
    for channelNames in channel_lists:
        buttons.append([KeyboardButton(channelNames)])

    staticsOfList = [KeyboardButton("➕ ADD CHANNEL")], [KeyboardButton("⛔ REMOVE CHANNEL")], [KeyboardButton("⬅️ BACK")]
    buttons = buttons + list(staticsOfList)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please Select the Group", reply_markup=ReplyKeyboardMarkup(buttons))


def listPosts(update,context):
    buttons = []

    user = update.message.from_user
    currentUser = user['username']
    jsonFile = open("users/{}/userJson.json".format(currentUser), "r")
    jsonText = jsonFile.read()
    jsonFile.close()
    convertedDict = json.loads(jsonText)

    adList = convertedDict["post-data"].keys()

    staticsOfList = [KeyboardButton("➕ ADD POST")], [KeyboardButton("⛔ REMOVE POST")], [KeyboardButton("⬅️ BACK")]

    for adNames in adList:
        buttons.append([KeyboardButton(adNames)])

    buttons = buttons + list(staticsOfList)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please Select the Ad",reply_markup=ReplyKeyboardMarkup(buttons))

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
        if(update.message.text != "💬 PUBLISHING ADS"):
            global selectedGroup
            selectedGroup = update.message.text
            groupSelection(update,context,selectedGroup)
            inputMode = "postSelection"

    elif(inputMode == "postSelection"):
        postSelection(update,context,selectedPost=update.message.text)

    elif(inputMode == "publishAreYouSure"):
        publishIfSure(update,context,message=update.message.text)

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
    buttons = [[KeyboardButton("Add Media")],[KeyboardButton("Skip Media")],[KeyboardButton("⬅️ BACK")]]

    if(showMessage):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please Enter the (Ad Name,Ad Text)",reply_markup=ReplyKeyboardMarkup(buttons))
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
    user = update.message.from_user
    currentUser = user['username']
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
    activeWork = open("active-works.json","r")

    activeWorkText = activeWork.read()
    activeWork.close()

    convertedDict = json.loads(activeWorkText)

    convertedDict.update({selectedGroup:""})

    userJsonWrite = open("active-works.json", "w")
    userJsonWrite.write(json.dumps(convertedDict))
    userJsonWrite.close()

    context.bot.send_message(chat_id=update.effective_chat.id,text="Group Succesfully Selected and Saved! Now Please Pick Post For Your Group:")
    listPosts(update,context)


def postSelection(update,context,selectedPost):
    user = update.message.from_user
    currentUser = user['username']

    activeWork = open("active-works.json", "r")
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
    userJsonWrite = open("active-works.json", "w")
    userJsonWrite.write(json.dumps(convertedDictActiveWorks))
    userJsonWrite.close()

    context.bot.send_message(chat_id=update.effective_chat.id,text="{}".format(convertedDictActiveWorks))

    buttons = [[KeyboardButton("YES")],[KeyboardButton("NO")]]
    context.bot.send_message(chat_id=update.effective_chat.id,text="ARE YOU SURE?".format(convertedDictActiveWorks),reply_markup=ReplyKeyboardMarkup(buttons))
    global inputMode
    inputMode = "publishAreYouSure"

def publishIfSure(update,context,message):
    if(message == "YES"):
        user = update.message.from_user
        currentUser = user['username']

        activeWork = open("active-works.json", "r")
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
            publish(channelID=channel_id,adText=post_data)


    elif(message == "NO"):
        mainMenu(update,context)


def publish(update,context,channelID,adText):
    print("publish")
    baseUrl = "https://api.telegram.org/bot5149901305:AAFBvwD3N1UCCkBDmNlRE9nH5YMa6fFAYtM/sendMessage?chat_id={}&text={}".format(channelID, adText)
    requests.get(baseUrl)
    updateCommand(update,context)

def deactivateBot():
    print("Bot Is Deactivating")


def fileListener(update,context):
    print("image handler")
    context.bot.get_file(update.message.document).download()


if __name__ == '__main__':

    updater = Updater(token="5149901305:AAFBvwD3N1UCCkBDmNlRE9nH5YMa6fFAYtM")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start",startCommand))
    dispatcher.add_handler(CommandHandler("update",updateCommand))
    dispatcher.add_handler(MessageHandler(Filters.text, generalMessageHandler))
    dispatcher.add_handler(MessageHandler(Filters.text, awaitForInput), group=1)#GROUP=1 DIYEREK DAHA FAZLA HANDLER KYOABILIYORUZ, https://github.com/python-telegram-bot/python-telegram-bot/issues/1133

    dispatcher.add_handler(MessageHandler(Filters.document,fileListener))

    inputMode = "None"
    selectedGroup = "None"
    updater.start_polling()
    updater.idle()

    #ADD GRUPTA 2 HANDLER KULLANDIM, BIRISI GENERAL HANDLER ILK BASISI ALGILAMAK ICIN (OZEL HANDLER ADD GRUP MESAJINA TEPKI VERMIYOR) DIGERI DE ADD GRUP MESAJINDAN SONRAKI INPUTU YAKALAMASI ICIN