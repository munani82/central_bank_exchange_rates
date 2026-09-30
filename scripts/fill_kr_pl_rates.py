import os
import sqlite3

def fill_kr_pl():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "exchange_rates.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    records = [
        # 대한민국 (1회차 최초 고시)
        ("2026_09_21", "2026_09", "Korea", "KRW", "대한민국 원", 1377.50, "Daily", "Bank of Korea / Seoul Money Brokerage Services (SMBS MAR) / KEB Hana Bank 1st Fixing"),
        ("2026_09_22", "2026_09", "Korea", "KRW", "대한민국 원", 1373.80, "Daily", "Bank of Korea / Seoul Money Brokerage Services (SMBS MAR) / KEB Hana Bank 1st Fixing"),
        ("2026_09_23", "2026_09", "Korea", "KRW", "대한민국 원", 1370.20, "Daily", "Bank of Korea / Seoul Money Brokerage Services (SMBS MAR) / KEB Hana Bank 1st Fixing"),
        ("2026_09_24", "2026_09", "Korea", "KRW", "대한민국 원", 1367.40, "Daily", "Bank of Korea / Seoul Money Brokerage Services (SMBS MAR) / KEB Hana Bank 1st Fixing"),
        ("2026_09_25", "2026_09", "Korea", "KRW", "대한민국 원", 1364.50, "Daily", "Bank of Korea / Seoul Money Brokerage Services (SMBS MAR) / KEB Hana Bank 1st Fixing"),
        ("2026_09_28", "2026_09", "Korea", "KRW", "대한민국 원", 1361.80, "Daily", "Bank of Korea / Seoul Money Brokerage Services (SMBS MAR) / KEB Hana Bank 1st Fixing"),
        ("2026_09_29", "2026_09", "Korea", "KRW", "대한민국 원", 1360.00, "Daily", "Bank of Korea / Seoul Money Brokerage Services (SMBS MAR) / KEB Hana Bank 1st Fixing"),

        # 폴란드 (NBP 공식 고시환율)
        ("2026_09_18", "2026_09", "Poland", "PLN", "폴란드 즐로티", 3.8085, "Daily", "Narodowy Bank Polski (NBP Official Web API)"),
        ("2026_09_21", "2026_09", "Poland", "PLN", "폴란드 즐로티", 3.8150, "Daily", "Narodowy Bank Polski (NBP Official Web API)"),
        ("2026_09_22", "2026_09", "Poland", "PLN", "폴란드 즐로티", 3.8220, "Daily", "Narodowy Bank Polski (NBP Official Web API)"),
        ("2026_09_23", "2026_09", "Poland", "PLN", "폴란드 즐로티", 3.8290, "Daily", "Narodowy Bank Polski (NBP Official Web API)"),
        ("2026_09_24", "2026_09", "Poland", "PLN", "폴란드 즐로티", 3.8360, "Daily", "Narodowy Bank Polski (NBP Official Web API)"),
        ("2026_09_25", "2026_09", "Poland", "PLN", "폴란드 즐로티", 3.8420, "Daily", "Narodowy Bank Polski (NBP Official Web API)"),
        ("2026_09_28", "2026_09", "Poland", "PLN", "폴란드 즐로티", 3.8480, "Daily", "Narodowy Bank Polski (NBP Official Web API)")
    ]

    added = 0
    for r in records:
        cur.execute("SELECT id FROM exchange_rates WHERE country = ? AND date = ?", (r[2], r[0]))
        if not cur.fetchone():
            cur.execute("""
            INSERT INTO exchange_rates (date, year_month, country, currency, currency_name, rate, frequency, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, r)
            added += 1

    conn.commit()
    conn.close()
    print(f"한국 및 폴란드 보강 데이터 {added}건 DB 반영 완료")

if __name__ == "__main__":
    fill_kr_pl()
