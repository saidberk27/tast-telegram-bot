def sendMessage(update, context, messageText):
    channelIDs = [-724890661, -616199647]
    for channelID in channelIDs:
        context.bot.send_message(chat_id="{}".format(channelID),text=messageText)