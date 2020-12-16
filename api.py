def fetch_wallet_balance(address, currency='usd'):
    api_url = 'https://api.covalenthq.com'
    endpoint = f'/v1/1/address/{address}/balances_v2/'
    url = api_url + endpoint
    
    payload = {
        "key": config("API_KEY"),
        "quote-currency": currency
    }

    r = requests.get(url, params=payload)
    return(r.json())
