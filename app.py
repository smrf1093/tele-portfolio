import os
from flask import Flask, render_template, jsonify, request, send_from_directory
from api import fetch_wallet_balance


app = Flask(__name__, static_url_path='')


@app.route('/dist/<path:path>')
def send_js(path):
    return send_from_directory('dist', path)

@app.route('/')
def index():
    address = request.args.get('wallet')
    currency = request.args.get('currency')
    r = fetch_wallet_balance(address, currency)
    return render_template('layout-dark.html',error=r, data=r['data'])

if __name__ == '__main__':
    app.run()

