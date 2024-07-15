import requests
import json
import time
import scraper_blockchaindotcom
import scraper_blockstreaminfo
import scraper_electrumrpc
import fetch_proxies
import random
import concurrent.futures

import pandas as pd
import os
from dotenv import load_dotenv

def preprocess_csv():
    load_dotenv()
    file_path = os.path.join(os.getenv('OUTPUT_DIR'), os.getenv('TXS_LIST'))
    dataset = pd.read_csv(file_path)
    if 'scraped' not in dataset.columns:
        dataset['scraped'] = False
    if 'proxyAddr' not in dataset.columns:
        dataset['proxyAddr'] = ''
    dataset.to_csv(file_path, index=False)
    return dataset

def make_request(proxies):
    source = os.getenv('SOURCE')
    tx_id = '5658a925ca3a5528353ae9324263d688c8b5932eac4261dae035bf948deb0f8d'
    while True:
        proxy = random.choice(proxies)
        proxy_dict = {
            'http': f'http://{proxy}',
        }
        try:
            if source == 'BLOCKCHAINDOTCOM':
                res_json = scraper_blockchaindotcom.fetchTx(tx_id, proxy_dict)
            elif source == 'ELECTRUMRPC':
                res_json = scraper_electrumrpc.fetchTx(tx_id, os.getenv('RPC_URL'), os.getenv('RPC_USER'), os.getenv('RPC_PASSWORD'))
            elif source == 'BLOCKSTREAM':
                res_json = scraper_blockchaindotcom.fetchTx(tx_id, proxy_dict)
            if res_json:
                print(f"Request success using proxy: {proxy}")
                print(res_json)
                print("-----------------------------")
                return
            else:
                print(f"Request failed using proxy: {proxy}") 
        except requests.exceptions.RequestException as e:
            print(f"Request failed using proxy: {proxy}")
            print(e)

if __name__ == "__main__":
    load_dotenv()
    # df = preprocess_csv()
    workers = int(os.getenv('NUM_WORKER'))
    proxies = fetch_proxies.load_proxies(os.path.join(os.getcwd(), 'proxies_list.txt'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(make_request, proxies) for _ in range(workers)]
        concurrent.futures.wait(futures)
    
    