import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
subdirs = [
    "primary_data",
    "secondary_data",
    "intermediate_results",
    "visualizations",
    "interim_reports",
    "scripts",
    "pdfs",
    "static"
]

for d in subdirs:
    target_path = os.path.join(base_dir, d)
    os.makedirs(target_path, exist_ok=True)
    print(f"디렉토리 준비 완료: {target_path}")

print("기본 폴더 구조 초기화 완료")
