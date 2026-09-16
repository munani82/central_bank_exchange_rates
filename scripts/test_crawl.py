import requests
import urllib3
urllib3.disable_warnings()

headers = {
    'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

urls = [
    "https://www.cbe.org.eg/en/markets/foreign_exchange/cbe_exchange_rates",
    "https://www.cbe.org.eg/en/economic_research/rates/rates_daily.htm",
    "https://www.sbv.gov.vn/webcenter/portal/en/menu/trangchu/tt_cntt/tgnt"
]

for u in urls:
    try:
        r = requests.get(u, headers=headers, verify=False, timeout=15)
        print(f"URL: {u}")
        print(f"상태: {r.status_code}, 크기: {len(r.text)}")
        if "USD" in r.text or "Dollar" in r.text or "dollar" in r.text:
            print("USD 키워드 발견!")
    except Exception as e:
        print(f"URL {u} 에러: {e}")
