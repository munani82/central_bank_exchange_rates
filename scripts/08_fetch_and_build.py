import os
import json
import sqlite3
import requests
import urllib3
from datetime import datetime

urllib3.disable_warnings()

def run_fetch_and_build():
    H = chr(45)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "exchange_rates.db")
    static_data_dir = os.path.join(base_dir, "static", "data")
    os.makedirs(static_data_dir, exist_ok=True)

    headers = {'User_Agent': 'Mozilla/5.0'}
    updated_items = []
    now_str = datetime.now().strftime("%Y_%m_%d %H:%M:%S")

    # 1. 폴란드 NBP 공식 Web API 수집
    try:
        url_nbp = "https://api.nbp.pl/api/exchangerates/rates/a/usd/?format=json"
        r = requests.get(url_nbp, headers=headers, verify=False, timeout=10)
        if r.status_code == 200:
            rate_info = r.json().get("rates", [])[0]
            eff_date = rate_info["effectiveDate"].replace(H, "_")
            rate_val = float(rate_info["mid"])
            updated_items.append({
                "country": "Poland",
                "currency": "PLN",
                "currency_name": "폴란드 즐로티",
                "date": eff_date,
                "year_month": eff_date[:7],
                "rate": rate_val,
                "frequency": "Daily",
                "source": "Narodowy Bank Polski (NBP Official Web API)"
            })
            print(f"[폴란드 NBP 수집 성공] {eff_date}: {rate_val} PLN")
    except Exception as e:
        print(f"[폴란드 NBP 수집 경고] {e}")

    # 2. DB 반영
    if updated_items and os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            for item in updated_items:
                cur.execute("SELECT id FROM exchange_rates WHERE country = ? AND date = ?", (item["country"], item["date"]))
                if not cur.fetchone():
                    cur.execute("""
                    INSERT INTO exchange_rates (date, year_month, country, currency, currency_name, rate, frequency, source)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        item["date"],
                        item["year_month"],
                        item["country"],
                        item["currency"],
                        item["currency_name"],
                        item["rate"],
                        item["frequency"],
                        item["source"]
                    ))
            conn.commit()
            conn.close()
            print("DB 동기화 완료")
        except Exception as e:
            print(f"[DB 동기화 오류] {e}")

    # 3. 정적 JSON 빌드 호출 (scripts/07_build_static_data.py 실행)
    import subprocess
    script_07 = os.path.join(base_dir, "scripts", "07_build_static_data.py")
    subprocess.run(["python", script_07], check=True)
    print(f"[{now_str}] 정적 JSON 빌드 완료")

if __name__ == "__main__":
    run_fetch_and_build()
