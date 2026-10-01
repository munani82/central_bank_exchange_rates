import os
import json
import sqlite3
import requests
import re
import sys
import urllib3
from datetime import datetime, timezone, timedelta

urllib3.disable_warnings()

class CentralBankFetchError(Exception):
    """공식 중앙은행 환율 수집 실패 시 발생하는 명시적 예외"""
    pass

def run_fetch_and_build():
    H = chr(45)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "exchange_rates.db")
    static_data_dir = os.path.join(base_dir, "static", "data")
    os.makedirs(static_data_dir, exist_ok=True)

    # KST 기준 시간 산출 (GitHub Actions 우분투 러너 및 로컬 환경 동시 호환)
    kst_tz = timezone(timedelta(hours=9))
    now_kst = datetime.now(kst_tz)
    now_str = now_kst.strftime("%Y_%m_%d %H:%M:%S")
    today_ymd_hyphen = now_kst.strftime(f"%Y{H}%m{H}%d")
    today_ymd_under = now_kst.strftime("%Y_%m_%d")
    current_hhmm = now_kst.strftime("%H:%M")
    is_weekend = now_kst.weekday() in [5, 6]

    headers = {'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    updated_items = []
    critical_errors = []

    print(f"==================================================")
    print(f"[파이프라인 실행 시작] KST 현재 시각: {now_str}")
    print(f"주말 여부: {'주말(외환시장 휴장)' if is_weekend else '영업일'}")
    print(f"==================================================")

    # 각국별 공식 고시 예정 시각(KST) 및 휴일 규정
    configs = {
        "Korea": {
            "name": "대한민국 원 (KRW)",
            "announcement_time": "09:00",
            "source_name": "Bank of Korea / Seoul Money Brokerage Services (SMBS MAR) / KEB Hana Bank 1st Fixing"
        },
        "China": {
            "name": "중국 위안 (CNY)",
            "announcement_time": "10:15",
            "source_name": "State Administration of Foreign Exchange (SAFE) / People's Bank of China (PBOC)"
        },
        "Vietnam": {
            "name": "베트남 동 (VND)",
            "announcement_time": "10:30",
            "source_name": "State Bank of Vietnam (sbv.gov.vn)"
        },
        "Indonesia": {
            "name": "인도네시아 루피아 (IDR)",
            "announcement_time": "18:15",
            "source_name": "Bank Indonesia (bi.go.id JISDOR)"
        },
        "Poland": {
            "name": "폴란드 즐로티 (PLN)",
            "announcement_time": "19:15",
            "source_name": "Narodowy Bank Polski (NBP Official Web API)"
        },
        "Egypt": {
            "name": "이집트 파운드 (EGP)",
            "announcement_time": "21:00",
            "source_name": "Central Bank of Egypt (cbe.org.eg)"
        }
    }

    # 공통 판정 함수: 정당한 스킵 사유(주말 또는 발표 전)인지 확인
    def is_eligible_for_fetch(country_key):
        cfg = configs[country_key]
        if is_weekend:
            print(f"[{country_key}] 주말 외환시장 정기 휴장으로 수집 대상 아님 (정상 스킵)")
            return False, "주말 정기 휴장"
        if current_hhmm < cfg["announcement_time"]:
            print(f"[{country_key}] 공식 고시 예정 시각({cfg['announcement_time']} KST) 이전 (현재 {current_hhmm} KST)으로 수집 대기 (정상 대기)")
            return False, "고시 시각 미도래"
        return True, "수집 대상 영업 시간"

    # 1. 대한민국 (하나은행 외환포털 1회차 최초 고시)
    kr_eligible, kr_reason = is_eligible_for_fetch("Korea")
    if kr_eligible:
        try:
            url_hana = "https://www.kebhana.com/cms/rate/wpfxd651_01i_01.do"
            today_nodash = now_kst.strftime("%Y%m%d")
            r_hana = requests.post(url_hana, data={'curCd': 'USD', 'inqDat': today_nodash, 'pbldDvCd': '1'}, headers=headers, verify=False, timeout=12)
            parsed_kr = False
            if r_hana.status_code == 200 and "USD" in r_hana.text:
                trs = re.findall(r'<tr>(.*?)</tr>', r_hana.text, re.DOTALL)
                for tr in trs:
                    if "USD" in tr:
                        tds = [re.sub(r'<[^>]+>', '', td).strip() for td in re.findall(r'<td.*?>(.*?)</td>', tr, re.DOTALL)]
                        if len(tds) >= 9:
                            raw_rate = tds[8].replace(",", "")
                            korea_val = float(raw_rate)
                            updated_items.append({
                                "country": "Korea",
                                "currency": "KRW",
                                "currency_name": "대한민국 원",
                                "date": today_ymd_under,
                                "year_month": today_ymd_under[:7],
                                "rate": korea_val,
                                "frequency": "Daily",
                                "source": configs["Korea"]["source_name"]
                            })
                            print(f"[대한민국 실측 성공] {today_ymd_under}: {korea_val} KRW")
                            parsed_kr = True
                            break
            if not parsed_kr:
                # 공휴일 응답 여부 확인
                err_msg = f"대한민국 1회차 최초고시 수집 실패 (HTTP 상태 {r_hana.status_code}, 파싱 실패). 평일 고시 시각 경과 후 미수신."
                print(f"[치명적 오류] {err_msg}")
                critical_errors.append(err_msg)
        except Exception as e:
            err_msg = f"대한민국 수집 중 네트워크/통신 예외 발생: {e}"
            print(f"[치명적 오류] {err_msg}")
            critical_errors.append(err_msg)

    # 2. 중국 (국가외환관리국 SAFE 및 인민은행 PBOC 공식 중간가)
    cn_eligible, cn_reason = is_eligible_for_fetch("China")
    if cn_eligible:
        try:
            url_safe = "https://www.safe.gov.cn/AppStructured/hlw/RMBQuery.do"
            r_safe = requests.get(url_safe, headers=headers, verify=False, timeout=12)
            parsed_cn = False
            if r_safe.status_code == 200:
                m = re.search(r'<td[^>]*>\s*(\d{4}' + H + r'\d{2}' + H + r'\d{2})\s*</td>\s*<td[^>]*>\s*([\d.]+)\s*</td>', r_safe.text)
                if m:
                    s_date_str, s_rate_str = m.groups()
                    china_date = s_date_str.replace(H, "_")
                    china_val = round(float(s_rate_str) / 100.0, 4)
                    updated_items.append({
                        "country": "China",
                        "currency": "CNY",
                        "currency_name": "중국 위안",
                        "date": china_date,
                        "year_month": china_date[:7],
                        "rate": china_val,
                        "frequency": "Daily",
                        "source": configs["China"]["source_name"]
                    })
                    print(f"[중국 SAFE 실측 성공] {china_date}: {china_val} CNY")
                    parsed_cn = True
            if not parsed_cn:
                err_msg = f"중국 SAFE 중간가 수집 실패 (HTTP 상태 {r_safe.status_code if 'r_safe' in locals() else 'None'}). 평일 고시 시각 경과 후 미수신."
                print(f"[치명적 오류] {err_msg}")
                critical_errors.append(err_msg)
        except Exception as e:
            err_msg = f"중국 SAFE 수집 중 네트워크/통신 예외 발생: {e}"
            print(f"[치명적 오류] {err_msg}")
            critical_errors.append(err_msg)

    # 3. 폴란드 (NBP 공식 Web API)
    pl_eligible, pl_reason = is_eligible_for_fetch("Poland")
    if pl_eligible:
        try:
            url_nbp = "https://api.nbp.pl/api/exchangerates/rates/a/usd/?format=json"
            r_nbp = requests.get(url_nbp, headers=headers, verify=False, timeout=12)
            parsed_pl = False
            if r_nbp.status_code == 200:
                rate_info = r_nbp.json().get("rates", [])[0]
                eff_date = rate_info["effectiveDate"].replace(H, "_")
                rate_val = float(rate_info["mid"])
                updated_items.append({
                    "country": "Poland",
                    "currency": "PLN",
                    "currency_name": "폴란드 즐로티",
                    "date": eff_date,
                    "year_month": eff_date[:7],
                    "rate": rate_val,
                    "frequency": "Daily",
                    "source": configs["Poland"]["source_name"]
                })
                print(f"[폴란드 NBP 실측 성공] {eff_date}: {rate_val} PLN")
                parsed_pl = True
            if not parsed_pl:
                err_msg = f"폴란드 NBP 공식 API 수집 실패 (HTTP 상태 {r_nbp.status_code if 'r_nbp' in locals() else 'None'})."
                print(f"[치명적 오류] {err_msg}")
                critical_errors.append(err_msg)
        except Exception as e:
            err_msg = f"폴란드 NBP API 통신 예외 발생: {e}"
            print(f"[치명적 오류] {err_msg}")
            critical_errors.append(err_msg)

    # 4. 베트남 (베트남 국가은행 SBV 공식 중심환율)
    vn_eligible, vn_reason = is_eligible_for_fetch("Vietnam")
    if vn_eligible:
        try:
            url_sbv = "https://www.sbv.gov.vn/webcenter/portal/en/menu/trangchu/tt_cntt/tgnt"
            r_sbv = requests.get(url_sbv, headers=headers, verify=False, timeout=12)
            parsed_vn = False
            if r_sbv.status_code == 200:
                m_sbv = re.search(r'(\d{2}/\d{2}/\d{4}).*?USD.*?([\d,.]+)', r_sbv.text, re.DOTALL)
                if m_sbv:
                    s_d, s_r = m_sbv.groups()
                    raw_val = float(s_r.replace(",", ""))
                    parts = s_d.split("/")
                    norm_d = f"{parts[2]}_{parts[1]}_{parts[0]}"
                    updated_items.append({
                        "country": "Vietnam",
                        "currency": "VND",
                        "currency_name": "베트남 동",
                        "date": norm_d,
                        "year_month": norm_d[:7],
                        "rate": raw_val,
                        "frequency": "Daily",
                        "source": configs["Vietnam"]["source_name"]
                    })
                    print(f"[베트남 SBV 실측 성공] {norm_d}: {raw_val} VND")
                    parsed_vn = True
            if not parsed_vn:
                err_msg = f"베트남 국가은행(SBV) 공식 중심환율 파싱 실패 (HTTP 상태 {r_sbv.status_code if 'r_sbv' in locals() else 'None'}). 고시 시각 경과 후 미확인."
                print(f"[치명적 오류] {err_msg}")
                critical_errors.append(err_msg)
        except Exception as e:
            err_msg = f"베트남 SBV 통신 예외 발생: {e}"
            print(f"[치명적 오류] {err_msg}")
            critical_errors.append(err_msg)

    # 5. 인도네시아 (Bank Indonesia 공식 JISDOR)
    id_eligible, id_reason = is_eligible_for_fetch("Indonesia")
    if id_eligible:
        try:
            url_bi = "https://www.bi.go.id/biweb/api/ExchangeRate/JISDOR"
            r_bi = requests.get(url_bi, headers=headers, verify=False, timeout=12)
            parsed_id = False
            if r_bi.status_code == 200 and "USD" in r_bi.text:
                pass
            if not parsed_id:
                err_msg = f"인도네시아 중앙은행(BI) 공식 JISDOR 파싱 실패 (HTTP 상태 {r_bi.status_code if 'r_bi' in locals() else 'None'}). 장마감 고시 경과 후 미수신."
                print(f"[치명적 오류] {err_msg}")
                critical_errors.append(err_msg)
        except Exception as e:
            err_msg = f"인도네시아 BI 통신 예외 발생: {e}"
            print(f"[치명적 오류] {err_msg}")
            critical_errors.append(err_msg)

    # 6. 이집트 (Central Bank of Egypt 공식 고시환율)
    eg_eligible, eg_reason = is_eligible_for_fetch("Egypt")
    if eg_eligible:
        try:
            url_cbe = "https://www.cbe.org.eg/en/markets/foreign_exchange/cbe_exchange_rates"
            r_cbe = requests.get(url_cbe, headers=headers, verify=False, timeout=12)
            parsed_eg = False
            if r_cbe.status_code == 200:
                pass
            if not parsed_eg:
                err_msg = f"이집트 중앙은행(CBE) 공식 환율 파싱 실패 (HTTP 상태 {r_cbe.status_code if 'r_cbe' in locals() else 'None'}). 당일 고시 경과 후 미수신."
                print(f"[치명적 오류] {err_msg}")
                critical_errors.append(err_msg)
        except Exception as e:
            err_msg = f"이집트 CBE 통신 예외 발생: {e}"
            print(f"[치명적 오류] {err_msg}")
            critical_errors.append(err_msg)

    # 7. DB 동기화
    if updated_items and os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            new_count = 0
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
                    new_count += 1
                else:
                    cur.execute("""
                    UPDATE exchange_rates SET rate = ?, source = ? WHERE country = ? AND date = ?
                    """, (item["rate"], item["source"], item["country"], item["date"]))
            conn.commit()
            conn.close()
            print(f"[DB 동기화] 신규/갱신 순수 실측 레코드 {len(updated_items)}건 반영 완료")
        except Exception as e:
            print(f"[DB 동기화 치명적 오류] {e}")
            critical_errors.append(f"DB 동기화 실패: {e}")

    # 8. 정적 데이터 빌드
    import subprocess
    script_07 = os.path.join(base_dir, "scripts", "07_build_static_data.py")
    subprocess.run(["python", script_07], check=True)
    print(f"[{now_str}] 정적 JSON 배포 파일 동기화 완료")

    # 9. 검증 및 최종 에러 판정 (조용히 스킵하지 않고 에러 발생)
    print(f"==================================================")
    if critical_errors:
        print(f"!!! [경고 및 치명적 에러 감지] 총 {len(critical_errors)}건의 정당한 사유 없는 수집 실패 발생 !!!")
        for err in critical_errors:
            sys.stderr.write(f"ERROR: {err}\n")
        print(f"==================================================")
        raise CentralBankFetchError(f"정당한 사유(휴일/고시 시각 미도래) 없는 공식 데이터 수집 실패 감지: {critical_errors}")
    else:
        print(f"[파이프라인 정상 완료] 모든 수집 대상 국가가 정상 수신되었거나 정당한 사유(휴일/고시 시각 미도래)로 안전 대기 중입니다.")
        print(f"==================================================")

if __name__ == "__main__":
    run_fetch_and_build()
