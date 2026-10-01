import sqlite3
import csv
import os

def format_rate_by_country(val, country):
    if val is None:
        return None
    val = float(val)
    if country in ("Vietnam", "Indonesia"):
        return int(round(val))
    else:
        return round(val, 2)

def update_db_and_export_csv():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "exchange_rates.db")
    csv_path = os.path.join(base_dir, "secondary_data", "cleaned_exchange_rates.csv")
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # 1. Update rates in DB according to country decimal rules
    # Vietnam & Indonesia: round to integer
    cur.execute("""
        UPDATE exchange_rates
        SET rate = ROUND(rate, 0)
        WHERE country IN ('Vietnam', 'Indonesia')
    """)
    print(f"Updated Vietnam & Indonesia integer rates: {cur.rowcount} rows")
    
    # Other countries (China, Egypt, Korea, Poland): round to 2 decimals
    cur.execute("""
        UPDATE exchange_rates
        SET rate = ROUND(rate, 2)
        WHERE country IN ('China', 'Egypt', 'Korea', 'Poland')
    """)
    print(f"Updated 4 countries 2-decimal rates: {cur.rowcount} rows")
    
    conn.commit()
    
    # 2. Export to secondary_data/cleaned_exchange_rates.csv
    cur.execute("""
        SELECT id, date, year_month, country, currency, currency_name, rate, frequency, source, created_at
        FROM exchange_rates
        ORDER BY country, date
    """)
    rows = cur.fetchall()
    headers = [d[0] for d in cur.description]
    
    formatted_rows = []
    for r in rows:
        row_list = list(r)
        c = row_list[3]
        orig_rate = row_list[6]
        row_list[6] = format_rate_by_country(orig_rate, c)
        formatted_rows.append(row_list)
        
    conn.close()
    
    with open(csv_path, "w", newline="", encoding="utf_8_sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(formatted_rows)
        
    print(f"Exported cleaned_exchange_rates.csv successfully. Total rows: {len(formatted_rows)}")

if __name__ == "__main__":
    update_db_and_export_csv()
