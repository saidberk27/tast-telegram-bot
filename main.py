import telegram
from telegram import *
from telegram.ext import *

import threading
import time
from save_data import *
from datetime import datetime
from authentication import Auth
import strings
from flood_prevention import FloodPrevention

class MainMethods:
    global string
    def sendMessage(context, update, messageText, channelList, fileName, buttonList):
        reply_markup = InlineKeyboardMarkup(buttonList)
        fileType = detectFileType(fileName)
        try:
            for channelID in channelList:
                if(fileName == None): #dosya ismi yoksa dosya yoktur :p
                    context.bot.send_message(chat_id="{}".format(channelID), text=messageText, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)
                elif(fileType == "document"):
                    context.bot.send_document(channelID, document=open("Medias/{}".format(fileName), 'rb'), caption=messageText, reply_markup=reply_markup, parse_mode= telegram.ParseMode.MARKDOWN)
                elif(fileType == "video"):
                    context.bot.send_video(channelID, video=open("Medias/{}".format(fileName), 'rb'), caption=messageText, reply_markup=reply_markup, parse_mode= telegram.ParseMode.MARKDOWN)
                elif(fileType == "photo"):
                    context.bot.send_photo(channelID, photo=open("Medias/{}".format(fileName), 'rb'), caption=messageText, reply_markup=reply_markup, parse_mode= telegram.ParseMode.MARKDOWN)
        except Exception as e:
            mainMenu(update,context,menuText=string["long_caption"] + " or " + str(e))
            deleteAd(update, context, -1)
    def resetGlobalVars(self):
        global state
        global messageText
        global messageTimer
        global adTitle
        global channelID
        global channelName
        global adChannelName
        global adChannelID
        global media
        global buttonsTempList
        global channelList
        global buttonText
        global buttonLink

        state = "MAIN MENU"
        messageText = "Yok"
        messageTimer = "Yok"
        adTitle = "Yok"
        channelID = None
        channelName = None
        adChannelName = None
        adChannelID = None
        media = None
        buttonsTempList = []
        channelList = []
        buttonText = None
        buttonLink = None
class MainViews:
    def getMainKeyboard(self):
        global string
        keyboard = [
            [InlineKeyboardButton(string["channels"], callback_data='channels')],
            [InlineKeyboardButton(string["create_ad"], callback_data='create an ad')],
            [InlineKeyboardButton(string["delete_ad"], callback_data='delete an ad')],
            [InlineKeyboardButton(string["add_manager"], callback_data='add manager')],
            [InlineKeyboardButton(string["change_language"], callback_data='change language')],

        ]

        return keyboard
    def getTimerKeyboard(self):
        global string

        timerKeyboard = [[
                        InlineKeyboardButton(string["10_sec"], callback_data="10"),
                     InlineKeyboardButton(string["30_sec"], callback_data="30"),
                     InlineKeyboardButton(string["45_sec"], callback_data="45")],
                    [InlineKeyboardButton(string["1_min"], callback_data="60"),
                     InlineKeyboardButton(string["5_min"], callback_data="300"),
                     InlineKeyboardButton(string["10_min"], callback_data="600")],
                    [InlineKeyboardButton(string["15_min"], callback_data="900"),
                     InlineKeyboardButton(string["30_min"], callback_data="1800"),
                     InlineKeyboardButton(string["45_min"], callback_data="2700"),
                     InlineKeyboardButton(string["1_hour"], callback_data="3600")],
                    [InlineKeyboardButton(string["3_hour"], callback_data="10800"),
                     InlineKeyboardButton(string["6_hour"], callback_data="21600"),
                     InlineKeyboardButton(string["9_hour"], callback_data="32400"),
                     InlineKeyboardButton(string["12_hour"], callback_data="43200")],
                    [InlineKeyboardButton(string["15_hour"], callback_data="54000"),
                     InlineKeyboardButton(string["18_hour"], callback_data="64800"),
                     InlineKeyboardButton(string["24_hour"], callback_data="86400")],
                    [InlineKeyboardButton(string["back"], callback_data="BACK")]
                    ]

        return timerKeyboard

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
            self.function(self.context,self.update, self.messageText, self.channelList, self.fileName, self.buttonList)
            self.wait(seconds)

    def __init__(self, seconds, function, context,update, messageText, channelList, fileName, buttonList):
        self.running = True
        self.function = function
        self.context = context
        self.update = update
        self.messageText = messageText
        self.channelList = channelList
        self.fileName = fileName
        self.buttonList = buttonList
        # Starts new thread instead of running it in the main thread
        # is because so it will not block other code
        self.thread = threading.Thread(target=self.run, args=(seconds,))# args = (seconds,) anlamadim arastiricam ama dokunma simdilik.
        self.thread.start()


