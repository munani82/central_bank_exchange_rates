from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.hanabank.com/cont/mall/mall15/mall1503/index.jsp", wait_until="networkidle")
    frame = page.frame(name="bankIframe")
    
    # Fill form
    frame.evaluate('''() => {
        const form = document.forms['inqFrm'];
        
        // 1. Select period (inqType_p = 3)
        const radP = document.getElementById("inqType_p");
        if (radP) radP.checked = true;
        for (let r of form.inqType) {
            if (r.value === "3") r.checked = true;
        }
        
        // 2. Set start and end dates
        form.tmpInqStrDt_p.value = "2026-09-01";
        form.tmpInqEndDt_p.value = "2026-09-30";
        
        // 3. Select 1st notice (최초고시: tmpPbldDvCd_2 = 0)
        const radNotice = document.getElementById("tmpPbldDvCd_2");
        if (radNotice) radNotice.checked = true;
        for (let r of form.tmpPbldDvCd) {
            if (r.value === "0") r.checked = true;
        }
        
        // 4. Select currency USD
        form.curCd.value = "USD";
        
        // Execute search
        pbk.foreign.rate.pbld.flct.search(form);
    }''')
    
    page.wait_for_timeout(4000)
    
    # Read table rows
    rows = frame.locator("table tbody tr").all()
    print(f"Total rows found: {len(rows)}")
    
    official_data = []
    
    for r in rows:
        tds = [td.inner_text().strip().replace("\n", " ") for td in r.locator("td, th").all()]
        if len(tds) >= 7 and tds[0].startswith("2026-09-"):
            date_str = tds[0]
            # In mall1503 table columns:
            # 0: 날짜 (YYYY-MM-DD)
            # 1: 현찰 사실때
            # 2: 현찰 파실때
            # 3: 송금 보낼때
            # 4: 송금 받을때
            # 5: 외화수표 파실때
            # 6: 매매기준율 (Basic Rate)
            # 7: 전일대비
            cash_buy = float(tds[1].replace(",", ""))
            cash_sell = float(tds[2].replace(",", ""))
            send = float(tds[3].replace(",", ""))
            receive = float(tds[4].replace(",", ""))
            tc_sell = float(tds[5].replace(",", ""))
            base_rate = float(tds[6].replace(",", ""))
            
            official_data.append({
                "date": date_str,
                "rate": base_rate,
                "cash_buy": cash_buy,
                "cash_sell": cash_sell,
                "send": send,
                "receive": receive,
                "source": "Hana Bank Official Portal (1st Notice)"
            })
            
    browser.close()
    
# Sort ascending by date
official_data.sort(key=lambda x: x["date"])

print(f"Extracted {len(official_data)} trading days for September 2026:")
rates = [d["rate"] for d in official_data]
for d in official_data:
    print(f"  {d['date']}: {d['rate']:.2f} 원")

mean_rate = sum(rates) / len(rates)
print(f"\nTotal Days: {len(rates)}")
print(f"Sum: {sum(rates):.2f}")
print(f"Arithmetic Mean: {mean_rate:.4f} 원")

with open("primary_data/korea_hana_september_exact_official.json", "w", encoding="utf_8_sig") as f:
    json.dump(official_data, f, ensure_ascii=False, indent=2)
print("Saved to primary_data/korea_hana_september_exact_official.json")
