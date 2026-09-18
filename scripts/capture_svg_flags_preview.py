import subprocess
import os

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out = os.path.abspath("visualizations/svg_flags_rendered.png")

# index.html 직접 렌더링
test_url = "file:///" + os.path.abspath("index.html").replace("\\", "/")
subprocess.run([chrome, "--headless", "--disable-gpu", "--window-size=1440,850", "--virtual-time-budget=4000", f"--screenshot={out}", test_url])
print("Flags preview rendered:", os.path.exists(out))
