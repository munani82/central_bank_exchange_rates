
// 6개국 공인 고화질 벡터 SVG 국기 (윈도우/맥/모바일 전 플랫폼 100% 국기 렌더링 보장)
const SVG_FLAGS = {
  "Korea": `<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><mask id="mask_kr"><circle cx="256" cy="256" r="256" fill="#fff"/></mask><g mask="url(#mask_kr)"><path fill="#eee" d="M0 0h512v512H0Z"/><path fill="#333" d="m350 335 24-24 16 16-24 23zm-39 39 24-24 15 16-23 24zm87 8 23-24 16 16-24 24zm-40 39 24-23 16 15-24 24Zm16-63 24-23 15 15-23 24zm-39 40 23-24 16 16-24 23zm63-221-63-63 15-15 64 63zm-63-15-24-24 16-16 23 24zm39 39-24-24 16-15 24 23zm8-87-24-23 16-16 24 24Zm39 40-23-24 15-16 24 24ZM91 358l63 63-16 16-63-63zm63 16 23 24-15 15-24-23zm-40-39 24 23-16 16-23-24zm24-24 63 63-16 16-63-63zm16-220-63 63-16-16 63-63zm23 23-63 63-15-16 63-63zm24 24-63 63-16-16 63-63z"/><path fill="#d80027" d="M319 319 193 193a89 89 0 1 1 126 126z"/><path fill="#0052b4" d="M319 319a89 89 0 1 1-126-126z"/><circle cx="224.5" cy="224.5" r="44.5" fill="#d80027"/><circle cx="287.5" cy="287.5" r="44.5" fill="#0052b4"/></g></svg>`,
  "China": `<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><mask id="mask_cn"><circle cx="256" cy="256" r="256" fill="#fff"/></mask><g mask="url(#mask_cn)"><path fill="#d80027" d="M0 0h512v512H0z"/><path fill="#ffda44" d="m140.1 155.8 22.1 68h71.5l-57.8 42.1 22.1 68-57.9-42-57.9 42 22.2-68-57.9-42.1H118zm163.4 240.7-16.9-20.8-25 9.7 14.5-22.5-16.9-20.9 25.9 6.9 14.6-22.5 1.4 26.8 26 6.9-25.1 9.6zm33.6-61 8-25.6-21.9-15.5 26.8-.4 7.9-25.6 8.7 25.4 26.8-.3-21.5 16 8.6 25.4-21.9-15.5zm45.3-147.6L370.6 212l19.2 18.7-26.5-3.8-11.8 24-4.6-26.4-26.6-3.8 23.8-12.5-4.6-26.5 19.2 18.7zm-78.2-73-2 26.7 24.9 10.1-26.1 6.4-1.9 26.8-14.1-22.8-26.1 6.4 17.3-20.5-14.2-22.7 24.9 10.1z"/></g></svg>`,
  "Vietnam": `<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><mask id="mask_vn"><circle cx="256" cy="256" r="256" fill="#fff"/></mask><g mask="url(#mask_vn)"><path fill="#d80027" d="M0 0h512v512H0Z"/><path fill="#ffda44" d="m176 378 208-150H128l208 150-80-244Z"/></g></svg>`,
  "Indonesia": `<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><mask id="mask_id"><circle cx="256" cy="256" r="256" fill="#fff"/></mask><g mask="url(#mask_id)"><path fill="#eee" d="m0 256 249.6-41.3L512 256v256H0z"/><path fill="#d80027" d="M0 0h512v256H0z"/></g></svg>`,
  "Poland": `<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><mask id="mask_pl"><circle cx="256" cy="256" r="256" fill="#fff"/></mask><g mask="url(#mask_pl)"><path fill="#d80027" d="m0 256 256.4-44.3L512 256v256H0z"/><path fill="#eee" d="M0 0h512v256H0z"/></g></svg>`,
  "Egypt": `<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><mask id="mask_eg"><circle cx="256" cy="256" r="256" fill="#fff"/></mask><g mask="url(#mask_eg)"><path fill="#eee" d="m0 144 256-32 256 32v224l-256 32L0 368Z"/><path fill="#d80027" d="M0 0h512v144H0Z"/><path fill="#333" d="M0 368h512v144H0Z"/><path fill="#ff9811" d="M250 191c-8 0-17 4-22 14 5-3 16-1 16 13 0 4-2 8-5 10-8 0-14-14-29-14-10 0-19 7-19 17v69l46-7-14 27h66l-14-27 46 7v-69c0-10-9-17-19-17-15 0-21 14-29 14 8-23-7-37-23-37z"/></g></svg>`,
};


