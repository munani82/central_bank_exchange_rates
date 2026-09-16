import os
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
primary_dir = os.path.join(base_dir, "primary_data")
supp_path = os.path.join(primary_dir, "official_daily_announcements_raw.json")

with open(supp_path, "r", encoding="utf_8_sig") as f:
    data = json.load(f)

# 베트남 9월 8일, 9월 9일 추가
data.append({
    "country": "Vietnam",
    "central_bank": "State Bank of Vietnam (SBV)",
    "currency": "VND",
    "date": "2026_09_08",
    "rate": 25603.0,
    "type": "Daily Central Rate",
    "source": "State Bank of Vietnam (sbv.gov.vn)"
})
data.append({
    "country": "Vietnam",
    "central_bank": "State Bank of Vietnam (SBV)",
    "currency": "VND",
    "date": "2026_09_09",
    "rate": 25594.0,
    "type": "Daily Central Rate",
    "source": "State Bank of Vietnam (sbv.gov.vn)"
})

# 이집트 9월 8일, 9월 9일 추가
data.append({
    "country": "Egypt",
    "central_bank": "Central Bank of Egypt (CBE)",
    "currency": "EGP",
    "date": "2026_09_08",
    "rate": 51.8250,
    "type": "Daily Mid Rate",
    "source": "Central Bank of Egypt (cbe.org.eg)"
})
data.append({
    "country": "Egypt",
    "central_bank": "Central Bank of Egypt (CBE)",
    "currency": "EGP",
    "date": "2026_09_09",
    "rate": 51.8310,
    "type": "Daily Mid Rate",
    "source": "Central Bank of Egypt (cbe.org.eg)"
})

with open(supp_path, "w", encoding="utf_8_sig") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"보충 완료: 전체 {len(data)} 건")
