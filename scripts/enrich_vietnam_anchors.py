import sqlite3
import os
import subprocess

base_dir = r"c:\Users\Enduser\.gemini\antigravity-ide\scratch\central_bank_exchange_rates"
db_path = os.path.join(base_dir, "exchange_rates.db")

anchors_2025 = [
    ("2025_01_02", 24335.0),
    ("2025_01_03", 24334.0),
    ("2025_02_03", 24325.0),
    ("2025_03_03", 24758.0),
    ("2025_04_01", 24835.0)
]

conn = sqlite3.connect(db_path)
cur = conn.cursor()

for d, rate in anchors_2025:
    ym = d[:7]
    cur.execute("""
        INSERT OR REPLACE INTO exchange_rates (date, year_month, country, currency, currency_name, rate, frequency, source)
        VALUES (?, ?, 'Vietnam', 'VND', '베트남 동', ?, 'Daily', 'State Bank of Vietnam (sbv.gov.vn Official Central Rate)')
    """, (d, ym, rate))

conn.commit()

cur.execute("SELECT count(*), min(date), max(date) FROM exchange_rates WHERE country='Vietnam'")
print("Vietnam updated summary:", cur.fetchone())

conn.close()

# 07_build_static_data.py 실행
subprocess.run(["python", os.path.join(base_dir, "scripts", "07_build_static_data.py")], check=True)
print("Build complete!")
