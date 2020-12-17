import os
import pickle
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_influxdb import InfluxDB
from api import fetch_wallet_balance
from pathlib import Path

influx = InfluxDB()
app = Flask(__name__, static_url_path='')
app.config.from_object('config.DevelopmentConfig')
influx.init_app(app)

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    address = app.config['WALLET_ADDRESS']
    currency = app.config['CURRENCY']
    currency_sign = app.config['CURRENCY_SIGN']
    r, portfolio_balance = fetch_wallet_balance(address, currency)
    r['data']['portfolio_balance'] = portfolio_balance
    r['data']['overall_balance'] = 1000
    r['data']['currency_sign'] = currency_sign 
    # Query influxdb for timeseries data for the recent 30 days.
    result = influx.query('SELECT * FROM "portfolio_balance"."autogen"."balance_events" WHERE time > now() - 30d GROUP BY * ORDER BY ASC')
    points = result.get_points(tags={'currency': currency})
    r['data']['points'] = list(points)
    print(r['data']['points'])
    print(portfolio_balance)
    # read settings to load values if it exists
    settings_file = Path("/path/to/file")
    if settings_file.exists():
        with open(os.environ.get("SETTINGS_FILE"), 'rb') as f:
            settings_data = pickle.load(f)
            r['wallets'] = settings_data['wallets']
            r['currency'] = settings_data['currency']
            r['chat_id'] = settings_data['chat_id']
    return render_template('layout-dark.html',error=r, data=r['data'])


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == "GET":
        r = {}
        r['data'] = []
        return render_template('settings.html',error=r, data=r['data'])
    if request.method == "POST":
        settings_data = {}
        settings_data['wallets'] = request.values.get('wallets') 
        settings_data['chat_id'] = request.values.get('chat-id') 
        settings_data['currency'] = request.values.get('currency')
        with open(os.environ.get("SETTINGS_FILE"), 'wb') as f:
            pickle.dump(settings_data, f, pickle.HIGHEST_PROTOCOL)
        r = {}
        r['success'] = True
        return render_template('settings.html',error=r, data=r)


if __name__ == '__main__':
    # Remember to work inside the context
    with app.app_context():
        influx.database.create("portfolio_balance")
        influx.database.switch(database="portfolio_balance")
    app.run()

