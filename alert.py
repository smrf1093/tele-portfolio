import time
import requests
from flask import current_app
from influxdb import InfluxDBClient

def telegram_bot_sendtext(bot_message):
    
    bot_token = current_app.config['bot_token']
    bot_chatID = current_app.config['bot_chatID']
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


def report(balance, change):
    my_message = "Alert! Current balance is: {}, changed from last time by %s percent!".format(balance, change)   ## Customize your message
    telegram_bot_sendtext(my_message)


    
def start_alerting_forever():
    client = InfluxDBClient(host=current_app.config['INFLUX_HOST'], port=current_app.config['INFLUX_PORT'])
    client.create_database('portfolio_')
    while True:
        # get current portfolio price
        json_body = [
            {
                "measurement": "cpu_load_short",
                "tags": {
                    "host": "server01",
                    "region": "us-west"
                },
                "time": "2009-11-10T23:00:00Z",
                "fields": {
                    "value": 0.64
                }
            }
        ]
        result = client.query('select value from cpu_load_short;')
        print("Result: {0}".format(result))
        # get last portfolio price
        # alert if some threshold has met
        # report(balance, change)
        # Sleep 1 hour
        time.sleep(3600*1)
