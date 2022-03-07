import time

import requests
import schedule

def main():
    channelID = "-642743936"
    file = {'photo':open('C:\\Users\\C Said Berk\\Pictures\\mater.jpg', 'rb')}
    baseUrl = "https://api.telegram.org/bot5224789011:AAF0wt8Y-n_hfjdp_m7Fe8N9d_6WFZKW6bg/sendPhoto?chat_id={}&caption=Test Photo".format(channelID)
    requests.post(baseUrl, files=file)

if __name__ == '__main__':
    schedule.every(1).seconds.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
