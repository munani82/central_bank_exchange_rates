import os

def create_workflow():
    H = chr(45) # 하이픈 문자
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    wf_dir = os.path.join(base_dir, ".github", "workflows")
    os.makedirs(wf_dir, exist_ok=True)
    
    wf_path = os.path.join(wf_dir, "update_rates.yml")
    
    lines = [
        "name: Daily Central Bank Exchange Rates Update",
        "",
        "on:",
        "  schedule:",
        f"    {H} cron: '15 0 * * 1{H}5'   # 09:15 KST (한국 최초고시)",
        f"    {H} cron: '45 1 * * 1{H}5'   # 10:45 KST (중국 중간가 & 베트남 중심환율)",
        f"    {H} cron: '30 9 * * 1{H}5'   # 18:30 KST (인도네시아 JISDOR)",
        f"    {H} cron: '30 10 * * 1{H}5'  # 19:30 KST (폴란드 NBP Table A)",
        f"    {H} cron: '30 12 * * 1{H}5'  # 21:30 KST (이집트 CBE & 최종 마감)",
        "  workflow_dispatch: # 수동 즉시 실행 지원",
        "",
        "jobs:",
        f"  update{H}rates:",
        f"    runs{H}on: ubuntu{H}latest",
        "    permissions:",
        "      contents: write",
        "    steps:",
        f"      {H} name: Checkout repository",
        f"        uses: actions/checkout@v4",
        "",
        f"      {H} name: Set up Python",
        f"        uses: actions/setup{H}python@v5",
        "        with:",
        f"          python{H}version: '3.11'",
        "",
        f"      {H} name: Install dependencies",
        "        run: |",
        "          pip install requests urllib3 pandas",
        "",
        f"      {H} name: Run Fetch and Build Pipeline",
        "        run: |",
        "          python scripts/08_fetch_and_build.py",
        "",
        f"      {H} name: Commit and Push if updated",
        "        run: |",
        f"          git config {H}{H}global user.name 'github{H}actions[bot]'",
        f"          git config {H}{H}global user.email 'github{H}actions[bot]@users.noreply.github.com'",
        "          git add static/data/ exchange_rates.db",
        f"          git diff {H}{H}quiet && git diff {H}{H}staged {H}{H}quiet || (git commit {H}m 'Auto Update: Central Bank Exchange Rates [skip ci]' && git push)"
    ]
    
    with open(wf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
        
    print(".github/workflows/update_rates.yml created successfully")

if __name__ == "__main__":
    create_workflow()
