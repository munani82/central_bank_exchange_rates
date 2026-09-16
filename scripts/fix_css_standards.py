import os
import re

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
css_path = os.path.join(base_dir, "static", "style.css")

with open(css_path, "r", encoding="utf_8_sig") as f:
    content = f.read()

h = chr(45)

# 1. 표준 CSS 속성명 복원
standard_props = [
    "font_family", "font_size", "font_weight", "line_height", "letter_spacing",
    "border_radius", "box_sizing", "box_shadow", "background_color", "border_color",
    "align_items", "justify_content", "flex_direction", "flex_wrap", "flex_shrink",
    "white_space", "list_style", "margin_top", "margin_bottom", "margin_left", "margin_right",
    "padding_top", "padding_bottom", "padding_left", "padding_right",
    "max_width", "min_height", "overflow_x", "overflow_y", "pointer_events",
    "z_index", "backdrop_filter", "border_collapse", "text_align", "text_overflow",
    "grid_template_columns", "webkit_backdrop_filter", "webkit_font_smoothing"
]

for prop in standard_props:
    target_pattern = prop
    corrected = prop.replace("_", h)
    content = re.sub(r'\b' + target_pattern + r'\b(?=\s*:)', corrected, content)

content = content.replace("border_box", f"border{h}box")
content = content.replace("sans_serif", f"sans{h}serif")
content = content.replace("linear_gradient", f"linear{h}gradient")
content = content.replace("radial_gradient", f"radial{h}gradient")
content = content.replace("inline_flex", f"inline{h}flex")

# CSS 변수 언더스코어 -> 하이픈
def fix_vars(m):
    return m.group(0).replace("_", h)

content = re.sub(r'--[a-zA-Z0-9_]+', fix_vars, content)
content = re.sub(r'var\(--[a-zA-Z0-9_]+\)', fix_vars, content)

# 2. 폰트 패밀리 확실한 고딕 선언 주입
font_gothic_rule = f"'Pretendard', 'Noto Sans KR', 'Malgun Gothic', '맑은 고딕', 'Apple SD Gothic Neo', Arial, sans{h}serif"
content = re.sub(r'--font-primary:\s*[^;]+;', f"--font-primary: {font_gothic_rule};", content)
content = re.sub(r'--font-heading:\s*[^;]+;', f"--font-heading: {font_gothic_rule};", content)
content = re.sub(r'--font-body:\s*[^;]+;', f"--font-body: {font_gothic_rule};", content)

# 3. 전역 모든 요소에 고딕 폰트 강제 적용
font_all_force = f"* {{\n  box{h}sizing: border{h}box;\n  margin: 0;\n  padding: 0;\n  font{h}family: {font_gothic_rule} !important;\n}}"
content = re.sub(r'\*\s*\{[^}]+\}', font_all_force, content)

# 4. 탭 바 및 액티브 탭 버튼 스타일 세련되게 업그레이드
tab_active_style = f""".nav_tab_btn.active {{
  color: #ffffff;
  background: linear{h}gradient(135deg, #2563eb, #1d4ed8);
  border{h}radius: 8px;
  box{h}shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
}}"""
content = re.sub(r'\.nav_tab_btn\.active\s*\{[^}]+\}', tab_active_style, content)

tab_bar_style = f""".nav_segmented_bar {{
  display: flex;
  gap: 8px;
  padding: 6px;
  background: rgba(12, 18, 34, 0.7);
  backdrop{h}filter: blur(16px);
  border: 1px solid var({h}{h}border{h}glass);
  border{h}radius: var({h}{h}radius{h}lg);
  margin{h}bottom: 32px;
  overflow{h}x: auto;
}}"""
content = re.sub(r'\.nav_segmented_bar\s*\{[^}]+\}', tab_bar_style, content)

brand_icon_style = f""".brand_icon_box {{
  width: 52px;
  height: 52px;
  display: flex;
  align{h}items: center;
  justify{h}content: center;
  background: linear{h}gradient(135deg, #2563eb, #4f46e5);
  color: #ffffff;
  border{h}radius: var({h}{h}radius{h}lg);
  box{h}shadow: 0 4px 18px rgba(37, 99, 235, 0.4);
  flex{h}shrink: 0;
}}"""
content = re.sub(r'\.brand_icon_box\s*\{[^}]+\}', brand_icon_style, content)

with open(css_path, "w", encoding="utf_8_sig") as f:
    f.write(content)

print("CSS 파일 표준 속성 복원 및 맑은 고딕 완전 강제 지정 완료")
