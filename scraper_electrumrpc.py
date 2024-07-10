import requests
import json

def fetchTx(tx_id, rpc_url, rpc_user, rpc_password):
    # Create the JSON-RPC payload to get transaction details
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "gettransaction",
        "params": [tx_id],
        "id": 1
    })

    # Send the request with basic authentication
    res_temp = requests.post(rpc_url, headers={'content-type': 'application/json'}, data=payload, auth=(rpc_user, rpc_password))
    
    transaction_encrypted = res_temp.json()
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "deserialize",
        "params": [transaction_encrypted['result']],
        "id": 1
    })

    response = requests.post(rpc_url, headers={'content-type': 'application/json'}, data=payload, auth=(rpc_user, rpc_password))

    return response.json()

def fetchAddrHist(addr, rpc_url, rpc_user, rpc_password):
    # Create the JSON-RPC payload to get the history of any wallet address
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "getaddresshistory",
        "params": [addr],
        "id": 1
    })

    # Send the request with basic authentication
    response = requests.post(rpc_url, headers={'content-type': 'application/json'}, data=payload, auth=(rpc_user, rpc_password))

    return response.json()

if __name__ == "__main__":
    url = "http://127.0.0.1:7777"
    rpc_user = 'user'
    rpc_password = 'Empress_3'
    tx_id = '5658a925ca3a5528353ae9324263d688c8b5932eac4261dae035bf948deb0f8d'
    res = fetchTx(tx_id, url, rpc_user, rpc_password)
    print(res)  
    addr = '3AujBhj7bAFgGVb8gYccUDpWcAYYUJ37WY'
    res = fetchAddrHist(addr, url, rpc_user, rpc_password)
    print(res)  