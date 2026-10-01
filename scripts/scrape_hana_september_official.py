from playwright.sync_api import sync_playwright
import time
import json
from datetime import datetime, timedelta

def scrape_hana_september():
    results = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.hanabank.com/cont/mall/mall15/mall1501/index.jsp?_menuNo=23100", wait_until="networkidle")
        frame = page.frame(name="bankIframe")
        
        # Check all dates from 2026-09-01 to 2026-09-30
        start_date = datetime(2026, 9, 1)
        end_date = datetime(2026, 9, 30)
        curr = start_date
        
        while curr <= end_date:
            date_str_dash = curr.strftime("%Y-%m-%d")
            date_str_nodash = curr.strftime("%Y%m%d")
            
            # Form submission
            frame.evaluate(f'''() => {{
                const form = document.forms['inqFrm'];
                form.tmpInqStrDt.value = "{date_str_dash}";
                form.inqStrDt.value = "{date_str_nodash}";
                const rad = document.getElementById("pbldDvCd_2");
                if (rad) rad.checked = true;
                for (let r of form.pbldDvCd) {{
                    if (r.value === "3") r.checked = true;
                }}
                pbk.foreign.rate.pbld.prs.search(form);
            }}''')
            
            time.sleep(1.5)
            
            # Read USD row
            usd_rate = None
            rows = frame.locator("table tbody tr").all()
            for r in rows:
                tds = [td.inner_text().strip().replace("\n", " ") for td in r.locator("td, th").all()]
                if len(tds) > 0 and ("USD" in tds[0] or "미국" in tds[0]):
                    # Base rate is index 8 (1,359.30)
                    try:
                        rate_str = tds[8].replace(",", "")
                        usd_rate = float(rate_str)
                    except:
                        pass
                    break
            
            # Also extract inquiry actual date from page to verify if it is holiday
            actual_inq_info = frame.evaluate('''() => {
                const info = document.querySelector(".tbl_info");
                return info ? info.innerText : "";
            }''')
            
            print(f"Date: {date_str_dash} -> USD Rate: {usd_rate}, Info: {actual_inq_info.strip()}")
            results[date_str_dash] = {
                "date": date_str_dash,
                "rate": usd_rate,
                "info": actual_inq_info.strip()
            }
            
            curr += timedelta(days=1)
            
        browser.close()
        
    with open("primary_data/korea_hana_september_scraped.json", "w", encoding="utf_8_sig") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("Scraping completed and saved to primary_data/korea_hana_september_scraped.json")

if __name__ == "__main__":
    scrape_hana_september()
