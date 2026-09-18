import subprocess
import os

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out = os.path.abspath("visualizations/period_tab_rendered.png")

# index.html의 tab_period를 기본 active로 임시 테스트하거나 클릭
# intermediate_results/test_period_view.html 생성
with open("index.html", "r", encoding="utf-8") as f:
    h = f.read()

# 탭을 period 활성 상태로 변경한 임시 뷰 생성
h_period = h.replace('class="tab_pane active" id="tab_latest"', 'class="tab_pane" id="tab_latest"')
h_period = h_period.replace('<section id="tab_latest" class="tab_pane active">', '<section id="tab_latest" class="tab_pane">')
h_period = h_period.replace('<section id="tab_period" class="tab_pane">', '<section id="tab_period" class="tab_pane active">')
h_period = h_period.replace('data_tab="tab_latest"', 'data_tab="tab_latest"')

temp_html_path = os.path.abspath("intermediate_results/period_preview.html")
with open(temp_html_path, "w", encoding="utf-8") as f:
    f.write(h_period)

file_url = "file:///" + temp_html_path.replace("\\", "/")
subprocess.run([chrome, "--headless", "--disable-gpu", "--window-size=1440,700", f"--screenshot={out}", file_url])
print("Preview rendered:", os.path.exists(out))
