# -*- coding: utf-8 -*-
"""
폴란드 NBP 공식 Table A (USD mid) 기간 조회 결과를 그대로 DB에 동기화.
원천: https://api.nbp.pl/api/exchangerates/rates/a/usd/{start}/{end}/
값의 가공, 보간, 반올림을 일절 하지 않음. API에 없는 날짜는 적재하지 않음.
사용: python scripts/sync_poland_nbp_official.py 2026-10-01 2026-10-08
"""
import os
import sys
import sqlite3
import requests

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(BASE, "exchange_rates.db")
SOURCE = "Narodowy Bank Polski (NBP Official Web API)"


def main(start, end):
    url = f"https://api.nbp.pl/api/exchangerates/rates/a/usd/{start}/{end}/?format=json"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    rates = r.json()["rates"]
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    for x in rates:
        d = x["effectiveDate"].replace(chr(45), "_")
        cur.execute("SELECT id FROM exchange_rates WHERE country='Poland' AND date=?", (d,))
        if cur.fetchone():
            cur.execute("UPDATE exchange_rates SET rate=?, source=? WHERE country='Poland' AND date=?",
                        (float(x["mid"]), SOURCE, d))
        else:
            cur.execute("""INSERT INTO exchange_rates
                (date, year_month, country, currency, currency_name, rate, frequency, source)
                VALUES (?, ?, 'Poland', 'PLN', '폴란드 즐로티', ?, 'Daily', ?)""",
                        (d, d[:7], float(x["mid"]), SOURCE))
        print(f"{d} {x['no']} mid={x['mid']}")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
