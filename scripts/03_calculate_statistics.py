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

# 1. 6개국 당일 최신 환율 산출 (원본 실측 정밀도 유지)
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
        item["diff"] = round(diff, 4)
        item["change_pct"] = round((diff / prev_rate) * 100.0, 3) if prev_rate else 0.0
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

# 3. 기간평균 계산 함수 정의
def get_period_average(start_date, end_date):
    query = """
    SELECT 
        country,
        currency,
        currency_name,
        ROUND(AVG(rate), 4) as period_avg,
        MIN(rate) as period_min,
        MAX(rate) as period_max,
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

# 2026년 연초 이후 (YTD) 기간평균
period_ytd = get_period_average("2026_01_01", "2026_09_30")

# 산출물 저장 (CSV: utf_8_sig, JSON)
with open(os.path.join(inter_dir, "latest_rates.json"), "w", encoding="utf_8_sig") as f:
    json.dump(latest_rates, f, ensure_ascii=False, indent=2)

with open(os.path.join(inter_dir, "latest_rates.csv"), "w", newline="", encoding="utf_8_sig") as f:
    if latest_rates:
        writer = csv.DictWriter(f, fieldnames=latest_rates[0].keys())
        writer.writeheader()
        writer.writerows(latest_rates)

with open(os.path.join(inter_dir, "monthly_averages.csv"), "w", newline="", encoding="utf_8_sig") as f:
    if monthly_averages:
        writer = csv.DictWriter(f, fieldnames=monthly_averages[0].keys())
        writer.writeheader()
        writer.writerows(monthly_averages)

with open(os.path.join(inter_dir, "period_averages_ytd.csv"), "w", newline="", encoding="utf_8_sig") as f:
    if period_ytd:
        writer = csv.DictWriter(f, fieldnames=period_ytd[0].keys())
        writer.writeheader()
        writer.writerows(period_ytd)

print("\n=== 6개국 최신 환율 (원시 실측 정밀도 유지) ===")
for r in latest_rates:
    print(f"[{r['country']}] {r['currency']}/USD: {r['rate']} ({r['date']}) | 출처: {r['source']}")

conn.close()
print("=== 3단계 통계 집계 완료 ===")
