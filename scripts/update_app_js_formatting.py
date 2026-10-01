import re

app_js_path = "static/app.js"

with open(app_js_path, "r", encoding="utf_8") as f:
    code = f.read()

# 1. Add formatRateValue helper function near top
helper_func = """
// 국가별 환율 소수점 규격 포맷터 (베트남/인도네시아: 정수, 나머지 4개국: 소수점 2자리 통일)
function formatRateValue(val, country) {
  if (val === null || val === undefined || isNaN(val)) return "0";
  const num = Number(val);
  if (country === "Vietnam" || country === "Indonesia") {
    return Math.round(num).toLocaleString(undefined, {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    });
  } else {
    return num.toLocaleString(undefined, {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
  }
}
"""

# Insert after SVG_FLAGS
if "function formatRateValue" not in code:
    code = code.replace("const SVG_FLAGS = {", helper_func + "\nconst SVG_FLAGS = {")

# 2. Update loadLatestRates
old_latest_format = """      const formattedRate = Number(item.rate).toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 4
      });"""

new_latest_format = """      const formattedRate = formatRateValue(item.rate, item.country);"""
code = code.replace(old_latest_format, new_latest_format)

# 3. Update executePeriodCalculation
old_period_format = """      const avgFormatted = Number(avg).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 4 });
      const minFormatted = Number(min).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 4 });
      const maxFormatted = Number(max).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 4 });"""

new_period_format = """      const avgFormatted = formatRateValue(avg, c);
      const minFormatted = formatRateValue(min, c);
      const maxFormatted = formatRateValue(max, c);"""
code = code.replace(old_period_format, new_period_format)

# 4. Update loadMonthlyRates
old_monthly_format = """      const avgFormatted = Number(item.avg_rate).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 4 });
      const minFormatted = Number(item.min_rate).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 4 });
      const maxFormatted = Number(item.max_rate).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 4 });"""

new_monthly_format = """      const avgFormatted = formatRateValue(item.avg_rate, item.country);
      const minFormatted = formatRateValue(item.min_rate, item.country);
      const maxFormatted = formatRateValue(item.max_rate, item.country);"""
code = code.replace(old_monthly_format, new_monthly_format)

# 5. Update renderSelectedHistory Y-axis text
old_chart_y = """      ctx.fillText(yVal.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 4 }), padLeft - 10, py + 4);"""
new_chart_y = """      ctx.fillText(formatRateValue(yVal, country), padLeft - 10, py + 4);"""
code = code.replace(old_chart_y, new_chart_y)

with open(app_js_path, "w", encoding="utf_8") as f:
    f.write(code)

print("Updated static/app.js with formatRateValue successfully.")
