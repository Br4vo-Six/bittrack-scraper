import requests
import json
import time
import os
from dotenv import load_dotenv

def fetchTx(tx_id, proxy=None):
    load_dotenv()
    # Base URL for the API
    base_url = 'https://api.blockcypher.com/v1/btc/main/txs/'
    
    # Complete URL with the transaction ID
    url = f'{base_url}{tx_id}?limit=24385'
    try:
        # Send the GET request
        response = requests.get(url, proxies=proxy, timeout=int(os.getenv('MAX_TIMEOUT')), verify=False)
        if response.status_code == 200:
            json_data = response.json()
            return json_data
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def fetchAddrHist(addr, proxy=None):
    load_dotenv()
    # Base URL for the API
    base_url = 'https://api.blockcypher.com/v1/btc/main/addrs/'
    
    # Complete URL with the Bitcoin address
    url = f'{base_url}{addr}'
    
    try:
        response = requests.get(url, proxies=proxy,timeout=int(os.getenv('MAX_TIMEOUT')), verify=False)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response content as JSON
            json_data = response.json()
            return json_data
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

if __name__ == "__main__":
    tx_id = '5658a925ca3a5528353ae9324263d688c8b5932eac4261dae035bf948deb0f8d'
    start_time = time.time()
    transaction_details = fetchTx(tx_id)
    end_time = time.time()
    duration = end_time - start_time
    if transaction_details:
        print(transaction_details)
        print(f'Results fetched in {duration} s')
        print("-----------------------")
    bitcoin_address = '3AujBhj7bAFgGVb8gYccUDpWcAYYUJ37WY'
    start_time = time.time()
    address_details = fetchAddrHist(bitcoin_address)
    end_time = time.time()
    duration = end_time - start_time
    if address_details:
        print(address_details)
        print(f'Results fetched in {duration} s')
        print("-----------------------")