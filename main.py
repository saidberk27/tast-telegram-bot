from telegram import *
from telegram.ext import *
from user_data import UserData
import threading
import time
from save_data import *

class MainMethods:
    def sendMessage(context, messageText, channelList, fileName, buttonList):
        reply_markup = InlineKeyboardMarkup(buttonList)
        for channelID in channelList:
            if(fileName == None):
                context.bot.send_message(chat_id="{}".format(channelID), text=messageText, reply_markup=reply_markup)
            else:
                context.bot.send_photo(channelID, photo=open("Medias/{}".format(fileName), 'rb'), caption=messageText, reply_markup=reply_markup)

class MainViews:
    keyboard = [
        [InlineKeyboardButton("🔥 CHANNELS", callback_data='channels')],
        [InlineKeyboardButton("➕ CREATE AN AD", callback_data='create an ad')],
        [InlineKeyboardButton("❌ DELETE AN AD ", callback_data='delete an ad')],
        [InlineKeyboardButton("✔ BOT IS ACTIVE", callback_data='isActive')],
        [InlineKeyboardButton("Media Test", callback_data='media')],
    ]

    timerKeyboard = [[InlineKeyboardButton("10 Seconds", callback_data="10"),
                      InlineKeyboardButton("30 Seconds", callback_data="30"),
                      InlineKeyboardButton("45 Seconds", callback_data="45")],
                     [InlineKeyboardButton("1 Minute", callback_data="60"),
                      InlineKeyboardButton("5 Minutes", callback_data="300"),
                      InlineKeyboardButton("10 Minutes", callback_data="600")],
                     [InlineKeyboardButton("15 Minutes", callback_data="900"),
                      InlineKeyboardButton("30 Minutes", callback_data="1800"),
                      InlineKeyboardButton("45 Minutes", callback_data="2700"),
                      InlineKeyboardButton("1 Hour", callback_data="3600")],
                     [InlineKeyboardButton("3 Hours", callback_data="10800"),
                      InlineKeyboardButton("6 Hours", callback_data="21600"),
                      InlineKeyboardButton("9 Hours", callback_data="32400"),
                      InlineKeyboardButton("12 Hours", callback_data="43200")],
                     [InlineKeyboardButton("15 Hours", callback_data="54000"),
                      InlineKeyboardButton("18 Hours", callback_data="64800"),
                      InlineKeyboardButton("24 Hours", callback_data="86400")],
                     [InlineKeyboardButton("BACK ⬅", callback_data="BACK")]
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
            self.function(self.context, self.messageText, self.channelList, self.fileName, self.buttonList)
            self.wait(seconds)

    def __init__(self, seconds, function, context, messageText, channelList, fileName, buttonList):
        self.running = True
        self.function = function
        self.context = context
        self.messageText = messageText
        self.channelList = channelList
        self.fileName = fileName
        self.buttonList = buttonList
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
    print(buttonsTempList)


def mainMenu(update, context, menuText = "Main Menu ⭐"):
    global state
    global keyboard
    keyboard = MainViews.keyboard
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text=menuText, reply_markup=reply_markup)

    state = "MAIN MENU"

