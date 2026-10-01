# -*- coding: utf-8 -*-
"""
베트남 국영 공식 통신사(VietnamPlus / VNA) 아카이브에서
베트남 국가은행(SBV) 공식 중심환율(Tỷ giá trung tâm) 전수 크롤링 및 파싱 스크립트
"""
import requests
import urllib3
import re
import json

urllib3.disable_warnings()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def crawl_sbv_rates():
    print("=== VietnamPlus 공식 중심환율 기사 검색 및 수집 시작 ===")
    base_search = "https://www.vietnamplus.vn/tim-kiem?q=t%E1%BB%B7+gi%C3%A1+trung+t%C3%A2m&page="
    
    extracted = {}
    
    for page in range(1, 25):
        url = f"{base_search}{page}"
        try:
            r = requests.get(url, headers=headers, timeout=12)
            if r.status_code != 200:
                print(f"Page {page} status {r.status_code}")
                continue
                
            # 기사 링크 추출
            links = re.findall(r'href=[\'"]([^\'"]+post\d+\.vnp)[\'"]', r.text)
            links = list(set(links))
            print(f"Page {page}: {len(links)}개 기사 발견")
            
            for link in links:
                full_url = link if link.startswith("http") else f"https://www.vietnamplus.vn{link}"
                try:
                    ar = requests.get(full_url, headers=headers, timeout=10)
                    if ar.status_code == 200:
                        # 기사 발행일자 파싱 (예: 29/09/2026 또는 2026-09-29)
                        date_match = re.search(r'(\d{2}/\d{2}/\d{4})', ar.text)
                        # 중심환율 수치 파싱 (예: "tỷ giá trung tâm... 25.630" 또는 "tỷ giá trung tâm... 25.624")
                        rate_match = re.search(r'tỷ giá trung tâm[^\d]{1,100}?(\d{2}[.,]\d{3})', ar.text, re.IGNORECASE)
                        if not rate_match:
                            rate_match = re.search(r'tỷ giá trung tâm.*?là\s*(\d{2}[.,]\d{3})', ar.text, re.IGNORECASE)
                            
                        if date_match and rate_match:
                            raw_date = date_match.group(1)
                            raw_rate = rate_match.group(1).replace(".", "").replace(",", "")
                            rate_val = float(raw_rate)
                            
                            # 날짜 형식 변환: DD/MM/YYYY -> YYYY_MM_DD
                            p = raw_date.split("/")
                            norm_date = f"{p[2]}_{p[1]}_{p[0]}"
                            
                            if (norm_date.startswith("2025_") or norm_date.startswith("2026_")) and (24000.0 <= rate_val <= 27000.0):
                                extracted[norm_date] = rate_val
                except Exception:
                    pass
        except Exception as e:
            print(f"Error on page {page}: {e}")
            break
            
    print(f"\n총 수집된 SBV 공식 중심환율 실측치: {len(extracted)}건")
    sorted_dates = sorted(extracted.keys())
    for d in sorted_dates[:5]:
        print(f"  {d}: {extracted[d]} VND")
    for d in sorted_dates[-5:]:
        print(f"  {d}: {extracted[d]} VND")
        
    return extracted

if __name__ == "__main__":
    crawl_sbv_rates()
