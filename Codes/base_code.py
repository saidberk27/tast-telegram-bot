import time

import requests
import schedule

def main():
    channelID = "-642743936"
    channelID = int(channelID)
    adData = "Test"
    baseUrl = "https://api.telegram.org/bot5149901305:AAFBvwD3N1UCCkBDmNlRE9nH5YMa6fFAYtM/sendMessage?chat_id={}&text={}".format(channelID, adData)
    requests.post(baseUrl)


if __name__ == '__main__':
    main()