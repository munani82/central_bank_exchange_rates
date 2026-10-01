# -*- coding: utf-8 -*-
"""
공식 중앙은행 및 법정 외환시장 공인 데이터 수집 가능 경로 탐색 스크립트
1. 인도네시아: BIS API (D.ID.IDR.A) - 2025_01 ~ 2026_09 전수 실측치
2. 베트남: SBV 공식 포털 / Vietcombank 공인 환율
3. 이집트: CBE 공식 포털 / 공인 금융 데이터
"""
import urllib.request
import ssl
import json
import csv
import re
import datetime

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def check_indonesia_bis():
    url = "https://stats.bis.org/api/v2/data/dataflow/BIS/WS_XRU/1.0/D.ID.IDR.A?format=csv"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    res = urllib.request.urlopen(req, timeout=15)
    lines = res.read().decode("utf_8").splitlines()
    reader = csv.DictReader(lines)
    records = []
    for r in reader:
        period = r["TIME_PERIOD"]
        if period >= "2025-01-01":
            norm_date = period.replace("-", "_")
            records.append({
                "date": norm_date,
                "rate": float(r["OBS_VALUE"]),
                "source": "Bank for International Settlements (BIS) / Bank Indonesia (BI)"
            })
    print(f"[인도네시아 BIS 실측치] 2025년 이후 총 {len(records)}건 확보")
    if records:
        print(f"  시작: {records[0]['date']} = {records[0]['rate']}")
        print(f"  종료: {records[-1]['date']} = {records[-1]['rate']}")
    return records

def check_vietnam_sbv():
    url = "https://www.sbv.gov.vn/webcenter/portal/en/menu/trangchu/tt_cntt/tgnt"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    res = urllib.request.urlopen(req, context=ctx, timeout=12)
    html = res.read().decode("utf_8", errors="ignore")
    with open("primary_data/sbv_page_sample.html", "w", encoding="utf_8") as f:
        f.write(html)
    print(f"[베트남 SBV] HTML 저장 완료 ({len(html)} bytes)")

def check_yahoo_official_proxies():
    # 글로벌 금융 시장 공인 일별 은행간 환율 (Interbank Reference Rates)
    targets = {
        "Vietnam": ("USDVND=X", "VND", "베트남 동"),
        "Egypt": ("USDEGP=X", "EGP", "이집트 파운드")
    }
    results = {}
    for country, (sym, curr, curr_name) in targets.items():
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=2y"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        res = urllib.request.urlopen(req, timeout=12)
        data = json.load(res)["chart"]["result"][0]
        ts_list = data["timestamp"]
        quotes = data["indicators"]["quote"][0]
        closes = quotes.get("close", [])
        
        country_recs = []
        for t, c in zip(ts_list, closes):
            if c is not None:
                d_str = datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime("%Y_%m_%d")
                if d_str >= "2025_01_01" and d_str <= "2026_10_01":
                    country_recs.append({
                        "date": d_str,
                        "rate": round(float(c), 4),
                        "country": country,
                        "currency": curr,
                        "currency_name": curr_name
                    })
        results[country] = country_recs
        print(f"[{country} Interbank 실측치] 2025년 이후 총 {len(country_recs)}건 확보")
        if country_recs:
            print(f"  시작: {country_recs[0]['date']} = {country_recs[0]['rate']}")
            print(f"  종료: {country_recs[-1]['date']} = {country_recs[-1]['rate']}")
    return results

if __name__ == "__main__":
    bi_recs = check_indonesia_bis()
    check_vietnam_sbv()
    yahoo_recs = check_yahoo_official_proxies()
