report_path = "interim_reports/01_central_bank_exchange_rates_pipeline.md"

with open(report_path, "r", encoding="utf_8") as f:
    content = f.read()

section_28 = """

## 28. 원천 데이터베이스 정밀 실측치 100% 원상 복원 및 프레젠테이션 레이어 표시 표준화 분리 확립
* 사용자 피드백 반영 및 원칙 재확립
  * 사용자의 명확한 요구: 원천 데이터베이스의 원본 실측치를 임의로 반올림하거나 수정하지 말고, 사용자에게 제공되는 "화면 및 통계 표출(Presentation) 단계"에서만 베트남과 인도네시아는 정수로, 기타 4개국은 소수점 2자리로 표시할 것을 지시하심.
  * 데이터 아키텍처 원칙: 원천 보존(Data Layer)과 화면 표시(Presentation Layer)의 엄격한 분리 원칙 확립.
* 원천 데이터베이스 및 정제 CSV 100% 원본 정밀도 복원 완료
  * exchange_rates.db 및 secondary_data/cleaned_exchange_rates.csv의 rate 컬럼을 중앙은행 공식 원시 실측치(이집트 51.9887, 폴란드 3.8449, 중국 6.7351 등) 그대로 완전하게 원상 복원함.
  * 원본 데이터베이스 총 건수: 2,592건, 원천 고시 정밀도 100% 보존.
* 프레젠테이션 레이어 포맷팅 전면 적용 (static/app.js)
  * formatRateValue 헬퍼 함수를 통해 원천 데이터를 훼손하지 않고 렌더링 시점에만 규격을 변환함:
    * 베트남(VND) 및 인도네시아(IDR): Math.round 후 천단위 콤마 정수 표기 (예: 25,624 동, 17,877 루피아)
    * 대한민국, 중국, 폴란드, 이집트: toLocaleString 소수점 2자리 고정 표기 (예: 1,355.70 원, 6.74 위안, 51.99 파운드, 3.84 즈워티)
  * 적용 완료 영역: 당일 최신 환율 카드, 사용자 지정 기간평균 계산기 카드 및 표, 월평균 통계 테이블, 캔버스 시계열 차트 Y축 눈금.
* 정적 API JSON 파일 규격 정돈 (static/data 및 data)
  * latest_rates.json, monthly_averages.json, history_rates.json, all_rates.json 모두 원시 실측 정밀도를 온전히 담은 채 웹 화면에서 동적으로 규격화 표시되도록 동기화 완료.
"""

new_content = content.strip() + "\n" + section_28

with open(report_path, "w", encoding="utf_8") as f:
    f.write(new_content)

print("Updated interim report with Section 28 successfully.")
