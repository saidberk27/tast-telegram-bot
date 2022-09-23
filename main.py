from telegram import *
from telegram.ext import *
from user_data import UserData
import threading
import time
from save_data import *

class MainMethods:
    def sendMessage(context, messageText, channelList):
        for channelID in channelList:
            context.bot.send_message(chat_id="{}".format(channelID), text=messageText)


class MainViews:
    keyboard = [
        [InlineKeyboardButton("Channels", callback_data='channels')],
        [InlineKeyboardButton("Create an Ad", callback_data='create an ad')],
        [InlineKeyboardButton("Stop an Ad", callback_data='stop an ad')],
        [InlineKeyboardButton("Bot is Active", callback_data='isActive')],
        [InlineKeyboardButton("Lanugage", callback_data='language')],
    ]

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



def start(update: Update, context: CallbackContext):
    global state
    user = update.message.from_user
    username = user['username']

    keyboard = MainViews.keyboard
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Hello {} Welcome the bot 🔥🔥🔥".format(username),reply_markup=reply_markup)

    state = "MAIN MENU"
    print(state)


def mainMenu(update, context):
    global state
    global keyboard
    keyboard = MainViews.keyboard
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Main Menu", reply_markup=reply_markup)

    state = "MAIN MENU"

def messageListener(update, context):
    global state
    global messageText
    global messageTimer
    global channelID
    global adTitle

    print("Message Listener State = ",state)

    if(state == "WAIT_FOR_AD_TITLE"):
        adTitle = update.message.text
        update.message.reply_text("Title {} saved.Please Type Your Post Text".format(adTitle))
        state = "WAIT_FOR_TEXT"

    elif(state == "WAIT_FOR_TEXT"):
        messageText = update.message.text
        state = "WAIT_FOR_CHANNEL"
        update.message.reply_text("Text {} saved.Please Type Channel ID".format(messageText))

    elif(state == "WAIT_FOR_CHANNEL"):
        channelID = int(update.message.text)
        state = "WAIT_FOR_TIMER"
        update.message.reply_text("Text {} saved.Please Type Timer Data".format(messageText))
    elif(state == "WAIT_FOR_TIMER"):
        try:
            messageTimer = int(update.message.text)
            update.message.reply_text("Timer {} saved.".format(messageTimer))
            createAd(update, context, adTitle=adTitle, timer=messageTimer, messageText="{}".format(messageText), channelList=[channelID])
            mainMenu(update, context)
        except ValueError: #nedense int yuzunden valuerror firlatiyor (false olmasina ragmen)
            pass


def queryListener(update: Update, context: CallbackContext):
    global state
    userdata = UserData()

    query = update.callback_query
    query.answer()
    print("state = ",state)
    if(state == "MAIN MENU"):
        if(query.data == "channels"):
            state = "CHANNELS SELECTED"
            listChannels(update, context)

        if(query.data == "posts"):
            state = "POSTS SELECTED"

        if (query.data == "create an ad"):
            state = "CREATE AN AD SELECTED"

        if (query.data == "isActive"):
            state = "BOT IS ACTIVE SELECTED"

        if (query.data == "language"):
            state = "LANGUAGE SELECTED"

        if(query.data == "stop an ad"):
            state = "STOP AN AD"
            listAds(update, context)

    if(state == "STOP AN AD"):
        if(query.data != "BACK"):
            stopAd(query.data)

    if(state == "CREATE AN AD SELECTED"):
        context.bot.send_message(chat_id=update.effective_chat.id, text="What is the name of title?")
        state = "WAIT_FOR_AD_TITLE"
    if(query.data == "BACK"):
        mainMenu(update,context)

def listChannels(update,context):
    userdata = UserData()
    keyboard = []
    for channelName in userdata.getChannelNames():
        keyboard.append([InlineKeyboardButton("{}".format(channelName), callback_data="{}".format(channelName))])
    keyboard.append([InlineKeyboardButton("ADD NEW CHANNEL", callback_data="ADD NEW CHANNEL")])
    keyboard.append([InlineKeyboardButton("BACK", callback_data="BACK")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Your Channels:", reply_markup=reply_markup)

async def listAds(update, context):
    global state

    keyboard = []
    _adTitles = []

    _jsonFile = open("userData.json", "r")
    _jsonText = _jsonFile.read()
    _jsonFile.close()
    _convertedDict = json.loads(_jsonText)
    _adList = _convertedDict["Ads"]

    for _ad in _adList:
        _adTitles.append(_ad["Ad Title"])

    _adNumber = 0
    for _adTitle in _adTitles:
        keyboard.append([InlineKeyboardButton("{}".format(_adTitle), callback_data="{}".format(_adNumber))])
        _adNumber = _adNumber + 1

    keyboard.append([InlineKeyboardButton("BACK", callback_data="BACK")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Your Active Ads:", reply_markup=reply_markup)

    #await client.edit_message(chat, message.id, 'hello!!')
    #context.bot.editMessageText(chat_id=update.effective_chat.id, text="Your Active Ads:", reply_markup=reply_markup)

def createAd(update, context, adTitle, timer, messageText, channelList):
    global active_slots
    global passive_slots
    global adOne
    active_slots[0] = loop(timer, MainMethods.sendMessage, context, messageText="{}".format(messageText), channelList=channelList)
    passive_slots.append(active_slots[0])
    active_slots.pop(0)
    print("Bekle...")
    #time.sleep(8)
    #stopAd(passive_slots[len(passive_slots) - 1])#passive slots listesi bossa 0. index bir eleman varsa 1. index 2 eleman varasa 2. index ... seklinde gitsin
    print(passive_slots, active_slots)
    SaveData(adTitle=adTitle, adContent=messageText,channelList=channelList, adTimer=timer).saveAdToJson()


def stopAd(adNumber):
    try:
        adNumber = int(adNumber)
    except ValueError:
        pass

    passive_slots[adNumber].running = False
    print(active_slots, passive_slots)
    passive_slots.pop(adNumber)
    active_slots.insert(adNumber, "Free Slot {}".format(adNumber + 1)) #adNumber + 1 cünkü 1, 2, 3 seklinde gitsin sifirdan baslamasin.
    print(passive_slots, active_slots)

if __name__ == '__main__':
    state = None
    messageText = "Yok"
    messageTimer = "Yok"
    adTitle = "Yok"
    channelID = None

    adOne = "Free Slot 1"
    adTwo = "Free Slot 2"
    adThree = "Free Slot 3"
    adFour = "Free Slot 4"
    adFive = "Free Slot 5"

    active_slots = [adOne, adTwo, adThree, adFour, adFive]
    passive_slots = []

    updater = Updater("5746559989:AAHKLZEkp7Cz_Kko0_r6kA9a626OEB-Crc0", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CallbackQueryHandler(queryListener))
    dp.add_handler(MessageHandler(Filters.text, messageListener))
    updater.start_polling()
    updater.idle()



