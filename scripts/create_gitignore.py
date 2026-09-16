import os

def make_gitignore():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gi_path = os.path.join(base_dir, ".gitignore")
    
    content = """__pycache__/
*.py[cod]
*$py.class
.venv/
env/
venv/
.DS_Store
Thumbs.db
*.log
"""
    with open(gi_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(".gitignore created successfully")

if __name__ == "__main__":
    make_gitignore()
