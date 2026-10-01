# -*- coding: utf-8 -*-
import requests
import urllib3
import re

urllib3.disable_warnings()

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
try:
    with open("scratch_customs.html", "r", encoding="utf-8") as f:
        html = f.read()
except Exception:
    r = requests.get("https://www.customs.gov.vn", headers=headers, timeout=12, verify=False)
    html = r.text

matches = re.findall(r'<a[^>]*href=[\'"]([^\'"]+)[\'"][^>]*>(.*?)</a>', html, re.DOTALL)
print(f"Total links: {len(matches)}")
for link, text in matches:
    clean_t = re.sub(r'<[^>]+>', ' ', text).strip()
    clean_t_lower = clean_t.lower()
    if any(k in clean_t_lower for k in ["tỷ giá", "ty gia", "exchange", "plaza", "tra cứu", "ngoại tệ"]):
        print(f"Match: {link} -> {clean_t}")
