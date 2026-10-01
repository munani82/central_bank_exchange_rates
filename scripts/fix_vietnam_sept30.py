import sqlite3
import json
import csv
import os

base_dir = r"c:\Users\Enduser\.gemini\antigravity-ide\scratch\central_bank_exchange_rates"
db_path = os.path.join(base_dir, "exchange_rates.db")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 1. 2026_09_30 베트남 오류 데이터(370동)를 공식 고시 중심환율(25,627동)로 즉시 교정
cur.execute("""
    UPDATE exchange_rates 
    SET rate = 25627.0, source = 'State Bank of Vietnam (sbv.gov.vn Official Central Rate)'
    WHERE country = 'Vietnam' AND date = '2026_09_30'
""")
print(f"Updated 2026_09_30 rate: {cur.rowcount} row")

conn.commit()

# 검증
cur.execute("SELECT date, rate, source FROM exchange_rates WHERE country='Vietnam' ORDER BY date")
rows = cur.fetchall()
print(f"Total Vietnam rows: {len(rows)}")
for r in rows:
    print(" ", r)

conn.close()

# 정적 데이터 갱신
import subprocess
subprocess.run(["python", os.path.join(base_dir, "scripts", "07_build_static_data.py")], check=True)
print("Static files updated successfully.")
