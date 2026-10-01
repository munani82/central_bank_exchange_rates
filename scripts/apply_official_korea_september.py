import sqlite3
import json
import os

def apply_official_korea_september():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "exchange_rates.db")
    json_path = os.path.join(base_dir, "primary_data", "korea_hana_september_exact_official.json")
    
    with open(json_path, "r", encoding="utf_8_sig") as f:
        data = json.load(f)
        
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # First, delete existing Korea September 2026 records to cleanly replace with exact official records
    cur.execute("DELETE FROM exchange_rates WHERE country = 'Korea' AND date LIKE '2026-09-%'")
    print(f"Deleted old Korea September records: {cur.rowcount}")
    
    # Insert official records
    for item in data:
        dt = item["date"]
        ym = dt[:7]
        rate = item["rate"]
        cur.execute("""
            INSERT INTO exchange_rates (date, year_month, country, currency, currency_name, rate, frequency, source)
            VALUES (?, ?, 'Korea', 'KRW', 'South Korean Won', ?, 'Daily', 'Hana Bank Official Portal (1st Notice)')
        """, (dt, ym, rate))
        
    conn.commit()
    
    # Query summary
    cur.execute("""
        SELECT count(*), avg(rate), min(rate), max(rate)
        FROM exchange_rates
        WHERE country = 'Korea' AND date LIKE '2026-09-%'
    """)
    cnt, avg_val, min_val, max_val = cur.fetchone()
    print(f"Korea September 2026 in DB: {cnt} days, Avg: {avg_val:.4f}, Min: {min_val}, Max: {max_val}")
    
    # Query total records by country
    cur.execute("""
        SELECT country, count(*), min(date), max(date), avg(rate)
        FROM exchange_rates
        GROUP BY country
        ORDER BY country
    """)
    print("\nAll Countries Summary:")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]} records, {row[2]} ~ {row[3]}, avg: {row[4]:.2f}")
        
    conn.close()

if __name__ == "__main__":
    apply_official_korea_september()
