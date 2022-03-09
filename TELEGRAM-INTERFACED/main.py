from telegram import *
from telegram.ext import *
from requests import *

updater = Updater(token="5224789011:AAF0wt8Y-n_hfjdp_m7Fe8N9d_6WFZKW6bg")
dispatcher = updater.dispatcher

def createAd(update,context):
    print("creating an ad...")
    buttons = [[KeyboardButton("Add Media")], [KeyboardButton("Save Ad")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please Enter the Ad Data", reply_markup=ReplyKeyboardMarkup(buttons))

def publishAd(update,context):
    print("publishing an ad...")
    buttons = [[KeyboardButton("GROUP 1")], [KeyboardButton("GROUP 2")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please Select the Group", reply_markup=ReplyKeyboardMarkup(buttons))

def startCommand(update: Updater,context: CallbackContext):
    buttons = [[KeyboardButton("PUBLISH ADS")],[KeyboardButton("CREATE AN AD")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to bot!", reply_markup=ReplyKeyboardMarkup(buttons))

def messageHandler(update: Updater,context: CallbackContext):
    if("CREATE AN AD" in update.message.text):
        createAd(update,context)
    if("PUBLISH ADS" in update.message.text):
        publishAd(update,context)

dispatcher.add_handler(CommandHandler("start",startCommand))
dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))

updater.start_polling()