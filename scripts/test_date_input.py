import subprocess
import os

html_test = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body { background: #060913; color: white; padding: 20px; font-family: sans-serif; }
.box { margin-bottom: 20px; }
input { background: #111827; color: white; border: 1px solid #374151; padding: 10px; font-size: 14px; border-radius: 6px; }
</style>
</head>
<body>
<div class="box">
  <p>1. Default type="date"</p>
  <input type="date" value="2026-01-01">
</div>
<div class="box">
  <p>2. lang="en-CA" type="date" (ISO format YYYY-MM-DD)</p>
  <input type="date" lang="en-CA" value="2026-01-01">
</div>
<div class="box">
  <p>3. Custom styled type="text"</p>
  <input type="text" value="2026-01-01" style="width: 140px; text-align: center;">
</div>
</body>
</html>"""

with open("intermediate_results/test_date.html", "w", encoding="utf-8") as f:
    f.write(html_test)

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out = os.path.abspath("visualizations/date_test_render.png")
test_url = "file:///" + os.path.abspath("intermediate_results/test_date.html").replace("\\", "/")

subprocess.run([chrome, "--headless", "--disable-gpu", "--window-size=600,600", f"--screenshot={out}", test_url])
print("Rendered:", os.path.exists(out))
