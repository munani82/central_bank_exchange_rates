import os

def append_report():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    report_path = os.path.join(base_dir, "interim_reports", "01_central_bank_exchange_rates_pipeline.md")
    
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    section_8 = """
***

## 8. Vercel 및 GitHub Actions 클라우드 무중단 배포 아키텍처 구축
로컬 PC를 상시 가동하지 않고도 전 세계 누구나 웹에서 조회하고, 각국 고시 시점에 맞춰 100% 무료로 자동 갱신되는 클라우드 Jamstack 파이프라인을 구축하였습니다.

* 정적 데이터 세트 자동 사전 빌드 파이프라인 (scripts/07_build_static_data.py)
  * 로컬 DB(exchange_rates.db)의 원천 데이터를 Vercel 초고속 정적 서빙 규격인 static/data/ 폴더(latest_rates.json, monthly_averages.json, history_rates.json, all_rates.json)로 자동 추출 및 변환
* 프론트엔드 오프라인 및 Vercel 정적 호스팅 하이브리드 지원 (static/app.js)
  * 백엔드 API 서버 부재 시에도 정적 JSON을 즉각 로드하는 fetchWithFallback 로직 적용
  * 사용자가 일자를 직접 선택하는 기간평균 계산기도 all_rates.json을 바탕으로 브라우저(클라이언트)에서 실시간으로 평균 및 최저, 최고를 즉각 연산하도록 완전 구현
* Vercel 배포 라우팅 설정 (vercel.json)
  * 루트 경로 접속 시 static/index.html로 매핑하고 정적 데이터(/data) 라우팅을 자동 연결
* GitHub Actions 하루 5회 정밀 자동 갱신 워크플로우 (.github/workflows/update_rates.yml)
  * 월요일부터 금요일까지 각국 공식 고시 시각에 맞춰 하루 5회(09:15, 10:45, 18:30, 19:30, 21:30 KST) 자동 실행
  * 파이썬 환경에서 신규 환율을 수집 및 DB 반영 후 static/data/를 최신화하고 Git 자동 커밋 및 푸시 수행
  * Vercel은 깃허브 main 브랜치 푸시를 감지하여 10초 내에 전 세계 글로벌 CDN으로 자동 무중단 재배포
"""

    if "## 8. Vercel 및 GitHub Actions" not in content:
        content += "\n" + section_8

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Report updated successfully")

if __name__ == "__main__":
    append_report()
