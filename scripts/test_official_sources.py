import requests
import re
import urllib3

urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# 1. 베트남 SBV
try:
    r = requests.get('https://www.sbv.gov.vn', headers=headers, verify=False, timeout=10)
    print(f"SBV 메인 상태: {r.status_code}")
    # 환율 관련 링크
    links = [l for l in re.findall(r'href=[\'"]([^\'"]+)[\'"]', r.text) if 'tgnt' in l or 'exchange' in l or 'rate' in l]
    print(f"SBV 환율 링크: {links[:5]}")
except Exception as e:
    print(f"SBV 에러: {e}")

# 2. 인도네시아 BI JISDOR
try:
    r = requests.get('https://www.bi.go.id/id/statistik/informasi-kurs/jisdor/Default.aspx', headers=headers, verify=False, timeout=10)
    print(f"BI JISDOR 웹 상태: {r.status_code}")
    if r.status_code == 200:
        # JISDOR 테이블
        trs = re.findall(r'<tr[^>]*>(.*?)</tr>', r.text, re.DOTALL)
        print(f"BI JISDOR trs: {len(trs)}")
except Exception as e:
    print(f"BI JISDOR 에러: {e}")

# 3. 이집트 CBE
try:
    r = requests.get('https://www.cbe.org.eg/en/markets/foreign_exchange/cbe_exchange_rates', headers=headers, verify=False, timeout=10)
    print(f"CBE 상태: {r.status_code}")
except Exception as e:
    print(f"CBE 에러: {e}")
