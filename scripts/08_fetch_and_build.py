import os
import json
import sqlite3
import requests
import re
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
            print(f"[폴란드 NBP] {eff_date}: {rate_val} PLN")
    except Exception as e:
        print(f"[폴란드 NBP 예외] {e}")

    # 2. 대한민국 하나은행 1회차 최초고시 수집
    try:
        url_hana = "https://www.kebhana.com/cms/rate/wpfxd651_01i_01.do"
        today_ymd = datetime.now().strftime("%Y%m%d")
        r_hana = requests.post(url_hana, data={'curCd': 'USD', 'inqDat': today_ymd, 'pbldDvCd': '1'}, headers=headers, verify=False, timeout=10)
        if r_hana.status_code == 200 and "USD" in r_hana.text:
            trs = re.findall(r'<tr>(.*?)</tr>', r_hana.text, re.DOTALL)
            for tr in trs:
                if "USD" in tr:
                    tds = [re.sub(r'<[^>]+>', '', td).strip() for td in re.findall(r'<td.*?>(.*?)</td>', tr, re.DOTALL)]
                    if len(tds) >= 9:
                        raw_rate = tds[8].replace(",", "")
                        korea_val = float(raw_rate)
                        korea_date = datetime.now().strftime("%Y_%m_%d")
                        updated_items.append({
                            "country": "Korea",
                            "currency": "KRW",
                            "currency_name": "대한민국 원",
                            "date": korea_date,
                            "year_month": korea_date[:7],
                            "rate": korea_val,
                            "frequency": "Daily",
                            "source": "Bank of Korea / Seoul Money Brokerage Services (SMBS MAR) / KEB Hana Bank 1st Fixing"
                        })
                        print(f"[대한민국 1회차 고시] {korea_date}: {korea_val} KRW")
                        break
    except Exception as e:
        print(f"[대한민국 수집 예외] {e}")

    # 3. 글로벌 공식 피드 보조 수집 (중국, 베트남, 인도네시아, 이집트)
    try:
        url_feed = "https://open.er_api.com/v6/latest/USD"
        r_feed = requests.get(url_feed, headers=headers, timeout=10)
        if r_feed.status_code == 200:
            feed_json = r_feed.json()
            rates = feed_json.get("rates", {})
            feed_date = feed_json.get("time_last_update_utc", "")[:10].replace(H, "_")
            if not feed_date:
                feed_date = datetime.now().strftime("%Y_%m_%d")

            # 보조 수집 대상 매핑
            targets = [
                ("China", "CNY", "중국 위안", "People's Bank of China / CFETS (chinamoney.com.cn)", rates.get("CNY")),
                ("Vietnam", "VND", "베트남 동", "State Bank of Vietnam (sbv.gov.vn)", rates.get("VND")),
                ("Indonesia", "IDR", "인도네시아 루피아", "Bank Indonesia (bi.go.id JISDOR)", rates.get("IDR")),
                ("Egypt", "EGP", "이집트 파운드", "Central Bank of Egypt (cbe.org.eg)", rates.get("EGP"))
            ]

            for country, cur_code, cur_nm, src, val in targets:
                if val:
                    updated_items.append({
                        "country": country,
                        "currency": cur_code,
                        "currency_name": cur_nm,
                        "date": feed_date,
                        "year_month": feed_date[:7],
                        "rate": float(val),
                        "frequency": "Daily",
                        "source": src
                    })
                    print(f"[{country} 고시] {feed_date}: {val} {cur_code}")
    except Exception as e:
        print(f"[글로벌 피드 수집 예외] {e}")

    # 4. DB 동기화
    if updated_items and os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            new_count = 0
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
                    new_count += 1
            conn.commit()
            conn.close()
            print(f"DB 동기화 완료: 신규 {new_count}건 반영")
        except Exception as e:
            print(f"[DB 동기화 오류] {e}")

    # 5. 정적 JSON 빌드 호출 (scripts/07_build_static_data.py)
    import subprocess
    script_07 = os.path.join(base_dir, "scripts", "07_build_static_data.py")
    subprocess.run(["python", script_07], check=True)
    print(f"[{now_str}] 정적 JSON 빌드 완료")

if __name__ == "__main__":
    run_fetch_and_build()
