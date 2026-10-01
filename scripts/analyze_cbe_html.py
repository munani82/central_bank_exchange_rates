# -*- coding: utf-8 -*-
import re

with open("scratch_cbe-exchange-rates.html", "r", encoding="utf-8") as f:
    c = f.read()

print("HTML length:", len(c))
tables = re.findall(r'<table[^>]*>(.*?)</table>', c, re.DOTALL)
print("Tables count:", len(tables))

iframes = re.findall(r'<iframe[^>]*src=[\'"]([^\'"]+)[\'"]', c)
print("Iframes:", iframes)

# 환율 데이터가 있는지 확인
matches = re.findall(r'(\d+\.\d{2,4})', c)
print("Numeric values in page count:", len(matches))
if matches:
    print("Sample numbers:", matches[:10])
