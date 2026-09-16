import requests
import urllib3
urllib3.disable_warnings()

headers = {'User_Agent': 'Mozilla/5.0'}

# IMF Representative Exchange Rates TSV 테스트
# 매월 또는 일별
url_imf = "https://www.imf.org/external/np/fin/data/rms_mth.aspx?SelectDate=2026_09_01&reportType=REP&tsvflag=Y"
try:
    r = requests.get(url_imf, headers=headers, verify=False, timeout=10)
    print(f"IMF 상태: {r.status_code}, 길이: {len(r.text)}")
    lines = [line for line in r.text.splitlines() if line.strip()]
    print("IMF 처음 15줄:")
    for l in lines[:15]:
        print(l)
except Exception as e:
    print(f"IMF 에러: {e}")
