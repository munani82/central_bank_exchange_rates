import os

def update_version():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for fpath in [os.path.join(base_dir, "index.html"), os.path.join(base_dir, "static", "index.html")]:
        with open(fpath, "r", encoding="utf-8") as f:
            c = f.read()
        c = c.replace("20260916_25", "20260916_30")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(c)
    print("Version updated to 20260916_30")

if __name__ == "__main__":
    update_version()