def restore(update: Update, context: CallbackContext):
    global media
    global buttonsTempList
    with open("userData.json", "r+") as jsonFile:
        data = json.load(jsonFile)

        for ad in data["Ads"]:
            adTitle = ad['Ad Title']
            timer = ad['Ad Timer']
            messageText = ad['Ad Content']
            channelList = ad['Ad Channels']
            media = ad['Ad Media']
            #buttons = ad['Ad Buttons']

            #for button in buttons:
                #createButton(button['Button Text'], buttonLink=button['Button Link'])


            print("ad one ")
            #print(buttons, "\n")
            #print(buttonsTempList)
            createAd(update, context, adTitle=adTitle, timer=timer, messageText="{}".format(messageText), channelList=channelList,buttonList = buttonsTempList, saveToJson=False)

    update.message.reply_text("Ads are being restored. ", parse_mode=telegram.ParseMode.MARKDOWN)



def start(update: Update, context: CallbackContext):
    print("Start")
    user = update.message.from_user
    username = str(user['id'])
    print(user)
    if(Auth(username=username).isManager()):
        global state
        keyboard = MainViews().getMainKeyboard()
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(string["wellcome_message"].format(username),reply_markup=reply_markup,parse_mode=telegram.ParseMode.MARKDOWN)
        state = "MAIN MENU"
        MainMethods().resetGlobalVars()
        print("STATE = {}".format(state))

    else:
        keyboard = [[InlineKeyboardButton("צור קשר עם המוכר",url="https://t.me/PRSAOMbot")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("""
        *ברוכים הבאים*  🎁- עוד מערכת משוכללת *מבית קידום ממומן* 🙆🏻‍♂
עם קיבלת את ההודעה זה *אומר* שהבוט לא *שלך!* 😼 רוצה לקנות אותי ? ולפרסם בקבוצות        
נטושות 🥹 ללא ניהול ? *פנה אלי בכפתור למטה*        
        """,reply_markup=reply_markup,parse_mode=telegram.ParseMode.MARKDOWN)

def mainMenu(update, context, menuText = "Main Menu / תפריט ראשי"):
    global string
    global state
    global keyboard
    keyboard = MainViews().getMainKeyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text=menuText, reply_markup=reply_markup,parse_mode=telegram.ParseMode.MARKDOWN)

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
    global string
    global buttonData
    print("STATE = {}".format(state))

    if(state == "WAIT_FOR_AD_TITLE"):
        adTitle = update.message.text
        update.message.reply_text(string["title_saved"].format(adTitle),parse_mode=telegram.ParseMode.MARKDOWN)
        state = "WAIT_FOR_TEXT"

    elif(state == "WAIT_FOR_TEXT"):
        messageText = update.message.text_markdown_v2.replace("\.", ".") #url lerde noktalar bozulmasin diye replace yapiliyor.
        #replace("**", "\\*")
        state = "WAIT_FOR_MEDIA"
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(string["skip"], callback_data="skip")]])
        update.message.reply_text(string["text_saved"].format(messageText), reply_markup=reply_markup,parse_mode=telegram.ParseMode.MARKDOWN)

        #WAIT_FOR_MEDIA Supervising at FileHandler handleMedia()

    elif(state == "WAIT_FOR_CHANNEL"):
        with open("userData.json", "r") as file:
            channels = json.loads(file.read())["channels"]

        keyboard = [[
                    InlineKeyboardButton(string["10_sec"], callback_data="10"),
                     InlineKeyboardButton(string["30_sec"], callback_data="30"),
                     InlineKeyboardButton(string["45_sec"], callback_data="45")],
                    [InlineKeyboardButton(string["1_min"], callback_data="60"),
                     InlineKeyboardButton(string["5_min"], callback_data="300"),
                     InlineKeyboardButton(string["10_min"], callback_data="600")],
                    [InlineKeyboardButton(string["15_min"], callback_data="900"),
                     InlineKeyboardButton(string["30_min"], callback_data="1800"),
                     InlineKeyboardButton(string["45_min"], callback_data="2700"),
                     InlineKeyboardButton(string["1_hour"], callback_data="3600")],
                    [InlineKeyboardButton(string["3_hour"], callback_data="10800"),
                     InlineKeyboardButton(string["6_hour"], callback_data="21600"),
                     InlineKeyboardButton(string["9_hour"], callback_data="32400"),
                     InlineKeyboardButton(string["12_hour"], callback_data="43200")],
                    [InlineKeyboardButton(string["15_hour"], callback_data="54000"),
                     InlineKeyboardButton(string["18_hour"], callback_data="64800"),
                     InlineKeyboardButton(string["24_hour"], callback_data="86400")],
                    [InlineKeyboardButton(string["back"], callback_data="BACK")]
                    ]
        channelID = int(update.message.text)
            # WAIT FOR TIMER STATE'I QUERY LISTENER'DA DENETLENIYOR.
        state = "WAIT_FOR_TIMER"
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(string["channel_id_saved"].format(messageText), reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)

    elif(state == "WAIT_FOR_CHANNEL_NAME"):
        channelName = update.message.text
        state = "WAIT_FOR_CHANNEL_ID"
        context.bot.send_message(chat_id=update.effective_chat.id, text=string["channel_name_saved"].format(channelName),parse_mode=telegram.ParseMode.MARKDOWN)

    elif(state == "WAIT_FOR_CHANNEL_ID"):
        channelID = int(update.message.text)
        if(not SaveData(channelID=channelID).isChannelExist()):
            SaveData(channelName=channelName, channelID=channelID).saveChanneltoJson()
            mainMenu(update, context, menuText=string["channel_saved"].format(channelName))
        else:
            mainMenu(update, context, menuText="Channel Already Added.")

    elif(state == "WAIT_FOR_BUTTON_TEXT"):
        state = "WAIT_FOR_BUTTON_LINK"
        buttonText = update.message.text
        context.bot.send_message(chat_id=update.effective_chat.id, text=string["button_text_saved"].format(buttonText),parse_mode=telegram.ParseMode.MARKDOWN)

    elif(state == "WAIT_FOR_BUTTON_LINK"):
        try:
            buttonLink = update.message.text
            buttonData.append({"Button Text":buttonText, "Button Link":buttonLink})

            if("http" in update.message.text or "www" in update.message.text or ".com" in update.message.text or "net" in update.message.text): # web sitesi olup olmadigini kontrol
                createButton(buttonText=buttonText, buttonLink=buttonLink)
                keyboard = [[InlineKeyboardButton(string["add_buttons"], callback_data="add buttons"), InlineKeyboardButton(string["continue"], callback_data="continue")]]
                reply_markup = InlineKeyboardMarkup(buttonsTempList)
                reply_markup2 = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(chat_id=update.effective_chat.id, text=string["button_saved"],
                                         reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)
                context.bot.send_message(chat_id=update.effective_chat.id, text=string["add_more_button_or_continue"],
                                         reply_markup=reply_markup2, parse_mode=telegram.ParseMode.MARKDOWN)
                state = "WAIT_FOR_BUTTON"
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text=string["invalid_button_url"])

        except Exception as e:
            print("link hatasi", e)
            #mainMenu(update, context, menuText=string["invalid_button_url"])

    elif(state == "WAIT_FOR_MANAGER_USERNAME"):
        manager_username = update.message.text
        if(Auth(username=manager_username).addManager()):
            mainMenu(update, context, menuText=string["manager_added"])
        else:
            mainMenu(update, context, menuText="!!! You Have Tried Add More Than 3 Managers or Same User as a Manager Again!")

