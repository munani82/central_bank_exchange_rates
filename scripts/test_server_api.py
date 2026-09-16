import urllib.request
import json

base_url = "http://localhost:8080"

endpoints = [
    ("/", "메인 대시보드 페이지"),
    ("/api/latest", "5개국 당일 최신 환율 API"),
    ("/api/period_average?start=2026_01_01&end=2026_09_15", "기간평균 API"),
    ("/api/monthly_average?year=2026", "2026년 월평균 API"),
    ("/api/history?country=Poland&limit=5", "폴란드 시계열 API")
]

for ep, desc in endpoints:
    url = base_url + ep
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read()
            print(f"[{desc}] 상태코드: {resp.status}, 응답바이트: {len(data)}")
            if "api" in ep:
                j = json.loads(data.decode("utf_8"))
                print(f"  응답 건수: {len(j.get('data', []))}")
    except Exception as e:
        print(f"[{desc}] 실패: {e}")
