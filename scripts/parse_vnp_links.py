# -*- coding: utf-8 -*-
import re

with open("scratch_vnp_search.html", "r", encoding="utf-8") as f:
    c = f.read()

links = re.findall(r'href=[\'"]([^\'"]+)[\'"]', c)
vnp_links = [l for l in links if "vietnamplus.vn" in l or l.startswith("/")]
print("Links count:", len(vnp_links))
for l in vnp_links[:20]:
    print(" ", l)
