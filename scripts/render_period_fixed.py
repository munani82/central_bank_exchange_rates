import subprocess
import os

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out = os.path.abspath("visualizations/period_fixed_preview.png")

with open("index.html", "r", encoding="utf-8") as f:
    h = f.read()

h = h.replace('<section id="tab_latest" class="tab_pane active">', '<section id="tab_latest" class="tab_pane">')
h = h.replace('<section id="tab_period" class="tab_pane">', '<section id="tab_period" class="tab_pane active">')

with open("temp_preview.html", "w", encoding="utf-8") as f:
    f.write(h)

test_url = "file:///" + os.path.abspath("temp_preview.html").replace("\\", "/")
subprocess.run([chrome, "--headless", "--disable-gpu", "--window-size=1440,700", f"--screenshot={out}", test_url])

if os.path.exists("temp_preview.html"):
    os.remove("temp_preview.html")

print("Rendered successfully:", os.path.exists(out))
