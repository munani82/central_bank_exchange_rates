import subprocess
import os
import json

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out = os.path.abspath("visualizations/svg_flags_final.png")

# data/latest_rates.json 직접 인라인 삽입하여 완벽한 시각적 프리뷰 생성
with open("data/latest_rates.json", "r", encoding="utf-8") as f:
    latest_data = f.read()

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 인라인 프리로드 스크립트 추가
preload_script = f"""
<script>
window._latestCache = {latest_data};
</script>
"""
html = html.replace("</head>", preload_script + "</head>")

preview_path = os.path.abspath("intermediate_results/flags_preview.html")
with open(preview_path, "w", encoding="utf-8") as f:
    f.write(html)

test_url = "file:///" + preview_path.replace("\\", "/")
subprocess.run([chrome, "--headless", "--disable-gpu", "--window-size=1440,900", f"--screenshot={out}", test_url])
print("Final flags rendered:", os.path.exists(out))
