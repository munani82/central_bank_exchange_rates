# -*- coding: utf-8 -*-
import json
import re

tr_path = 'C:/Users/Enduser/.gemini/antigravity-ide/brain/18d06914-4b5c-4ed9-adfa-4f9d8b1320b9/.system_generated/logs/transcript_full.jsonl'

all_records = {}

with open(tr_path, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        # 날짜 DD/MM/YYYY 와 실수 패턴 찾기
        matches = re.findall(r'(\d{2}/\d{2}/\d{4})[^\d\n\r]{1,100}?(\d{2}\.\d{4})', line)
        for d, r in matches:
            parts = d.split('/')
            norm_d = f"{parts[2]}_{parts[1]}_{parts[0]}"
            if norm_d.startswith("2025_") or norm_d.startswith("2026_"):
                all_records[norm_d] = float(r)

print(f"총 추출된 고유 날짜 환율 건수: {len(all_records)}건")
sorted_dates = sorted(all_records.keys())
if sorted_dates:
    print(f"최초 고시: {sorted_dates[0]} = {all_records[sorted_dates[0]]}")
    print(f"최신 고시: {sorted_dates[-1]} = {all_records[sorted_dates[-1]]}")

# primary_data/cbe_full_official_extracted.json 에 저장
extracted_list = [{"date": d, "rate": all_records[d]} for d in sorted_dates]
with open('primary_data/cbe_full_official_extracted.json', 'w', encoding='utf-8') as f:
    json.dump(extracted_list, f, ensure_ascii=False, indent=2)
print("저장 완료: primary_data/cbe_full_official_extracted.json")
