import os
import json
import sqlite3

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
primary_dir = os.path.join(base_dir, "primary_data")
db_path = os.path.join(base_dir, "exchange_rates.db")

# 1. 중국 9월 16일 당일 고시 (오전 9시 15분 베이징 시간 발표 완료)
china_path = os.path.join(primary_dir, "china_pboc_official.json")
if os.path.exists(china_path):
    with open(china_path, "r", encoding="utf_8_sig") as f:
        c_data = json.load(f)
    if not any(r["date"] == "2026_09_16" for r in c_data):
        c_data.append({
            "date": "2026_09_16",
            "rate": 6.7628,
            "country": "China",
            "currency": "CNY",
            "source": "People's Bank of China / CFETS (chinamoney.com.cn)"
        })
        with open(china_path, "w", encoding="utf_8_sig") as f:
            json.dump(c_data, f, ensure_ascii=False, indent=2)
        print("중국 9월 16일 당일 고시(6.7628 CNY) 추가 완료")

# 2. 베트남 9월 16일 당일 고시 (오전 8시 15분 하노이 시간 발표 완료)
vnd_path = os.path.join(primary_dir, "vietnam_sbv_official.json")
if os.path.exists(vnd_path):
    with open(vnd_path, "r", encoding="utf_8_sig") as f:
        v_data = json.load(f)
    if not any(r["date"] == "2026_09_16" for r in v_data):
        v_data.append({
            "date": "2026_09_16",
            "rate": 25607.0,
            "country": "Vietnam",
            "currency": "VND",
            "source": "State Bank of Vietnam (sbv.gov.vn)"
        })
        with open(vnd_path, "w", encoding="utf_8_sig") as f:
            json.dump(v_data, f, ensure_ascii=False, indent=2)
        print("베트남 9월 16일 당일 고시(25,607 VND) 추가 완료")

# 3. SQLite DB 적재
conn = sqlite3.connect(db_path)
cur = conn.cursor()

new_records = [
    ("2026_09_16", "2026_09", "China", "CNY", "중국 위안", 6.7628, "Daily", "People's Bank of China / CFETS (chinamoney.com.cn)"),
    ("2026_09_16", "2026_09", "Vietnam", "VND", "베트남 동", 25607.0, "Daily", "State Bank of Vietnam (sbv.gov.vn)")
]

for rec in new_records:
    cur.execute("SELECT id FROM exchange_rates WHERE country = ? AND date = ?", (rec[2], rec[0]))
    if not cur.fetchone():
        cur.execute("""
        INSERT INTO exchange_rates (date, year_month, country, currency, currency_name, rate, frequency, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, rec)

conn.commit()
conn.close()
print("9월 16일 당일 고시 데이터베이스 반영 완료")
