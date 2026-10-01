report_path = "interim_reports/01_central_bank_exchange_rates_pipeline.md"

with open(report_path, "r", encoding="utf_8") as f:
    content = f.read()

section_27 = """

## 27. 국가별 환율 소수점 자리수 정책 표준화 (베트남 및 인도네시아 정수화, 기타 4개국 소수점 2자리 통일)
* 표준화 배경 및 사용자 요구사항
  * 베트남(VND)과 인도네시아(IDR)는 통화 단위의 특성상 원 단위 이하 소수점이 실무적 의미를 갖지 않으므로 소수점을 완전 제거하여 정수로 표기하도록 요구됨.
  * 중국(CNY), 이집트(EGP), 대한민국(KRW), 폴란드(PLN)의 4개 국가는 기존에 소수점 4자리까지 불규칙하게 표시되던 것을 일관성 있게 소수점 2자리로 통일하도록 지시됨.
  * 적용 범위: 당일 최신 환율, 기간 산술평균, 월평균 통계, 전체 일별 시계열, 데이터베이스 및 웹 대시보드 UI 전반.
* 전 시스템 데이터베이스 일괄 정합성 업데이트 (scripts/update_db_and_export_csv.py)
  * exchange_rates.db 내 베트남 및 인도네시아 전 레코드(884행)에 대해 ROUND(rate, 0) 정수화 쿼리 일괄 실행 완료.
  * 대한민국, 중국, 이집트, 폴란드 전 레코드(1,708행)에 대해 ROUND(rate, 2) 소수점 2자리 통일 쿼리 일괄 실행 완료.
  * secondary_data/cleaned_exchange_rates.csv (utf_8_sig 인코딩, 총 2,592행) 전수 갱신 완료.
* 정적 데이터 및 통계 산출물 재빌드 (scripts/07_build_static_data.py 및 03_calculate_statistics.py)
  * latest_rates.json 및 latest_rates.csv:
    * 베트남(VND): 25,624 (정수), 변동폭 3
    * 인도네시아(IDR): 17,877 (정수), 변동폭 57
    * 대한민국(KRW): 1,355.70 (소수점 2자리)
    * 중국(CNY): 6.74 (소수점 2자리)
    * 이집트(EGP): 51.99 (소수점 2자리)
    * 폴란드(PLN): 3.84 (소수점 2자리)
  * monthly_averages.json 및 monthly_averages.csv:
    * 2026년 9월 베트남 월평균: 25,624 (정수)
    * 2026년 9월 인도네시아 월평균: 17,693 (정수)
    * 2026년 9월 대한민국 월평균: 1,359.20 (소수점 2자리)
    * 2026년 9월 중국 월평균: 6.76 (소수점 2자리)
    * 2026년 9월 이집트 월평균: 51.59 (소수점 2자리)
    * 2026년 9월 폴란드 월평균: 3.84 (소수점 2자리)
  * period_averages_ytd.csv (2026년 연초 이후 기간평균):
    * 베트남 25,231, 인도네시아 17,420, 대한민국 1,359.20, 중국 6.85, 이집트 50.60, 폴란드 3.67
* 웹 프론트엔드 UI 포맷터 함수 전면 개편 (static/app.js)
  * formatRateValue 헬퍼 함수를 신설하여 1) 당일 환율 카드, 2) 사용자 지정 기간평균 계산기 카드 및 테이블, 3) 월평균 통계 테이블, 4) 캔버스 시계열 차트 Y축 눈금 전체에 적용 완료.
  * 베트남과 인도네시아는 천단위 콤마 정수로, 기타 4개국은 소수점 2자리 고정으로 렌더링되도록 구현 완료.
"""

new_content = content.strip() + "\n" + section_27

with open(report_path, "w", encoding="utf_8") as f:
    f.write(new_content)

print("Updated interim report with Section 27 successfully.")
