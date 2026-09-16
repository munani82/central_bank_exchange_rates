import os
import sqlite3

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "exchange_rates.db")
vis_dir = os.path.join(base_dir, "visualizations")
os.makedirs(vis_dir, exist_ok=True)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 1. 2026년 6개국 최신 환율 초고대비 프리미엄 오버뷰 SVG 생성
cur.execute("""
WITH ranked AS (
    SELECT country, currency, rate, date,
           ROW_NUMBER() OVER (PARTITION BY country ORDER BY date DESC) as rn
    FROM exchange_rates
)
SELECT country, currency, rate, date FROM ranked WHERE rn = 1 ORDER BY country
""")
latest_rows = cur.fetchall()

colors = {
    "Korea": "#38bdf8",
    "China": "#fb7185",
    "Vietnam": "#34d399",
    "Indonesia": "#22d3ee",
    "Poland": "#c084fc",
    "Egypt": "#fbbf24"
}

country_ko = {
    "Korea": "대한민국",
    "China": "중국",
    "Vietnam": "베트남",
    "Indonesia": "인도네시아",
    "Poland": "폴란드",
    "Egypt": "이집트"
}

flag_emojis = {
    "Korea": "KR",
    "China": "CN",
    "Vietnam": "VN",
    "Indonesia": "ID",
    "Poland": "PL",
    "Egypt": "EG"
}

# 6개국 카드형 최신 환율 SVG (가로 1260, 세로 490 초고해상도 여유 레이아웃)
svg_bar = []
svg_bar.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1260 490" width="100%" height="100%">')
svg_bar.append('<defs>')
svg_bar.append('  <linearGradient id="card_grad" x1="0%" y1="0%" x2="100%" y2="100%">')
svg_bar.append('    <stop offset="0%" stop_color="#131e36" stop_opacity="0.98"/>')
svg_bar.append('    <stop offset="100%" stop_color="#0d1527" stop_opacity="0.98"/>')
svg_bar.append('  </linearGradient>')
svg_bar.append('</defs>')
svg_bar.append('<rect width="1260" height="490" fill="#080e1c" rx="18"/>')
svg_bar.append('<text x="630" y="44" font_family="Pretendard, sans_serif" font_size="22" font_weight="700" fill="#ffffff" text_anchor="middle">6개국 중앙은행 공식 당일 고시환율 요약</text>')
svg_bar.append('<text x="630" y="70" font_family="Pretendard, sans_serif" font_size="13" font_weight="500" fill="#94a3b8" text_anchor="middle">한국, 중국, 베트남, 인도네시아, 폴란드, 이집트 100% 공식 고시 실측 데이터 (기준: 1 USD)</text>')

sort_order = ["Korea", "China", "Vietnam", "Indonesia", "Poland", "Egypt"]
rows_dict = {r[0]: r for r in latest_rows}

# 2열 3행 초여유 와이드 좌표 (카드 폭 580, 높이 106, 간격 30)
col_coords = [(35, 95), (645, 95), (35, 218), (645, 218), (35, 341), (645, 341)]

for idx, c_key in enumerate(sort_order):
    if c_key not in rows_dict:
        continue
    r = rows_dict[c_key]
    country, curr, rate, d = r
    bx, by = col_coords[idx]
    c_color = colors.get(country, "#38bdf8")
    k_name = country_ko.get(country, country)
    f_code = flag_emojis.get(country, "")

    # 카드 본체 (폭 580, 높이 106)
    svg_bar.append(f'<rect x="{bx}" y="{by}" width="580" height="106" fill="url(#card_grad)" rx="14" stroke="rgba(255,255,255,0.14)" stroke_width="1.2"/>')
    # 좌측 악센트 바
    svg_bar.append(f'<rect x="{bx}" y="{by}" width="6" height="106" fill="{c_color}" rx="3"/>')

    # 국가 엠블럼 및 명칭
    svg_bar.append(f'<circle cx="{bx + 40}" cy="{by + 40}" r="17" fill="rgba(255,255,255,0.08)" stroke="{c_color}" stroke_width="1.5"/>')
    svg_bar.append(f'<text x="{bx + 40}" y="{by + 45}" font_family="Pretendard, sans_serif" font_size="11" font_weight="700" fill="#ffffff" text_anchor="middle">{f_code}</text>')
    svg_bar.append(f'<text x="{bx + 72}" y="{by + 40}" font_family="Pretendard, sans_serif" font_size="18" font_weight="700" fill="#ffffff">{k_name}</text>')
    svg_bar.append(f'<text x="{bx + 72}" y="{by + 60}" font_family="Pretendard, sans_serif" font_size="12" font_weight="500" fill="#94a3b8">{country} ({curr})</text>')

    # 고대비 선명한 화이트 환율 수치 (안전한 좌측 기준 정렬: bx + 370)
    disp_rate = f"{rate:,.2f}" if rate > 100 else f"{rate:,.4f}"
    svg_bar.append(f'<text x="{bx + 370}" y="{by + 45}" font_family="JetBrains Mono, monospace" font_size="22" font_weight="800" fill="#ffffff">{disp_rate}</text>')

    # 하단 메타 정보 (고시일 및 고시 회차)
    d_clean = str(d).replace("_", ".")
    svg_bar.append(f'<rect x="{bx + 72}" y="{by + 74}" width="105" height="22" rx="6" fill="rgba(255,255,255,0.06)"/>')
    svg_bar.append(f'<text x="{bx + 124}" y="{by + 89}" font_family="Pretendard, sans_serif" font_size="11" font_weight="500" fill="#38bdf8" text_anchor="middle">공식 고시 실측치</text>')
    svg_bar.append(f'<text x="{bx + 370}" y="{by + 89}" font_family="Pretendard, sans_serif" font_size="12" font_weight="500" fill="#cbd5e1">고시일: {d_clean}</text>')