def queryListener(update: Update, context: CallbackContext):
    global state
    global adChannelName
    global adChannelID
    global buttonsTempList
    global string
    global channelList


    query = update.callback_query
    query.answer()
    print("STATE = {}".format(state))

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
            if(FloodPrevention(messageTimer).calculateAdsPerMinute()):
                if(len(active_slots) != 0):
                    context.bot.send_message(chat_id=update.effective_chat.id, text=string["timer_saved_ad_is_running"],parse_mode=telegram.ParseMode.MARKDOWN)
                    createAd(update, context, adTitle=adTitle, timer=messageTimer, messageText="{}".format(messageText), channelList=channelList, buttonList = buttonsTempList)
                    buttonsTempList = []
                    MainMethods().resetGlobalVars()
                    mainMenu(update, context)
                else:
                    mainMenu(update, context, menuText=string["bot_can_only_post_10_ads"])
            else:
                reply_markup = InlineKeyboardMarkup(MainViews().getTimerKeyboard())
                context.bot.send_message(chat_id=update.effective_chat.id, text=string["timer_opiton_is_invalid"],parse_mode=telegram.ParseMode.MARKDOWN,reply_markup=reply_markup)

        except ValueError:  # nedense int yuzunden valuerror firlatiyor (false olmasina ragmen)
            pass

    if(state == "DELETE AN AD SELECTED"):
        if(query.data != "BACK"):
            deleteAd(update, context, query.data)

    if(state == "CREATE AN AD SELECTED"):
        context.bot.send_message(chat_id=update.effective_chat.id, text=string["what_is_the_title"],parse_mode=telegram.ParseMode.MARKDOWN)
        state = "WAIT_FOR_AD_TITLE"

    if(state == "CHANNELS SELECTED"):
        if(query.data == "ADD NEW CHANNEL"):
            state = "WAIT_FOR_CHANNEL_NAME"
            context.bot.send_message(chat_id=update.effective_chat.id, text=string["what_is_the_name_of_channel"],parse_mode=telegram.ParseMode.MARKDOWN)


        elif(query.data == "DELETE CHANNEL"):
            state = "WAIT_FOR_NAME_OF_DELETED_CHANNEL"
            listChannels(update, context, string["please_select_channel"])

    if(state == "WAIT_FOR_NAME_OF_DELETED_CHANNEL"):
        if(query.data != "DELETE CHANNEL" and query.data != "ADD NEW CHANNEL" and query.data != "BACK"):
            delete_channel = SaveData(channelName=query.data)
            delete_channel.deleteChannelFromJson()
            mainMenu(update, context, string["channel_succesfully_removed"])

    if(state == "WAIT_FOR_CHANNEL"):
        _jsonFile = open("userData.json", "r")
        _jsonText = _jsonFile.read()
        _jsonFile.close()
        _convertedDict = json.loads(_jsonText)
        reply_markup = InlineKeyboardMarkup(MainViews().getTimerKeyboard())

        if(query.data == "POST TO ALL GROUPS"):
            channelList = list(_convertedDict["channels"].values())
            state = "WAIT_FOR_TIMER"
            context.bot.send_message(chat_id=update.effective_chat.id, text=string["all_channels_selected"], reply_markup=reply_markup)

        else:
            adChannelName = query.data
            adChannelID = _convertedDict["channels"][adChannelName]
            channelList = [adChannelID]
            state = "WAIT_FOR_TIMER"
            context.bot.send_message(chat_id=update.effective_chat.id, text=string["channel_selected"].format(adChannelName), reply_markup=reply_markup,parse_mode=telegram.ParseMode.MARKDOWN)

    if(state == "WAIT_FOR_BUTTON"):
        if(query.data == "continue"):
            state = "WAIT_FOR_CHANNEL"
            context.bot.send_message(chat_id=update.effective_chat.id, text=string["please_select_group"],parse_mode=telegram.ParseMode.MARKDOWN)
            listChannels(update, context, hideOptions=True, showSendToAllGroupsOption=True)

        elif(query.data == "add buttons"):
            state = "WAIT_FOR_BUTTON_TEXT"
            context.bot.send_message(chat_id=update.effective_chat.id, text=string["what_is_the_text_of_button"],parse_mode=telegram.ParseMode.MARKDOWN)

    if(state == "WAIT_FOR_MEDIA" and query.data == "skip"):
        state = "WAIT_FOR_BUTTON"
        keyboard = [[InlineKeyboardButton(string["add_buttons"], callback_data="add buttons"),
                     InlineKeyboardButton(string["continue"], callback_data="continue")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id, text=string["adding_file_skipped"], reply_markup=reply_markup,parse_mode=telegram.ParseMode.MARKDOWN)

    if(query.data == "BACK"):
        mainMenu(update,context)

    if(query.data == "add manager"):
        state = "WAIT_FOR_MANAGER_USERNAME"
        context.bot.send_message(chat_id=update.effective_chat.id, text=string["what_is_username"],parse_mode=telegram.ParseMode.MARKDOWN)

    if(query.data == "change language"):
        state = "WAIT_FOR_LANGUAGE"
        keyboard = [[InlineKeyboardButton("ENGLISH", callback_data="en")],
                        [InlineKeyboardButton("עִברִית", callback_data="he")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        context.bot.send_message(chat_id=update.effective_chat.id, text=string["please_select_language"], reply_markup = reply_markup,parse_mode=telegram.ParseMode.MARKDOWN)

    if(state == "WAIT_FOR_LANGUAGE"):
        if(query.data == "he"):
            string = strings.he
            mainMenu(update, context, string["language_succesfully_changed"])

        elif(query.data == "en"):
            string = strings.en
            mainMenu(update, context,  string["language_succesfully_changed"])

def listChannels(update, context, message="Your Channels", hideOptions = False, showSendToAllGroupsOption=False):
    _jsonFile = open("userData.json", "r")
    _jsonText = _jsonFile.read()
    _jsonFile.close()
    _convertedDict = json.loads(_jsonText)
    channelNamesList = _convertedDict['channels'].keys()
    keyboard = []
    for channelName in channelNamesList:
        keyboard.append([InlineKeyboardButton("{}".format(channelName), callback_data="{}".format(channelName))])

    if(showSendToAllGroupsOption):
        keyboard.append([InlineKeyboardButton(string["post_all_groups"], callback_data="POST TO ALL GROUPS")])
    if(hideOptions):
        pass
    else:
        keyboard.append([InlineKeyboardButton(string["add_new_channel"], callback_data="ADD NEW CHANNEL")])
        keyboard.append([InlineKeyboardButton(string["delete_channel"], callback_data="DELETE CHANNEL")])
        keyboard.append([InlineKeyboardButton(string["back"], callback_data="BACK")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup,parse_mode=telegram.ParseMode.MARKDOWN)

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

    keyboard.append([InlineKeyboardButton(string["back"], callback_data="BACK")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text=string["your_active_ads"], reply_markup=reply_markup,parse_mode=telegram.ParseMode.MARKDOWN)

    #await client.edit_message(chat, message.id, 'hello!!')
    #context.bot.editMessageText(chat_id=update.effective_chat.id, text="Your Active Ads:", reply_markup=reply_markup)

def handleMedia(update: Update, context: CallbackContext):
    global state
    global media

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")

    if(state == "WAIT_FOR_MEDIA"):
        state = "WAIT_FOR_BUTTON"
        file_id = update.message.document["file_id"]
        media = "{}".format(dt_string)

        try:
            context.bot.get_file(file_id).download(custom_path="Medias/{}".format(media))
            keyboard = [[InlineKeyboardButton(string["add_buttons"], callback_data="add buttons"),
                         InlineKeyboardButton(string["continue"], callback_data="continue")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=update.effective_chat.id, text=string["file_saved_to_ad"],
                                     reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)
            # listChannels(update, context)
        except Exception as e:
            print(e)
            state = "WAIT_FOR_MEDIA"
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(string["skip"], callback_data="skip")]])
            context.bot.send_message(chat_id=update.effective_chat.id, text=string["file_is_too_big"],
                                     reply_markup=reply_markup)



def handleVideo(update: Update, context: CallbackContext):
    global state
    global media
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")

    if(state == "WAIT_FOR_MEDIA"):
        state = "WAIT_FOR_BUTTON"
        file_id = update.message.video["file_id"]
        media = "{}.mp4".format(dt_string)
        try:
            context.bot.get_file(file_id).download(custom_path="Medias/{}".format(media))
            keyboard = [[InlineKeyboardButton(string["add_buttons"], callback_data="add buttons"),
                         InlineKeyboardButton(string["continue"], callback_data="continue")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=update.effective_chat.id, text=string["file_saved_to_ad"],
                                     reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)
            # listChannels(update, context)

        except Exception as e:
            print(e)
            state = "WAIT_FOR_MEDIA"
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(string["skip"], callback_data="skip")]])
            context.bot.send_message(chat_id=update.effective_chat.id, text=string["file_is_too_big"], reply_markup=reply_markup)

def handlePhoto(update: Update, context: CallbackContext):
    global state
    global media
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")

    if(state == "WAIT_FOR_MEDIA"):
        state = "WAIT_FOR_BUTTON"
        file_id = update.message.photo[-1].file_id
        media = "{}.jpg".format(dt_string)
        try:
            context.bot.get_file(file_id).download(custom_path="Medias/{}".format(media))
            keyboard = [[InlineKeyboardButton(string["add_buttons"], callback_data="add buttons"), InlineKeyboardButton(string["continue"], callback_data="continue")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=update.effective_chat.id, text=string["file_saved_to_ad"], reply_markup=reply_markup,parse_mode=telegram.ParseMode.MARKDOWN)
            #listChannels(update, context)

        except Exception as e:
            print(e)
            state = "WAIT_FOR_MEDIA"
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(string["skip"], callback_data="skip")]])
            context.bot.send_message(chat_id=update.effective_chat.id, text=string["file_is_too_big"], reply_markup=reply_markup)


