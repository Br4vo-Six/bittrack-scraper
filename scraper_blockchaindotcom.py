import requests
import json

def fetchTx(tx_id):
    # Base URL for the API
    base_url = 'https://blockchain.info/rawtx/'
    
    # Complete URL with the transaction ID
    url = f'{base_url}{tx_id}'
    
    try:
        # Send the GET request
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response content as JSON
            json_data = response.json()
            return json_data
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def fetchAddrHist(addr):
    # Base URL for the API
    base_url = 'https://blockchain.info/rawaddr/'
    
    # Complete URL with the Bitcoin address
    url = f'{base_url}{addr}'
    
    try:
        # Send the GET request
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response content as JSON
            json_data = response.json()
            return json_data
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    tx_id = '5658a925ca3a5528353ae9324263d688c8b5932eac4261dae035bf948deb0f8d'
    transaction_details = fetchTx(tx_id)
    if transaction_details:
        print(transaction_details)
    bitcoin_address = '3AujBhj7bAFgGVb8gYccUDpWcAYYUJ37WY'
    address_details = fetchAddrHist(bitcoin_address)
    if address_details:
        print(address_details)
    