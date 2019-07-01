import sqlite3


conn = sqlite3.connect('golden-eye.db')

cur = conn.cursor()

cur.execute("SELECT * FROM xrates")

rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()
