# -*- coding: utf-8 -*-

from telegram import *
from telegram.ext import *
from requests import *
import send_message
import ast

def startCommand(update: Updater,context: CallbackContext):
    user = update.message.from_user
    buttons = [[KeyboardButton("🔥 CHANNELS")],[KeyboardButton("💥 POSTS")],[KeyboardButton("✅ BOT IS ACTIVE")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello {} Welcome to bot!".format(user['username']), reply_markup=ReplyKeyboardMarkup(buttons))

def mainMenu(update,context):
    buttons = [[KeyboardButton("🔥 CHANNELS")],[KeyboardButton("💥 POSTS")],[KeyboardButton("✅ BOT IS ACTIVE")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please Select the Group",reply_markup=ReplyKeyboardMarkup(buttons))


def generalMessageHandler(update: Updater, context: CallbackContext):

    try:
        logFile = open("logs.txt","a")
        logFile.write(update.message.text + "\n")
    except UnicodeEncodeError:
        logFile.write(update.message.text[2:] + "\n")

#------------------------------GENERAL----------------------------#
    if("🔥 CHANNELS" in update.message.text):
        #fileListener(update,context)
        listChannels(update,context)
    if("💥 POSTS" in update.message.text):
        listPosts(update,context)

    if ("✅ BOT IS ACTIVE" in update.message.text):
        deactivateBot()

    if ("⬅️ BACK" in update.message.text):
        print("Back Tapped")
        mainMenu(update,context)
#------------------------------GENERAL----------------------------#
#------------------------------LIST CHANNELS----------------------------#
    if("➕ ADD CHANNEL" in update.message.text):
        addChannel(update,context)

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

def addChannel(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please Enter the Name of the Channel")

    userJson = open("users.txt", "r")
    userJsonList = userJson.readlines()
    user = update.message.from_user
    currentUser = user['username']
    for users in userJsonList:
        convertedDict = ast.literal_eval(users)
        if (convertedDict['username'] == currentUser):
            print(convertedDict['channel-name'])
def listPosts(update,context):
    buttons = [[KeyboardButton("✉️ POST 1")], [KeyboardButton("✉️ POST 2")],[KeyboardButton("➕ ADD POST")],[KeyboardButton("⛔ REMOVE POST")],[KeyboardButton("⬅️ BACK")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please Select the Group", reply_markup=ReplyKeyboardMarkup(buttons))


def deactivateBot():
    print("Bot Is Deactivating")




def fileListener(update,context):
    print("image handler")
    context.bot.get_file(update.message.document).download()


if __name__ == '__main__':

    updater = Updater(token="5149901305:AAFBvwD3N1UCCkBDmNlRE9nH5YMa6fFAYtM")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start",startCommand))
    dispatcher.add_handler(MessageHandler(Filters.text, generalMessageHandler))


    dispatcher.add_handler(MessageHandler(Filters.document,fileListener))

    updater.start_polling()
    updater.idle()