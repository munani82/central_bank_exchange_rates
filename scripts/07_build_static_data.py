import os
import json
import sqlite3

def build_static_json():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "exchange_rates.db")
    static_data_dir = os.path.join(base_dir, "static", "data")
    root_data_dir = os.path.join(base_dir, "data")
    os.makedirs(static_data_dir, exist_ok=True)
    os.makedirs(root_data_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 1. 최신 환율 (latest_rates.json)
    cur.execute("""
    WITH ranked AS (
        SELECT country, currency, currency_name, date, rate, frequency, source,
               ROW_NUMBER() OVER (PARTITION BY country ORDER BY date DESC) as rn
        FROM exchange_rates
    )
    SELECT country, currency, currency_name, date, rate, frequency, source
    FROM ranked WHERE rn = 1 ORDER BY country ASC
    """)
    latest_rows = [dict(r) for r in cur.fetchall()]

    for item in latest_rows:
        c = item["country"]
        d = item["date"]
        cur.execute("""
        SELECT date, rate FROM exchange_rates
        WHERE country = ? AND date < ?
        ORDER BY date DESC LIMIT 1
        """, (c, d))
        p_row = cur.fetchone()
        if p_row:
            pr = p_row["rate"]
            item["prev_date"] = p_row["date"]
            item["prev_rate"] = pr
            diff = item["rate"] - pr
            item["diff"] = round(diff, 4)
            item["change_pct"] = round((diff / pr) * 100.0, 3)
        else:
            item["prev_date"] = None
            item["prev_rate"] = None
            item["diff"] = 0.0
            item["change_pct"] = 0.0

    latest_json_path = os.path.join(static_data_dir, "latest_rates.json")
    with open(latest_json_path, "w", encoding="utf-8") as f:
        json.dump({"status": "success", "count": len(latest_rows), "data": latest_rows}, f, ensure_ascii=False, indent=2)
    print("latest_rates.json 생성 완료")

    # 2. 월평균 통계 (monthly_averages.json)
    cur.execute("""
    SELECT year_month, country, currency, currency_name,
           ROUND(AVG(rate), 4) as avg_rate,
           ROUND(MIN(rate), 4) as min_rate,
           ROUND(MAX(rate), 4) as max_rate,
           COUNT(rate) as data_points
    FROM exchange_rates
    GROUP BY year_month, country
    ORDER BY year_month DESC, country ASC
    """)
    monthly_rows = [dict(r) for r in cur.fetchall()]
    monthly_json_path = os.path.join(static_data_dir, "monthly_averages.json")
    with open(monthly_json_path, "w", encoding="utf-8") as f:
        json.dump({"status": "success", "count": len(monthly_rows), "data": monthly_rows}, f, ensure_ascii=False, indent=2)
    print("monthly_averages.json 생성 완료")

    # 3. 국가별 시계열 (history_rates.json)
    cur.execute("""
    SELECT date, country, currency, rate, source
    FROM exchange_rates
    ORDER BY date ASC, country ASC
    """)
    all_history = [dict(r) for r in cur.fetchall()]
    history_json_path = os.path.join(static_data_dir, "history_rates.json")
    with open(history_json_path, "w", encoding="utf-8") as f:
        json.dump({"status": "success", "count": len(all_history), "data": all_history}, f, ensure_ascii=False, indent=2)
    print("history_rates.json 생성 완료")

    # 4. 전체 일별 데이터 (all_rates.json)
    all_rates_path = os.path.join(static_data_dir, "all_rates.json")
    with open(all_rates_path, "w", encoding="utf-8") as f:
        json.dump({"status": "success", "count": len(all_history), "data": all_history}, f, ensure_ascii=False)
    print("all_rates.json 생성 완료")

    conn.close()
    import shutil
    for fn in ["latest_rates.json", "monthly_averages.json", "history_rates.json", "all_rates.json"]:
        src_f = os.path.join(static_data_dir, fn)
        dst_f = os.path.join(root_data_dir, fn)
        if os.path.exists(src_f):
            shutil.copy2(src_f, dst_f)

if __name__ == "__main__":
    build_static_json()
