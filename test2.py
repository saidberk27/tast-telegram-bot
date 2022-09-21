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
            self.function(self.context, self.messageText)
            self.wait(seconds)

    def __init__(self, seconds, function, context, messageText):
        self.running = True
        self.function = function
        self.context = context
        self.messageText = messageText
        # Starts new thread instead of running it in the main thread
        # is because so it will not block other code
        self.thread = threading.Thread(target=self.run, args=(seconds,))
        self.thread.start()


def sendMessage(context, messageText):
    channelIDs = [-724890661]
    for channelID in channelIDs:
        context.bot.send_message(chat_id="{}".format(channelID), text=messageText)

def start(update: Update, context: CallbackContext):
    global adOne
    user = update.message.from_user
    username = user['username']
    update.message.reply_text("Hello {} Starting Posting".format(username))

    adOne = loop(3,sendMessage,context,messageText="bu birinci kanal")

def stop(update: Update, context: CallbackContext):
    global adOne
    user = update.message.from_user
    username = user['username']
    update.message.reply_text("Hello {} Stopping Posting".format(username))

    adOne.running = False

if __name__ == '__main__':
    updater = Updater("5746559989:AAHKLZEkp7Cz_Kko0_r6kA9a626OEB-Crc0", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))

    adOne = None

    updater.start_polling()
    updater.idle()

