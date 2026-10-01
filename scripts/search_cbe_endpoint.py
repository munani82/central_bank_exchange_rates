# -*- coding: utf-8 -*-
import re

with open("scratch_foreign-exchange.html", "r", encoding="utf-8") as f:
    text = f.read()

forms = re.findall(r'<form[^>]*action=[\'"]([^\'"]*)[\'"][^>]*>', text)
print("Forms actions:", forms)

for line in text.splitlines():
    lower = line.lower()
    if any(k in lower for k in ["fetch(", "$.ajax", "axios", "getjson", "/api/", "historical-data"]):
        print("Line:", line.strip()[:140])
