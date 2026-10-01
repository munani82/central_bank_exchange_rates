import os
import json
import re
import requests
import urllib3
from datetime import datetime

urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
url = 'https://www.safe.gov.cn/AppStructured/hlw/RMBQuery.do'

# 2025년 1월부터 2026년 9월 30일까지 분기별로 조회
quarters = [
    ("2025-01-01", "2025-03-31"),
    ("2025-04-01", "2025-06-30"),
    ("2025-07-01", "2025-09-30"),
    ("2025-10-01", "2025-12-31"),
    ("2026-01-01", "2026-03-31"),
    ("2026-04-01", "2026-06-30"),
    ("2026-07-01", "2026-09-30")
]

china_pure_records = {}

print("=== 중국 SAFE 국가외환관리국 공식 일별 고시환율 전수 수집 시작 ===")

for s_d, e_d in quarters:
    data = {'startDate': s_d, 'endDate': e_d, 'queryYN': 'true'}
    try:
        r = requests.post(url, data=data, headers=headers, verify=False, timeout=20)
        if r.status_code == 200:
            trs = re.findall(r'<tr class="first"[^>]*>(.*?)</tr>', r.text, re.DOTALL)
            q_count = 0
            for tr in trs:
                tds = [re.sub(r'<[^>]+>', '', td).strip() for td in re.findall(r'<td[^>]*>(.*?)</td>', tr, re.DOTALL)]
                if len(tds) >= 2:
                    raw_date = tds[0].strip()
                    raw_rate = tds[1].strip().replace(",", "")
                    if re.match(r'^\d{4}-\d{2}-\d{2}$', raw_date):
                        norm_date = raw_date.replace("-", "_")
                        # SAFE는 100달러 당 위안화 기준이므로 100으로 나눔
                        cny_rate = round(float(raw_rate) / 100.0, 4)
                        china_pure_records[norm_date] = cny_rate
                        q_count += 1
            print(f"SAFE {s_d} ~ {e_d}: 공식 고시 실측치 {q_count}건 수집 완료")
    except Exception as e:
        print(f"SAFE {s_d} ~ {e_d} 오류: {e}")

sorted_dates = sorted(china_pure_records.keys())
print(f"\n총 수집된 중국 SAFE 공식 실측 일별 고시건수: {len(sorted_dates)}건")
print(f"기간 범위: {sorted_dates[0]} ~ {sorted_dates[-1]}")

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out_path = os.path.join(base_dir, "primary_data", "china_pboc_official.json")

output_list = [
    {
        "date": d,
        "rate": china_pure_records[d],
        "country": "China",
        "currency": "CNY",
        "source": "State Administration of Foreign Exchange (SAFE) / People's Bank of China (PBOC)"
    }
    for d in sorted_dates
]

with open(out_path, "w", encoding="utf_8_sig") as f:
    json.dump(output_list, f, ensure_ascii=False, indent=2)

print(f"중국 SAFE 순수 공식 데이터 저장 완료: {out_path}")
