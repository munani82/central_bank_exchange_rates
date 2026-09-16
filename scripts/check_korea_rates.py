import sqlite3

conn = sqlite3.connect('exchange_rates.db')
cur = conn.cursor()
cur.execute("""
SELECT year_month, ROUND(AVG(rate), 2), MIN(rate), MAX(rate), COUNT(*) 
FROM exchange_rates 
WHERE country='Korea' 
GROUP BY year_month 
ORDER BY year_month DESC
""")
for r in cur.fetchall():
    print(f"{r[0]}: 평균 {r[1]} (최저 {r[2]}, 최고 {r[3]}, 관측 {r[4]}일)")
conn.close()
