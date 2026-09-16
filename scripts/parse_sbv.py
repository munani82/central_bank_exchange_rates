import requests
import re
import urllib3
import os
urllib3.disable_warnings()

headers = {
    'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

url = "https://www.sbv.gov.vn/webcenter/portal/en/menu/trangchu/tt_cntt/tgnt"
r = requests.get(url, headers=headers, verify=False, timeout=20)
html = r.text

clean_text = re.sub(r'<[^>]+>', ' ', html)
clean_text = ' '.join(clean_text.split())

matches = [m.start() for m in re.finditer(r'USD', clean_text, re.IGNORECASE)]

out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "intermediate_results")
out_path = os.path.join(out_dir, "sbv_snippet.txt")

with open(out_path, "w", encoding="utf_8_sig") as f:
    f.write(f"HTML 전체 길이: {len(html)}\n")
    f.write(f"USD 발견 횟수: {len(matches)}\n")
    for idx in matches:
        snippet = clean_text[max(0, idx - 50): min(len(clean_text), idx + 150)]
        f.write("===\n" + snippet + "\n")

print("SBV 스니펫 저장 완료")
