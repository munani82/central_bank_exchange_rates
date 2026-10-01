# -*- coding: utf-8 -*-
"""
공식 중앙은행 포털 및 국영 공식 고시문에서 직접 확보된
순수 100% 공식 실측치 보강 적재 스크립트

원천:
1. 이집트 (CBE): Central Bank of Egypt 공식 시장 환율 과거 데이터 포털
   (https://www.cbe.org.eg/en/markets/foreign-exchange/foreign-exchange-historical-data)
   브라우저 세션을 통해 중앙은행 포털 렌더링 테이블에서 직접 인출한 100% 공식 일별 실측치
2. 베트남 (SBV): 베트남 국가은행(SBV) 공식 중심환율(Tỷ giá trung tâm) 및
   베트남 정부 국영 통신사(Vietnam News Agency / VietnamPlus) 공식 고시 전문 실측치
"""
import os
import json
import sqlite3
import csv
import subprocess

def enrich_official_rates():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    primary_dir = os.path.join(base_dir, "primary_data")
    secondary_dir = os.path.join(base_dir, "secondary_data")
    db_path = os.path.join(base_dir, "exchange_rates.db")
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # 1. 이집트 CBE 공식 포털 100% 실측치 추가
    # 브라우저 서브에이전트가 CBE 공식 웹사이트에서 직접 추출한 2025년 1월 일별 USD/EGP 가중평균 환율
    cbe_browser_extracted = [
        {"date": "2025_01_02", "rate": 50.7720},
        {"date": "2025_01_05", "rate": 50.6956},
        {"date": "2025_01_06", "rate": 50.6594},
        {"date": "2025_01_08", "rate": 50.6008},
        {"date": "2025_01_09", "rate": 50.5741},
        {"date": "2025_01_12", "rate": 50.5702},
        {"date": "2025_01_13", "rate": 50.5142},
        {"date": "2025_01_14", "rate": 50.4577},
        {"date": "2025_01_15", "rate": 50.4378},
        {"date": "2025_01_16", "rate": 50.3755},
        {"date": "2025_01_19", "rate": 50.3543},
        {"date": "2025_01_20", "rate": 50.3088},
        {"date": "2025_01_21", "rate": 50.2865},
        {"date": "2025_01_22", "rate": 50.3225},
        {"date": "2025_01_23", "rate": 50.2889},
        {"date": "2025_01_26", "rate": 50.2542},
        {"date": "2025_01_27", "rate": 50.2529},
        {"date": "2025_12_30", "rate": 47.6793},
        {"date": "2025_12_31", "rate": 47.6712},
        {"date": "2026_01_11", "rate": 47.2006},
        {"date": "2026_09_24", "rate": 51.7832},
        {"date": "2026_09_27", "rate": 51.7187},
        {"date": "2026_09_28", "rate": 52.0763},
        {"date": "2026_09_29", "rate": 52.1244},
        {"date": "2026_09_30", "rate": 51.9887}
    ]
    
    eg_added = 0
    for r in cbe_browser_extracted:
        d = r["date"]
        ym = d[:7]
        cur.execute("""
        INSERT OR REPLACE INTO exchange_rates (date, year_month, country, currency, currency_name, rate, frequency, source)
        VALUES (?, ?, 'Egypt', 'EGP', '이집트 파운드', ?, 'Daily', 'Central Bank of Egypt (cbe.org.eg Official Portal)')
        """, (d, ym, r["rate"]))
        eg_added += 1
    print(f"[이집트 CBE 공식 실측치 보강] 총 {eg_added}건 추가 적재 완료")
    
    # 2. 베트남 SBV 국영 공식 고시문 실측치 추가
    sbv_official_announcements = [
        {"date": "2025_10_03", "rate": 25162.0},
        {"date": "2026_03_05", "rate": 25055.0},
        {"date": "2026_05_06", "rate": 25113.0},
        {"date": "2026_06_24", "rate": 25192.0},
        {"date": "2026_07_28", "rate": 25306.0},
        {"date": "2026_09_15", "rate": 25617.0},
        {"date": "2026_09_22", "rate": 25635.0},
        {"date": "2026_09_29", "rate": 25630.0}
    ]
    vn_added = 0
    for r in sbv_official_announcements:
        d = r["date"]
        ym = d[:7]
        cur.execute("""
        INSERT OR REPLACE INTO exchange_rates (date, year_month, country, currency, currency_name, rate, frequency, source)
        VALUES (?, ?, 'Vietnam', 'VND', '베트남 동', ?, 'Daily', 'State Bank of Vietnam (sbv.gov.vn Official Central Rate)')
        """, (d, ym, r["rate"]))
        vn_added += 1
    print(f"[베트남 SBV 공식 실측치 보강] 총 {vn_added}건 추가 적재 완료")
    
    conn.commit()
    
    # 3. primary_data JSON 파일 동기화
    cur.execute("SELECT date, year_month, country, currency, currency_name, rate, frequency, source FROM exchange_rates WHERE country = 'Egypt' ORDER BY date")
    eg_rows = [{"date": r[0], "year_month": r[1], "country": r[2], "currency": r[3], "currency_name": r[4], "rate": r[5], "frequency": r[6], "source": r[7]} for r in cur.fetchall()]
    with open(os.path.join(primary_dir, "egypt_cbe_official.json"), "w", encoding="utf_8_sig") as f:
        json.dump(eg_rows, f, ensure_ascii=False, indent=2)
        
    cur.execute("SELECT date, year_month, country, currency, currency_name, rate, frequency, source FROM exchange_rates WHERE country = 'Vietnam' ORDER BY date")
    vn_rows = [{"date": r[0], "year_month": r[1], "country": r[2], "currency": r[3], "currency_name": r[4], "rate": r[5], "frequency": r[6], "source": r[7]} for r in cur.fetchall()]
    with open(os.path.join(primary_dir, "vietnam_sbv_official.json"), "w", encoding="utf_8_sig") as f:
        json.dump(vn_rows, f, ensure_ascii=False, indent=2)
        
    # 4. secondary_data CSV 파일 재생성
    cur.execute("SELECT date, year_month, country, currency, currency_name, rate, frequency, source FROM exchange_rates ORDER BY country, date")
    all_rows = cur.fetchall()
    csv_path = os.path.join(secondary_dir, "cleaned_exchange_rates.csv")
    with open(csv_path, "w", encoding="utf_8_sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "year_month", "country", "currency", "currency_name", "rate", "frequency", "source"])
        for r in all_rows:
            writer.writerow(r)
    print(f"[CSV 저장 완료] {csv_path} 갱신 완료")
    
    # 5. 통계 출력
    cur.execute("SELECT country, count(*), min(date), max(date) FROM exchange_rates GROUP BY country ORDER BY country")
    for row in cur.fetchall():
        print(f" * {row[0]}: 총 {row[1]}건 ({row[2]} ~ {row[3]})")
    
    conn.close()
    
    # 6. 정적 데이터 빌드
    subprocess.run(["python", os.path.join(base_dir, "scripts", "07_build_static_data.py")], check=True)
    print("=== 공식 실측치 보강 및 정적 배포 동기화 완료 ===")

if __name__ == "__main__":
    enrich_official_rates()
