import requests
import urllib3
urllib3.disable_warnings()

headers = {
    'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# BIS API 테스트 (D: 일별, 월별 등)
# 통화: PLN, VND, EGP, IDR, CNY
currencies = ['PLN', 'VND', 'EGP', 'IDR', 'CNY']
for c in currencies:
    url = f"https://stats.bis.org/api/v1/data/WS_XRU/D.{c}.USD.A?format=csv"
    try:
        r = requests.get(url, headers=headers, verify=False, timeout=15)
        print(f"BIS 통화 {c}: 상태 {r.status_code}, 데이터 길이: {len(r.text)}")
        if r.status_code == 200:
            lines = r.text.strip().split('\n')
            print(f"헤더: {lines[0][:80]}")
            if len(lines) > 1:
                print(f"최근 데이터: {lines[-1]}")
    except Exception as e:
        print(f"BIS 통화 {c} 에러: {e}")
