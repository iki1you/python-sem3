import re


s = 'Python\nМатематическая статистика\nPandas\nОбучение\nУмение принимать решения'
s2 = 'Обучение персонала\n1С: Торговля, 1С: Розница\nОбучение и развитие\n1С: Склад\nАдминистрирование\nОпыт продаж\nНавыки межличностного общения\nУмение работать в команде\nОбеспечение жизнедеятельности офиса\nУправление магазином\nРазвитие продаж\nCRM\nInternet Marketing'

print(re.split(r'[(\n]', s))
print(re.split(r',\s|\n', s2))