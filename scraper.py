import requests
import json
import time
import scraper_blockchaindotcom
import scraper_blockstreaminfo
import scraper_electrumrpc

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

if __name__ == "__main__":
    preprocess_csv()