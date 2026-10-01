# -*- coding: utf-8 -*-
import requests
import urllib3
import re
import json

urllib3.disable_warnings()
s = requests.Session()
s.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

def test():
    urls = [
        "/en/economic-research/statistics/cbe-exchange-rates",
        "/en/economic-research/statistics/exchange-rates",
        "/en/markets/foreign-exchange"
    ]
    for p in urls:
        url = "https://www.cbe.org.eg" + p
        try:
            r = s.get(url, verify=False, timeout=15)
            print(p, "Status:", r.status_code, "Len:", len(r.text))
            with open(f"scratch_{p.split('/')[-1]}.html", "w", encoding="utf-8") as f:
                f.write(r.text)
            
            # API 호출 URL이나 JSON/Excel 다운로드 링크 찾기
            excel_links = re.findall(r'href=[\'"]([^\'"]+\.(?:xlsx|xls|csv))[\'"]', r.text, re.IGNORECASE)
            print("  Excel links:", excel_links)
            api_links = re.findall(r'[\'"](/api/[^\'"]+)[\'"]', r.text)
            print("  API links:", set(api_links[:10]))
        except Exception as e:
            print(p, "Error:", e)

if __name__ == "__main__":
    test()
