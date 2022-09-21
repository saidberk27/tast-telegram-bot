import time
from threading import Timer
import telegram
from telegram import *
from telegram.ext import *
from user_data import UserData

class AdSlotOne(Timer):
    isRunning = True
    collapse = False

    def run(self):
        if(self.isRunning):
            while not self.finished.wait(self.interval):
                print("Calisiyor")
                self.function(*self.args, **self.kwargs)

                if(self.collapse):
                    print("Collapsing")
                    break
        else:
            print("Ad Stopped")

    def stopAd(self):
        self.isRunning = False
        self.collapse = True

class AdSlotTwo(Timer):
    isRunning = True
    collapse = False

    def run(self):
        if(self.isRunning):
            while not self.finished.wait(self.interval):
                print("Calisiyor")
                self.function(*self.args, **self.kwargs)

                if(self.collapse):
                    print("Collapsing")
                    break
        else:
            print("Ad Stopped")

    def stopAd(self):
        self.isRunning = False
        self.collapse = True


def sendMessage(context, messageText, channelIDs):
    if(isRunning):
        for channelID in channelIDs:
            context.bot.send_message(chat_id="{}".format(channelID),text=messageText)


class initAdOne:
    def __init__(self,context):
        self.channelIDs = [-724890661]
        self.context = context
        self.adSlotOne = AdSlotOne(3, sendMessage, [self.context, "deneme", self.channelIDs])

    def startAd(self):
        self.adSlotOne.start()

    def stopAd(self):
        self.adSlotOne.stopAd()

class initAdTwo:
    def __init__(self,context):
        self.channelIDs = [-616199647]
        self.context = context
        self.adSlotTwo = AdSlotTwo(5, sendMessage, [self.context, "deneme", self.channelIDs])

    def startAd(self):
        self.adSlotTwo.start()

    @staticmethod
    def stopAd(self):
        self.adSlotTwo.stopAd()

def start(update: Update, context: CallbackContext):
    global state
    global initAdOne
    global initAdTwo

    user = update.message.from_user
    username = user['username']
    update.message.reply_text("Hello {} Starting Posting".format(username))
    InitAdOne = initAdOne(context=context)
    InitAdOne.startAd()
    InitAdTwo = initAdTwo(context=context)
    InitAdTwo.startAd()

def stop1(update: Update, conte  xt: CallbackContext):
    global InitAdOne
    print("STOP BIR")
    InitAdOne.stopAd()

def stop2(update: Update, context: CallbackContext):
    print("STOP IKI")

    InitAdTwo = initAdTwo(context=context)
    InitAdTwo.stopAd()

isRunning = True
collapse = False

InitAdOne = ""
InitAdTwo = ""

updater = Updater("5746559989:AAHKLZEkp7Cz_Kko0_r6kA9a626OEB-Crc0", use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("stop1", stop1))
dp.add_handler(CommandHandler("stop2", stop2))
#dp.add_handler(CommandHandler("stop", stop))

updater.start_polling()
updater.idle()