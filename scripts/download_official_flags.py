import os
import requests

def fetch_official_flags():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # hatscripts circle-flags 공식 공인 국기 SVG 다운로드
    country_codes = {
        "Korea": "kr",
        "China": "cn",
        "Vietnam": "vn",
        "Indonesia": "id",
        "Poland": "pl",
        "Egypt": "eg"
    }

    svg_map = {}
    for country, code in country_codes.items():
        url = f"https://raw.githubusercontent.com/hatscripts/circle-flags/gh-pages/flags/{code}.svg"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                svg_clean = r.text.strip()
                # 고유 마스크 id 충돌 방지
                svg_clean = svg_clean.replace('id="a"', f'id="mask_{code}"')
                svg_clean = svg_clean.replace('url(#a)', f'url(#mask_{code})')
                svg_map[country] = svg_clean
                print(f"[성공] {country} ({code}.svg) 공식 국기 수신 완료")
            else:
                print(f"[실패] {country} HTTP {r.status_code}")
        except Exception as e:
            print(f"[에러] {country}: {e}")

    # app.js 및 static/app.js의 SVG_FLAGS 교체
    if len(svg_map) == 6:
        # 자바스크립트 객체 코드로 변환
        js_flags_code = "const SVG_FLAGS = {\n"
        for country, svg_str in svg_map.items():
            # 백틱 이스케이프
            safe_svg = svg_str.replace("`", "\\`").replace("${", "\\${")
            js_flags_code += f'  "{country}": `{safe_svg}`,\n'
        js_flags_code += "};\n"

        for fname in ["app.js", "static/app.js"]:
            fpath = os.path.join(base_dir, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                code = f.read()

            import re
            code_new = re.sub(r'const SVG_FLAGS = \{.*?\};\n', js_flags_code, code, flags=re.DOTALL)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(code_new)
            print(f"Updated {fname} with official circle-flags vectors!")

if __name__ == "__main__":
    fetch_official_flags()
