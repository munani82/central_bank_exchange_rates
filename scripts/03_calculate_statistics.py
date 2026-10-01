import os
import sqlite3
import json
import csv

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "exchange_rates.db")
inter_dir = os.path.join(base_dir, "intermediate_results")
os.makedirs(inter_dir, exist_ok=True)

def format_rate_by_country(val, country):
    if val is None:
        return None
    val = float(val)
    if country in ("Vietnam", "Indonesia"):
        return int(round(val))
    else:
        return round(val, 2)

print("=== 3단계: 통계 분석 및 환율 집계 엔진 가동 ===")

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# 1. 6개국 당일 최신 환율 산출
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

# 전일 대비 변동폭 계산 및 국가별 자리수 포맷팅
for item in latest_rates:
    c = item["country"]
    d = item["date"]
    item["rate"] = format_rate_by_country(item["rate"], c)
    
    prev_sql = """
    SELECT date, rate FROM exchange_rates
    WHERE country = ? AND date < ?
    ORDER BY date DESC LIMIT 1
    """
    cur.execute(prev_sql, (c, d))
    prev_row = cur.fetchone()
    if prev_row:
        prev_rate = format_rate_by_country(prev_row["rate"], c)
        item["prev_date"] = prev_row["date"]
        item["prev_rate"] = prev_rate
        diff = item["rate"] - prev_rate
        if c in ("Vietnam", "Indonesia"):
            item["diff"] = int(round(diff))
        else:
            item["diff"] = round(diff, 2)
        item["change_pct"] = round((diff / prev_rate) * 100.0, 2) if prev_rate else 0.0
    else:
        item["prev_date"] = None
        item["prev_rate"] = None
        item["diff"] = 0 if c in ("Vietnam", "Indonesia") else 0.0
        item["change_pct"] = 0.0

# 2. 최근 12개월 국가별 월평균 환율 산출
monthly_sql = """
SELECT 
    year_month,
    country,
    currency,
    currency_name,
    AVG(rate) as raw_avg,
    MIN(rate) as raw_min,
    MAX(rate) as raw_max,
    COUNT(rate) as data_points
FROM exchange_rates
WHERE year_month >= '2025_01'
GROUP BY year_month, country, currency, currency_name
ORDER BY year_month DESC, country ASC
"""
cur.execute(monthly_sql)
raw_monthly = [dict(row) for row in cur.fetchall()]
monthly_averages = []
for r in raw_monthly:
    c = r["country"]
    monthly_averages.append({
        "year_month": r["year_month"],
        "country": c,
        "currency": r["currency"],
        "currency_name": r["currency_name"],
        "avg_rate": format_rate_by_country(r["raw_avg"], c),
        "min_rate": format_rate_by_country(r["raw_min"], c),
        "max_rate": format_rate_by_country(r["raw_max"], c),
        "data_points": r["data_points"]
    })

# 3. 기간평균 계산 함수 정의
def get_period_average(start_date, end_date):
    query = """
    SELECT 
        country,
        currency,
        currency_name,
        AVG(rate) as raw_avg,
        MIN(rate) as raw_min,
        MAX(rate) as raw_max,
        COUNT(rate) as count_points,
        MIN(date) as actual_start,
        MAX(date) as actual_end
    FROM exchange_rates
    WHERE date >= ? AND date <= ?
    GROUP BY country, currency, currency_name
    ORDER BY country ASC
    """
    cur.execute(query, (start_date, end_date))
    raw_res = [dict(row) for row in cur.fetchall()]
    res = []
    for r in raw_res:
        c = r["country"]
        res.append({
            "country": c,
            "currency": r["currency"],
            "currency_name": r["currency_name"],
            "period_avg": format_rate_by_country(r["raw_avg"], c),
            "period_min": format_rate_by_country(r["raw_min"], c),
            "period_max": format_rate_by_country(r["raw_max"], c),
            "count_points": r["count_points"],
            "actual_start": r["actual_start"],
            "actual_end": r["actual_end"]
        })
    return res

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

print("\n=== 6개국 최신 환율 (자리수 규격 적용) ===")
for r in latest_rates:
    print(f"[{r['country']}] {r['currency']}/USD: {r['rate']} ({r['date']}) | 출처: {r['source']}")

print("\n=== 2026년 YTD(2026_01_01 ~ 2026_09_30) 기간평균 ===")
for p in period_ytd:
    print(f"[{p['country']}] 평균: {p['period_avg']} (최저 {p['period_min']} ~ 최고 {p['period_max']}) | 관측일: {p['count_points']}")

conn.close()
print("=== 3단계 통계 집계 완료 ===")