def messageListener(update, context):
    global state
    global messageText
    global messageTimer
    global channelID
    global adTitle
    global channelName
    global buttonsTempList
    global buttonText
    global buttonLink

    print("Message Listener State = ",state)

    if(state == "WAIT_FOR_AD_TITLE"):
        adTitle = update.message.text
        update.message.reply_text("Title {} saved.Please Type Your Post Text".format(adTitle))
        state = "WAIT_FOR_TEXT"

    elif(state == "WAIT_FOR_TEXT"):
        messageText = update.message.text
        state = "WAIT_FOR_MEDIA"
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Skip", callback_data="skip")]])
        update.message.reply_text("Text {} saved. Please Add Image/Video/Gif or Skip".format(messageText), reply_markup=reply_markup)

        #WAIT_FOR_MEDIA Supervising at FileHandler handleMedia()

    elif(state == "WAIT_FOR_CHANNEL"):
        keyboard = [[InlineKeyboardButton("10 Seconds", callback_data="10"),
                     InlineKeyboardButton("30 Seconds", callback_data="30"),
                     InlineKeyboardButton("45 Seconds", callback_data="45")],
                    [InlineKeyboardButton("1 Minute", callback_data="60"),
                     InlineKeyboardButton("5 Minutes", callback_data="300"),
                     InlineKeyboardButton("10 Minutes", callback_data="600")],
                    [InlineKeyboardButton("15 Minutes", callback_data="900"),
                     InlineKeyboardButton("30 Minutes", callback_data="1800"),
                     InlineKeyboardButton("45 Minutes", callback_data="2700"),
                     InlineKeyboardButton("1 Hour", callback_data="3600")],
                    [InlineKeyboardButton("3 Hours", callback_data="10800"),
                     InlineKeyboardButton("6 Hours", callback_data="21600"),
                     InlineKeyboardButton("9 Hours", callback_data="32400"),
                     InlineKeyboardButton("12 Hours", callback_data="43200")],
                    [InlineKeyboardButton("15 Hours", callback_data="54000"),
                     InlineKeyboardButton("18 Hours", callback_data="64800"),
                     InlineKeyboardButton("24 Hours", callback_data="86400")],
                    [InlineKeyboardButton("BACK ⬅", callback_data="BACK")]
                    ]
        channelID = int(update.message.text)
        state = "WAIT_FOR_TIMER"
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Text {} saved.Please Select Timer Data".format(messageText),
                                  reply_markup=reply_markup)
    # WAIT FOR TIMER STATE'I QUERY LISTENER'DA DENETLENIYOR.

    elif(state == "WAIT_FOR_CHANNEL_NAME"):
        channelName = update.message.text
        state = "WAIT_FOR_CHANNEL_ID"
        context.bot.send_message(chat_id=update.effective_chat.id, text="Channel Name {} Saved. Please Enter Chat ID".format(channelName))

    elif(state == "WAIT_FOR_CHANNEL_ID"):
        channelID = int(update.message.text)
        SaveData(channelName=channelName, channelID=channelID).saveChanneltoJson()
        mainMenu(update, context, menuText="Channel Succesfully Saved. You Can Use it with Your Ads".format(channelName))

    elif(state == "WAIT_FOR_BUTTON_TEXT"):
        state = "WAIT_FOR_BUTTON_LINK"
        buttonText = update.message.text
        context.bot.send_message(chat_id=update.effective_chat.id, text="Button Text {} Saved. Please Enter Button Link".format(buttonText))

    elif(state == "WAIT_FOR_BUTTON_LINK"):
        state = "WAIT_FOR_BUTTON"
        buttonLink = update.message.text
        createButton(buttonText=buttonText, buttonLink=buttonLink)
        keyboard = [[InlineKeyboardButton("Add Buttons", callback_data="add buttons"), InlineKeyboardButton("Continue", callback_data="continue")]]
        reply_markup = InlineKeyboardMarkup(buttonsTempList)
        reply_markup2 = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Button Succesfully Saved!", reply_markup=reply_markup)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Add More Button or Continue", reply_markup=reply_markup2)


