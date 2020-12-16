import time
import requests
from app import app

def telegram_bot_sendtext(bot_message):
    
    bot_token = app.config['bot_token']
    bot_chatID = app.config['bot_chatID']
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


def report(balance, change):
    my_message = "Alert! Current balance is: {}, changed from last time by %s percent!".format(balance, change)   ## Customize your message
    telegram_bot_sendtext(my_message)


    

while True:
    # get current portfolio price
    # get last portfolio price
    # alert if some threshold has met
    # report(balance, change)
    time.sleep(3600*1)
