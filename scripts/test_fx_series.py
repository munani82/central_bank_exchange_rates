import requests
import json
import urllib3
urllib3.disable_warnings()

headers = {
    'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

symbols = ['USDPLN=X', 'USDVND=X', 'USDEGP=X', 'USDIDR=X', 'USDCNY=X']

for sym in symbols:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=5d"
    try:
        r = requests.get(url, headers=headers, verify=False, timeout=10)
        print(f"심볼 {sym}: 상태 {r.status_code}")
        if r.status_code == 200:
            res = r.json()
            result = res['chart']['result'][0]
            timestamps = result['timestamp']
            closes = result['indicators']['quote'][0]['close']
            print(f"최근 데이터수: {len(timestamps)}, 최신 종가: {closes[-1]}")
    except Exception as e:
        print(f"심볼 {sym} 에러: {e}")
