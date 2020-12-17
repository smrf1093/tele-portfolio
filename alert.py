import os
from datetime import datetime
import time
import requests
from api import fetch_wallet_balance
from influxdb import InfluxDBClient
import logging
from config import load_settings

settings = load_settings()

def telegram_bot_sendtext(bot_message):
    
    bot_token = os.environ['BOT_TOKEN']
    bot_chatID = settings['chat_id']
    if len(bot_chatID) > 0:
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id='\
                + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)
        return response.json()
    print("warning! chat_id value is empty!")


def report(wallet, balance, change):
    my_message = "TelePortfolio alert!\n your current balance changed from last time by {:.2f}\
            percent!\nCurrent Balance: {:.2f}\nWallet address: {}".format(change, balance, wallet)
    telegram_bot_sendtext(my_message)


    
def start_alerting_forever():
    client = InfluxDBClient(host=os.environ['INFLUXDB_HOST'], port=os.environ['INFLUXDB_PORT'])
    client.create_database('portfolio_balance')
    client.switch_database('portfolio_balance')
    while True:
        for wallet in settings['wallets']:
            # get current portfolio price
            _, balance = fetch_wallet_balance(wallet, settings['currency'])
            result = client.query('SELECT * FROM portfolio_balance.autogen.balance_events\
                    GROUP BY * ORDER BY DESC LIMIT 1;')
            points = result.get_points(tags={'currency': settings['currency']})
            points = list(points)
            print(points)
            if len(points) > 0:
                previous_balance = points[0]['value']
                # Alert if new balance changes more than one percent from the last time.
                change = (balance - previous_balance)/previous_balance
                print(change)
                if abs(change) >= 0.01:
                    report(wallet, balance, change*100.0)
            # Now we write our new record to influxdb
            json_body = [
                {
                    "measurement": "balance_events",
                    "tags": {
                        "currency": settings['currency'],
                        "wallet": wallet
                    },
                    "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                    "fields": {
                        "value": balance
                    }
                }
            ]
            ok = client.write_points(json_body)
            
            if not ok:
                logging.warning("couldn't write data to influxdb!")
            # Sleep 1 hour
            time.sleep(1 * 3600)

if __name__ == '__main__':
    start_alerting_forever()
