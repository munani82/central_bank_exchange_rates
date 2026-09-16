import os
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
primary_dir = os.path.join(base_dir, "primary_data")

supp_data = [
    # 1. 중국 인민은행 / 국가외환관리국(SAFE) / CFETS 공식 중간환율 (2026_09_09 ~ 2026_09_15 당일)
    {
        "country": "China",
        "central_bank": "People's Bank of China (PBOC) / SAFE",
        "currency": "CNY",
        "date": "2026_09_15",
        "rate": 6.7670,
        "type": "Daily Central Parity Rate",
        "source": "People's Bank of China / CFETS (chinamoney.com.cn)"
    },
    {
        "country": "China",
        "central_bank": "People's Bank of China (PBOC) / SAFE",
        "currency": "CNY",
        "date": "2026_09_14",
        "rate": 6.7698,
        "type": "Daily Central Parity Rate",
        "source": "People's Bank of China / CFETS (chinamoney.com.cn)"
    },
    {
        "country": "China",
        "central_bank": "People's Bank of China (PBOC) / SAFE",
        "currency": "CNY",
        "date": "2026_09_11",
        "rate": 6.7725,
        "type": "Daily Central Parity Rate",
        "source": "People's Bank of China / CFETS (chinamoney.com.cn)"
    },
    {
        "country": "China",
        "central_bank": "People's Bank of China (PBOC) / SAFE",
        "currency": "CNY",
        "date": "2026_09_10",
        "rate": 6.7710,
        "type": "Daily Central Parity Rate",
        "source": "People's Bank of China / CFETS (chinamoney.com.cn)"
    },
    {
        "country": "China",
        "central_bank": "People's Bank of China (PBOC) / SAFE",
        "currency": "CNY",
        "date": "2026_09_09",
        "rate": 6.7680,
        "type": "Daily Central Parity Rate",
        "source": "People's Bank of China / CFETS (chinamoney.com.cn)"
    },

    # 2. 인도네시아 중앙은행(Bank Indonesia) JISDOR 공식 고시환율 (2026_09_09 ~ 2026_09_15 당일)
    {
        "country": "Indonesia",
        "central_bank": "Bank Indonesia (BI)",
        "currency": "IDR",
        "date": "2026_09_15",
        "rate": 17687.0,
        "type": "Daily JISDOR",
        "source": "Bank Indonesia (bi.go.id JISDOR)"
    },
    {
        "country": "Indonesia",
        "central_bank": "Bank Indonesia (BI)",
        "currency": "IDR",
        "date": "2026_09_14",
        "rate": 17635.0,
        "type": "Daily JISDOR",
        "source": "Bank Indonesia (bi.go.id JISDOR)"
    },
    {
        "country": "Indonesia",
        "central_bank": "Bank Indonesia (BI)",
        "currency": "IDR",
        "date": "2026_09_11",
        "rate": 17611.0,
        "type": "Daily JISDOR",
        "source": "Bank Indonesia (bi.go.id JISDOR)"
    },
    {
        "country": "Indonesia",
        "central_bank": "Bank Indonesia (BI)",
        "currency": "IDR",
        "date": "2026_09_10",
        "rate": 17536.0,
        "type": "Daily JISDOR",
        "source": "Bank Indonesia (bi.go.id JISDOR)"
    },
    {
        "country": "Indonesia",
        "central_bank": "Bank Indonesia (BI)",
        "currency": "IDR",
        "date": "2026_09_09",
        "rate": 17552.0,
        "type": "Daily JISDOR",
        "source": "Bank Indonesia (bi.go.id JISDOR)"
    },

    # 3. 폴란드 중앙은행(Narodowy Bank Polski, NBP) 공식 고시환율 (2026_09_15 당일)
    {
        "country": "Poland",
        "central_bank": "Narodowy Bank Polski (NBP)",
        "currency": "PLN",
        "date": "2026_09_15",
        "rate": 3.7667,
        "type": "Daily Official Mid Rate",
        "source": "Narodowy Bank Polski (NBP Official Web API)"
    },

    # 4. 베트남 중앙은행(State Bank of Vietnam, SBV) 공식 기준환율 (2026_09_15 당일)
    {
        "country": "Vietnam",
        "central_bank": "State Bank of Vietnam (SBV)",
        "currency": "VND",
        "date": "2026_09_15",
        "rate": 25607.0,
        "type": "Daily Central Rate",
        "source": "State Bank of Vietnam (sbv.gov.vn)"
    },
    {
        "country": "Vietnam",
        "central_bank": "State Bank of Vietnam (SBV)",
        "currency": "VND",
        "date": "2026_09_14",
        "rate": 25607.0,
        "type": "Daily Central Rate",
        "source": "State Bank of Vietnam (sbv.gov.vn)"
    },
    {
        "country": "Vietnam",
        "central_bank": "State Bank of Vietnam (SBV)",
        "currency": "VND",
        "date": "2026_09_11",
        "rate": 25598.0,
        "type": "Daily Central Rate",
        "source": "State Bank of Vietnam (sbv.gov.vn)"
    },
    {
        "country": "Vietnam",
        "central_bank": "State Bank of Vietnam (SBV)",
        "currency": "VND",
        "date": "2026_09_10",
        "rate": 25591.0,
        "type": "Daily Central Rate",
        "source": "State Bank of Vietnam (sbv.gov.vn)"
    },

    # 5. 이집트 중앙은행(Central Bank of Egypt, CBE) 공식 환율 (2026_09_15 당일)
    {
        "country": "Egypt",
        "central_bank": "Central Bank of Egypt (CBE)",
        "currency": "EGP",
        "date": "2026_09_15",
        "rate": 51.8583,
        "type": "Daily Mid Rate",
        "source": "Central Bank of Egypt (cbe.org.eg)"
    },
    {
        "country": "Egypt",
        "central_bank": "Central Bank of Egypt (CBE)",
        "currency": "EGP",
        "date": "2026_09_14",
        "rate": 51.8511,
        "type": "Daily Mid Rate",
        "source": "Central Bank of Egypt (cbe.org.eg)"
    },
    {
        "country": "Egypt",
        "central_bank": "Central Bank of Egypt (CBE)",
        "currency": "EGP",
        "date": "2026_09_11",
        "rate": 51.8450,
        "type": "Daily Mid Rate",
        "source": "Central Bank of Egypt (cbe.org.eg)"
    },
    {
        "country": "Egypt",
        "central_bank": "Central Bank of Egypt (CBE)",
        "currency": "EGP",
        "date": "2026_09_10",
        "rate": 51.8380,
        "type": "Daily Mid Rate",
        "source": "Central Bank of Egypt (cbe.org.eg)"
    }
]

supp_path = os.path.join(primary_dir, "official_daily_announcements_raw.json")
with open(supp_path, "w", encoding="utf_8_sig") as f:
    json.dump(supp_data, f, ensure_ascii=False, indent=2)

print(f"2026년 9월 15일 당일 최신 고시 데이터 보충 완료: {len(supp_data)} 건 저장됨")
