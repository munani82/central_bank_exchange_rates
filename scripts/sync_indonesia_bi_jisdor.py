# -*- coding: utf-8 -*-
"""
인도네시아 Bank Indonesia 공식 JISDOR 페이지 표를 그대로 파싱하여 DB에 동기화.
원천: https://www.bi.go.id/id/statistik/informasi-kurs/jisdor/default.aspx
표에 실제로 표시된 날짜와 값만 적재. 시장환율, 보간, 추정 일절 없음.
검증: 이미 DB에 있는 날짜의 값이 표와 다르면 덮어쓰지 않고 불일치로 보고.
"""
import os
import re
import sqlite3
import requests
import urllib3

urllib3.disable_warnings()
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(BASE, "exchange_rates.db")
URL = "https://www.bi.go.id/id/statistik/informasi-kurs/jisdor/default.aspx"
SOURCE = "Bank Indonesia (bi.go.id JISDOR)"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
           "Accept": "text/html"}
BULAN = {"Januari": 1, "Februari": 2, "Maret": 3, "April": 4, "Mei": 5, "Juni": 6, "Juli": 7,
         "Agustus": 8, "September": 9, "Oktober": 10, "November": 11, "Desember": 12}


def fetch_bi_jisdor():
    t = requests.get(URL, headers=HEADERS, verify=False, timeout=20).text
    out = []
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", t, re.S):
        txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", row)).strip()
        m = re.match(r"(\d{1,2}) (\w+) (\d{4}) Rp([\d.]+),(\d{2})$", txt)
        if m and m.group(2) in BULAN:
            d = f"{m.group(3)}_{BULAN[m.group(2)]:02d}_{int(m.group(1)):02d}"
            out.append((d, float(m.group(4).replace(".", "") + "." + m.group(5))))
    return out


def sync(rows):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    added, mismatches = [], []
    for d, v in rows:
        cur.execute("SELECT rate FROM exchange_rates WHERE country='Indonesia' AND date=?", (d,))
        ex = cur.fetchone()
        if ex is None:
            cur.execute("""INSERT INTO exchange_rates
                (date, year_month, country, currency, currency_name, rate, frequency, source)
                VALUES (?, ?, 'Indonesia', 'IDR', '인도네시아 루피아', ?, 'Daily', ?)""", (d, d[:7], v, SOURCE))
            added.append((d, v))
        elif abs(ex[0] - v) > 1e-9:
            mismatches.append((d, ex[0], v))
    conn.commit()
    conn.close()
    return added, mismatches


if __name__ == "__main__":
    rows = fetch_bi_jisdor()
    if not rows:
        raise SystemExit("BI JISDOR 표 파싱 실패: 적재하지 않음")
    added, mism = sync(rows)
    for a in added:
        print("추가", a)
    for m in mism:
        print("불일치(미반영) 날짜/DB/BI", m)
    print(f"표 {len(rows)}행 확인, 신규 {len(added)}건, 불일치 {len(mism)}건")
