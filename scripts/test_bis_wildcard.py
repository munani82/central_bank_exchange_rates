import requests
import urllib3
urllib3.disable_warnings()

headers = {'User_Agent': 'Mozilla/5.0'}

for q in ["D.VN.VND..", "D.EG.EGP..", "D..VND..", "D..EGP.."]:
    url = f"https://stats.bis.org/api/v1/data/WS_XRU/{q}?format=csv"
    try:
        r = requests.get(url, headers=headers, verify=False, timeout=10)
        print(f"쿼리 {q}: 상태 {r.status_code}, 바이트: {len(r.text)}")
        if r.status_code == 200:
            lines = r.text.splitlines()
            print(f"라인수: {len(lines)}")
            if len(lines) > 1:
                print(lines[1][:120])
    except Exception as e:
        print(f"에러: {e}")
