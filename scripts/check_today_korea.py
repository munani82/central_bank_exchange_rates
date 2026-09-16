import sqlite3
conn = sqlite3.connect('exchange_rates.db')
cur = conn.cursor()
cur.execute("SELECT date, rate, source FROM exchange_rates WHERE country='Korea' AND date='2026_09_16'")
row = cur.fetchone()
print(f"대한민국 당일 환율: {row[0]} -> {row[1]} 원 (출처: {row[2]})")
conn.close()
