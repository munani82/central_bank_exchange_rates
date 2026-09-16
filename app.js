
// 정적 Jamstack 및 Vercel 배포를 위한 스마트 데이터 로더
let _allRatesCache = null;
let _monthlyCache = null;
let _historyCache = null;

async function fetchWithFallback(apiUrl, staticUrl) {
  try {
    const res = await fetch(apiUrl);
    if (res.ok) {
      const json = await res.json();
      if (json && json.status === "success") return json;
    }
  } catch (e) {
    // API 서버가 없는 정적 호스팅 환경인 경우 fallback
  }
  const staticRes = await fetch(staticUrl);
  return await staticRes.json();
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
      loadLatestRates();
    });
  }
}

// 2. 6개국 당일 최신 환율 로드 및 프리미엄 카드 렌더링
async function loadLatestRates() {
  const grid = document.getElementById("latest_cards_grid");
  try {
    const json = await fetchWithFallback("/api/refresh", "data/latest_rates.json");
    if (json.status !== "success" || !json.data) return;

    grid.innerHTML = "";

    // 국가 우선 정렬 순서: 한국, 중국, 베트남, 인도네시아, 폴란드, 이집트
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
            <div class="flag_round_badge">${meta.flag}</div>
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
  const btnCalc = document.getElementById("btn_calculate_period");
  const startInput = document.getElementById("period_start");
  const endInput = document.getElementById("period_end");

  if (btnCalc) {
    btnCalc.addEventListener("click", () => {
      executePeriodCalculation(startInput.value, endInput.value);
    });
  }

  // 프리셋 버튼 이벤트 처리
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

  // 초기 로드 시 2026년 YTD 자동 실행
  executePeriodCalculation("2026_01_01", "2026_09_16");
}

function applyDatePreset(type) {
  const startInput = document.getElementById("period_start");
  const endInput = document.getElementById("period_end");

  const baseEnd = new Date(2026, 8, 16);
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

  startInput.value = formatDateForPicker(startDate);
  endInput.value = formatDateForPicker(baseEnd);
}

function formatDateForPicker(d) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
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
    let json = null;
    try {
      const res = await fetch(`/api/period_average?start=${sNorm}&end=${eNorm}`);
      if (res.ok) {
        json = await res.json();
      }
    } catch (e) {
      json = null;
    }

    if (!json || json.status !== "success") {
      // 정적 호스팅(Vercel) 환경: all_rates.json을 사용하여 브라우저에서 직접 계산
      if (!_allRatesCache) {
        const staticRes = await fetch("data/all_rates.json");
        const staticJson = await staticRes.json();
        _allRatesCache = staticJson.data || [];
      }
      
      const filtered = _allRatesCache.filter(item => {
        const d = (item.date || "").replace(/-/g, "_");
        return d >= sNorm && d <= eNorm;
      });

      const grouped = {};
      filtered.forEach(item => {
        if (!grouped[item.country]) {
          grouped[item.country] = {
            country: item.country,
            currency: item.currency,
            currency_name: item.currency_name || item.currency,
            rates: []
          };
        }
        grouped[item.country].rates.push(Number(item.rate));
      });

      const calculatedData = Object.values(grouped).map(g => {
        const count = g.rates.length;
        const sum = g.rates.reduce((a, b) => a + b, 0);
        const avg = count > 0 ? (sum / count) : 0;
        const min = count > 0 ? Math.min(...g.rates) : 0;
        const max = count > 0 ? Math.max(...g.rates) : 0;
        return {
          country: g.country,
          currency: g.currency,
          currency_name: g.currency_name,
          data_points: count,
          period_avg: Number(avg.toFixed(4)),
          period_min: Number(min.toFixed(4)),
          period_max: Number(max.toFixed(4))
        };
      });

      json = { status: "success", count: calculatedData.length, data: calculatedData };
    }
    if (!json || json.status !== "success" || !json.data) return;

    if (cardsGrid) cardsGrid.innerHTML = "";
    if (tbody) tbody.innerHTML = "";

    if (json.data.length === 0) {
      if (cardsGrid) cardsGrid.innerHTML = `<div class="cell_empty">지정된 기간에 해당하는 공식 환율 관측치가 없습니다.</div>`;
      if (tbody) tbody.innerHTML = `<tr><td colspan="7" class="cell_empty">조회 결과가 없습니다.</td></tr>`;
      return;
    }

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
        color: "#6366f1"
      };

      const avgFormatted = Number(item.period_avg).toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 4
      });
      const minFormatted = Number(item.period_min).toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 4
      });
      const maxFormatted = Number(item.period_max).toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 4
      });

      // 1. 기간 요약 카드
      if (cardsGrid) {
        const card = document.createElement("div");
        card.className = "fintech_period_card";
        card.style.borderLeft = `4px solid ${meta.color}`;
        card.innerHTML = `
          <div class="period_card_head">
            <div class="country_identity_block">
              <span class="flag_round_badge" style="width:30px; height:30px; font-size:16px;">${meta.flag}</span>
              <span class="country_name_text" style="font-size:15px;">${meta.name_ko}</span>
            </div>
            <span class="currency_code_pill">${item.currency}</span>
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
              <span class="stat_val">${item.count_points} 일</span>
            </div>
          </div>
        `;
        cardsGrid.appendChild(card);
      }

      // 2. 요약 테이블 행
      if (tbody) {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td><strong>${meta.flag} ${meta.name_ko}</strong></td>
          <td><span class="currency_code_pill">${item.currency}</span></td>
          <td style="color: var(--accent_cyan); font-weight: 700; font-family: var(--font_num); font-size: 15px;">${avgFormatted}</td>
          <td style="font-family: var(--font_num);">${minFormatted}</td>
          <td style="font-family: var(--font_num);">${maxFormatted}</td>
          <td style="font-family: var(--font_num); font-weight: 600;">${item.count_points} 일</td>
          <td style="font-family: var(--font_num); font-size: 12px; color: var(--text_dim);">${item.actual_start} ~ ${item.actual_end}</td>
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
    const res = await fetch(`/api/monthly_average?year=${year}`);
    const json = await res.json();
    if (json.status !== "success" || !json.data) return;

    tbody.innerHTML = "";
    if (json.data.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" class="cell_empty">${year}년 공식 고시 데이터가 존재하지 않습니다.</td></tr>`;
      return;
    }

    const sortOrder = ["Korea", "China", "Vietnam", "Indonesia", "Poland", "Egypt"];
    const sortedData = json.data.sort((a, b) => {
      if (a.year_month !== b.year_month) {
        return b.year_month.localeCompare(a.year_month);
      }
      const idxA = sortOrder.indexOf(a.country);
      const idxB = sortOrder.indexOf(b.country);
      return (idxA !== -1 ? idxA : 99) - (idxB !== -1 ? idxB : 99);
    });

    sortedData.forEach(item => {
      const meta = COUNTRY_META[item.country] || { flag: "🌐", name_ko: item.country };
      const avgFormatted = Number(item.avg_rate).toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 4
      });
      const minFormatted = Number(item.min_rate).toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 4
      });
      const maxFormatted = Number(item.max_rate).toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 4
      });

      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><span class="currency_code_pill" style="color:var(--text_bright); font-size:12px;">${item.year_month}</span></td>
        <td><strong>${meta.flag} ${meta.name_ko}</strong></td>
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

  // 배경
  ctx.fillStyle = "#0a0f1d";
  ctx.fillRect(0, 0, w, h);
  ctx.fillStyle = "#64748b";
  ctx.font = "14px Pretendard Variable, sans_serif";
  ctx.textAlign = "center";
  ctx.fillText("공식 시계열 데이터를 불러오는 중...", w / 2, h / 2);

  try {
    const res = await fetch(`/api/history?country=${country}&limit=120`);
    const json = await res.json();
    if (json.status !== "success" || !json.data || json.data.length === 0) {
      ctx.fillStyle = "#0a0f1d";
      ctx.fillRect(0, 0, w, h);
      ctx.fillStyle = "#64748b";
      ctx.fillText("표시할 시계열 데이터가 존재하지 않습니다.", w / 2, h / 2);
      return;
    }

    const data = json.data;
    const countBadge = document.getElementById("history_points_count");
    if (countBadge) {
      countBadge.innerText = `최근 ${data.length}개 공식 고시 관측치`;
    }

    const rates = data.map(d => d.rate);
    const minRate = Math.min(...rates);
    const maxRate = Math.max(...rates);
    const rateRange = (maxRate - minRate) || (minRate * 0.05);

    // 차트 배경 초기화
    ctx.fillStyle = "#0a0f1d";
    ctx.fillRect(0, 0, w, h);

    const padLeft = 75;
    const padRight = 35;
    const padTop = 30;
    const padBottom = 45;
    const chartW = w - padLeft - padRight;
    const chartH = h - padTop - padBottom;

    // Y축 수평 가이드선
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
      ctx.lineTo(w - padRight, py);
      ctx.stroke();

      const dispVal = Number(yVal).toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
      ctx.fillText(dispVal, padLeft - 10, py + 4);
    }

    // 좌표 포인트 계산
    const points = data.map((d, i) => {
      const px = padLeft + (chartW * (i / (data.length - 1)));
      const py = padTop + chartH - ((d.rate - minRate) / rateRange * chartH);
      return { x: px, y: py, ...d };
    });

    // 영역 채우기 그라디언트
    const grad = ctx.createLinearGradient(0, padTop, 0, padTop + chartH);
    grad.addColorStop(0, `${meta.color}44`);
    grad.addColorStop(1, `${meta.color}00`);

    ctx.beginPath();
    ctx.moveTo(points[0].x, padTop + chartH);
    points.forEach(p => ctx.lineTo(p.x, p.y));
    ctx.lineTo(points[points.length - 1].x, padTop + chartH);
    ctx.closePath();
    ctx.fillStyle = grad;
    ctx.fill();

    // 메인 곡선 라인
    ctx.beginPath();
    ctx.moveTo(points[0].x, points[0].y);
    for (let i = 1; i < points.length; i++) {
      ctx.lineTo(points[i].x, points[i].y);
    }
    ctx.strokeStyle = meta.color;
    ctx.lineWidth = 2.5;
    ctx.stroke();

    // X축 시작일 및 종료일 표시
    ctx.fillStyle = "#94a3b8";
    ctx.font = "11px JetBrains Mono, monospace";
    ctx.textAlign = "left";
    ctx.fillText(data[0].date, padLeft, h - 16);
    ctx.textAlign = "right";
    ctx.fillText(data[data.length - 1].date, w - padRight, h - 16);

    // 최신 관측점 하이라이트
    const lastP = points[points.length - 1];
    ctx.beginPath();
    ctx.arc(lastP.x, lastP.y, 6, 0, Math.PI * 2);
    ctx.fillStyle = "#ffffff";
    ctx.fill();
    ctx.strokeStyle = meta.color;
    ctx.lineWidth = 2.5;
    ctx.stroke();

  } catch (err) {
    ctx.fillText(`차트 로드 오류: ${err.message}`, w / 2, h / 2);
  }
}
