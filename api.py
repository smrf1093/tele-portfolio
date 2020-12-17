import os
import requests

supported_currencies = ['usd', 'eur']


def fetch_wallet_balance(address, currency='usd'):
    if currency not in supported_currencies:
        raise Exception("Unsupported currency!")

    api_url = 'https://api.covalenthq.com'
    endpoint = f'/v1/1/address/{address}/balances_v2/'
    url = api_url + endpoint
    
    payload = {
        "key": os.environ['COVALENT_API_KEY'],
        "quote-currency": currency
    }

    r = requests.get(url, params=payload)
    data = r.json()
    # We don't need nft data right now
    data['data']['items'] = [item for item in data['data']['items'] if item['type'] != 'nft' ]
 
    portfolio_balance = 0.0
    for item in data['data']['items']:
        portfolio_balance += item['quote']
        
    return data, portfolio_balance
