import os
import shutil
import json

def sync_root():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(base_dir, "static")
    
    # 1. 루트 index.html 생성 (상대 경로로 완벽 호환)
    src_html = os.path.join(static_dir, "index.html")
    dst_html = os.path.join(base_dir, "index.html")
    with open(src_html, "r", encoding="utf-8") as f:
        html = f.read()
    
    # /static/style.css -> style.css, /static/app.js -> app.js, /static/favicon.svg -> favicon.svg
    html_root = html.replace("/static/style.css", "style.css")
    html_root = html_root.replace("/static/app.js", "app.js")
    html_root = html_root.replace("/static/favicon.svg", "favicon.svg")
    
    with open(dst_html, "w", encoding="utf-8") as f:
        f.write(html_root)
    print("루트 index.html 생성 완료")

    # 2. style.css 복사
    shutil.copy2(os.path.join(static_dir, "style.css"), os.path.join(base_dir, "style.css"))
    print("루트 style.css 복사 완료")

    # 3. favicon.svg 복사
    shutil.copy2(os.path.join(static_dir, "favicon.svg"), os.path.join(base_dir, "favicon.svg"))
    print("루트 favicon.svg 복사 완료")

    # 4. app.js 복사 및 상대 경로 호환
    src_app = os.path.join(static_dir, "app.js")
    dst_app = os.path.join(base_dir, "app.js")
    with open(src_app, "r", encoding="utf-8") as f:
        app_js = f.read()
    with open(dst_app, "w", encoding="utf-8") as f:
        f.write(app_js)
    print("루트 app.js 복사 완료")

    # 5. data 폴더 복사
    src_data = os.path.join(static_dir, "data")
    dst_data = os.path.join(base_dir, "data")
    if os.path.exists(dst_data):
        shutil.rmtree(dst_data)
    shutil.copytree(src_data, dst_data)
    print("루트 data 폴더 복사 완료")

    # 6. vercel.json 갱신 (Vercel 기본 표준 정적 웹사이트 규격)
    v_path = os.path.join(base_dir, "vercel.json")
    v_config = {
        "version": 2,
        "cleanUrls": True
    }
    with open(v_path, "w", encoding="utf-8") as f:
        json.dump(v_config, f, indent=2)
    print("vercel.json 표준화 완료")

    # 7. scripts/07_build_static_data.py 도 루트 data 폴더도 함께 갱신하도록 보강
    script_07_path = os.path.join(base_dir, "scripts", "07_build_static_data.py")
    with open(script_07_path, "r", encoding="utf-8") as f:
        s07 = f.read()
    
    if "root_data_dir" not in s07:
        old_dir_def = 'static_data_dir = os.path.join(base_dir, "static", "data")\n    os.makedirs(static_data_dir, exist_ok=True)'
        new_dir_def = """static_data_dir = os.path.join(base_dir, "static", "data")
    root_data_dir = os.path.join(base_dir, "data")
    os.makedirs(static_data_dir, exist_ok=True)
    os.makedirs(root_data_dir, exist_ok=True)"""
        s07 = s07.replace(old_dir_def, new_dir_def)

        # 복사 로직 추가
        old_end = 'conn.close()'
        new_end = """conn.close()
    import shutil
    for fn in ["latest_rates.json", "monthly_averages.json", "history_rates.json", "all_rates.json"]:
        src_f = os.path.join(static_data_dir, fn)
        dst_f = os.path.join(root_data_dir, fn)
        if os.path.exists(src_f):
            shutil.copy2(src_f, dst_f)"""
        s07 = s07.replace(old_end, new_end)

        with open(script_07_path, "w", encoding="utf-8") as f:
            f.write(s07)
        print("07_build_static_data.py 동기화 보강 완료")

if __name__ == "__main__":
    sync_root()
