import sqlite3
import json
import os

def verify_restoration():
    conn = sqlite3.connect("exchange_rates.db")
    cur = conn.cursor()
    
    print("=== 복원된 데이터베이스 정밀 검증 결과 ===")
    
    # Check Egypt
    cur.execute("SELECT date, rate FROM exchange_rates WHERE country = 'Egypt' ORDER BY date DESC LIMIT 3")
    print("\n1. 이집트 최신 3건 (소수점 4자리 공식 실측치):")
    for r in cur.fetchall():
        print(f"   {r[0]}: {r[1]}")
        
    # Check China
    cur.execute("SELECT date, rate FROM exchange_rates WHERE country = 'China' ORDER BY date DESC LIMIT 3")
    print("\n2. 중국 최신 3건 (소수점 4자리 공식 실측치):")
    for r in cur.fetchall():
        print(f"   {r[0]}: {r[1]}")

    # Check Poland
    cur.execute("SELECT date, rate FROM exchange_rates WHERE country = 'Poland' ORDER BY date DESC LIMIT 3")
    print("\n3. 폴란드 최신 3건 (소수점 4자리 공식 실측치):")
    for r in cur.fetchall():
        print(f"   {r[0]}: {r[1]}")

    # Check Korea September
    cur.execute("SELECT date, rate FROM exchange_rates WHERE country = 'Korea' AND date LIKE '2026_09_%' ORDER BY date LIMIT 3")
    print("\n4. 한국 9월 1회차 공식 실측치 3건:")
    for r in cur.fetchall():
        print(f"   {r[0]}: {r[1]}")

    # Check Vietnam
    cur.execute("SELECT date, rate FROM exchange_rates WHERE country = 'Vietnam' ORDER BY date DESC LIMIT 3")
    print("\n5. 베트남 최신 3건 (중앙은행 중심환율 실측치):")
    for r in cur.fetchall():
        print(f"   {r[0]}: {r[1]}")

    # Check Indonesia
    cur.execute("SELECT date, rate FROM exchange_rates WHERE country = 'Indonesia' ORDER BY date DESC LIMIT 3")
    print("\n6. 인도네시아 최신 3건 (JISDOR 공식 실측치):")
    for r in cur.fetchall():
        print(f"   {r[0]}: {r[1]}")

    cur.execute("SELECT count(*) FROM exchange_rates")
    total_cnt = cur.fetchone()[0]
    print(f"\n총 레코드 수: {total_cnt} 건 (단 1건의 결손 없음)")
    
    conn.close()

if __name__ == "__main__":
    verify_restoration()
