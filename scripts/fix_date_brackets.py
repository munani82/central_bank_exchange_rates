import os

def fix_date_inputs():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    H = chr(45)

    # 1. HTML 수정
    for html_name in ["index.html", "static/index.html"]:
        p = os.path.join(base_dir, html_name)
        with open(p, "r", encoding="utf-8") as f:
            html = f.read()

        old_cluster = """          <div class="inputs_cluster">
            <div class="date_field_wrap">
              <label for="period_start" class="field_label">조회 시작일</label>
              <input type="date" id="period_start" class="input_date_picker" value="2026-01-01">
            </div>
            <div class="date_sep_arrow">→</div>
            <div class="date_field_wrap">
              <label for="period_end" class="field_label">조회 종료일</label>
              <input type="date" id="period_end" class="input_date_picker" value="2026-09-16">
            </div>
          </div>"""

        new_cluster = f"""          <div class="inputs_cluster">
            <div class="date_field_wrap">
              <label for="period_start" class="field_label">조회 시작일</label>
              <div class="custom_date_box">
                <input type="text" id="period_start" class="input_date_clean" value="2026{H}01{H}01" maxlength="10" placeholder="YYYY{H}MM{H}DD">
                <input type="date" id="native_picker_start" class="hidden_native_picker" tabindex="{H}1">
                <button type="button" class="btn_calendar_trigger" onclick="openDatePicker('start')">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke{H}width="2">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                  </svg>
                </button>
              </div>
            </div>
            <div class="date_sep_arrow">→</div>
            <div class="date_field_wrap">
              <label for="period_end" class="field_label">조회 종료일</label>
              <div class="custom_date_box">
                <input type="text" id="period_end" class="input_date_clean" value="2026{H}09{H}18" maxlength="10" placeholder="YYYY{H}MM{H}DD">
                <input type="date" id="native_picker_end" class="hidden_native_picker" tabindex="{H}1">
                <button type="button" class="btn_calendar_trigger" onclick="openDatePicker('end')">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke{H}width="2">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                  </svg>
                </button>
              </div>
            </div>
          </div>"""

        if old_cluster in html:
            html = html.replace(old_cluster, new_cluster)
            html = html.replace("v=20260916_35", "v=20260918_01")
            with open(p, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"Updated {html_name}")

    # 2. CSS 스타일 보강
    css_extra = f"""
/* 괄호 결함 없는 프리미엄 커스텀 날짜 선택기 */
.custom_date_box {{
  position: relative;
  display: flex;
  align{H}items: center;
}}

.input_date_clean {{
  background: var(--bg-glass-input);
  border: 1px solid var(--border-glass);
  border{H}radius: var(--radius-md);
  padding: 9px 38px 9px 14px;
  color: #ffffff;
  font{H}family: var(--font-num);
  font{H}size: 13.5px;
  font{H}weight: 600;
  letter{H}spacing: 0.04em;
  width: 145px;
  outline: none;
  transition: all 0.2s ease;
}}

.input_date_clean:focus {{
  border{H}color: var(--accent-indigo);
  box{H}shadow: 0 0 12px rgba(99, 102, 241, 0.35);
}}

.btn_calendar_trigger {{
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY({H}50%);
  background: transparent;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  display: flex;
  align{H}items: center;
  justify{H}content: center;
  padding: 4px;
  border{H}radius: 4px;
  transition: color 0.2s, transform 0.2s;
}}

.btn_calendar_trigger:hover {{
  color: #38bdf8;
  transform: translateY({H}50%) scale(1.1);
}}

.hidden_native_picker {{
  position: absolute;
  opacity: 0;
  pointer{H}events: none;
  width: 0;
  height: 0;
}}
"""
    for css_name in ["style.css", "static/style.css"]:
        cp = os.path.join(base_dir, css_name)
        with open(cp, "r", encoding="utf-8") as f:
            css = f.read()
        if "input_date_clean" not in css:
            css += "\n" + css_extra
            with open(cp, "w", encoding="utf-8") as f:
                f.write(css)
            print(f"Updated {css_name}")

    # 3. app.js 로직 보강
    js_func = f"""
// 괄호 결함 없는 날짜 피커 제어기
function openDatePicker(target) {{
  const nativePicker = document.getElementById(target === 'start' ? 'native_picker_start' : 'native_picker_end');
  const cleanInput = document.getElementById(target === 'start' ? 'period_start' : 'period_end');
  if (nativePicker) {{
    if (cleanInput && cleanInput.value) nativePicker.value = cleanInput.value;
    try {{
      if (typeof nativePicker.showPicker === 'function') {{
        nativePicker.showPicker();
      }} else {{
        nativePicker.focus();
        nativePicker.click();
      }}
    }} catch (e) {{
      nativePicker.focus();
    }}
  }}
}}
"""
    for js_name in ["app.js", "static/app.js"]:
        jp = os.path.join(base_dir, js_name)
        with open(jp, "r", encoding="utf-8") as f:
            js = f.read()

        if "openDatePicker" not in js:
            js = js_func + "\n" + js

        # 9월 18일 기본 기준일로 갱신
        js = js.replace('const baseEnd = new Date(2026, 8, 16);', 'const baseEnd = new Date(2026, 8, 18);')
        js = js.replace('executePeriodCalculation("2026_01_01", "2026_09_16");', 'executePeriodCalculation("2026_01_01", "2026_09_18");')

        # 네이티브 피커 변경 시 이벤트 리스너 추가
        old_init_period = 'function initPeriodCalculator() {'
        new_init_period = """function initPeriodCalculator() {
  const pStart = document.getElementById("native_picker_start");
  const pEnd = document.getElementById("native_picker_end");
  const cStart = document.getElementById("period_start");
  const cEnd = document.getElementById("period_end");

  if (pStart && cStart) {
    pStart.addEventListener("change", () => {
      cStart.value = pStart.value;
      executePeriodCalculation(cStart.value, cEnd.value);
    });
  }
  if (pEnd && cEnd) {
    pEnd.addEventListener("change", () => {
      cEnd.value = pEnd.value;
      executePeriodCalculation(cStart.value, cEnd.value);
    });
  }
  if (cStart) {
    cStart.addEventListener("change", () => {
      executePeriodCalculation(cStart.value, cEnd.value);
    });
  }
  if (cEnd) {
    cEnd.addEventListener("change", () => {
      executePeriodCalculation(cStart.value, cEnd.value);
    });
  }"""

        if old_init_period in js and "pStart" not in js:
            js = js.replace(old_init_period, new_init_period)

        with open(jp, "w", encoding="utf-8") as f:
            f.write(js)
        print(f"Updated {js_name}")

if __name__ == "__main__":
    fix_date_inputs()
