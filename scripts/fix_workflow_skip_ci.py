import os

def remove_skip_ci():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    wf_path = os.path.join(base_dir, ".github", "workflows", "update_rates.yml")
    
    with open(wf_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # [skip ci] 태그 제거 -> Vercel 자동 재배포 보장
    content = content.replace("[skip ci]", "")
    content = content.replace("Auto Update: Central Bank Exchange Rates ", "Auto Update: Central Bank Exchange Rates")
    
    with open(wf_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("update_rates.yml updated (removed [skip ci])")

if __name__ == "__main__":
    remove_skip_ci()
