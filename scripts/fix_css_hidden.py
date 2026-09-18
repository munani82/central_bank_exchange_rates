import os

def fix_css_hidden():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    old_css = """.hidden_native_picker {
  position: absolute;
  opacity: 0;
  pointer-events: none;
  width: 0;
  height: 0;
}"""

    new_css = """.hidden_native_picker {
  position: absolute;
  width: 0;
  height: 0;
  opacity: 0;
  pointer-events: none;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
  padding: 0;
  margin: -1px;
}"""

    for cname in ["style.css", "static/style.css"]:
        p = os.path.join(base_dir, cname)
        with open(p, "r", encoding="utf-8") as f:
            c = f.read()
        if old_css in c:
            c = c.replace(old_css, new_css)
            with open(p, "w", encoding="utf-8") as f:
                f.write(c)
            print(f"Updated {cname}")

if __name__ == "__main__":
    fix_css_hidden()
