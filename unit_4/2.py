import re


def change_time_format(s):
    for j in re.findall(r'\d{2}\.\d{2}[^%]', s):
        s = s.replace(j, j[0:2] + ':' + j[-3:])
    return s


def change_data_format(s):
    for j in re.findall(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}', s):
        s = s.replace(j, (j[11:] + ' ' + j[8:10] + '/' + j[5:7] + '/' + j[0:4]).replace(':', '-'))
    return s


def drop_tag(s):
    return re.sub(r'<.*?>', '', s)


def up_key_words(s, words):
    for key in words:
        for j in re.findall(r'\W*[A-Za-zА-Яа-я]*' + re.escape(key) + r'[A-Za-zА-Яа-я]*\W', s, re.IGNORECASE):
            s = s.replace(j, j.upper())
    return s


filename = input()
new_file = input()
highlight = input().split(',')

with open(filename, encoding='utf-8-sig') as file:
    data = [i for i in file]
output_data = [data[0]]
for i in data[1:]:
    output_data.append(change_data_format(drop_tag(change_time_format(up_key_words(i, highlight)))))
with open(new_file, mode='w', encoding='utf-8') as file:
    file.writelines(output_data)
