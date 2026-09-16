import os

def update_credits():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    targets = [os.path.join(base_dir, "index.html"), os.path.join(base_dir, "static", "index.html")]
    
    H = chr(45)
    
    old_target = """      <div class="header_status_card">
        <div class="status_pulse_box">"""

    new_replacement = f"""      <div class="header_status_card">
        <div class="creator_tag" style="font{H}size: 11.5px; color: #94a3b8; font{H}weight: 500; margin{H}bottom: 4px; display: flex; align{H}items: center; gap: 6px;">
          <span style="display:inline{H}block; width:5px; height:5px; border{H}radius:50%; background:#38bdf8;"></span>
          <span>기획 · 개발 : <strong style="color: #f1f5f9; font{H}weight: 600;">희성전자 최문환 책임</strong></span>
        </div>
        <div class="status_pulse_box">"""

    for p in targets:
        with open(p, "r", encoding="utf-8") as f:
            c = f.read()
        if old_target in c:
            c = c.replace(old_target, new_replacement)
            # 캐시 파라미터 갱신
            c = c.replace("20260916_30", "20260916_35")
            c = c.replace("20260916_04", "20260916_35")
            with open(p, "w", encoding="utf-8") as f:
                f.write(c)
            print(f"Updated {p}")
        else:
            print(f"Target not found in {p}")

if __name__ == "__main__":
    update_credits()
