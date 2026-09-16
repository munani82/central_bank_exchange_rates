import urllib.request
import re

url = "https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_USDKRW&page=1"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    html = urllib.request.urlopen(req).read().decode("cp949")
    dates = re.findall(r'<td class="date">\s*([0-9.]+)\s*</td>', html)
    # class="num" 인 태그들
    nums = re.findall(r'<td class="num">\s*([0-9,.]+)\s*</td>', html)
    print("Naver Finance (하나은행 고시환율 기반) 최신 일별 환율:")
    for d, r in zip(dates[:10], nums[:10]):
        print(f"{d.strip()}: {r.strip()}")
except Exception as e:
    print(f"Error: {e}")
