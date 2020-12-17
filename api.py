import os
import requests

supported_currencies = ['usd', 'eur']

test_data = {"data": {"address": "0x68581b09b9f815ad0a37477f340e7e211030c899", "updated_at": "2020-12-17T20:45:57.065290Z", "next_update_at": "2020-12-17T20:50:57.065291Z", "quote_currency": "EUR", "chain_id": 1, "items": [{"contract_decimals": 18, "contract_name": "Dai Stablecoin", "contract_ticker_symbol": "DAI", "contract_address": "0x6b175474e89094c44da98b954eedeac495271d0f", "logo_url": "https://logos.covalenthq.com/tokens/0x6b175474e89094c44da98b954eedeac495271d0f.png", "type": "dust", "balance": "1000000000000000000000", "quote_rate": 0.8116996, "quote": 811.69965, "nft_data": None}, {"contract_decimals": 6, "contract_name": "Tether USD", "contract_ticker_symbol": "USDT", "contract_address": "0xdac17f958d2ee523a2206206994597c13d831ec7", "logo_url": "https://logos.covalenthq.com/tokens/0xdac17f958d2ee523a2206206994597c13d831ec7.png", "type": "dust", "balance": "0", "quote_rate": 0.8107451, "quote": 0.0, "nft_data": None}, {"contract_decimals": 0, "contract_name": "KudosToken", "contract_ticker_symbol": "KDO", "contract_address": "0x2aea4add166ebf38b63d09a75de1a7b94aa24163", "logo_url": "https://logos.covalenthq.com/tokens/0x2aea4add166ebf38b63d09a75de1a7b94aa24163.png", "type": "nft", "balance": "0", "quote_rate": 0.0, "quote": 0.0, "nft_data": None}, {"contract_decimals": 18, "contract_name": "Golem Network Token", "contract_ticker_symbol": "GNT", "contract_address": "0xa74476443119a942de498590fe1f2454d7d4ac0d", "logo_url": "https://logos.covalenthq.com/tokens/0xa74476443119a942de498590fe1f2454d7d4ac0d.png", "type": "dust", "balance": "1000000000000000000000", "quote_rate": 0.0, "quote": 0.0, "nft_data": None}, {"contract_decimals": 6, "contract_name": "USD Coin", "contract_ticker_symbol": "USDC", "contract_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", "logo_url": "https://logos.covalenthq.com/tokens/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48.png", "type": "dust", "balance": "0", "quote_rate": 0.81208134, "quote": 0.0, "nft_data": None}, {"contract_decimals": 18, "contract_name": "Tellor Token", "contract_ticker_symbol": "TRB", "contract_address": "0x0ba45a8b5d5575935b8158a88c631e9f9c95a2e5", "logo_url": "https://logos.covalenthq.com/tokens/0x0ba45a8b5d5575935b8158a88c631e9f9c95a2e5.png", "type": "dust", "balance": "0", "quote_rate": 21.175968, "quote": 0.0, "nft_data": None}, {"contract_decimals": 18, "contract_name": "Ether", "contract_ticker_symbol": "ETH", "contract_address": "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", "logo_url": "https://logos.covalenthq.com/tokens/0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee.png", "type": "cryptocurrency", "balance": "0", "quote_rate": 544.24414, "quote": 0.0, "nft_data": None}], "pagination": None}, "error": False, "error_message": None, "error_code": None}

def fetch_wallet_balance(address, currency='usd'):
    return test_data, 1000.0    
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
