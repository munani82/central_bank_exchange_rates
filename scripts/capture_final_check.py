import subprocess
import os

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out = os.path.abspath("visualizations/period_final_check.png")

# index.html 직접 테스트 (상대 경로로 style.css 로드)
file_url = "file:///" + os.path.abspath("index.html").replace("\\", "/")
subprocess.run([chrome, "--headless", "--disable-gpu", "--window-size=1440,800", f"--screenshot={out}", file_url])
print("Final check rendered:", os.path.exists(out))
