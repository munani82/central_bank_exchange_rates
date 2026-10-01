# -*- coding: utf-8 -*-
"""
이집트 중앙은행(CBE) 공식 포털에서 브라우저를 통해 직접 전수 추출한
2025년 1월 ~ 2026년 9월 30일 전체 공식 일별 실측치(434행) 데이터베이스 및 primary_data 일괄 적재 스크립트
"""
import re
import json
import sqlite3
import os

def load_cbe_all():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    primary_dir = os.path.join(base_dir, "primary_data")
    db_path = os.path.join(base_dir, "exchange_rates.db")
    scratch_path = r"C:\Users\Enduser\.gemini\antigravity-ide\brain\18d06914-4b5c-4ed9-adfa-4f9d8b1320b9\browser\scratchpad_zyj8nmj5.md"
    
    with open(scratch_path, "r", encoding="utf-8") as f:
        text = f.read()

    matches = re.findall(r"(\d{4}_\d{2}_\d{2}):\s*([\d.]+)", text)
    print(f"스크래치패드에서 추출된 CBE 행 수: {len(matches)}건")
    if matches:
        print(f"최초 고시: {matches[-1][0]} = {matches[-1][1]} EGP")
        print(f"최신 고시: {matches[0][0]} = {matches[0][1]} EGP")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    inserted = 0
    for d, r in matches:
        ym = d[:7]
        rate_val = float(r)
        cur.execute("""
        INSERT OR REPLACE INTO exchange_rates (date, year_month, country, currency, currency_name, rate, frequency, source)
        VALUES (?, ?, 'Egypt', 'EGP', '이집트 파운드', ?, 'Daily', 'Central Bank of Egypt (cbe.org.eg Official Portal)')
        """, (d, ym, rate_val))
        inserted += 1
        
    conn.commit()
    print(f"DB에 적재/갱신된 이집트 CBE 실측치: {inserted}건")
    
    # primary_data/egypt_cbe_official.json 갱신
    cur.execute("""
    SELECT date, year_month, country, currency, currency_name, rate, frequency, source 
    FROM exchange_rates 
    WHERE country = 'Egypt' 
    ORDER BY date
    """)
    eg_rows = [
        {
            "date": r[0],
            "year_month": r[1],
            "country": r[2],
            "currency": r[3],
            "currency_name": r[4],
            "rate": r[5],
            "frequency": r[6],
            "source": r[7]
        }
        for r in cur.fetchall()
    ]
    with open(os.path.join(primary_dir, "egypt_cbe_official.json"), "w", encoding="utf_8_sig") as f:
        json.dump(eg_rows, f, ensure_ascii=False, indent=2)
    print(f"primary_data/egypt_cbe_official.json 동기화 완료: 총 {len(eg_rows)}건")
    
    conn.close()

if __name__ == "__main__":
    load_cbe_all()
