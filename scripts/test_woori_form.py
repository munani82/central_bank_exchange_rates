import requests
import re

url = "https://spot.wooribank.com/pot/Dream?withyou=FXXRT0011"
data = {
    "SELECT_DATE": "2026.09.18",
    "CUR_CD": "USD",
    "NTC_DIS": "B"
}
headers = {"User-Agent": "Mozilla/5.0"}
r = requests.post(url, data=data, headers=headers)

# 매매기준율 찾기
trs = re.findall(r'<tr>(.*?)</tr>', r.text, re.DOTALL)
for tr in trs:
    tds = [re.sub(r'<[^>]+>', '', td).strip() for td in re.findall(r'<td.*?>(.*?)</td>', tr, re.DOTALL)]
    if len(tds) >= 3:
        print(tds)
