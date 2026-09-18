import subprocess
import os

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out = os.path.abspath("visualizations/period_active_clean.png")

with open("index.html", "r", encoding="utf-8") as f:
    h = f.read()

# 탭을 period 활성 상태로 변경
h = h.replace('<section id="tab_latest" class="tab_pane active">', '<section id="tab_latest" class="tab_pane">')
h = h.replace('<section id="tab_period" class="tab_pane">', '<section id="tab_period" class="tab_pane active">')
h = h.replace('<button class="nav_tab_btn active" data_tab="tab_latest">', '<button class="nav_tab_btn" data_tab="tab_latest">')
h = h.replace('<button class="nav_tab_btn" data_tab="tab_period">', '<button class="nav_tab_btn active" data_tab="tab_period">')

temp_html = os.path.abspath("intermediate_results/period_test_clean.html")
with open(temp_html, "w", encoding="utf-8") as f:
    f.write(h)

file_url = "file:///" + temp_html.replace("\\", "/")
subprocess.run([chrome, "--headless", "--disable-gpu", "--window-size=1440,800", f"--screenshot={out}", file_url])
print("Period active captured:", os.path.exists(out))