// 괄호 결함 없는 날짜 피커 제어기
function openDatePicker(target) {
  const nativePicker = document.getElementById(target === 'start' ? 'native_picker_start' : 'native_picker_end');
  const cleanInput = document.getElementById(target === 'start' ? 'period_start' : 'period_end');
  if (nativePicker) {
    if (cleanInput && cleanInput.value) nativePicker.value = cleanInput.value;
    try {
      if (typeof nativePicker.showPicker === 'function') {
        nativePicker.showPicker();
      } else {
        nativePicker.focus();
        nativePicker.click();
      }
    } catch (e) {
      nativePicker.focus();
    }
  }
}

// 글로벌 중앙은행 공식 고시환율 인텔리전스 엔진 (Vercel Jamstack & 로컬 완벽 지원)
let _allRatesCache = null;
let _monthlyCache = null;
let _historyCache = null;
let _latestCache = null;

// 정적 데이터 안전 로더
async function loadJsonSafe(url) {
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error("HTTP " + res.status);
    return await res.json();
  } catch (err) {
    console.warn("데이터 로드 실패 (" + url + "):", err);
    return null;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  loadLatestRates();
  initPeriodCalculator();
  initMonthlyRates();
  initHistoryChart();
});

// 6개국 중앙은행 공식 메타데이터
const COUNTRY_META = {
  "Korea": {
    flag: "🇰🇷",
    name_ko: "대한민국",
    currency: "KRW",
    symbol: "₩",
    color: "#3b82f6",
    fullName: "원 (South Korean Won)",
    bankName: "한국은행 / 서울외국환중개 공식 매매기준율"
  },
  "China": {
    flag: "🇨🇳",
    name_ko: "중국",
    currency: "CNY",
    symbol: "¥",
    color: "#f43f5e",
    fullName: "위안 (Chinese Yuan)",
    bankName: "중국인민은행(PBOC) / CFETS 공식 중간가"
  },
  "Vietnam": {
    flag: "🇻🇳",
    name_ko: "베트남",
    currency: "VND",
    symbol: "₫",
    color: "#10b981",
    fullName: "동 (Vietnamese Dong)",
    bankName: "베트남국가은행(SBV) 공식 중심환율"
  },
  "Indonesia": {
    flag: "🇮🇩",
    name_ko: "인도네시아",
    currency: "IDR",
    symbol: "Rp",
    color: "#06b6d4",
    fullName: "루피아 (Indonesian Rupiah)",
    bankName: "인도네시아은행(BI) JISDOR 공식 기준환율"
  },
  "Poland": {
    flag: "🇵🇱",
    name_ko: "폴란드",
    currency: "PLN",
    symbol: "zł",
    color: "#a855f7",
    fullName: "즈워티 (Polish Zloty)",
    bankName: "폴란드국립은행(NBP) 공식 고시환율"
  },
  "Egypt": {
    flag: "🇪🇬",
    name_ko: "이집트",
    currency: "EGP",
    symbol: "E£",
    color: "#f59e0b",
    fullName: "파운드 (Egyptian Pound)",
    bankName: "이집트중앙은행(CBE) 공식 공표환율"
  }
};

// 1. 세그먼트 탭 전환 로직
function initTabs() {
  const tabs = document.querySelectorAll(".nav_tab_btn");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");

      const targetId = tab.getAttribute("data_tab");
      document.querySelectorAll(".tab_pane").forEach(pane => {
        pane.classList.remove("active");
      });
      const targetPane = document.getElementById(targetId);
      if (targetPane) {
        targetPane.classList.add("active");
      }

      if (targetId === "tab_history") {
        renderSelectedHistory();
      }
    });
  });

  const refreshBtn = document.getElementById("btn_refresh_latest");
  if (refreshBtn) {
    refreshBtn.addEventListener("click", () => {
      refreshBtn.style.transform = "rotate(180deg)";
      setTimeout(() => { refreshBtn.style.transform = "none"; }, 400);
      _latestCache = null;
      loadLatestRates();
    });
  }
}

