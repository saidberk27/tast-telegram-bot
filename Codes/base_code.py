import time

import requests
import schedule

def main():
    channelID = "-642743936"
    messageWillBeSent = "This Message Will Be Sent in Every 1 Hour"
    baseUrl = "https://api.telegram.org/bot5224789011:AAF0wt8Y-n_hfjdp_m7Fe8N9d_6WFZKW6bg/sendMessage?chat_id={}&text={}".format(channelID,messageWillBeSent)
    requests.get(baseUrl)

if __name__ == '__main__':
    schedule.every(10).seconds.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
