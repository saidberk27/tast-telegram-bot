import threading
import time
from threading import Timer
import telegram
from telegram import *
from telegram.ext import *



class loop:
    def wait(self, seconds):
        # This makes sure that when self.running is false it will instantly stop
        for a in range(seconds):
            if self.running:
                time.sleep(1)
            else:
                break

    def run(self, seconds):
        while self.running:
            # Runs function
            self.function(self.context, self.messageText, self.channelList)
            self.wait(seconds)

    def __init__(self, seconds, function, context, messageText, channelList):
        self.running = True
        self.function = function
        self.context = context
        self.messageText = messageText
        self.channelList = channelList
        # Starts new thread instead of running it in the main thread
        # is because so it will not block other code
        self.thread = threading.Thread(target=self.run, args=(seconds,))# args = (seconds,) anlamadim arastiricam ama dokunma simdilik.
        self.thread.start()


def sendMessage(context, messageText, channelList):
    for channelID in channelList:
        context.bot.send_message(chat_id="{}".format(channelID), text=messageText)

def start(update: Update, context: CallbackContext):
    global adOne
    global adTwo
    user = update.message.from_user
    username = user['username']
    update.message.reply_text("Hello {} Starting Posting".format(username))

    adOne = loop(3, sendMessage, context, messageText="bu birinci kanal", channelList=[-724890661])
    adTwo = loop(5, sendMessage, context, messageText="bu ikinci kanal", channelList=[-616199647])

def stopOne(update: Update, context: CallbackContext):
    global adOne

    user = update.message.from_user
    username = user['username']
    update.message.reply_text("Hello {} Stopping Posting".format(username))

    adOne.running = False

def stopTwo(update: Update, context: CallbackContext):
    global adTwo

    user = update.message.from_user
    username = user['username']
    update.message.reply_text("Hello {} Stopping Posting".format(username))

    adTwo.running = False

if __name__ == '__main__':
    updater = Updater("5746559989:AAHKLZEkp7Cz_Kko0_r6kA9a626OEB-Crc0", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stopOne", stopOne))
    dp.add_handler(CommandHandler("stopTwo", stopTwo))

    adOne = None
    adTwo = None

    updater.start_polling()
    updater.idle()

