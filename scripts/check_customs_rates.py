# -*- coding: utf-8 -*-
import requests
import urllib3
import re

urllib3.disable_warnings()

headers = {"User-Agent": "Mozilla/5.0"}
r = requests.get("https://www.customs.gov.vn", headers=headers, timeout=12, verify=False)
links = re.findall(r'href=[\'"]([^\'"]+)[\'"]', r.text)
found = set()
for l in links:
    if any(k in l.lower() for k in ["ty-gia", "ty_gia", "exchange", "currency"]):
        found.add(l)
for f in found:
    print("Customs rate link:", f)
