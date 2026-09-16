import os
import json

def create_vercel_config():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    v_path = os.path.join(base_dir, "vercel.json")
    
    H = chr(45)
    
    # Vercel 정적 배포 설정
    config = {
        "version": 2,
        "cleanUrls": True,
        "rewrites": [
            {"source": "/", "destination": "/static/index.html"},
            {"source": "/data/(.*)", "destination": "/static/data/$1"},
            {"source": "/static/(.*)", "destination": "/static/$1"}
        ]
    }
    
    with open(v_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
        
    print("vercel.json created successfully")

if __name__ == "__main__":
    create_vercel_config()
