import requests
import json
import time
import scraper_blockchaindotcom
import scraper_blockstreaminfo
import scraper_electrumrpc
import scraper_blockcypher
import fetch_proxies
import random
import concurrent.futures

import pandas as pd
import os
from dotenv import load_dotenv

import numpy as np

def preprocess_csv():
    load_dotenv()
    file_path = os.path.join(os.getenv('OUTPUT_DIR'), os.getenv('TXS_LIST'))
    dataset = pd.read_csv(file_path)
    if 'scraped' not in dataset.columns:
        dataset['scraped'] = False
    if 'proxyAddr' not in dataset.columns:
        dataset['proxyAddr'] = ''
    if 'tried' not in dataset.columns:
        dataset['tried'] = False
    if 'source' not in dataset.columns:
        dataset['source'] = ''
    if 'last_updated' not in dataset.columns:
        dataset['last_updated'] = None
    dataset.to_csv(file_path, index=False)
    return dataset

def reset_csv():
    load_dotenv()
    file_path = os.path.join(os.getenv('OUTPUT_DIR'), os.getenv('TXS_LIST'))
    dataset = pd.read_csv(file_path)
    if 'scraped' in dataset.columns:
        dataset['scraped'] = False
    if 'proxyAddr' in dataset.columns:
        dataset['proxyAddr'] = ''
    if 'tried' in dataset.columns:
        dataset['tried'] = False
    if 'source' in dataset.columns:
        dataset['source'] = ''
    if 'last_updated' in dataset.columns:
        dataset['last_updated'] = None
    dataset.to_csv(file_path, index=False)
    return dataset

def make_request_randomized(tx_id, tx_hash, proxies):
    source = os.getenv('SOURCE')
    tries = 0
    while True:
        if tries > int(os.getenv('MAX_TRIES')):
            return {'tx_id': tx_id, 'tx_hash': tx_hash, 'scraped': False, 'proxyAddr': '', 'res': {}, 'source': source}
        proxy = random.choice(proxies)
        proxy_dict = {
            'http': f'http://{proxy}',
        }
        try:
            if source == 'BLOCKCHAINDOTCOM':
                res_json = scraper_blockchaindotcom.fetchTx(tx_hash, proxy_dict)
            elif source == 'ELECTRUMRPC':
                res_json = scraper_electrumrpc.fetchTx(tx_hash, os.getenv('RPC_URL'), os.getenv('RPC_USER'), os.getenv('RPC_PASSWORD'))
            elif source == 'BLOCKSTREAM':
                res_json = scraper_blockstreaminfo.fetchTx(tx_hash, proxy_dict)
            elif source == 'BLOCKCYPHER':
                res_json = scraper_blockcypher.fetchTx(tx_hash, proxy_dict)
            if res_json:
                print(f"{tx_id} - Request success using proxy: {proxy}")
                return {'tx_id': tx_id, 'tx_hash': tx_hash,'scraped': True, 'proxyAddr': proxy, 'res': res_json, 'source': source}
            else:
                print(f"{tx_id} - Request failed using proxy: {proxy}") 
                tries += 1
        except requests.exceptions.RequestException as e:
            print(f"{tx_id} - Request failed using proxy: {proxy}")
            print(e)
            tries += 1

def make_request(tx_id, tx_hash, proxy):
    source = os.getenv('SOURCE')
    tries = 0
    while True:
        if tries > int(os.getenv('MAX_TRIES')):
            return {'tx_id': tx_id, 'tx_hash': tx_hash, 'scraped': False, 'proxyAddr': '', 'res': {}, 'source': source}
        
        if proxy:
            proxy_dict = {
                'http': f'http://{proxy}',
            }
        else:
            proxy_dict = None
        try:
            if source == 'BLOCKCHAINDOTCOM':
                res_json = scraper_blockchaindotcom.fetchTx(tx_hash, proxy_dict)
            elif source == 'ELECTRUMRPC':
                res_json = scraper_electrumrpc.fetchTx(tx_hash, os.getenv('RPC_URL'), os.getenv('RPC_USER'), os.getenv('RPC_PASSWORD'))
            elif source == 'BLOCKSTREAM':
                res_json = scraper_blockstreaminfo.fetchTx(tx_hash, proxy_dict)
            elif source == 'BLOCKCYPHER':
                res_json = scraper_blockcypher.fetchTx(tx_hash, proxy_dict)
            if res_json:
                print(f"{tx_id} - Request success using proxy: {proxy}")
                return {'tx_id': tx_id, 'tx_hash': tx_hash,'scraped': True, 'proxyAddr': proxy, 'res': res_json, 'source': source}
            else:
                print(f"{tx_id} - Request failed using proxy: {proxy}") 
                tries += 1
        except requests.exceptions.RequestException as e:
            print(f"{tx_id} - Request failed using proxy: {proxy}")
            print(e)
            tries += 1

