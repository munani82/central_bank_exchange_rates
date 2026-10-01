# -*- coding: utf-8 -*-
import re

with open("scratch_cbe-exchange-rates.html", "r", encoding="utf-8") as f:
    c = f.read()

forms = re.findall(r'<form[^>]*action=[\'"]([^\'"]*)[\'"][^>]*>(.*?)</form>', c, re.DOTALL)
print("Forms found:", len(forms))
for act, body in forms:
    print("Action:", act)
    inps = re.findall(r'<input[^>]*name=[\'"]([^\'"]*)[\'"][^>]*>', body)
    print("Inputs:", inps)

# date picker 또는 select 찾기
selects = re.findall(r'<select[^>]*name=[\'"]([^\'"]*)[\'"][^>]*>', c)
print("Selects:", selects)
