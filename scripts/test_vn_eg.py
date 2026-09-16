import requests
import urllib3
urllib3.disable_warnings()

headers = {
    'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# 1. Vietcombank 공식 환율 XML
url_vcb = "https://portal.vietcombank.com.vn/Usercontrols/TVWeb.TyGia/pXML.aspx"
try:
    r = requests.get(url_vcb, headers=headers, verify=False, timeout=10)
    print(f"Vietcombank 상태: {r.status_code}, 크기: {len(r.text)}")
    if r.status_code == 200:
        print(r.text[:300])
except Exception as e:
    print(f"Vietcombank 에러: {e}")

# 2. 이집트 NBE/CBE
url_nbe = "https://www.nbe.com.eg/NBE/E/#/EN/ExchangeRate"
try:
    r = requests.get("https://www.cbe.org.eg/en/markets/foreign_exchange/cbe_exchange_rates", headers=headers, verify=False, timeout=10)
    print(f"CBE 상태: {r.status_code}, 크기: {len(r.text)}")
except Exception as e:
    print(f"CBE 에러: {e}")
