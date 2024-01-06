import sqlite3



database = input()
table = input()

conn = sqlite3.connect(database)
cursor = conn.cursor()

query = f"""
    SELECT gender, ROUND(SUM(height) / COUNT(height), 2), SUM(weight)
    FROM {table}
    GROUP BY gender;
"""
cursor.execute(query)


result = cursor.fetchall()

for row in result:
    print(*row)

cursor.close()
conn.close()