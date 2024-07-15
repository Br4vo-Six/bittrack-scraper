import requests
from bs4 import BeautifulSoup

def fetch_proxy():
    d = requests.get("https://free-proxy-list.net/")
    soup = BeautifulSoup(d.content, 'html.parser')
    td_elements = soup.select('.fpl-list .table tbody tr td')
    ips = []
    ports = []
    for j in range(0, len(td_elements), 8):
        ips.append(td_elements[j].text.strip())
        ports.append(td_elements[j + 1].text.strip())
    with open("proxies_list.txt", "a") as myfile:
        for ip, port in zip(ips, ports):
            proxy = f"{ip}:{port}"
            print(proxy, file=myfile)

def load_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = file.readlines()
    proxies = [proxy.strip() for proxy in proxies]
    return proxies

if __name__ == "__main__":
    fetch_proxy()