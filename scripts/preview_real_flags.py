import subprocess
import os

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out = os.path.abspath("visualizations/official_flags_rendered.png")

with open("data/latest_rates.json", "r", encoding="utf-8") as f:
    latest_data = f.read()

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

preload_script = f"""
<script>
window._latestCache = {latest_data};
</script>
"""
html = html.replace("</head>", preload_script + "</head>")

preview_path = os.path.abspath("intermediate_results/official_flags_preview.html")
with open(preview_path, "w", encoding="utf-8") as f:
    f.write(html)

test_url = "file:///" + preview_path.replace("\\", "/")
subprocess.run([chrome, "--headless", "--disable-gpu", "--window-size=1440,850", f"--screenshot={out}", test_url])
print("Official flags preview rendered:", os.path.exists(out))
