import sqlite3
import pandas as pd

database_name = input()
table_name = input()
name_vac = input()
conn = sqlite3.connect(database_name)

df_years_salary = pd.read_sql(f"SELECT strftime('%Y',published_at) as 'Год', "
                              f"ROUND(AVG(salary), 2) as 'Средняя з/п' from {table_name} "
                              f"GROUP BY strftime('%Y',published_at)", conn)

df_years_count = pd.read_sql(f"SELECT strftime('%Y',published_at) as 'Год', "
                             f"COUNT(salary) as 'Количество вакансий' from {table_name} "
                             f"GROUP BY strftime('%Y',published_at)", conn)

df_years_salary_vac = pd.read_sql(f"SELECT strftime('%Y',published_at) as "
                                  f"'Год', ROUND(AVG(salary), 2) as 'Средняя з/п - {name_vac}' from {table_name}"
                                  f" WHERE name like '%{name_vac}%' GROUP BY strftime('%Y',published_at)", conn)

df_years_count_vac = pd.read_sql(f"SELECT strftime('%Y',published_at) as "
                                 f"'Год', COUNT(salary) as 'Количество вакансий - {name_vac}' from {table_name}"
                                 f" WHERE name like '%{name_vac}%' GROUP BY strftime('%Y',published_at)", conn)

df_area_salary = pd.read_sql(f"""SELECT area_name as Город, "Уровень зарплат по городам" from 
    (SELECT area_name, ROUND(AVG(salary), 2) as "Уровень зарплат по городам", COUNT(*) as k FROM {table_name} 
    GROUP BY area_name HAVING (COUNT(*) * 1.0 / (SELECT COUNT(*) FROM {table_name})) >= 0.008) 
    GROUP BY area_name ORDER BY "Уровень зарплат по городам" DESC LIMIT 10;""", conn)

df_area_count = pd.read_sql(f"""SELECT area_name as Город, 
    COUNT(*) * 1.0 / (SELECT COUNT(*) FROM {table_name}) AS 'Доля вакансий'
    FROM {table_name} GROUP BY area_name
    ORDER BY COUNT(*) DESC LIMIT 10;""", conn)

conn.close()
