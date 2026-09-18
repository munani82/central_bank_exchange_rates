import requests
import re
import urllib3

urllib3.disable_warnings()

url = "https://www.kebhana.com/cms/rate/index.do?target=wpfxd651_01i"
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, verify=False)
inputs = re.findall(r'<input[^>]+>', r.text)
for inp in inputs:
    print(inp)
