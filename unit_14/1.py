import sqlite3

database = input()
table = input()

connection = sqlite3.connect(database)
cursor = connection.cursor()
cursor.execute(f'SELECT id, name FROM {table} WHERE gender = "male" AND height > 1.8 ORDER BY name ASC')
users = cursor.fetchall()

# Выводим результаты
for user in users:
  print(user)

connection.close()