import requests
import re
import urllib3

urllib3.disable_warnings()

url = "https://www.kebhana.com/cms/rate/index.do?target=wpfxd651_01i"
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, verify=False)
scripts = re.findall(r'<script[^>]+src=[\'"]([^\'"]+)[\'"]', r.text)

for s in scripts:
    if not s.startswith("http"):
        s = "https://www.kebhana.com" + s
    try:
        res = requests.get(s, headers={"User-Agent": "Mozilla/5.0"}, verify=False, timeout=5)
        matches = re.findall(r'wpfxd651[a-zA-Z0-9_]*', res.text)
        if matches:
            print(s, set(matches))
            # 파라미터 찾기
            params = re.findall(r'(?:tmpInqStrDt|inqDat|curCd|pbldDvCd|inqDt)[a-zA-Z0-9_]*', res.text)
            print("  params:", set(params))
    except Exception:
        pass
