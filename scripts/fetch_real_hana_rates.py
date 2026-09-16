import urllib.request
import re
import time
import json
from datetime import datetime

rates_by_date = {}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

print("네이버 금융 (하나은행 고시 매매기준율) 크롤링 시작...")

# 50페이지 (약 500영업일 = 2년치)
for page in range(1, 55):
    url = f"https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_USDKRW&page={page}"
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode("cp949")
        dates = re.findall(r'<td class="date">\s*([0-9.]+)\s*</td>', html)
        nums = re.findall(r'<td class="num">\s*([0-9,.]+)\s*</td>', html)
        
        if not dates:
            break
            
        for d_str, r_str in zip(dates, nums):
            d_norm = d_str.strip().replace(".", "_")
            r_val = float(r_str.strip().replace(",", ""))
            if d_norm not in rates_by_date:
                rates_by_date[d_norm] = r_val
                
        # 2025년 1월 이전으로 가면 중단
        min_date = min(dates).replace(".", "_")
        if min_date < "2025_01_01":
            print(f"2025년 1월 데이터 도달 완료 (페이지 {page})")
            break
            
        time.sleep(0.1)
    except Exception as e:
        print(f"Page {page} error: {e}")
        break

print(f"총 수집된 일별 환율 건수: {len(rates_by_date)} 건")

# 월별 평균 계산
monthly_stats = {}
for d, r in rates_by_date.items():
    ym = d[:7]
    if ym not in monthly_stats:
        monthly_stats[ym] = []
    monthly_stats[ym].append(r)

print("\n=== 하나은행 고시 매매기준율 실제 월평균 ===")
for ym in sorted(monthly_stats.keys(), reverse=True):
    vals = monthly_stats[ym]
    avg_v = sum(vals) / len(vals)
    min_v = min(vals)
    max_v = max(vals)
    print(f"{ym}: 평균 {avg_v:,.2f}원 (최저 {min_v:,.2f}, 최고 {max_v:,.2f}, {len(vals)}일)")

# JSON 파일로 저장
output_path = "primary_data/korea_hana_real_official.json"
records = []
for d in sorted(rates_by_date.keys(), reverse=True):
    records.append({
        "date": d,
        "rate": rates_by_date[d],
        "country": "Korea",
        "currency": "KRW",
        "source": "KEB Hana Bank Official Fixing (Market Average Rate, MAR)"
    })

with open(output_path, "w", encoding="utf-8-sig") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print(f"\n실제 하나은행 공식 데이터 저장 완료: {output_path}")
