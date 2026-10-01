import shutil
import re

# 1. Copy static/app.js to root app.js
shutil.copy2("static/app.js", "app.js")
print("Copied static/app.js to app.js")

# 2. Update cache busting version in index.html (both root and static)
for p in ["index.html", "static/index.html"]:
    with open(p, "r", encoding="utf_8") as f:
        html = f.read()
    # update version parameter
    html = re.sub(r'app\.js\?v=[^\"]+', 'app.js?v=20261001_03', html)
    html = re.sub(r'style\.css\?v=[^\"]+', 'style.css?v=20261001_03', html)
    with open(p, "w", encoding="utf_8") as f:
        f.write(html)
    print(f"Updated cache bust version in {p}")
