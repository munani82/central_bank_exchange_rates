import requests
import re

url = "https://www.kebhana.com/cms/rate/index.do?target=wpfxd651_01i"
headers = {"User-Agent": "Mozilla/5.0"}
try:
    r = requests.get(url, headers=headers, timeout=10)
    print("status:", r.status_code)
    # form action 찾기
    actions = re.findall(r'<form[^>]*action=[\'"]([^\'"]+)[\'"]', r.text, re.I)
    print("actions:", actions)
    # url pattern
    urls = re.findall(r'(/cms/rate/[^"\'\s>]+)', r.text)
    print("found cms rate urls:", set(urls[:15]))
except Exception as e:
    print("error:", e)
