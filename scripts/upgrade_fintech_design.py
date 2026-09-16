import os

def upgrade():
    H = chr(45) # 하이픈 문자
    
    # 1. CSS 개선
    css_path = os.path.join("static", "style.css")
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()

    # 헤더 아이콘 박스 세련되게 개선
    old_brand_box = """.brand_icon_box {
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #2563eb, #4f46e5);
  color: #ffffff;
  border-radius: var(--radius-lg);
  box-shadow: 0 4px 18px rgba(37, 99, 235, 0.4);
  flex-shrink: 0;
}"""
    new_brand_box = f""".brand_icon_box {{
  width: 48px;
  height: 48px;
  display: flex;
  align{H}items: center;
  justify{H}content: center;
  background: linear{H}gradient(135deg, rgba(37, 99, 235, 0.2), rgba(99, 102, 241, 0.35));
  border: 1px solid rgba(99, 102, 241, 0.4);
  color: #60a5fa;
  border{H}radius: 14px;
  box{H}shadow: 0 4px 20px rgba(37, 99, 235, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.2);
  flex{H}shrink: 0;
}}"""

    if old_brand_box in css:
        css = css.replace(old_brand_box, new_brand_box)

    # 탭 네비게이션 및 활성 탭 버튼 스타일 업그레이드
    old_nav_active = """.nav_tab_btn.active {
  color: #ffffff;
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  border-radius: 8px;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
}"""
    new_nav_active = f""".nav_tab_btn.active {{
  color: #ffffff;
  background: linear{H}gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border{H}radius: 8px;
  box{H}shadow: 0 4px 16px rgba(37, 99, 235, 0.45), inset 0 1px 1px rgba(255, 255, 255, 0.3);
  font{H}weight: 700;
}}"""

    if old_nav_active in css:
        css = css.replace(old_nav_active, new_nav_active)

    # 탭 바 컨테이너 여백 및 패딩 보강
    old_nav_bar = """.nav_segmented_bar {
  display: flex;
  gap: 8px;
  padding: 6px;
  background: rgba(12, 18, 34, 0.7);
  backdrop-filter: blur(16px);
  border: 1px solid var(--border-glass);
  border-radius: var(--radius-lg);
  margin-bottom: 32px;
  overflow-x: auto;
}"""
    new_nav_bar = f""".nav_segmented_bar {{
  display: flex;
  gap: 6px;
  padding: 5px;
  background: rgba(10, 15, 30, 0.75);
  backdrop{H}filter: blur(20px);
  {H}webkit{H}backdrop{H}filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border{H}radius: 12px;
  margin{H}bottom: 32px;
  overflow{H}x: auto;
  box{H}shadow: inset 0 2px 6px rgba(0, 0, 0, 0.4);
}}"""

    if old_nav_bar in css:
        css = css.replace(old_nav_bar, new_nav_bar)

    # 최신 고시환율 카드 상단 타이틀 바 스타일 점검
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css)

    print("CSS upgraded successfully")

    # 2. index.html의 로고 SVG 교체 및 stroke-width 표준화
    html_path = os.path.join("static", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 달러 단독 기호 SVG를 모던한 글로벌 외환 심볼로 교체
    old_svg = """          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke_width="2.2" stroke_linecap="round" stroke_linejoin="round">
            <line x1="12" y1="2" x2="12" y2="22"></line>
            <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
          </svg>"""

    # 아름다운 외환 환전 루프 + 지구본 모던 심볼
    new_svg = f"""          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke{H}width="2" stroke{H}linecap="round" stroke{H}linejoin="round">
            <circle cx="12" cy="12" r="9"></circle>
            <line x1="3.6" y1="9" x2="20.4" y2="9"></line>
            <line x1="3.6" y1="15" x2="20.4" y2="15"></line>
            <path d="M11.5 3a17 17 0 0 0 0 18"></path>
            <path d="M12.5 3a17 17 0 0 1 0 18"></path>
          </svg>"""

    if old_svg in html:
        html = html.replace(old_svg, new_svg)

    # SVG stroke_width 속성들을 stroke-width로 정규화
    html = html.replace(f"stroke_width=", f"stroke{H}width=")
    html = html.replace(f"stroke_linecap=", f"stroke{H}linecap=")
    html = html.replace(f"stroke_linejoin=", f"stroke{H}linejoin=")

    # 캐시 방지 버전 업데이트
    html = html.replace("style.css?v=20260916_20", "style.css?v=20260916_25")
    html = html.replace("app.js?v=20260916_20", "app.js?v=20260916_25")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("HTML upgraded successfully")

if __name__ == "__main__":
    upgrade()
