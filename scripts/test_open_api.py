import requests
import json

urls = [
    "https://open.er_api.com/v6/latest/USD",
    "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency_api@latest/v1/currencies/usd.json"
]

for u in urls:
    try:
        r = requests.get(u, timeout=10)
        print(f"URL {u} 상태: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            rates = data.get('rates', {}) or data.get('usd', {})
            for c in ['pln', 'vnd', 'egp', 'idr', 'cny', 'PLN', 'VND', 'EGP', 'IDR', 'CNY']:
                if c in rates:
                    print(f"  {c}: {rates[c]}")
    except Exception as e:
        print(f"URL {u} 에러: {e}")