def createButton(buttonText, buttonLink):
    global buttonsTempList

    buttonsTempList.append([InlineKeyboardButton(buttonText, url=buttonLink)])

def createAd(update, context, adTitle, timer, messageText, channelList, buttonList = [], saveToJson=True):
    global active_slots
    global passive_slots
    global media

    active_slots[0] = loop(timer, MainMethods.sendMessage, context,update, messageText="{}".format(messageText), channelList=channelList, fileName=media, buttonList=buttonList)
    passive_slots.append(active_slots[0])
    active_slots.pop(0)

    #time.sleep(8)
    #stopAd(passive_slots[len(passive_slots) - 1])#passive slots listesi bossa 0. index bir eleman varsa 1. index 2 eleman varasa 2. index ... seklinde gitsin
    #print(passive_slots, active_slots)
    if(saveToJson):
        print(buttonData)
        SaveData(adTitle=adTitle, adContent=messageText,channelList=channelList, adTimer=timer, mediaName=media, buttonList=buttonData).saveAdToJson()

def deleteAd(update, context, adNumber):

    try:
        adNumber = int(adNumber)
        passive_slots[adNumber].running = False
        #print(active_slots, passive_slots)
        passive_slots.pop(adNumber)
        active_slots.insert(adNumber, "Free Slot {}".format(adNumber + 1)) #adNumber + 1 cünkü 1, 2, 3 seklinde gitsin sifirdan baslamasin.
        #print(passive_slots, active_slots)


        delete_ad = SaveData(adIndex = adNumber)
        delete_ad.deleteAdFromJson()
        if(adNumber != -1): #Caption too long hatasi alidigmiz zaman -1'i sonuncuyu silsin diye gonderiyoruz. Onda da main menuye redirect yapiyor tekrar yapmasina gerek yok.
            mainMenu(update, context, string["ad_deleted"])

    except:
        pass

