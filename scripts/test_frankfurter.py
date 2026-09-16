import requests
import json
import urllib3
urllib3.disable_warnings()

headers = {'User_Agent': 'Mozilla/5.0'}

# Frankfurter currencies test
url = "https://api.frankfurter.app/currencies"
try:
    r = requests.get(url, headers=headers, timeout=10)
    print(f"상태: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print("지원 통화 수:", len(data))
        for c in ['PLN', 'VND', 'EGP', 'IDR', 'CNY']:
            print(f"통화 {c} 지원 여부: {c in data}")
except Exception as e:
    print("에러:", e)
