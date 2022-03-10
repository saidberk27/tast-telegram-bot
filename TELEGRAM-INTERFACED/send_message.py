import time
import requests
import schedule

def sendText(adText):
    channelID = "-642743936"
    file = {'photo':open('C:\\Users\\C Said Berk\\Pictures\\mater.jpg', 'rb')}
    baseUrl = "https://api.telegram.org/bot5149901305:AAFBvwD3N1UCCkBDmNlRE9nH5YMa6fFAYtM/sendMessage?chat_id={}&text={}".format(channelID,adText)
    requests.post(baseUrl)


