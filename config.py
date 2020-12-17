import os
import json
basedir = os.path.abspath(os.path.dirname(__file__))

# Convert time string expressed as <number>[m|h|d|s|w] to seconds
seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
def convert_to_seconds(s):
    return int(s[:-1]) * seconds_per_unit[s[-1]]


def save_settings(wallets, currency, chat_id):
    wallets = wallets.split(",")
    data = {
            "wallets": wallets,
            "currency": currency, 
            "chat_id": chat_id
    }
    with open('config.json', 'w' , encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_settings():
    # init data object
    data = {
            "wallets": ["0x" + "0"*40],
            "currency": "usd", 
            "chat_id": ""
    }
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            data = json.load(f)
    return data

settings = load_settings()

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    # We use these for sending alert message through telegram bot api
    BOT_CHATID = settings["chat_id"]
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    API_KEY = os.environ.get("COVALENT_API")
    WALLET_ADDRESSES = settings["wallets"] 
    CURRENCY = settings["currency"]
    INFLUXDB_HOST = os.environ.get("INFLUXDB_HOST")
    INFLUXDB_PORT = os.getenv("INFLUXDB_PORT", "8086")
    INFLUXDB_WRITE_PERIOD = os.getenv("INFLUXDB_WRITE_PERIOD", "1h")
    INFLUXDB_WRITE_PERIOD = convert_to_seconds(INFLUXDB_WRITE_PERIOD)
    


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

