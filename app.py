import os
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_influxdb import InfluxDB
from api import fetch_wallet_balance

influx = InfluxDB()
app = Flask(__name__, static_url_path='')
app.config.from_object('config.DevelopmentConfig')
influx.init_app(app)

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    print(app.config)
    address = app.config['WALLET_ADDRESS']
    currency = app.config['CURRENCY']
    currency_sign = app.config['CURRENCY_SIGN']
    r, portfolio_balance = fetch_wallet_balance(address, currency)
    r['data']['portfolio_balance'] = portfolio_balance
    r['data']['currency_sign'] = currency_sign 
    # Query influxdb for timeseries data for the recent 30 days.
    result = influx.query('SELECT "value" FROM "portfolio_balance"."autogen"."balance_events" WHERE time > now() - 30d')
    points = result.get_points(tags={'currency': currency})
    r['data']['points'] = list(points)
    print(list(points))
    print(portfolio_balance)
    return render_template('layout-dark.html',error=r, data=r['data'])

if __name__ == '__main__':
    # Remember to work inside the context
    with app.app_context():
        influx.database.create("portfolio_balance")
        influx.database.switch(database="portfolio_balance")
    app.run()

