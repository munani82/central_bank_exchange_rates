import os
import sqlite3
import json
import csv

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "exchange_rates.db")
inter_dir = os.path.join(base_dir, "intermediate_results")
os.makedirs(inter_dir, exist_ok=True)

print("=== 3단계: 통계 분석 및 환율 집계 엔진 가동 ===")

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# 1. 5개국 당일 최신 환율 산출
latest_sql = """
WITH ranked_rates AS (
    SELECT 
        country,
        currency,
        currency_name,
        date,
        rate,
        frequency,
        source,
        ROW_NUMBER() OVER (PARTITION BY country ORDER BY date DESC) as rn
    FROM exchange_rates
)
SELECT country, currency, currency_name, date, rate, frequency, source
FROM ranked_rates
WHERE rn = 1
ORDER BY country
"""
cur.execute(latest_sql)
latest_rates = [dict(row) for row in cur.fetchall()]

# 전일 대비 변동폭 계산 (직전 영업일 환율 비교)
for item in latest_rates:
    c = item["country"]
    d = item["date"]
    prev_sql = """
    SELECT date, rate FROM exchange_rates
    WHERE country = ? AND date < ?
    ORDER BY date DESC LIMIT 1
    """
    cur.execute(prev_sql, (c, d))
    prev_row = cur.fetchone()
    if prev_row:
        prev_rate = prev_row["rate"]
        item["prev_date"] = prev_row["date"]
        item["prev_rate"] = prev_rate
        diff = item["rate"] - prev_rate
        item["diff"] = diff
        item["change_pct"] = (diff / prev_rate) * 100.0 if prev_rate else 0.0
    else:
        item["prev_date"] = None
        item["prev_rate"] = None
        item["diff"] = 0.0
        item["change_pct"] = 0.0

# 2. 최근 12개월 국가별 월평균 환율 산출
monthly_sql = """
SELECT 
    year_month,
    country,
    currency,
    currency_name,
    ROUND(AVG(rate), 4) as avg_rate,
    MIN(rate) as min_rate,
    MAX(rate) as max_rate,
    COUNT(rate) as data_points
FROM exchange_rates
WHERE year_month >= '2025_01'
GROUP BY year_month, country, currency, currency_name
ORDER BY year_month DESC, country ASC
"""
cur.execute(monthly_sql)
monthly_averages = [dict(row) for row in cur.fetchall()]

# 3. 기간평균 계산 함수 정의 (예: 2026_01_01 ~ 2026_09_15)
def get_period_average(start_date, end_date):
    query = """
    SELECT 
        country,
        currency,
        currency_name,
        ROUND(AVG(rate), 4) as period_avg,
        ROUND(MIN(rate), 4) as period_min,
        ROUND(MAX(rate), 4) as period_max,
        COUNT(rate) as count_points,
        MIN(date) as actual_start,
        MAX(date) as actual_end
    FROM exchange_rates
    WHERE date >= ? AND date <= ?
    GROUP BY country, currency, currency_name
    ORDER BY country ASC
    """
    cur.execute(query, (start_date, end_date))
    return [dict(row) for row in cur.fetchall()]

# 2026년 연초 이후 기간평균 계산 예시
ytd_period = get_period_average("2026_01_01", "2026_09_15")

# 4. 결과 저장
# intermediate_results/latest_rates.json
latest_json_path = os.path.join(inter_dir, "latest_rates.json")
with open(latest_json_path, "w", encoding="utf_8_sig") as f:
    json.dump(latest_rates, f, ensure_ascii=False, indent=2)

# intermediate_results/latest_rates.csv
latest_csv_path = os.path.join(inter_dir, "latest_rates.csv")
with open(latest_csv_path, "w", encoding="utf_8_sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(latest_rates[0].keys()))
    writer.writeheader()
    writer.writerows(latest_rates)

# intermediate_results/monthly_averages.csv
if monthly_averages:
    monthly_csv_path = os.path.join(inter_dir, "monthly_averages.csv")
    with open(monthly_csv_path, "w", encoding="utf_8_sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(monthly_averages[0].keys()))
        writer.writeheader()
        writer.writerows(monthly_averages)

# intermediate_results/period_averages_ytd.csv
if ytd_period:
    ytd_csv_path = os.path.join(inter_dir, "period_averages_ytd.csv")
    with open(ytd_csv_path, "w", encoding="utf_8_sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(ytd_period[0].keys()))
        writer.writeheader()
        writer.writerows(ytd_period)

print("\n=== 5개국 당일 최신 고시환율 ===")
for r in latest_rates:
    print(f"[{r['country']}] {r['currency']}/USD: {r['rate']:.4f} ({r['date']}) | 출처: {r['source']}")

print("\n=== 2026년 YTD(2026_01_01 ~ 2026_09_15) 기간평균 ===")
for r in ytd_period:
    print(f"[{r['country']}] 평균: {r['period_avg']} (최소 {r['period_min']} ~ 최대 {r['period_max']}) | 관측수: {r['count_points']}")

conn.close()
print("=== 3단계 통계 집계 완료 ===")
