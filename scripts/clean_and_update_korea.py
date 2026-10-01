import sqlite3
import json
import os

def clean_and_update_korea():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "exchange_rates.db")
    json_path = os.path.join(base_dir, "primary_data", "korea_hana_september_exact_official.json")
    
    with open(json_path, "r", encoding="utf_8_sig") as f:
        official_list = json.load(f)
        
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # 1. Delete hyphen-based records if any
    cur.execute("DELETE FROM exchange_rates WHERE country = 'Korea' AND date LIKE '2026-%'")
    print(f"Deleted hyphen records: {cur.rowcount}")
    
    # 2. Delete old calibrated September records
    cur.execute("DELETE FROM exchange_rates WHERE country = 'Korea' AND date LIKE '2026_09_%'")
    print(f"Deleted old calibrated September records: {cur.rowcount}")
    
    # 3. Insert 100% pure official records with YYYY_MM_DD format
    for item in official_list:
        raw_dt = item["date"]
        norm_dt = raw_dt.replace("-", "_")
        ym = norm_dt[:7]
        rate = item["rate"]
        cur.execute("""
            INSERT INTO exchange_rates (date, year_month, country, currency, currency_name, rate, frequency, source)
            VALUES (?, ?, 'Korea', 'KRW', 'South Korean Won', ?, 'Daily', 'Hana Bank Official Portal (1st Notice)')
        """, (norm_dt, ym, rate))
        
    conn.commit()
    
    # Verify September
    cur.execute("""
        SELECT date, rate, source
        FROM exchange_rates
        WHERE country = 'Korea' AND date LIKE '2026_09_%'
        ORDER BY date
    """)
    rows = cur.fetchall()
    print(f"\nOfficial Korea September 2026 Records ({len(rows)} days):")
    total_sum = 0
    for r in rows:
        print(f"  {r[0]}: {r[1]:.2f} 원")
        total_sum += r[1]
    avg_val = total_sum / len(rows)
    print(f"\nSum: {total_sum:.2f} 원")
    print(f"Mean: {avg_val:.4f} 원")
    
    # Total count for Korea
    cur.execute("SELECT count(*) FROM exchange_rates WHERE country = 'Korea'")
    print(f"Total Korea Records in DB: {cur.fetchone()[0]}")
    
    conn.close()

if __name__ == "__main__":
    clean_and_update_korea()
