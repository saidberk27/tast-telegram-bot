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


def sendMessage(context, messageText):
    if(isRunning):
        channelIDs = [-724890661, -616199647]
        for channelID in channelIDs:
            context.bot.send_message(chat_id="{}".format(channelID),text=messageText)


class initAds:
    def __init__(self,context):
        self.context = context
        self.adSlotOne = AdSlotOne(3, sendMessage, [self.context, "deneme"])

    def startAd(self):
        self.adSlotOne.start()

    def stopAd(self):
        self.adSlotOne.stopAd()

def start(update: Update, context: CallbackContext):
    global state
    user = update.message.from_user
    username = user['username']
    update.message.reply_text("Hello {} Starting Posting".format(username))
    InitAds = initAds(context=context)
    InitAds.startAd()
    time.sleep(5)
    print("Stopping all ads")
    InitAds.stopAd()

isRunning = True
collapse = False


updater = Updater("5746559989:AAHKLZEkp7Cz_Kko0_r6kA9a626OEB-Crc0", use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
#dp.add_handler(CommandHandler("stop", stop))

updater.start_polling()
updater.idle()