from threading import Timer
import telegram
from telegram import *
from telegram.ext import *

class PostToAllChannels(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
        print("Ad Stopped")


def start(update: Update, context: CallbackContext):
    global state
    user = update.message.from_user
    username = user['username']

    keyboard = [
        [InlineKeyboardButton("Channels", callback_data='posts')],
        [InlineKeyboardButton("Posts", callback_data='channels')],
        [InlineKeyboardButton("Bot is Active", callback_data='isActive')]
        [InlineKeyboardButton("Lanugage", callback_data='language')]
    ]
    update.message.reply_text("Hello {} Welcome the bot 🔥🔥🔥".format(username))


    state = "WAIT_FOR_TEXT"
    print(state)
def sendMessage(update, context, messageText):
    channelIDs = [-724890661, -616199647]
    for channelID in channelIDs:
        context.bot.send_message(chat_id="{}".format(channelID),text=messageText)

def messageListener(update, context):
    global state
    global messageText
    global messageTimer
    print(state)

    print(state == "WAIT_FOR_TIMER")
    if(state == "WAIT_FOR_TEXT"):
        messageText = update.message.text
        state = "WAIT_FOR_TIMER"
        update.message.reply_text("Text {} saved.Please Type Timer Data".format(messageText))
    if(state == "WAIT_FOR_TIMER"):
        try:
            messageTimer = int(update.message.text)
            update.message.reply_text("Timer {} saved.".format(messageTimer))
            update.message.reply_text("Message is being sending to all channels")
            PostToAllChannels(messageTimer, sendMessage, [update, context, messageText]).start()
        except ValueError: #nedense int yuzunden valuerror firlatiyor (false olmasina ragmen)
            pass

def queryListener(update, context):
    pass

if __name__ == '__main__':
    state = None
    messageText = "Yok"
    messageTimer = "Yok"

    updater = Updater("5746559989:AAHKLZEkp7Cz_Kko0_r6kA9a626OEB-Crc0", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CallbackQueryHandler(queryListener))
    dp.add_handler(MessageHandler(Filters.text, messageListener))
    updater.start_polling()
    updater.idle()



