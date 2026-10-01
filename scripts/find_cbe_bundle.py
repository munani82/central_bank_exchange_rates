# -*- coding: utf-8 -*-
import re

with open("scratch_foreign-exchange.html", "r", encoding="utf-8") as f:
    c = f.read()

srcs = re.findall(r'<script[^>]*src=[\'"]([^\'"]+)[\'"]', c)
for s in srcs:
    print("Script src:", s)
