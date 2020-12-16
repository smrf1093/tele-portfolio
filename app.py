import os
from flask import Flask, render_template, jsonify, request
from api import fetch_wallet_balance


app = Flask(__name__)


@app.route('/')
def index():
    address = request.args.get('wallet')
    currency = request.args.get('currency')
    r = fetch_wallet_balance(address, currency)
    return render_template('index.html',error=r, data=r['data'])

if __name__ == '__main__':
    app.run()

