import requests
import urllib3
urllib3.disable_warnings()

headers = {
    'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json'
}

url_nbp = "https://api.nbp.pl/api/exchangerates/rates/a/usd/last/10/?format=json"
r = requests.get(url_nbp, headers=headers, verify=False, timeout=10)
print(f"NBP 상태코드: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print("NBP 최신 5건:")
    for rate in data.get('rates', [])[-5:]:
        print(rate)
