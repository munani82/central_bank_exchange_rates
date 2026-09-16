import requests
import json
import urllib.request

headers = {
    'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print("1. 폴란드 NBP 테스트 시작")
try:
    url_nbp = "https://api.nbp.pl/api/exchangerates/rates/a/usd/last/10/?format=json"
    req = urllib.request.Request(url_nbp, headers={'User_Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf_8'))
        print(f"NBP 성공: 최근 {len(data.get('rates', []))} 건 수집, 최신환율: {data['rates'][-1]}")
except Exception as e:
    print(f"NBP 에러: {e}")

print("2. 중국 인민은행/SAFE/CFETS 테스트 시작")
try:
    url_cfets = "https://www.chinamoney.com.cn/ags/ms/cm_u_bk_ccpr/CcprHisNew?startDate=2026_01_01&endDate=2026_09_15&currency=USD/CNY"
    req = urllib.request.Request(url_cfets, headers={'User_Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        res = json.loads(resp.read().decode('utf_8'))
        print(f"CFETS 성공: {res.keys()}")
except Exception as e:
    print(f"CFETS 에러: {e}")

print("3. 이집트 CBE 테스트 시작")
try:
    url_cbe = "https://www.cbe.org.eg/en/economic_research/rates/rates_daily.htm"
    req = urllib.request.Request(url_cbe, headers={'User_Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf_8', errors='ignore')
        print(f"CBE 응답 크기: {len(html)}")
except Exception as e:
    print(f"CBE 에러: {e}")

print("4. 인도네시아 BI 테스트 시작")
try:
    url_bi = "https://www.bi.go.id/id/statistik/informasi_kurs/jisdor/Default.aspx"
    req = urllib.request.Request(url_bi, headers={'User_Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf_8', errors='ignore')
        print(f"BI 응답 크기: {len(html)}")
except Exception as e:
    print(f"BI 에러: {e}")

print("5. 베트남 SBV 테스트 시작")
try:
    url_sbv = "https://sbv.gov.vn/webcenter/portal/vi/menu/trangchu/tt_cntt/tgnt"
    req = urllib.request.Request(url_sbv, headers={'User_Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf_8', errors='ignore')
        print(f"SBV 응답 크기: {len(html)}")
except Exception as e:
    print(f"SBV 에러: {e}")
