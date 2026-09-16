import os

def update_app_js():
    app_js_path = os.path.join("static", "app.js")
    with open(app_js_path, "r", encoding="utf-8") as f:
        code = f.read()

    # 정적 데이터 캐시 및 fallback 헬퍼 삽입
    helper_code = """
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
"""

    if "fetchWithFallback" not in code:
        code = helper_code + "\n" + code

    # 1. loadLatestRates 수정: /api/refresh 실패 시 data/latest_rates.json 사용
    old_latest_fetch = 'const res = await fetch("/api/refresh");\n    const json = await res.json();'
    new_latest_fetch = 'const json = await fetchWithFallback("/api/refresh", "data/latest_rates.json");'
    if old_latest_fetch in code:
        code = code.replace(old_latest_fetch, new_latest_fetch)

    # 2. executePeriodCalculation 수정: API 실패 시 클라이언트 사이드에서 all_rates.json으로 실시간 계산
    old_period_fetch = """    const res = await fetch(`/api/period_average?start=${sNorm}&end=${eNorm}`);
    const json = await res.json();
    if (json.status !== "success" || !json.data) return;"""

    new_period_fetch = """    let json = null;
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
    if (!json || json.status !== "success" || !json.data) return;"""

    if old_period_fetch in code:
        code = code.replace(old_period_fetch, new_period_fetch)

    # 3. loadMonthlyRates 수정: API 실패 시 monthly_averages.json에서 필터링
    old_monthly_fetch = """    const res = await fetch(url);
    const json = await res.json();"""

    new_monthly_fetch = """    let json = null;
    try {
      const res = await fetch(url);
      if (res.ok) json = await res.json();
    } catch (e) {
      json = null;
    }

    if (!json || json.status !== "success") {
      if (!_monthlyCache) {
        const staticRes = await fetch("data/monthly_averages.json");
        const staticJson = await staticRes.json();
        _monthlyCache = staticJson.data || [];
      }
      let filtered = _monthlyCache.filter(item => (item.year_month || "").startsWith(selectedYear));
      if (selectedCountry) {
        filtered = filtered.filter(item => item.country === selectedCountry);
      }
      json = { status: "success", count: filtered.length, data: filtered };
    }"""

    if old_monthly_fetch in code:
        code = code.replace(old_monthly_fetch, new_monthly_fetch)

    # 4. renderHistoryChart 수정: API 실패 시 history_rates.json에서 필터링
    old_history_fetch = """    const res = await fetch(`/api/history?country=${country}`);
    const json = await res.json();"""

    new_history_fetch = """    let json = null;
    try {
      const res = await fetch(`/api/history?country=${country}`);
      if (res.ok) json = await res.json();
    } catch (e) {
      json = null;
    }

    if (!json || json.status !== "success") {
      if (!_historyCache) {
        const staticRes = await fetch("data/history_rates.json");
        const staticJson = await staticRes.json();
        _historyCache = staticJson.data || [];
      }
      const filtered = _historyCache.filter(item => item.country === country);
      json = { status: "success", count: filtered.length, data: filtered };
    }"""

    if old_history_fetch in code:
        code = code.replace(old_history_fetch, new_history_fetch)

    with open(app_js_path, "w", encoding="utf-8") as f:
        f.write(code)

    print("static/app.js successfully updated for Jamstack and Vercel!")

if __name__ == "__main__":
    update_app_js()