def divide_array(l, m, n=0):
    subarrays = [l[i:i+m] for i in range(0, len(l), m)]
    
    if n > 0:
        subsubarrays = [[subarray[j:j+n] for j in range(0, len(subarray), n)] for subarray in subarrays]
        return subsubarrays
    else:
        return subarrays

if __name__ == "__main__":
    load_dotenv()
    # reset_csv()
    df = preprocess_csv()
    workers = int(os.getenv('NUM_WORKER'))
    proxies = fetch_proxies.load_proxies(os.path.join(os.getcwd(), 'proxies_list.txt'))
    scraping_scheme = os.getenv('SCRAPING_SCHEME').lower()
    if scraping_scheme == 'randomized':
        for i in range(int(os.getenv('MAX_EPOCH')/workers)):
            results = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                df_chunks = df[df['tried'] == False].head(workers)
                futures = [executor.submit(make_request_randomized, int(df_chunks.iloc[i]['txId']), df_chunks.iloc[i]['transaction'], proxies) for i in range(workers)]
                for future in concurrent.futures.as_completed(futures):
                    filename = f"{future.result()['tx_hash']}_{future.result()['source']}.json"
                    filepath = os.path.join(os.getenv('OUTPUT_DIR'), filename)
                    with open(filepath, 'w') as json_file:
                        json.dump(future.result(), json_file)
                    results.append(future.result())
                    
            csv_file = os.path.join(os.getenv('OUTPUT_DIR'), os.getenv('TXS_LIST'))
            for res in results:
                df.loc[df['txId'] == res['tx_id'], 'scraped'] = res['scraped']
                df.loc[df['txId'] == res['tx_id'], 'proxyAddr'] = res['proxyAddr']
                df.loc[df['txId'] == res['tx_id'], 'tried'] = True
                df.loc[df['txId'] == res['tx_id'], 'source'] = res['source']
                df.loc[df['txId'] == res['tx_id'], 'last_updated'] = time.time()
            df.to_csv(csv_file, index=False)
    elif scraping_scheme == 'max_rate':
        start_proxy = int(os.getenv('PROXY_START'))
        api_rate = int(os.getenv('API_RATE'))
        idx = int(os.getenv('DATA_START'))
        max_epoch = int(os.getenv('MAX_EPOCH'))
        proxies = proxies[start_proxy:max_epoch//api_rate]
        df = df[df['tried'] == False].iloc[idx:idx + max_epoch]
        df_index = df['txId'].values
        df_index = divide_array(df_index, api_rate, workers)
        w = 0
        for proxy_reqs in df_index:
            sel_proxy = proxies[w]
            for chunk in proxy_reqs:
                results = []
                print("DF_INDEX", df_index)
                print("CHUNK", chunk)
                with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                    futures = [executor.submit(make_request, int(chunk[i]), df.loc[df['txId'] == chunk[i], 'transaction'].values[0],None) for i in range(workers)]
                    for future in concurrent.futures.as_completed(futures):
                        filename = f"{future.result()['tx_hash']}_{future.result()['source']}.json"
                        filepath = os.path.join(os.getenv('OUTPUT_DIR'), filename)
                        with open(filepath, 'w') as json_file:
                            json.dump(future.result(), json_file)
                        results.append(future.result())
                
                csv_file = os.path.join(os.getenv('OUTPUT_DIR'), os.getenv('TXS_LIST'))
                for res in results:
                    df.loc[df['txId'] == res['tx_id'], 'scraped'] = res['scraped']
                    df.loc[df['txId'] == res['tx_id'], 'proxyAddr'] = res['proxyAddr']
                    df.loc[df['txId'] == res['tx_id'], 'tried'] = True
                    df.loc[df['txId'] == res['tx_id'], 'source'] = res['source']
                    df.loc[df['txId'] == res['tx_id'], 'last_updated'] = time.time()
                df.to_csv(csv_file, index=False)
            w += 1
    else:
        print('No scraping scheme supplied')