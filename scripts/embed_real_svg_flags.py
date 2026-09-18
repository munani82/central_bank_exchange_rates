import os

def embed_flags():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 6개국 고화질 원형 벡터 SVG 국기 정의 (어떤 OS에서도 100% 선명하게 렌더링)
    flags_svg_code = """
// 6개국 공인 고화질 벡터 SVG 국기 (윈도우/맥/모바일 전 플랫폼 100% 국기 렌더링 보장)
const SVG_FLAGS = {
  "Korea": `<svg width="28" height="28" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="18" cy="18" r="18" fill="#ffffff"/>
    <path fill="#cd2e3a" d="M18,9 C22.97,9 27,13.03 27,18 C27,22.97 22.97,27 18,27 C13.03,27 9,22.97 9,18 C9,13.03 13.03,9 18,9 Z"/>
    <path fill="#0047a0" d="M18,9 C22.97,9 27,13.03 27,18 C27,18 22.5,22.5 18,22.5 C13.5,22.5 13.5,13.5 18,13.5 C22.5,13.5 22.5,27 18,27 C13.03,27 9,22.97 9,18 C9,13.03 13.03,9 18,9 Z"/>
    <circle cx="18" cy="13.5" r="4.5" fill="#cd2e3a"/>
    <circle cx="18" cy="22.5" r="4.5" fill="#0047a0"/>
    <rect x="4" y="6" width="3" height="1" transform="rotate(35 4 6)" fill="#000000"/>
    <rect x="5.5" y="4" width="3" height="1" transform="rotate(35 5.5 4)" fill="#000000"/>
    <rect x="2.5" y="8" width="3" height="1" transform="rotate(35 2.5 8)" fill="#000000"/>
    <rect x="29" y="24" width="3" height="1" transform="rotate(35 29 24)" fill="#000000"/>
    <rect x="30.5" y="22" width="3" height="1" transform="rotate(35 30.5 22)" fill="#000000"/>
    <rect x="27.5" y="26" width="3" height="1" transform="rotate(35 27.5 26)" fill="#000000"/>
  </svg>`,
  
  "China": `<svg width="28" height="28" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="18" cy="18" r="18" fill="#de2910"/>
    <polygon points="9,6 10.8,11.6 6,8.2 12,8.2 7.2,11.6" fill="#ffde00"/>
    <polygon points="15,4 15.6,5.8 14,4.7 16,4.7 14.4,5.8" fill="#ffde00"/>
    <polygon points="17,7 17.6,8.8 16,7.7 18,7.7 16.4,8.8" fill="#ffde00"/>
    <polygon points="17,11 17.6,12.8 16,11.7 18,11.7 16.4,12.8" fill="#ffde00"/>
    <polygon points="15,14 15.6,15.8 14,14.7 16,14.7 14.4,15.8" fill="#ffde00"/>
  </svg>`,

  "Vietnam": `<svg width="28" height="28" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="18" cy="18" r="18" fill="#da251d"/>
    <polygon points="18,7 21.2,16.8 12.8,10.7 23.2,10.7 14.8,16.8" fill="#ffff00"/>
  </svg>`,

  "Indonesia": `<svg width="28" height="28" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
    <clipPath id="circle_clip_id"><circle cx="18" cy="18" r="18"/></clipPath>
    <g clip-path="url(#circle_clip_id)">
      <rect width="36" height="18" fill="#ce1126"/>
      <rect y="18" width="36" height="18" fill="#ffffff"/>
    </g>
  </svg>`,

  "Poland": `<svg width="28" height="28" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
    <clipPath id="circle_clip_pl"><circle cx="18" cy="18" r="18"/></clipPath>
    <g clip-path="url(#circle_clip_pl)">
      <rect width="36" height="18" fill="#ffffff"/>
      <rect y="18" width="36" height="18" fill="#dc143c"/>
    </g>
  </svg>`,

  "Egypt": `<svg width="28" height="28" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
    <clipPath id="circle_clip_eg"><circle cx="18" cy="18" r="18"/></clipPath>
    <g clip-path="url(#circle_clip_eg)">
      <rect width="36" height="12" fill="#c8102e"/>
      <rect y="12" width="36" height="12" fill="#ffffff"/>
      <rect y="24" width="36" height="12" fill="#000000"/>
      <circle cx="18" cy="18" r="3.5" fill="#c09300"/>
    </g>
  </svg>`
};
"""

    for fname in ["app.js", "static/app.js"]:
        fpath = os.path.join(base_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            code = f.read()

        if "SVG_FLAGS" not in code:
            code = flags_svg_code + "\n" + code

        # 카드 생성 부분에서 국기 이모지 대신 SVG_FLAGS 우선 사용
        old_card_flag = '<div class="flag_round_badge">${meta.flag}</div>'
        new_card_flag = '<div class="flag_round_badge">${SVG_FLAGS[item.country] || meta.flag}</div>'
        if old_card_flag in code:
            code = code.replace(old_card_flag, new_card_flag)

        # 기간평균 카드 국기 부분
        old_period_flag = '<span class="flag_round_badge" style="width:30px; height:30px; font-size:16px;">${meta.flag}</span>'
        new_period_flag = '<span class="flag_round_badge" style="width:30px; height:30px;">${SVG_FLAGS[c] || meta.flag}</span>'
        if old_period_flag in code:
            code = code.replace(old_period_flag, new_period_flag)

        # 테이블 행 국기 부분
        old_tr_flag = '<td><strong>${meta.flag} ${meta.name_ko}</strong></td>'
        new_tr_flag = '<td style="display:flex; align-items:center; gap:8px;">${SVG_FLAGS[item.country] || ""} <strong>${meta.name_ko}</strong></td>'
        if old_tr_flag in code:
            code = code.replace(old_tr_flag, new_tr_flag)

        with open(fpath, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"Updated {fname} with real SVG flags")

    # style.css 에서 flag_round_badge 스타일 최적화 (SVG가 원형에 꽉 차고 예쁘게 들어가도록)
    for cname in ["style.css", "static/style.css"]:
        cp = os.path.join(base_dir, cname)
        with open(cp, "r", encoding="utf-8") as f:
            css = f.read()
        
        old_badge_css = """.flag_round_badge {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  flex-shrink: 0;
}"""
        new_badge_css = """.flag_round_badge {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.08);
  border: 1.5px solid rgba(255, 255, 255, 0.18);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.35);
  flex-shrink: 0;
}
.flag_round_badge svg {
  width: 100%;
  height: 100%;
  display: block;
}"""
        if old_badge_css in css:
            css = css.replace(old_badge_css, new_badge_css)
            with open(cp, "w", encoding="utf-8") as f:
                f.write(css)
            print(f"Updated {cname} badge styling")

if __name__ == "__main__":
    embed_flags()
