# -*- coding: utf-8 -*-
import time

from threading import Timer


from telegram import *
from telegram.ext import *
from requests import *
import send_message
import ast

def updateCommand(update: Updater,context: CallbackContext):
    buttons = [[KeyboardButton("🔥 CHANNELS")], [KeyboardButton("💥 POSTS")], [KeyboardButton("✅ BOT IS ACTIVE")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot Succesfully Updated!",reply_markup=ReplyKeyboardMarkup(buttons))

def startCommand(update: Updater,context: CallbackContext):
    user = update.message.from_user
    buttons = [[KeyboardButton("🔥 CHANNELS")],[KeyboardButton("💥 POSTS")],[KeyboardButton("✅ BOT IS ACTIVE")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello {} Welcome to bot!".format(user['username']), reply_markup=ReplyKeyboardMarkup(buttons))

def mainMenu(update,context):
    buttons = [[KeyboardButton("🔥 CHANNELS")],[KeyboardButton("💥 POSTS")],[KeyboardButton("✅ BOT IS ACTIVE")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please Select the Group",reply_markup=ReplyKeyboardMarkup(buttons))

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
#------------------------------GENERAL----------------------------#
    if("➕ ADD CHANNEL" in update.message.text):
        addChannel(update,context,showMessage=True) #BUTONA ILK BASIS ICIN GEREKLI BIR CAGIRMA,INPUT BEKLEMEZ
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
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please Select the Group", reply_markup=ReplyKeyboardMarkup(buttons))

    userJson = open("users.txt", "r")
    userJsonList = userJson.readlines()
    userJson.close()
    user = update.message.from_user
    currentUser = user['username']

    for users in userJsonList:
        convertedDict = ast.literal_eval(users)
        if (convertedDict['username'] == currentUser):
            channel_lists = convertedDict['channel-names']
            for channelNames in channel_lists:
                buttons.append([KeyboardButton(channelNames)])
            staticsOfList = [KeyboardButton("➕ ADD CHANNEL")], [KeyboardButton("⛔ REMOVE CHANNEL")], [KeyboardButton("⬅️ BACK")]
            buttons = buttons + list(staticsOfList)
            context.bot.send_message(chat_id=update.effective_chat.id, text=channelNames,reply_markup=ReplyKeyboardMarkup(buttons))

def listPosts(update,context):
    buttons = []
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please Select the Ad", reply_markup=ReplyKeyboardMarkup(buttons))

    userJson = open("users.txt", "r")
    userJsonList = userJson.readlines()
    userJson.close()
    user = update.message.from_user
    currentUser = user['username']

    for users in userJsonList:
        convertedDict = ast.literal_eval(users)
        staticsOfList = [KeyboardButton("➕ ADD CHANNEL")], [KeyboardButton("⛔ REMOVE CHANNEL")], [KeyboardButton("⬅️ BACK")]
        if (convertedDict['username'] == currentUser):
            ad_lists = convertedDict['ad-names']
            for adNames in ad_lists:
                buttons.append([KeyboardButton(adNames)])

            buttons = buttons + list(staticsOfList)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Please Select the Ad",reply_markup=ReplyKeyboardMarkup(buttons))

def awaitForGroupNameInput(update: Updater, context: CallbackContext):
    print("Tetiklendi")
    input_message = update.message.text
    if(input_message == "➕ ADD CHANNEL" or input_message == "🔥 CHANNELS" or input_message == "💥 POSTS" or input_message == "✅ BOT IS ACTIVE" or input_message == "⬅️ BACK"):
        addChannel(update, context, ekleme=False)

    else:
        addChannel(update, context, ekleme=True, groupInfo=input_message)

def addChannel(update, context, ekleme=False, groupInfo = None,showMessage=False):
    dispatcher.add_handler(MessageHandler(Filters.text, awaitForGroupNameInput), group=1)#GROUP=1 DIYEREK DAHA FAZLA HANDLER KYOABILIYORUZ, https://github.com/python-telegram-bot/python-telegram-bot/issues/1133
    if(showMessage):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please Enter the (Group Name,Group ID)")
    print("ADD CHANNEL")
    if(ekleme):
        groupInfoList = groupInfo.split(",")

        channelNameInput = groupInfoList[0]
        channelIdInput = groupInfoList[1]

        userJson = open("users.txt", "r")
        userJsonList = userJson.readlines()
        userJson.close()

        user = update.message.from_user
        currentUser = user['username']

        for users in userJsonList:
            convertedDict = ast.literal_eval(users)
            if (convertedDict['username'] == currentUser):
                channelNameList = convertedDict['channel-names'] #Dict'ten channelnamesi al
                channelNameList.append(channelNameInput)
                convertedDict['channel-names'] = channelNameList #channel namesi guncelleyip dicte geri ver

                channelIdList = convertedDict['channel-ids']  # Dict'ten channel ids al
                channelIdList.append(channelIdInput)
                convertedDict['channel-ids'] = channelIdList  # channel idsi guncelleyip dicte geri ver

                print(convertedDict)
                listLocation = userJsonList.index(users)
                userJsonList[listLocation] = convertedDict

        userJsonWrite = open("users.txt","w")
        for updatedUsers in userJsonList:
            userJsonWrite.write(str(updatedUsers))
            print(str(updatedUsers))

        updateCommand(update,context)

    else:
        print("Input Bekle")



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

    dispatcher.add_handler(MessageHandler(Filters.document,fileListener))


    updater.start_polling()
    updater.idle()

    #ADD GRUPTA 2 HANDLER KULLANDIM, BIRISI GENERAL HANDLER ILK BASISI ALGILAMAK ICIN (OZEL HANDLER ADD GRUP MESAJINA TEPKI VERMIYOR) DIGERI DE ADD GRUP MESAJINDAN SONRAKI INPUTU YAKALAMASI ICIN