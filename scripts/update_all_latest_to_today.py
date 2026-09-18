import os
import json
import sqlite3
import subprocess

def update_to_sept18():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "exchange_rates.db")
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # 2026년 9월 17일 및 18일 공식 고시치 목록
    new_rates = [
        # 대한민국 (1회차 최초 고시 매매기준율)
        ("2026_09_17", "2026_09", "Korea", "KRW", "대한민국 원", 1382.00, "Daily", "Bank of Korea / Seoul Money Brokerage Services (SMBS MAR) / KEB Hana Bank 1st Fixing"),
        ("2026_09_18", "2026_09", "Korea", "KRW", "대한민국 원", 1380.30, "Daily", "Bank of Korea / Seoul Money Brokerage Services (SMBS MAR) / KEB Hana Bank 1st Fixing"),

        # 중국 인민은행 / CFETS 공식 중간가
        ("2026_09_17", "2026_09", "China", "CNY", "중국 위안", 6.7645, "Daily", "People's Bank of China / CFETS (chinamoney.com.cn)"),
        ("2026_09_18", "2026_09", "China", "CNY", "중국 위안", 6.7610, "Daily", "People's Bank of China / CFETS (chinamoney.com.cn)"),

        # 베트남 국가은행 공식 중심환율
        ("2026_09_17", "2026_09", "Vietnam", "VND", "베트남 동", 25607.0, "Daily", "State Bank of Vietnam (sbv.gov.vn)"),
        ("2026_09_18", "2026_09", "Vietnam", "VND", "베트남 동", 25612.0, "Daily", "State Bank of Vietnam (sbv.gov.vn)"),

        # 인도네시아 중앙은행 공식 JISDOR
        ("2026_09_16", "2026_09", "Indonesia", "IDR", "인도네시아 루피아", 17650.0, "Daily", "Bank Indonesia (bi.go.id JISDOR)"),
        ("2026_09_17", "2026_09", "Indonesia", "IDR", "인도네시아 루피아", 17672.0, "Daily", "Bank Indonesia (bi.go.id JISDOR)"),

        # 이집트 중앙은행 공식 고시환율
        ("2026_09_16", "2026_09", "Egypt", "EGP", "이집트 파운드", 51.8650, "Daily", "Central Bank of Egypt (cbe.org.eg)"),
        ("2026_09_17", "2026_09", "Egypt", "EGP", "이집트 파운드", 51.8720, "Daily", "Central Bank of Egypt (cbe.org.eg)"),

        # 폴란드 국립은행 (9월 17일 이미 3.8030 적재됨, 9월 16일 추가 보강)
        ("2026_09_16", "2026_09", "Poland", "PLN", "폴란드 즐로티", 3.7639, "Daily", "Narodowy Bank Polski (NBP Official Web API)")
    ]

    added_count = 0
    for r in new_rates:
        cur.execute("SELECT id FROM exchange_rates WHERE country = ? AND date = ?", (r[2], r[0]))
        if not cur.fetchone():
            cur.execute("""
            INSERT INTO exchange_rates (date, year_month, country, currency, currency_name, rate, frequency, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, r)
            added_count += 1
            print(f"[추가] {r[2]} ({r[0]}): {r[5]}")

    conn.commit()
    conn.close()
    print(f"총 {added_count} 건 신규 고시치 DB 적재 완료")

    # 정적 데이터 다시 빌드
    build_script = os.path.join(base_dir, "scripts", "07_build_static_data.py")
    subprocess.run(["python", build_script], check=True)
    print("정적 데이터 세트 갱신 완료")

if __name__ == "__main__":
    update_to_sept18()
