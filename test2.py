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

    createAd(update, context, timer=2, messageText="Kanal Birrr", channelList=[-724890661])
    print(active_slots[0])
    time.sleep(3)

    #adOne = loop(3, sendMessage, context, messageText="bu birinci kanal", channelList=[-724890661])
    #adTwo = loop(5, sendMessage, context, messageText="bu ikinci kanal", channelList=[-616199647])


def stopAd(ad):
    ad.running = False

def createAd(update, context, timer, messageText, channelList):
    global active_slots
    global passive_slots
    global adOne
    active_slots[0] = loop(timer, sendMessage, context, messageText="{}".format(messageText), channelList=channelList)
    passive_slots.append(active_slots[0])
    active_slots.pop(0)
    print("Bekle...")
    time.sleep(8)
    stopAd(passive_slots[0])
    print(passive_slots, active_slots)



if __name__ == '__main__':
    updater = Updater("5746559989:AAHKLZEkp7Cz_Kko0_r6kA9a626OEB-Crc0", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))


    adOne = "Free Slot 1"
    adTwo = "Free Slot 2"
    adThree = "Free Slot 3"
    adFour = "Free Slot 4"
    adFive = "Free Slot 5"

    active_slots = [adOne, adTwo, adThree, adFour, adFive]
    passive_slots = []
    updater.start_polling()
    updater.idle()

