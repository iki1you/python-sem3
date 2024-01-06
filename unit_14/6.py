import pandas as pd
import sqlite3

database_name = input()
csv_file = input()
table_name = input()

conn = sqlite3.connect(database_name)
currencies = pd.read_csv(csv_file, encoding='utf8').to_sql(table_name, conn, index=False)
conn.commit()
conn.close()