// 2. 6개국 당일 최신 환율 로드 및 카드 렌더링
async function loadLatestRates() {
  const grid = document.getElementById("latest_cards_grid");
  if (!grid) return;

  try {
    let json = _latestCache;
    if (!json) {
      json = await loadJsonSafe("data/latest_rates.json");
      if (!json) json = await loadJsonSafe("/static/data/latest_rates.json");
      _latestCache = json;
    }

    if (!json || json.status !== "success" || !json.data) {
      grid.innerHTML = `<div class="cell_empty">최신 고시환율 데이터를 불러오는 중입니다...</div>`;
      return;
    }

    grid.innerHTML = "";
    const sortOrder = ["Korea", "China", "Vietnam", "Indonesia", "Poland", "Egypt"];
    const sortedData = json.data.sort((a, b) => {
      const idxA = sortOrder.indexOf(a.country);
      const idxB = sortOrder.indexOf(b.country);
      return (idxA !== -1 ? idxA : 99) - (idxB !== -1 ? idxB : 99);
    });

    sortedData.forEach(item => {
      const meta = COUNTRY_META[item.country] || {
        flag: "🌐",
        name_ko: item.country,
        currency: item.currency,
        color: "#6366f1",
        fullName: item.currency,
        bankName: item.source
      };

      const card = document.createElement("div");
      card.className = "fintech_rate_card";
      card.style.setProperty("--card_theme_color", meta.color);

      let chipClass = "chip_neutral";
      let changeSign = "";
      let arrowSymbol = "•";

      if (item.diff > 0) {
        chipClass = "chip_positive";
        changeSign = "+";
        arrowSymbol = "▲";
      } else if (item.diff < 0) {
        chipClass = "chip_negative";
        changeSign = "";
        arrowSymbol = "▼";
      }

      const formattedRate = Number(item.rate).toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 4
      });

      card.innerHTML = `
        <div class="card_header_row">
          <div class="country_identity_block">
            <div class="flag_round_badge">${SVG_FLAGS[item.country] || meta.flag}</div>
            <div class="country_text_group">
              <span class="country_name_text">${meta.name_ko}</span>
              <span class="currency_fullname">${meta.fullName}</span>
            </div>
          </div>
          <div class="currency_code_pill">${item.currency} / USD</div>
        </div>

        <div class="rate_hero_block">
          <div class="rate_metric_caption">공식 중앙은행 고시환율</div>
          <div class="rate_big_display">${formattedRate}</div>
          <div class="rate_sub_row">
            <span class="change_chip_modern ${chipClass}">
              <span>${arrowSymbol}</span>
              <span>${changeSign}${item.change_pct}%</span>
            </span>
            <span class="rate_date_text">기준일: ${item.date}</span>
          </div>
        </div>

        <div class="card_bottom_meta">
          <span class="source_pill_link" title="${item.source}">출처: ${item.source}</span>
        </div>
      `;
      grid.appendChild(card);
    });
  } catch (err) {
    grid.innerHTML = `<div class="cell_empty">환율 데이터를 불러오는 중 오류가 발생했습니다: ${err.message}</div>`;
  }
}

// 3. 사용자 지정 기간평균 계산기
function initPeriodCalculator() {
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
  }
  const btnCalc = document.getElementById("btn_calculate_period");
  const startInput = document.getElementById("period_start");
  const endInput = document.getElementById("period_end");

  if (btnCalc) {
    btnCalc.addEventListener("click", () => {
      executePeriodCalculation(startInput.value, endInput.value);
    });
  }

  const presetChips = document.querySelectorAll(".chip_btn");
  presetChips.forEach(btn => {
    btn.addEventListener("click", () => {
      presetChips.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      const rangeType = btn.getAttribute("data_range");
      applyDatePreset(rangeType);
      executePeriodCalculation(startInput.value, endInput.value);
    });
  });

  executePeriodCalculation("2026_01_01", "2026_09_18");
}

function applyDatePreset(type) {
  const startInput = document.getElementById("period_start");
  const endInput = document.getElementById("period_end");

  const baseEnd = new Date(2026, 8, 18);
  let startDate = new Date(baseEnd);

  if (type === "1w") {
    startDate.setDate(baseEnd.getDate() - 7);
  } else if (type === "1m") {
    startDate.setMonth(baseEnd.getMonth() - 1);
  } else if (type === "3m") {
    startDate.setMonth(baseEnd.getMonth() - 3);
  } else if (type === "6m") {
    startDate.setMonth(baseEnd.getMonth() - 6);
  } else if (type === "ytd") {
    startDate = new Date(2026, 0, 1);
  } else if (type === "1y") {
    startDate = new Date(2025, 8, 16);
  }

  const y1 = startDate.getFullYear();
  const m1 = String(startDate.getMonth() + 1).padStart(2, "0");
  const d1 = String(startDate.getDate()).padStart(2, "0");
  const y2 = baseEnd.getFullYear();
  const m2 = String(baseEnd.getMonth() + 1).padStart(2, "0");
  const d2 = String(baseEnd.getDate()).padStart(2, "0");

  startInput.value = `${y1}-${m1}-${d1}`;
  endInput.value = `${y2}-${m2}-${d2}`;
}

