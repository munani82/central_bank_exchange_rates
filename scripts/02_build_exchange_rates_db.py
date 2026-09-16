import os
import json
import csv
import sqlite3

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
primary_dir = os.path.join(base_dir, "primary_data")
secondary_dir = os.path.join(base_dir, "secondary_data")
db_path = os.path.join(base_dir, "exchange_rates.db")

os.makedirs(secondary_dir, exist_ok=True)

print("=== 2단계: 6개국 중앙은행 공식 데이터 정제 및 DB 적재 시작 ===")

all_records = []

# 1. 한국 한국은행/서울외국환중개 JSON 파싱
krw_path = os.path.join(primary_dir, "korea_bok_official.json")
if os.path.exists(krw_path):
    with open(krw_path, "r", encoding="utf_8_sig") as f:
        krw_items = json.load(f)
        for item in krw_items:
            all_records.append({
                "date": item["date"],
                "year_month": item["date"][:7],
                "country": "Korea",
                "currency": "KRW",
                "currency_name": "대한민국 원",
                "rate": float(item["rate"]),
                "frequency": "Daily",
                "source": item["source"]
            })
    print(f"한국은행 공식 고시 파싱: {len(krw_items)} 건")

# 2. 폴란드 NBP 공식 API JSON 파싱
nbp_path = os.path.join(primary_dir, "poland_nbp_official.json")
if os.path.exists(nbp_path):
    with open(nbp_path, "r", encoding="utf_8_sig") as f:
        nbp_items = json.load(f)
        for item in nbp_items:
            raw_d = item.get("effectiveDate")
            val = float(item.get("mid"))
            norm_d = raw_d.replace("-", "_")
            all_records.append({
                "date": norm_d,
                "year_month": norm_d[:7],
                "country": "Poland",
                "currency": "PLN",
                "currency_name": "폴란드 즐로티",
                "rate": val,
                "frequency": "Daily",
                "source": "Narodowy Bank Polski (NBP Official Web API)"
            })
    print(f"폴란드 NBP 공식 고시 파싱: {len(nbp_items)} 건")

# 3. 중국 인민은행 / CFETS 공식 중간가격 JSON 파싱
china_path = os.path.join(primary_dir, "china_pboc_official.json")
if os.path.exists(china_path):
    with open(china_path, "r", encoding="utf_8_sig") as f:
        china_items = json.load(f)
        for item in china_items:
            all_records.append({
                "date": item["date"],
                "year_month": item["date"][:7],
                "country": "China",
                "currency": "CNY",
                "currency_name": "중국 위안",
                "rate": float(item["rate"]),
                "frequency": "Daily",
                "source": item["source"]
            })
    print(f"중국 인민은행/CFETS 공식 고시 파싱: {len(china_items)} 건")

# 4. 인도네시아 중앙은행 공식 JISDOR JSON 파싱
idr_path = os.path.join(primary_dir, "indonesia_bi_official.json")
if os.path.exists(idr_path):
    with open(idr_path, "r", encoding="utf_8_sig") as f:
        idr_items = json.load(f)
        for item in idr_items:
            all_records.append({
                "date": item["date"],
                "year_month": item["date"][:7],
                "country": "Indonesia",
                "currency": "IDR",
                "currency_name": "인도네시아 루피아",
                "rate": float(item["rate"]),
                "frequency": "Daily",
                "source": item["source"]
            })
    print(f"인도네시아 BI JISDOR 공식 고시 파싱: {len(idr_items)} 건")

# 5. 베트남 중앙은행 공식 기준환율 JSON 파싱
vnd_path = os.path.join(primary_dir, "vietnam_sbv_official.json")
if os.path.exists(vnd_path):
    with open(vnd_path, "r", encoding="utf_8_sig") as f:
        vnd_items = json.load(f)
        for item in vnd_items:
            all_records.append({
                "date": item["date"],
                "year_month": item["date"][:7],
                "country": "Vietnam",
                "currency": "VND",
                "currency_name": "베트남 동",
                "rate": float(item["rate"]),
                "frequency": "Daily",
                "source": item["source"]
            })
    print(f"베트남 SBV 공식 기준환율 파싱: {len(vnd_items)} 건")

# 6. 이집트 중앙은행 공식 고시환율 JSON 파싱
egp_path = os.path.join(primary_dir, "egypt_cbe_official.json")
if os.path.exists(egp_path):
    with open(egp_path, "r", encoding="utf_8_sig") as f:
        egp_items = json.load(f)
        for item in egp_items:
            all_records.append({
                "date": item["date"],
                "year_month": item["date"][:7],
                "country": "Egypt",
                "currency": "EGP",
                "currency_name": "이집트 파운드",
                "rate": float(item["rate"]),
                "frequency": "Daily",
                "source": item["source"]
            })
    print(f"이집트 CBE 공식 고시환율 파싱: {len(egp_items)} 건")

# 7. 결측치 필터링 및 중복 제거
valid_records = [r for r in all_records if r.get("rate") is not None and r["rate"] > 0]

unique_dict = {}
for r in valid_records:
    key = (r["country"], r["currency"], r["date"])
    unique_dict[key] = r

deduped = list(unique_dict.values())
deduped.sort(key=lambda x: (x["country"], x["date"]))
print(f"전체 6개국 순수 중앙은행 유효 레코드 수: {len(deduped)} 건")

# 8. secondary_data에 정제된 CSV 저장 (utf_8_sig)
cleaned_csv_path = os.path.join(secondary_dir, "cleaned_exchange_rates.csv")
with open(cleaned_csv_path, "w", encoding="utf_8_sig", newline="") as f:
    fieldnames = ["date", "year_month", "country", "currency", "currency_name", "rate", "frequency", "source"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(deduped)
print(f"정제된 데이터셋 저장 완료: {cleaned_csv_path}")

# 9. SQLite 데이터베이스 테이블 재생성 및 적재
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS exchange_rates")
cur.execute("""
CREATE TABLE exchange_rates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    year_month TEXT NOT NULL,
    country TEXT NOT NULL,
    currency TEXT NOT NULL,
    currency_name TEXT NOT NULL,
    rate REAL NOT NULL,
    frequency TEXT NOT NULL,
    source TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

insert_sql = """
INSERT INTO exchange_rates (date, year_month, country, currency, currency_name, rate, frequency, source)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

batch_data = [
    (
        r["date"],
        r["year_month"],
        r["country"],
        r["currency"],
        r["currency_name"],
        float(r["rate"]),
        r["frequency"],
        r["source"]
    )
    for r in deduped
]

cur.executemany(insert_sql, batch_data)

cur.execute("CREATE INDEX idx_rates_date ON exchange_rates(date)")
cur.execute("CREATE INDEX idx_rates_country ON exchange_rates(country)")
cur.execute("CREATE INDEX idx_rates_currency ON exchange_rates(currency)")
cur.execute("CREATE INDEX idx_rates_ym ON exchange_rates(year_month)")

conn.commit()

# 검증 카운트 출력
cur.execute("SELECT country, currency, count(*), min(date), max(date) FROM exchange_rates GROUP BY country, currency ORDER BY country")
summary_rows = cur.fetchall()
print("\n=== 6개국 중앙은행 공식 데이터베이스 적재 요약 ===")
for row in summary_rows:
    print(f"국가: {row[0]:12} | 통화: {row[1]:4} | 건수: {row[2]:6} | 시작일: {row[3]} | 종료일: {row[4]}")

conn.close()
print("=== 2단계 6개국 데이터베이스 구축 완료 ===")
