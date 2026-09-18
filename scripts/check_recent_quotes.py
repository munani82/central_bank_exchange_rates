import urllib.request
import re

url = "https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_USDKRW&page=1"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req).read().decode("cp949")

dates = re.findall(r'<td class="date">\s*([0-9.]+)\s*</td>', html)
nums = re.findall(r'<td class="num">\s*([0-9,.]+)\s*</td>', html)

for d, n in zip(dates[:10], nums[:10]):
    print(d, n)
