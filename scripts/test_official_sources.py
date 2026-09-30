import requests
import json
import urllib3
urllib3.disable_warnings()

H = chr(45)
headers = {
    'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,application/json,*/*;q=0.8',
    'Accept_Language': 'ko,en_US;q=0.9,en;q=0.8'
}

print("=== 1. 중국 CFETS / PBOC 테스트 ===")
cfets_urls = [
    f"https://www.chinamoney.com.cn/ags/ms/cm{H}u{H}bk{H}ccpr/CcprHisEng",
    f"http://www.chinamoney.com.cn/r/cms/www/chinamoney/html/ccpr/ccpr_en.html",
    f"https://www.safe.gov.cn/safe/rmbhlzjj/index.html"
]
for u in cfets_urls:
    try:
        r = requests.get(u, headers=headers, verify=False, timeout=10)
        print(f"[CFETS] {u[:60]} -> {r.status_code}, len: {len(r.text)}")
    except Exception as e:
        print(f"[CFETS 예외] {e}")

print("\n=== 2. 베트남 SBV 테스트 ===")
sbv_urls = [
    "https://www.sbv.gov.vn/webcenter/portal/vi/menu/trangchu/tt_cntt/tgnt",
    "https://www.sbv.gov.vn/webcenter/portal/en/menu/trangchu/tt_cntt/tgnt"
]
for u in sbv_urls:
    try:
        r = requests.get(u, headers=headers, verify=False, timeout=10)
        print(f"[SBV] {u[:60]} -> {r.status_code}, len: {len(r.text)}")
        if "USD" in r.text:
            print("  SBV USD 키워드 포함 확인")
    except Exception as e:
        print(f"[SBV 예외] {e}")

print("\n=== 3. 인도네시아 BI JISDOR 테스트 ===")
bi_urls = [
    f"https://www.bi.go.id/biweb/api/KursJISDOR",
    f"https://www.bi.go.id/en/statistik/informasi{H}kurs/jisdor/Default.aspx",
    f"https://www.bi.go.id/id/statistik/informasi{H}kurs/jisdor/Default.aspx"
]
for u in bi_urls:
    try:
        r = requests.get(u, headers=headers, verify=False, timeout=10)
        print(f"[BI] {u[:60]} -> {r.status_code}, len: {len(r.text)}")
    except Exception as e:
        print(f"[BI 예외] {e}")

print("\n=== 4. 이집트 CBE 테스트 ===")
cbe_urls = [
    f"https://www.cbe.org.eg/en/economic{H}research/statistics/exchange{H}rates",
    f"https://www.cbe.org.eg/en/markets/foreign{H}exchange/cbe{H}exchange{H}rates"
]
for u in cbe_urls:
    try:
        r = requests.get(u, headers=headers, verify=False, timeout=10)
        print(f"[CBE] {u[:60]} -> {r.status_code}, len: {len(r.text)}")
    except Exception as e:
        print(f"[CBE 예외] {e}")
