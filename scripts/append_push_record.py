import os

def append_push_record():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    report_path = os.path.join(base_dir, "interim_reports", "01_central_bank_exchange_rates_pipeline.md")
    
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    section_git = """
***

## 9. GitHub 공식 원격 저장소 푸시 완료 내역
* 원격 레포지토리 주소: https://github.com/munani82/central_bank_exchange_rates.git
* 기본 브랜치: main
* 푸시 완료 시각: 2026년 9월 16일
* 적재 내용: 6개국 공식 고시환율 전체 데이터베이스(exchange_rates.db), Vercel 정적 배포 설정(vercel.json), GitHub Actions 하루 5회 자동 갱신 워크플로우(.github/workflows/update_rates.yml), 고딕 핀테크 웹 프론트엔드(static)
"""

    if "## 9. GitHub 공식 원격 저장소 푸시 완료 내역" not in content:
        content += "\n" + section_git

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Report push record appended successfully")

if __name__ == "__main__":
    append_push_record()
