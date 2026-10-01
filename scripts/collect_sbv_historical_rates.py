import requests
import urllib3
import re
import json
import sqlite3
import time
import os
import sys

urllib3.disable_warnings()

headers = {
    'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

def log_msg(msg):
    timestamp = time.strftime('%Y_%m_%d %H:%M:%S')
    line = f"[{timestamp}] {msg}"
    print(line, flush=True)
    with open("collect_sbv.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")

def fetch_vietnamplus_archive():
    log_msg("=== VietnamPlus 국영통신사 공식 중심환율 검색 시작 ===")
    results = {}
    
    # 2025년 및 2026년 키워드로 검색
    keywords = ["ty-gia-trung-tam", "ty-gia-ngan-hang-nha-nuoc"]
    for kw in keywords:
        for page in range(1, 30):
            url = f"https://www.vietnamplus.vn/{kw}/trang{page}.vnp"
            try:
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code != 200:
                    continue
                # 기사 링크 추출
                links = re.findall(r'href=["\'](/[^"\']*post\d+\.vnp)["\']', r.text)
                for l in set(links):
                    full_url = f"https://www.vietnamplus.vn{l}"
                    try:
                        ar = requests.get(full_url, headers=headers, timeout=8)
                        if ar.status_code == 200:
                            # 날짜와 환율 매칭
                            # 날짜: dd/mm/yyyy
                            date_m = re.search(r'(\d{2}/\d{2}/\d{4})', ar.text)
                            # 환율: tỷ giá trung tâm ... 25.xxx 또는 25,xxx
                            rate_m = re.search(r'tỷ giá trung tâm.*?(\d{2}[.,]\d{3})', ar.text, re.IGNORECASE)
                            if not rate_m:
                                rate_m = re.search(r'trung tâm.*?ở mức.*?(\d{2}[.,]\d{3})', ar.text, re.IGNORECASE)
                            
                            if date_m and rate_m:
                                d_str = date_m.group(1)
                                r_str = rate_m.group(1).replace('.', '').replace(',', '')
                                r_val = float(r_str)
                                p = d_str.split('/')
                                norm_date = f"{p[2]}_{p[1]}_{p[0]}"
                                if (norm_date.startswith("2025_") or norm_date.startswith("2026_")) and 24000 <= r_val <= 27000:
                                    results[norm_date] = r_val
                                    log_msg(f"발견: {norm_date} -> {r_val} VND ({full_url})")
                    except Exception:
                        pass
                time.sleep(0.5)
            except Exception as e:
                log_msg(f"에러: {e}")
    return results

def main():
    log_msg("SBV 과거 중심환율 백그라운드 수집기 기동")
    res = fetch_vietnamplus_archive()
    log_msg(f"수집 완료, 총 {len(res)}건 확보")
    
    # DB 적재
    if res:
        conn = sqlite3.connect("exchange_rates.db")
        cur = conn.cursor()
        inserted = 0
        for d, val in sorted(res.items()):
            cur.execute("""
                INSERT OR REPLACE INTO exchange_rates (date, country, currency, rate, source)
                VALUES (?, 'Vietnam', 'VND', ?, 'State Bank of Vietnam (sbv.gov.vn Official Central Rate)')
            """, (d, val))
            inserted += 1
        conn.commit()
        conn.close()
        log_msg(f"DB 반영 완료: {inserted}건")

if __name__ == "__main__":
    main()
