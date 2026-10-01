import sqlite3
import csv
import os

def export_cleaned_csv():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "exchange_rates.db")
    csv_path = os.path.join(base_dir, "secondary_data", "cleaned_exchange_rates.csv")
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, date, year_month, country, currency, currency_name, rate, frequency, source, created_at FROM exchange_rates ORDER BY country, date")
    rows = cur.fetchall()
    headers = [d[0] for d in cur.description]
    conn.close()
    
    with open(csv_path, "w", newline="", encoding="utf_8_sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
        
    print(f"Exported cleaned_exchange_rates.csv successfully. Total rows: {len(rows)}")

if __name__ == "__main__":
    export_cleaned_csv()