def queryListener(update: Update, context: CallbackContext):
    global state
    global adChannelName
    global adChannelID
    global buttonsTempList
    userdata = UserData()

    query = update.callback_query
    query.answer()
    print("state = ",state)

    if(query.data == "media"):
        handleMedia(update, context)
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

        if(query.data == "delete an ad"):
            state = "DELETE AN AD SELECTED"
            listAds(update, context)

    if(state == "WAIT_FOR_TIMER"):
        try:
            messageTimer = int(query.data)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Timer saved. Ad is Running")
            createAd(update, context, adTitle=adTitle, timer=messageTimer, messageText="{}".format(messageText), channelList=[adChannelID], buttonList = buttonsTempList)
            buttonsTempList = []
            mainMenu(update, context)
        except ValueError:  # nedense int yuzunden valuerror firlatiyor (false olmasina ragmen)
            pass

    if(state == "DELETE AN AD SELECTED"):
        if(query.data != "BACK"):
            deleteAd(update, context, query.data)

    if(state == "CREATE AN AD SELECTED"):
        context.bot.send_message(chat_id=update.effective_chat.id, text="What is the name of title?")
        state = "WAIT_FOR_AD_TITLE"

    if(state == "CHANNELS SELECTED"):
        if(query.data == "ADD NEW CHANNEL"):
            state = "WAIT_FOR_CHANNEL_NAME"
            context.bot.send_message(chat_id=update.effective_chat.id, text="What is the name of channel?")

        elif(query.data == "DELETE CHANNEL"):
            state = "WAIT_FOR_NAME_OF_DELETED_CHANNEL"
            listChannels(update, context, "Please Select a Channel You Want to Delete")

    if(state == "WAIT_FOR_NAME_OF_DELETED_CHANNEL"):
        if(query.data != "DELETE CHANNEL"):
            delete_channel = SaveData(channelName=query.data)
            delete_channel.deleteChannelFromJson()
            mainMenu(update, context, "CHANNEL SUCCESFULLY REMOVED")

    if(state == "WAIT_FOR_CHANNEL"):
        _jsonFile = open("userData.json", "r")
        _jsonText = _jsonFile.read()
        _jsonFile.close()
        _convertedDict = json.loads(_jsonText)


        adChannelName = query.data
        adChannelID = _convertedDict["channels"][adChannelName]
        state = "WAIT_FOR_TIMER"
        reply_markup = InlineKeyboardMarkup(MainViews.timerKeyboard)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Channel {} Selected. Please Select Timer Data".format(adChannelName), reply_markup=reply_markup)

    if(state == "WAIT_FOR_BUTTON"):
        if(query.data == "continue"):
            state = "WAIT_FOR_CHANNEL"
            context.bot.send_message(chat_id=update.effective_chat.id, text="Please Select the Group You Want To Post:")
            listChannels(update, context)

        elif(query.data == "add buttons"):
            state = "WAIT_FOR_BUTTON_TEXT"
            context.bot.send_message(chat_id=update.effective_chat.id, text="What is the Text of Button")

    if(state == "WAIT_FOR_MEDIA" and query.data == "skip"):
        state = "WAIT_FOR_BUTTON"
        keyboard = [[InlineKeyboardButton("Add Buttons", callback_data="add buttons"),
                     InlineKeyboardButton("Continue", callback_data="continue")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Adding File Skipped. Add Buttons Or Continue", reply_markup=reply_markup)

    if(query.data == "BACK"):
        mainMenu(update,context)

def listChannels(update, context, message="⭐ Your Channels:"):
    _jsonFile = open("userData.json", "r")
    _jsonText = _jsonFile.read()
    _jsonFile.close()
    _convertedDict = json.loads(_jsonText)
    channelNamesList = _convertedDict['channels'].keys()
    keyboard = []
    for channelName in channelNamesList:
        keyboard.append([InlineKeyboardButton("{}".format(channelName), callback_data="{}".format(channelName))])
    keyboard.append([InlineKeyboardButton("➕ ADD NEW CHANNEL", callback_data="ADD NEW CHANNEL")])
    keyboard.append([InlineKeyboardButton("DELETE CHANNEL", callback_data="DELETE CHANNEL")])
    keyboard.append([InlineKeyboardButton("BACK ⬅", callback_data="BACK")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)

def listAds(update, context):
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

    keyboard.append([InlineKeyboardButton("BACK ⬅", callback_data="BACK")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Your Active Ads:", reply_markup=reply_markup)

    #await client.edit_message(chat, message.id, 'hello!!')
    #context.bot.editMessageText(chat_id=update.effective_chat.id, text="Your Active Ads:", reply_markup=reply_markup)

def handleMedia(update: Update, context: CallbackContext):
    global state
    global media

    if(state == "WAIT_FOR_MEDIA"):
        state = "WAIT_FOR_BUTTON"
        file_id = update.message.document["file_id"]
        media = update.message.document["file_name"]
        context.bot.get_file(file_id).download(custom_path="Medias/{}".format(update.message.document["file_name"]))
        keyboard = [[InlineKeyboardButton("Add Buttons", callback_data="add buttons"), InlineKeyboardButton("Continue", callback_data="continue")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id, text="File {} Saved to Ad. Add Buttons Or Continue".format(update.message.document["file_name"]), reply_markup=reply_markup)
        #listChannels(update, context)

def createButton(buttonText, buttonLink):
    global buttonsTempList
    buttonsTempList.append([InlineKeyboardButton(buttonText, url=buttonLink)])



def createAd(update, context, adTitle, timer, messageText, channelList, buttonList):
    global active_slots
    global passive_slots
    global media

    active_slots[0] = loop(timer, MainMethods.sendMessage, context, messageText="{}".format(messageText), channelList=channelList, fileName=media, buttonList=buttonList)
    passive_slots.append(active_slots[0])
    active_slots.pop(0)
    print("Bekle...")
    #time.sleep(8)
    #stopAd(passive_slots[len(passive_slots) - 1])#passive slots listesi bossa 0. index bir eleman varsa 1. index 2 eleman varasa 2. index ... seklinde gitsin
    print(passive_slots, active_slots)
    SaveData(adTitle=adTitle, adContent=messageText,channelList=channelList, adTimer=timer, mediaName=media, buttonList=buttonList).saveAdToJson()


def deleteAd(update, context, adNumber):

    try:
        adNumber = int(adNumber)
        passive_slots[adNumber].running = False
        print(active_slots, passive_slots)
        passive_slots.pop(adNumber)
        active_slots.insert(adNumber, "Free Slot {}".format(adNumber + 1)) #adNumber + 1 cünkü 1, 2, 3 seklinde gitsin sifirdan baslamasin.
        print(passive_slots, active_slots)


        delete_ad = SaveData(adIndex = adNumber)
        delete_ad.deleteAdFromJson()
        mainMenu(update, context, "AD SUCCESFULLY DELETED")

    except:
        pass

if __name__ == '__main__':
    state = None
    messageText = "Yok"
    messageTimer = "Yok"
    adTitle = "Yok"
    channelID = None
    channelName = None
    adChannelName = None
    adChannelID = None
    media = None
    buttonsTempList = []
    buttonText = None
    buttonLink = None

    adOne = "Free Slot 1"
    adTwo = "Free Slot 2"
    adThree = "Free Slot 3"
    adFour = "Free Slot 4"
    adFive = "Free Slot 5"

    active_slots = [adOne, adTwo, adThree, adFour, adFive]
    active_slots_channel_names = []
    passive_slots = []

    updater = Updater("5746559989:AAHKLZEkp7Cz_Kko0_r6kA9a626OEB-Crc0", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CallbackQueryHandler(queryListener))
    dp.add_handler(MessageHandler(Filters.text, messageListener))
    dp.add_handler(MessageHandler(Filters.document, handleMedia))

    updater.start_polling()
    updater.idle()