svg_bar.append('<text x="630" y="468" font_family="Pretendard, sans_serif" font_size="12" font_weight="500" fill="#64748b" text_anchor="middle">데이터 출처: 한국은행 및 서울외국환중개, 중국인민은행, 베트남국가은행, 인도네시아은행, 폴란드국립은행, 이집트중앙은행</text>')
svg_bar.append('</svg>')

bar_path = os.path.join(vis_dir, "latest_rates_overview.svg")
with open(bar_path, "w", encoding="utf_8_sig") as f:
    f.write("\n".join(svg_bar))

print(f"6개국 최신 환율 오버뷰 SVG 고대비 갱신 완료: {bar_path}")

# 2. 2026년 6개국 월평균 추이 카드 SVG 생성
svg_trend = []
svg_trend.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1040 540" width="100%" height="100%">')
svg_trend.append('<rect width="1040" height="540" fill="#080e1c" rx="16"/>')
svg_trend.append('<text x="520" y="42" font_family="Pretendard, sans_serif" font_size="21" font_weight="700" fill="#ffffff" text_anchor="middle">2026년 6개국 공식 월평균 환율 추이</text>')
svg_trend.append('<text x="520" y="68" font_family="Pretendard, sans_serif" font_size="13" font_weight="500" fill="#94a3b8" text_anchor="middle">중앙은행 공식 고시환율 기반 2026년 월평균 변동 추이</text>')

trend_coords = [(35, 92), (370, 92), (705, 92), (35, 305), (370, 305), (705, 305)]

for idx, c_key in enumerate(sort_order):
    bx, by = trend_coords[idx]
    c_color = colors.get(c_key, "#38bdf8")
    k_name = country_ko.get(c_key, c_key)

    cur.execute("""
    SELECT year_month, ROUND(AVG(rate), 4)
    FROM exchange_rates
    WHERE country = ? AND year_month >= '2026_01'
    GROUP BY year_month ORDER BY year_month ASC
    """, (c_key,))
    c_data = cur.fetchall()

    svg_trend.append(f'<rect x="{bx}" y="{by}" width="300" height="195" rx="12" fill="#131e36" stroke="rgba(255,255,255,0.14)" stroke_width="1.2"/>')
    svg_trend.append(f'<rect x="{bx}" y="{by}" width="300" height="4" fill="{c_color}" rx="2"/>')
    svg_trend.append(f'<text x="{bx + 18}" y="{by + 32}" font_family="Pretendard, sans_serif" font_size="17" font_weight="700" fill="#ffffff">{k_name}</text>')
    svg_trend.append(f'<text x="{bx + 18}" y="{by + 52}" font_family="Pretendard, sans_serif" font_size="12" font_weight="500" fill="#94a3b8">{c_key} ({rows_dict.get(c_key, ("","USD"))[1]})</text>')

    if c_data:
        avg_vals = [row[1] for row in c_data]
        min_v = min(avg_vals)
        max_v = max(avg_vals)
        latest_avg = avg_vals[-1]

        disp_latest = f"{latest_avg:,.2f}" if latest_avg > 100 else f"{latest_avg:,.4f}"
        disp_min = f"{min_v:,.2f}" if min_v > 100 else f"{min_v:,.4f}"
        disp_max = f"{max_v:,.2f}" if max_v > 100 else f"{max_v:,.4f}"

        svg_trend.append(f'<text x="{bx + 18}" y="{by + 88}" font_family="Pretendard, sans_serif" font_size="13" font_weight="500" fill="#cbd5e1">최근 월평균:</text>')
        svg_trend.append(f'<text x="{bx + 282}" y="{by + 88}" font_family="JetBrains Mono, monospace" font_size="17" font_weight="800" fill="#ffffff" text_anchor="end">{disp_latest}</text>')

        svg_trend.append(f'<text x="{bx + 18}" y="{by + 118}" font_family="Pretendard, sans_serif" font_size="12" font_weight="500" fill="#94a3b8">2026년 최저:</text>')
        svg_trend.append(f'<text x="{bx + 282}" y="{by + 118}" font_family="JetBrains Mono, monospace" font_size="14" font_weight="700" fill="#38bdf8" text_anchor="end">{disp_min}</text>')

        svg_trend.append(f'<text x="{bx + 18}" y="{by + 144}" font_family="Pretendard, sans_serif" font_size="12" font_weight="500" fill="#94a3b8">2026년 최고:</text>')
        svg_trend.append(f'<text x="{bx + 282}" y="{by + 144}" font_family="JetBrains Mono, monospace" font_size="14" font_weight="700" fill="#fb7185" text_anchor="end">{disp_max}</text>')

        svg_trend.append(f'<text x="{bx + 18}" y="{by + 175}" font_family="Pretendard, sans_serif" font_size="12" font_weight="500" fill="#64748b">집계 기간: 2026년 1월 ~ 9월</text>')

svg_trend.append('<text x="520" y="520" font_family="Pretendard, sans_serif" font_size="12" font_weight="500" fill="#64748b" text_anchor="middle">공식 월평균 산출: 각국 중앙은행 및 법정 공인 영업일 고시환율 산술평균</text>')
svg_trend.append('</svg>')

trend_path = os.path.join(vis_dir, "monthly_averages_trend.svg")
with open(trend_path, "w", encoding="utf_8_sig") as f:
    f.write("\n".join(svg_trend))

print(f"6개국 월평균 추이 SVG 고대비 갱신 완료: {trend_path}")
conn.close()