def detectFileType(fileName):
    extensions = {"png":"photo", "jpg":"photo", "mp4":"video", "avi":"video", "wmv":"video"}
    try:
        extension = fileName.split(".")[1] #burada hata veriyorsa - AttributeError: 'NoneType' object has no attribute 'split' handleImage'de unique id ile calistigindan oturu veriyor ( niye cozemedim henuz )
        try:
            return extensions[extension]
        except KeyError:
            return "document"

    except:
        return "photo"



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
    channelList = []
    buttonText = None
    buttonLink = None
    buttonData = []
    string = strings.he

    adOne = "Free Slot 1"
    adTwo = "Free Slot 2"
    adThree = "Free Slot 3"
    adFour = "Free Slot 4"
    adFive = "Free Slot 5"
    adSix = "Free Slot 6"
    adSeven = "Free Slot 7"
    adEight = "Free Slot 8"
    adNine = "Free Slot 9"
    adTen = "Free Slot 10"

    adOne1 = "Free Slot 1"
    adTwo1 = "Free Slot 2"
    adThree1 = "Free Slot 3"
    adFour1 = "Free Slot 4"
    adFive1 = "Free Slot 5"
    adSix1 = "Free Slot 6"
    adSeven1 = "Free Slot 7"
    adEight1 = "Free Slot 8"
    adNine1 = "Free Slot 9"
    adTen1 = "Free Slot 10"

    adOne2 = "Free Slot 1"
    adTwo2 = "Free Slot 2"
    adThree2 = "Free Slot 3"
    adFour2 = "Free Slot 4"
    adFive2 = "Free Slot 5"
    adSix2 = "Free Slot 6"
    adSeven2 = "Free Slot 7"
    adEight2 = "Free Slot 8"
    adNine2 = "Free Slot 9"
    adTen2 = "Free Slot 10"

    adOne3 = "Free Slot 1"
    adTwo3 = "Free Slot 2"
    adThree3 = "Free Slot 3"
    adFour3 = "Free Slot 4"
    adFive3 = "Free Slot 5"
    adSix3 = "Free Slot 6"
    adSeven3 = "Free Slot 7"
    adEight3 = "Free Slot 8"
    adNine3 = "Free Slot 9"
    adTen3 = "Free Slot 10"
    active_slots = [adOne, adTwo, adThree, adFour, adFive, adSix, adSeven, adEight, adNine, adTen,
                    adOne1, adTwo1, adThree1, adFour1, adFive1, adSix1, adSeven1, adEight1, adNine1, adTen1,
                    adOne2, adTwo2, adThree2, adFour2, adFive2, adSix2, adSeven2, adEight2, adNine2, adTen2,
                    adOne3, adTwo3, adThree3, adFour3, adFive3, adSix3, adSeven3, adEight3, adNine3, adTen3]
    active_slots_channel_names = []
    passive_slots = []


    userName = input("What is the Customer's Username? : ")
    botToken = input("What is the Bot Token? : ")
    SaveData(botToken=botToken).saveBotToken()
    Auth(username=userName).initializeFirstManager()

    updater = Updater("{}".format(botToken), use_context=True)
    print("Bot has started, you are free to use it.")

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("restore", restore))
    dp.add_handler(CallbackQueryHandler(queryListener))
    dp.add_handler(MessageHandler(Filters.text, messageListener))
    dp.add_handler(MessageHandler(Filters.document, handleMedia))
    dp.add_handler(MessageHandler(Filters.video, handleVideo))
    dp.add_handler(MessageHandler(Filters.photo, handlePhoto))

    updater.start_polling()
    updater.idle()