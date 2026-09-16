import os

def fix_wf():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    wf_path = os.path.join(base_dir, ".github", "workflows", "update_rates.yml")
    with open(wf_path, "r", encoding="utf-8") as f:
        wf = f.read()
    
    wf = wf.replace("git add static/data/ exchange_rates.db", "git add data/ static/data/ exchange_rates.db")
    with open(wf_path, "w", encoding="utf-8") as f:
        f.write(wf)
    print("Workflow git add updated successfully")

if __name__ == "__main__":
    fix_wf()
