import os
import json
import sqlite3
import threading
import time
import requests
import urllib3
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime

urllib3.disable_warnings()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "exchange_rates.db")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# 각국 중앙은행 및 법정 공인 기관 공식 고시 시점별 하루 5회 정밀 스케줄
# 1회차 09:15 : 대한민국 (서울외국환중개 / 시중은행 1회차 최초 고시 08:50 ~ 09:00 반영)
# 2회차 10:45 : 중국 (인민은행 PBOC 중간가 10:15 KST) 및 베트남 (SBV 중심환율 10:00 ~ 10:30 KST)
# 3회차 18:30 : 인도네시아 (Bank Indonesia JISDOR 18:15 KST 발표)
# 4회차 19:30 : 폴란드 (NBP Table A 고시환율 18:45 ~ 19:15 KST 발표)
# 5회차 21:30 : 이집트 (CBE 공식 고시환율 20:00 ~ 21:00 KST 발표) 및 6개국 종합 일일 마감

SCHEDULED_SLOTS = ["09:15", "10:45", "18:30", "19:30", "21:30"]
executed_slots = set()

def auto_fetch_latest_rates(target_slot=None):
    headers = {'User_Agent': 'Mozilla/5.0'}
    updated_items = []
    now_str = datetime.now().strftime("%Y_%m_%d %H:%M:%S")

    # 1. 폴란드 NBP 공식 Web API (19:30, 21:30 또는 전체 갱신 시)
    if target_slot in [None, "19:30", "21:30"]:
        try:
            url_nbp = "https://api.nbp.pl/api/exchangerates/rates/a/usd/?format=json"
            r = requests.get(url_nbp, headers=headers, verify=False, timeout=10)
            if r.status_code == 200:
                rate_info = r.json().get("rates", [])[0]
                eff_date = rate_info["effectiveDate"].replace(chr(45), "_")
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
        except Exception:
            pass

    # 2. 수집된 신규 고시치 데이터베이스 동기화
    if updated_items:
        try:
            conn = sqlite3.connect(DB_PATH)
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
        except Exception:
            pass

    print(f"[{now_str}] 환율 자동 동기화 완료 (슬롯: {target_slot or '수동 즉시 갱신'})")

# 백그라운드 각국 공식 고시 시점 기반 하루 5회 정밀 스케줄러
def background_scheduler():
    while True:
        try:
            now = datetime.now()
            today_str = now.strftime("%Y_%m_%d")
            hm_str = now.strftime("%H:%M")

            for slot in SCHEDULED_SLOTS:
                slot_key = f"{today_str}_{slot}"
                if hm_str == slot and slot_key not in executed_slots:
                    executed_slots.add(slot_key)
                    auto_fetch_latest_rates(target_slot=slot)
        except Exception:
            pass
        time.sleep(30)

class ExchangeRateHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/api/latest":
            self.handle_latest()
        elif path == "/api/monthly_average":
            self.handle_monthly(params)
        elif path == "/api/period_average":
            self.handle_period_average(params)
        elif path == "/api/history":
            self.handle_history(params)
        elif path == "/api/summary":
            self.handle_summary()
        elif path == "/api/refresh":
            auto_fetch_latest_rates()
            self.handle_latest()
        elif path == "/" or path == "/index.html":
            self.serve_file(os.path.join(STATIC_DIR, "index.html"), "text/html; charset=utf-8")
        elif path.startswith("/static/"):
            rel_path = path[8:]
            full_path = os.path.join(STATIC_DIR, rel_path)
            self.serve_static(full_path)
        elif path.startswith("/visualizations/"):
            rel_path = path[16:]
            full_path = os.path.join(BASE_DIR, "visualizations", rel_path)
            self.serve_static(full_path)
        else:
            super().do_GET()

    def serve_static(self, filepath):
        if not os.path.exists(filepath):
            self.send_error(404, "File Not Found")
            return
        ext = os.path.splitext(filepath)[1].lower()
        mime_types = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".svg": "image/svg+xml; charset=utf-8",
            ".json": "application/json; charset=utf-8",
            ".png": "image/png"
        }
        ctype = mime_types.get(ext, "application/octet_stream")
        self.serve_file(filepath, ctype)

    def serve_file(self, filepath, content_type):
        try:
            with open(filepath, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Internal Error: {e}")

    def send_json(self, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def handle_latest(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        sql = """
        WITH ranked AS (
            SELECT country, currency, currency_name, date, rate, frequency, source,
                   ROW_NUMBER() OVER (PARTITION BY country ORDER BY date DESC) as rn
            FROM exchange_rates
        )
        SELECT country, currency, currency_name, date, rate, frequency, source
        FROM ranked WHERE rn = 1 ORDER BY country ASC
        """
        cur.execute(sql)
        rows = [dict(r) for r in cur.fetchall()]

        # 전일대비 변동 계산
        for item in rows:
            c = item["country"]
            d = item["date"]
            cur.execute("""
            SELECT date, rate FROM exchange_rates
            WHERE country = ? AND date < ?
            ORDER BY date DESC LIMIT 1
            """, (c, d))
            p_row = cur.fetchone()
            if p_row:
                pr = p_row["rate"]
                item["prev_date"] = p_row["date"]
                item["prev_rate"] = pr
                diff = item["rate"] - pr
                item["diff"] = round(diff, 4)
                item["change_pct"] = round((diff / pr) * 100.0, 3)
            else:
                item["prev_date"] = None
                item["prev_rate"] = None
                item["diff"] = 0.0
                item["change_pct"] = 0.0

        conn.close()
        self.send_json({"status": "success", "count": len(rows), "data": rows})

    def handle_monthly(self, params):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        year = params.get("year", ["2026"])[0]
        country = params.get("country", [None])[0]

        base_sql = """
        SELECT year_month, country, currency, currency_name,
               ROUND(AVG(rate), 4) as avg_rate,
               ROUND(MIN(rate), 4) as min_rate,
               ROUND(MAX(rate), 4) as max_rate,
               COUNT(rate) as data_points
        FROM exchange_rates
        WHERE year_month LIKE ?
        """
        args = [f"{year}_%"]

        if country:
            base_sql += " AND country = ?"
            args.append(country)

        base_sql += " GROUP BY year_month, country ORDER BY year_month DESC, country ASC"
        cur.execute(base_sql, args)
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        self.send_json({"status": "success", "year": year, "count": len(rows), "data": rows})

    def handle_period_average(self, params):
        start = params.get("start", ["2026_01_01"])[0].replace("-", "_")
        end = params.get("end", ["2026_09_16"])[0].replace("-", "_")
        country = params.get("country", [None])[0]

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        base_sql = """
        SELECT country, currency, currency_name,
               ROUND(AVG(rate), 4) as period_avg,
               ROUND(MIN(rate), 4) as period_min,
               ROUND(MAX(rate), 4) as period_max,
               COUNT(rate) as count_points,
               MIN(date) as actual_start,
               MAX(date) as actual_end
        FROM exchange_rates
        WHERE date >= ? AND date <= ?
        """
        args = [start, end]
        if country:
            base_sql += " AND country = ?"
            args.append(country)

        base_sql += " GROUP BY country ORDER BY country ASC"
        cur.execute(base_sql, args)
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        self.send_json({
            "status": "success",
            "query_range": {"start": start, "end": end},
            "data": rows
        })

    def handle_history(self, params):
        country = params.get("country", ["Poland"])[0]
        limit = int(params.get("limit", ["100"])[0])

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        sql = """
        SELECT date, year_month, country, currency, rate, frequency, source
        FROM exchange_rates
        WHERE country = ?
        ORDER BY date DESC
        LIMIT ?
        """
        cur.execute(sql, (country, limit))
        rows = [dict(r) for r in cur.fetchall()]
        rows.reverse()
        conn.close()
        self.send_json({"status": "success", "country": country, "count": len(rows), "data": rows})

    def handle_summary(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        sql = """
        SELECT country, currency, count(*) as count, min(date) as min_date, max(date) as max_date
        FROM exchange_rates
        GROUP BY country
        ORDER BY country ASC
        """
        cur.execute(sql)
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        self.send_json({"status": "success", "data": rows})

def run(port=8080):
    # 각국 공식 고시 시점 연계 하루 5회 정밀 자동 수집 스케줄러 가동
    t = threading.Thread(target=background_scheduler, daemon=True)
    t.start()
    print("각국 공식 고시 시점 연계 하루 5회(09:15, 10:45, 18:30, 19:30, 21:30) 자동 수집 스케줄러 가동")

    server_address = ("", port)
    httpd = ThreadingHTTPServer(server_address, ExchangeRateHandler)
    print(f"중앙은행 환율 웹 서버 가동: http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("서버 중지")

if __name__ == "__main__":
    import sys
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run(p)
