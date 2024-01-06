import sqlite3


database = input()
table = input()
mark_table = input()

conn = sqlite3.connect(database)
cursor = conn.cursor()

query = f"""
    SELECT name, ROUND(SUM(mark)*1.0 / COUNT(mark))
    FROM {table} INNER JOIN {mark_table} ON {table}.id = {mark_table}.id
    GROUP BY {table}.id;
"""
cursor.execute(query)


result = cursor.fetchall()

for row in result:
    print(*row)

cursor.close()
conn.close()