async function executePeriodCalculation(startStr, endStr) {
  const sNorm = (startStr || "").replace(/-/g, "_");
  const eNorm = (endStr || "").replace(/-/g, "_");
  const cardsGrid = document.getElementById("period_result_cards");
  const tbody = document.getElementById("period_table_body");

  if (cardsGrid) {
    cardsGrid.innerHTML = `<div class="loading_shimmer">지정 기간의 통계를 산출하고 있습니다...</div>`;
  }

  try {
    if (!_allRatesCache) {
      let json = await loadJsonSafe("data/all_rates.json");
      if (!json) json = await loadJsonSafe("/static/data/all_rates.json");
      _allRatesCache = (json && json.data) ? json.data : [];
    }

    const filtered = _allRatesCache.filter(item => {
      const d = (item.date || "").replace(/-/g, "_");
      return d >= sNorm && d <= eNorm;
    });

    if (cardsGrid) cardsGrid.innerHTML = "";
    if (tbody) tbody.innerHTML = "";

    if (filtered.length === 0) {
      if (cardsGrid) cardsGrid.innerHTML = `<div class="cell_empty">지정된 기간에 해당하는 공식 환율 관측치가 없습니다.</div>`;
      if (tbody) tbody.innerHTML = `<tr><td colspan="7" class="cell_empty">조회 결과가 없습니다.</td></tr>`;
      return;
    }

    const grouped = {};
    filtered.forEach(item => {
      const c = item.country;
      if (!grouped[c]) {
        grouped[c] = {
          country: c,
          currency: item.currency,
          rates: [],
          dates: []
        };
      }
      grouped[c].rates.push(Number(item.rate));
      grouped[c].dates.push(item.date);
    });

    const sortOrder = ["Korea", "China", "Vietnam", "Indonesia", "Poland", "Egypt"];
    const countryKeys = Object.keys(grouped).sort((a, b) => {
      const idxA = sortOrder.indexOf(a);
      const idxB = sortOrder.indexOf(b);
      return (idxA !== -1 ? idxA : 99) - (idxB !== -1 ? idxB : 99);
    });

    countryKeys.forEach(c => {
      const g = grouped[c];
      const meta = COUNTRY_META[c] || { flag: "🌐", name_ko: c, currency: g.currency, color: "#6366f1" };
      const count = g.rates.length;
      const sum = g.rates.reduce((acc, v) => acc + v, 0);
      const avg = count > 0 ? (sum / count) : 0;
      const min = count > 0 ? Math.min(...g.rates) : 0;
      const max = count > 0 ? Math.max(...g.rates) : 0;
      const actualStart = g.dates[0];
      const actualEnd = g.dates[g.dates.length - 1];

      const avgFormatted = Number(avg).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 4 });
      const minFormatted = Number(min).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 4 });
      const maxFormatted = Number(max).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 4 });

      if (cardsGrid) {
        const card = document.createElement("div");
        card.className = "fintech_period_card";
        card.style.borderLeft = `4px solid ${meta.color}`;
        card.innerHTML = `
          <div class="period_card_head">
            <div class="country_identity_block">
              <span class="flag_round_badge" style="width:30px; height:30px;">${SVG_FLAGS[c] || meta.flag}</span>
              <span class="country_name_text" style="font-size:15px;">${meta.name_ko}</span>
            </div>
            <span class="currency_code_pill">${meta.currency}</span>
          </div>
          <div class="period_avg_hero">
            <div class="rate_metric_caption">기간 산술평균</div>
            <div class="period_avg_num">${avgFormatted}</div>
          </div>
          <div class="period_stats_grid">
            <div class="stat_box">
              <span class="stat_lbl">기간 최저</span>
              <span class="stat_val" style="color:#60a5fa;">${minFormatted}</span>
            </div>
            <div class="stat_box">
              <span class="stat_lbl">기간 최고</span>
              <span class="stat_val" style="color:#f87171;">${maxFormatted}</span>
            </div>
            <div class="stat_box">
              <span class="stat_lbl">공식 고시일</span>
              <span class="stat_val">${count} 일</span>
            </div>
          </div>
        `;
        cardsGrid.appendChild(card);
      }

      if (tbody) {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td style="display:flex; align-items:center; gap:8px;">${SVG_FLAGS[item.country] || ""} <strong>${meta.name_ko}</strong></td>
          <td><span class="currency_code_pill">${meta.currency}</span></td>
          <td style="color: var(--accent_cyan); font-weight: 700; font-family: var(--font_num); font-size: 15px;">${avgFormatted}</td>
          <td style="font-family: var(--font_num);">${minFormatted}</td>
          <td style="font-family: var(--font_num);">${maxFormatted}</td>
          <td style="font-family: var(--font_num); font-weight: 600;">${count} 일</td>
          <td style="font-family: var(--font_num); font-size: 12px; color: var(--text_dim);">${actualStart} ~ ${actualEnd}</td>
        `;
        tbody.appendChild(tr);
      }
    });
  } catch (err) {
    if (cardsGrid) cardsGrid.innerHTML = `<div class="cell_empty">계산 처리 오류: ${err.message}</div>`;
  }
}

// 4. 월평균 통계 및 내역
function initMonthlyRates() {
  const selectYear = document.getElementById("select_year");
  if (selectYear) {
    selectYear.addEventListener("change", () => {
      loadMonthlyRates(selectYear.value);
    });
  }
  loadMonthlyRates("2026");
}

async function loadMonthlyRates(year) {
  const tbody = document.getElementById("monthly_table_body");
  if (!tbody) return;
  tbody.innerHTML = `<tr><td colspan="7" class="cell_empty">${year}년 월평균 데이터를 조회하고 있습니다...</td></tr>`;

  try {
    if (!_monthlyCache) {
      let json = await loadJsonSafe("data/monthly_averages.json");
      if (!json) json = await loadJsonSafe("/static/data/monthly_averages.json");
      _monthlyCache = (json && json.data) ? json.data : [];
    }

    const filtered = _monthlyCache.filter(item => (item.year_month || "").startsWith(year));
    tbody.innerHTML = "";

    if (filtered.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" class="cell_empty">${year}년 공식 고시 데이터가 존재하지 않습니다.</td></tr>`;
      return;
    }

    const sortOrder = ["Korea", "China", "Vietnam", "Indonesia", "Poland", "Egypt"];
    const sortedData = filtered.sort((a, b) => {
      if (a.year_month !== b.year_month) {
        return b.year_month.localeCompare(a.year_month);
      }
      const idxA = sortOrder.indexOf(a.country);
      const idxB = sortOrder.indexOf(b.country);
      return (idxA !== -1 ? idxA : 99) - (idxB !== -1 ? idxB : 99);
    });

    sortedData.forEach(item => {
      const meta = COUNTRY_META[item.country] || { flag: "🌐", name_ko: item.country };
      const avgFormatted = Number(item.avg_rate).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 4 });
      const minFormatted = Number(item.min_rate).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 4 });
      const maxFormatted = Number(item.max_rate).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 4 });

      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><span class="currency_code_pill" style="color:var(--text_bright); font-size:12px;">${item.year_month}</span></td>
        <td style="display:flex; align-items:center; gap:8px;">${SVG_FLAGS[item.country] || ""} <strong>${meta.name_ko}</strong></td>
        <td>${item.currency}</td>
        <td style="color: var(--accent_emerald); font-weight: 700; font-family: var(--font_num); font-size: 15px;">${avgFormatted}</td>
        <td style="font-family: var(--font_num);">${minFormatted}</td>
        <td style="font-family: var(--font_num);">${maxFormatted}</td>
        <td style="font-family: var(--font_num);">${item.data_points} 일</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="7" class="cell_empty">월평균 로드 실패: ${err.message}</td></tr>`;
  }
}

// 5. 캔버스 고해상도 시계열 차트
function initHistoryChart() {
  const sel = document.getElementById("select_history_country");
  if (sel) {
    sel.addEventListener("change", renderSelectedHistory);
  }
}

async function renderSelectedHistory() {
  const sel = document.getElementById("select_history_country");
  if (!sel) return;
  const country = sel.value;
  const meta = COUNTRY_META[country] || { name_ko: country, currency: "USD", color: "#6366f1" };

  const titleEl = document.getElementById("history_chart_title");
  if (titleEl) {
    titleEl.innerText = `${meta.name_ko} (${meta.currency} / USD) 공식 일별 환율 시계열`;
  }

  const canvas = document.getElementById("canvas_history");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = rect.width * dpr;
  canvas.height = 360 * dpr;
  ctx.scale(dpr, dpr);

  const w = rect.width;
  const h = 360;

  ctx.fillStyle = "#0a0f1d";
  ctx.fillRect(0, 0, w, h);
  ctx.fillStyle = "#64748b";
  ctx.font = "14px Pretendard Variable, sans-serif";
  ctx.textAlign = "center";
  ctx.fillText("공식 시계열 데이터를 불러오는 중...", w / 2, h / 2);

  try {
    if (!_historyCache) {
      let json = await loadJsonSafe("data/history_rates.json");
      if (!json) json = await loadJsonSafe("/static/data/history_rates.json");
      _historyCache = (json && json.data) ? json.data : [];
    }

    const countryData = _historyCache.filter(item => item.country === country);

    if (countryData.length === 0) {
      ctx.fillStyle = "#0a0f1d";
      ctx.fillRect(0, 0, w, h);
      ctx.fillStyle = "#64748b";
      ctx.fillText("표시할 시계열 데이터가 존재하지 않습니다.", w / 2, h / 2);
      return;
    }

    const data = countryData.slice(-120);
    const countBadge = document.getElementById("history_points_count");
    if (countBadge) {
      countBadge.innerText = `최근 ${data.length}개 공식 고시 관측치`;
    }

    const rates = data.map(d => Number(d.rate));
    const minRate = Math.min(...rates);
    const maxRate = Math.max(...rates);
    const rateRange = (maxRate - minRate) || (minRate * 0.05);

    ctx.fillStyle = "#0a0f1d";
    ctx.fillRect(0, 0, w, h);

    const padLeft = 75;
    const padRight = 35;
    const padTop = 30;
    const padBottom = 45;
    const chartW = w - padLeft - padRight;
    const chartH = h - padTop - padBottom;

    ctx.strokeStyle = "rgba(255, 255, 255, 0.06)";
    ctx.lineWidth = 1;
    ctx.fillStyle = "#64748b";
    ctx.font = "11px JetBrains Mono, monospace";
    ctx.textAlign = "right";

    const steps = 4;
    for (let i = 0; i <= steps; i++) {
      const yVal = minRate + (rateRange * (i / steps));
      const py = padTop + chartH - (chartH * (i / steps));
      ctx.beginPath();
      ctx.moveTo(padLeft, py);
      ctx.lineTo(padLeft + chartW, py);
      ctx.stroke();
      ctx.fillText(yVal.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 4 }), padLeft - 10, py + 4);
    }

    const points = [];
    const n = data.length;
    for (let i = 0; i < n; i++) {
      const px = padLeft + (chartW * (i / (n - 1 || 1)));
      const py = padTop + chartH - (chartH * ((rates[i] - minRate) / rateRange));
      points.push({ x: px, y: py, date: data[i].date, rate: rates[i] });
    }

    const grad = ctx.createLinearGradient(0, padTop, 0, padTop + chartH);
    grad.addColorStop(0, meta.color + "40");
    grad.addColorStop(1, meta.color + "00");

    ctx.beginPath();
    ctx.moveTo(points[0].x, padTop + chartH);
    for (let i = 0; i < n; i++) {
      ctx.lineTo(points[i].x, points[i].y);
    }
    ctx.lineTo(points[n - 1].x, padTop + chartH);
    ctx.closePath();
    ctx.fillStyle = grad;
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(points[0].x, points[0].y);
    for (let i = 1; i < n; i++) {
      ctx.lineTo(points[i].x, points[i].y);
    }
    ctx.strokeStyle = meta.color;
    ctx.lineWidth = 2.5;
    ctx.stroke();

    ctx.fillStyle = "#64748b";
    ctx.font = "11px JetBrains Mono, monospace";
    ctx.textAlign = "center";
    const xStep = Math.max(1, Math.floor(n / 6));
    for (let i = 0; i < n; i += xStep) {
      ctx.fillText(data[i].date, points[i].x, padTop + chartH + 22);
    }
    if ((n - 1) % xStep !== 0) {
      ctx.fillText(data[n - 1].date, points[n - 1].x, padTop + chartH + 22);
    }

    const lastPt = points[n - 1];
    ctx.beginPath();
    ctx.arc(lastPt.x, lastPt.y, 5, 0, Math.PI * 2);
    ctx.fillStyle = meta.color;
    ctx.fill();
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 2;
    ctx.stroke();
  } catch (err) {
    ctx.fillStyle = "#0a0f1d";
    ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = "#f87171";
    ctx.fillText("차트 렌더링 오류: " + err.message, w / 2, h / 2);
  }
}
