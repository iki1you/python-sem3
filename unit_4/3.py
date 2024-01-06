import re


def up_key_words(data, words):
    total = []

    for i in data:
        for key in words:
            a = re.findall(r'\s*\S*' + re.escape(key) + r'\S*\s*', i, re.IGNORECASE)
            for j in a:
                i = i.replace(j, j.upper())
        total.append(i)

    return total


s = ['here some example for your Exam',
    'Вася решил устроиться на работу Python-Разработчиком',
    'Вася съел кусок торта, запил его апельсиновым соком, сидя на высокой табуретке']

keywords = 'exam,раб,сок'.split(',')
print(up_key_words(s, keywords))
