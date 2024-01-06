import csv
import re


def drop_extra_spaces(line):
    return ' '.join(filter(lambda x: not x.isspace(), ', '.join([i.strip() for i in line.split('\n')]).split()))


def drop_tags(line):
    return re.sub(r'<.*?>', '', line)


def parse_data(data):
    headers = list(data[0])
    rows = list(filter(lambda x: len(x) == len(headers), filter(lambda x: all([len(e) > 0 for e in x]), data[1:])))
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            rows[i][j] = drop_extra_spaces(drop_tags(rows[i][j]))
    return [dict((x, y) for (x, y) in zip(headers, rows[i])) for i in range(len(rows))]


filename = input()
with open(filename, encoding='utf-8-sig') as file:
    parsed_data = parse_data([i for i in csv.reader(file)])

for i in range(len(parsed_data)):
    for key, value in parsed_data[i].items():
        print(f'{key}: {value}')
    if len(parsed_data) - i - 1 != 0:
        print()
