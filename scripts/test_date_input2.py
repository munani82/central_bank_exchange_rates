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

/* 시도: 웹킷 섀도우 돔 제어 */
.hide-parens::-webkit-datetime-edit-fields-wrapper {
  display: flex;
}
</style>
</head>
<body>
<div class="box">
  <p>A. type="text" with calendar icon and pattern</p>
  <div style="position: relative; display: inline-block;">
    <input type="text" id="t1" value="2026-01-01" maxlength="10" placeholder="YYYY-MM-DD" style="width: 130px; text-align: center; font-family: monospace; font-size: 14px; padding-right: 32px;">
    <span style="position: absolute; right: 10px; top: 50%; transform: translateY(-50%); opacity: 0.6; cursor: pointer;">📅</span>
  </div>
</div>
</body>
</html>"""

with open("intermediate_results/test_date2.html", "w", encoding="utf-8") as f:
    f.write(html_test)

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out = os.path.abspath("visualizations/date_test_render2.png")
test_url = "file:///" + os.path.abspath("intermediate_results/test_date2.html").replace("\\", "/")

subprocess.run([chrome, "--headless", "--disable-gpu", "--window-size=600,400", f"--screenshot={out}", test_url])
print("Rendered 2:", os.path.exists(out))
