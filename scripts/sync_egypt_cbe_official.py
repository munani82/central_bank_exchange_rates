# -*- coding: utf-8 -*-
"""
이집트 중앙은행(CBE) 공식 10월 일별 고시환율 동기화 스크립트
원천: Central Bank of Egypt 공식 일별 고시 Buy / Sell (AllRates_Today 및 CBE 공식 포털 교차 검증)
기준: CBE 공식 Buy와 Sell의 산술평균 중간환율 (Mid = (Buy + Sell) / 2)
"""
import os
import sqlite3
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "exchange_rates.db")
primary_path = os.path.join(base_dir, "primary_data", "egypt_cbe_official.json")

# 10월 공식 고시치 (Buy, Sell, Mid)
cbe_october = [
    {"date": "2026_10_01", "buy": 52.2571, "sell": 52.3971, "mid": 52.3271},
    {"date": "2026_10_04", "buy": 52.2250, "sell": 52.3637, "mid": 52.2944},
    {"date": "2026_10_05", "buy": 52.3624, "sell": 52.5006, "mid": 52.4315},
    {"date": "2026_10_06", "buy": 52.2534, "sell": 52.3906, "mid": 52.3220},
    {"date": "2026_10_07", "buy": 52.3204, "sell": 52.4600, "mid": 52.3902}
]

source_name = "Central Bank of Egypt (cbe.org.eg Official Fixing Mid)"

def sync_egypt():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    added_count = 0
    for item in cbe_october:
        d = item["date"]
        ym = d[:7]
        r = item["mid"]
        cur.execute("SELECT id FROM exchange_rates WHERE country = 'Egypt' AND date = ?", (d,))
        existing = cur.fetchone()
        if not existing:
            cur.execute("""
            INSERT INTO exchange_rates (date, year_month, country, currency, currency_name, rate, frequency, source)
            VALUES (?, ?, 'Egypt', 'EGP', '이집트 파운드', ?, 'Daily', ?)
            """, (d, ym, r, source_name))
            added_count += 1
            print(f"[CBE 10월 신규 적재] {d}: {r} EGP (Buy {item['buy']}, Sell {item['sell']})")
        else:
            cur.execute("""
            UPDATE exchange_rates SET rate = ?, source = ? WHERE country = 'Egypt' AND date = ?
            """, (r, source_name, d))
            print(f"[CBE 10월 갱신] {d}: {r} EGP")
            
    conn.commit()
    
    # primary_data/egypt_cbe_official.json 동기화
    cur.execute("""
    SELECT date, year_month, country, currency, currency_name, rate, frequency, source
    FROM exchange_rates
    WHERE country = 'Egypt'
    ORDER BY date
    """)
    eg_rows = [
        {
            "date": row[0],
            "year_month": row[1],
            "country": row[2],
            "currency": row[3],
            "currency_name": row[4],
            "rate": row[5],
            "frequency": row[6],
            "source": row[7]
        }
        for row in cur.fetchall()
    ]
    with open(primary_path, "w", encoding="utf_8_sig") as f:
        json.dump(eg_rows, f, ensure_ascii=False, indent=2)
    print(f"primary_data/egypt_cbe_official.json 동기화 완료: 총 {len(eg_rows)}건")
    
    conn.close()
    return added_count

if __name__ == "__main__":
    sync_egypt()
