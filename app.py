import os
import pickle
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_influxdb import InfluxDB
from api import fetch_wallet_balance
from config import save_settings, load_settings 

influx = InfluxDB()
app = Flask(__name__, static_url_path='')
app.config.from_object('config.DevelopmentConfig')
influx.init_app(app)

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    wallet = request.args.get('wallet')
    settings_data = load_settings()
    if wallet is None or len(wallet) == 0:
        wallet = settings_data['wallets'][0]
    # calc overall balance
    portfolio_balance = None
    overall_balance = 0.0
    for w in settings_data['wallets']:
        r, balance = fetch_wallet_balance(w, settings_data['currency'])
        overall_balance += balance
        if wallet == w:
            portfolio_balance = balance

    r['data']['portfolio_balance'] = portfolio_balance
    r['data']['overall_balance'] = overall_balance
    # Query influxdb for timeseries data for the recent 30 days.
    result = influx.query('SELECT * FROM "portfolio_balance"."autogen"."balance_events" WHERE time > now() - 30d GROUP BY * ORDER BY ASC')
    points = result.get_points(tags={'currency': settings_data['currency'], "wallet": wallet})
    r['data']['points'] = list(points)
    print(r['data']['points'])
    print(portfolio_balance)
    # read settings to load values if it exists
    r['data']['default_wallet'] = wallet
    r['data']['wallets'] = settings_data['wallets']
    r['data']['currency'] = settings_data['currency']
    r['data']['chat_id'] = settings_data['chat_id']
    return render_template('layout-dark.html',error=r, data=r['data'])


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == "GET":
        r = {}
        settings_data = load_settings()
        if wallet is None or len(wallet) == 0:
           wallet = settings_data['wallets'][0]
        r['data']['default_wallet'] = wallet
        r['data']['wallets'] = settings_data['wallets']
        r['data']['currency'] = settings_data['currency']
        r['data']['chat_id'] = settings_data['chat_id']
        return render_template('settings.html',error=r, data=r['data'])
        
    if request.method == "POST":
        settings_data = {}
        settings_data['wallets'] = request.values.get('wallets') 
        settings_data['chat_id'] = request.values.get('chat-id') 
        settings_data['currency'] = request.values.get('currency')
        save_settings(**settings_data)
        r = {}
        r['success'] = True
        return render_template('settings.html',error=r, data=r)


if __name__ == '__main__':
    # Remember to work inside the context
    with app.app_context():
        influx.database.create("portfolio_balance")
        influx.database.switch(database="portfolio_balance")
    app.run()

