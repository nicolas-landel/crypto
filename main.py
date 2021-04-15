# Requires python-requests. Install with pip:
#
#   pip install requests
#
# or, with easy-install:
#
#   easy_install requests
import os, sys
import json, hmac, hashlib, time, requests
from requests.auth import AuthBase
from dotenv import load_dotenv

# Before implementation, set environmental variables with the names API_KEY and API_SECRET
load_dotenv()
API_KEY = os.getenv("key")
API_SECRET = os.getenv("secret")

# Create custom authentication for Coinbase API
class CoinbaseWalletAuth(AuthBase):
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def __call__(self, request):
        timestamp = str(int(time.time()))
        if request.body:
          message = timestamp + request.method.upper() + request.path_url + request.body
        else:
          message = timestamp + request.method.upper() + request.path_url + ''          
        message_b = bytes(message, 'latin-1')
        signature = hmac.new(bytes(self.secret_key, 'latin-1'), message_b, hashlib.sha256).hexdigest()

        request.headers.update({
          'CB-ACCESS-SIGN': signature,
          'CB-ACCESS-TIMESTAMP': timestamp,
          'CB-ACCESS-KEY': self.api_key,
        })
        return request

api_url = 'https://api.coinbase.com/v2/'
auth = CoinbaseWalletAuth(API_KEY, API_SECRET)

# query = 'users'
# query = 'accounts'

account_data = requests.get(api_url + 'accounts', auth=auth).json()


# print(account_data['data'], type(account_data['data']), type(account_data['data'][0]))

def create_currency_list(account_data):
    currency_list = []
    
    currency_list = [
        currency_data['currency']['code'] for currency_data in account_data['data'] if float(currency_data['balance']['amount']) != 0
    ]
    return currency_list
  
def init_currency_dic(account_data):
    currency_data = {}
    
    currency_data = {
        currency_data['currency']['code']: currency_data['balance']['amount'] for currency_data in account_data['data'] if float(currency_data['balance']['amount']) != 0
    }
    return currency_data

currency_list = create_currency_list(account_data)
currency_amount_dic = init_currency_dic(account_data)
print(currency_list, currency_amount_dic)




query = 'prices/DASH-EUR/buy'
r = requests.get(api_url + query, auth=auth)
print(r.json())

def create_currency_value_dic(currency_list, currency_amount_dic):
    data_dic = {}

    for i, cur in enumerate(currency_list):
        query = f'prices/{cur}-EUR/buy'
        request_val_price = requests.get(api_url + query, auth=auth)
        json_price = request_val_price.json()
        data_dic[cur] = round(float(json_price['data']['amount']) * float(currency_amount_dic.get(cur)), 2)
    
    return data_dic

data_dic = create_currency_value_dic(currency_list, currency_amount_dic)

print(data_dic)

def save_in_csv(data_dic):
    # directory = os.path.dirname(sys.argv[0])
    print("DIRECTORy", os.path)
    if not os.path.isfile('data.csv'):
        print(f"File path 'data.csv' does not exist. Exiting...")
        sys.exit()

    with open('data.csv', 'r', encoding="utf-8") as file_data:
        raw_data = file_data.read()
    
    print("RAW", raw_data)

    return None



save_in_csv(data_dic)