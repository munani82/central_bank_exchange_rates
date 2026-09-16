import requests
import urllib3
urllib3.disable_warnings()

headers = {'User_Agent': 'Mozilla/5.0'}
keys = [
    ("PL", "PLN"),
    ("VN", "VND"),
    ("EG", "EGP"),
    ("ID", "IDR"),
    ("CN", "CNY")
]

for area, curr in keys:
    # D: Daily, M: Monthly
    url = f"https://stats.bis.org/api/v1/data/WS_XRU/D.{area}.{curr}.A?format=csv"
    try:
        r = requests.get(url, headers=headers, verify=False, timeout=10)
        print(f"Daily {area}/{curr}: 상태 {r.status_code}")
        if r.status_code == 200:
            print(f"성공! 라인수: {len(r.text.splitlines())}")
            print(r.text.splitlines()[-1])
        else:
            url_m = f"https://stats.bis.org/api/v1/data/WS_XRU/M.{area}.{curr}.A?format=csv"
            r_m = requests.get(url_m, headers=headers, verify=False, timeout=10)
            print(f"Monthly {area}/{curr}: 상태 {r_m.status_code}")
            if r_m.status_code == 200:
                print(f"Monthly 성공! 라인수: {len(r_m.text.splitlines())}")
                print(r_m.text.splitlines()[-1])
    except Exception as e:
        print(f"에러 {curr}: {e}")
