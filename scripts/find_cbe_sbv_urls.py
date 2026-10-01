# -*- coding: utf-8 -*-
import requests
import urllib3
import re

urllib3.disable_warnings()
s = requests.Session()
s.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

def find_cbe():
    print("=== CBE 링크 탐색 ===")
    try:
        r = s.get("https://www.cbe.org.eg/en", verify=False, timeout=15)
        print("CBE Home:", r.status_code)
        links = re.findall(r'href=[\'"]([^\'"]+)[\'"]', r.text)
        found = set()
        for l in links:
            lower = l.lower()
            if any(k in lower for k in ["exchange", "rate", "statistic"]):
                found.add(l)
        for f in sorted(found):
            print(" CBE Link:", f)
    except Exception as e:
        print("CBE Error:", e)

def find_sbv():
    print("\n=== SBV 링크 탐색 ===")
    try:
        r = s.get("https://www.sbv.gov.vn", verify=False, timeout=15)
        print("SBV Home:", r.status_code)
        links = re.findall(r'href=[\'"]([^\'"]+)[\'"]', r.text)
        found = set()
        for l in links:
            lower = l.lower()
            if any(k in lower for k in ["ty-gia", "ty_gia", "exchange", "tgnt"]):
                found.add(l)
        for f in sorted(found):
            print(" SBV Link:", f)
    except Exception as e:
        print("SBV Error:", e)

if __name__ == "__main__":
    find_cbe()
    find_sbv()
