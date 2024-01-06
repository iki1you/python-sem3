import csv


filename = input()
with open(filename, encoding='utf-8-sig') as file:
    data = [i for i in csv.reader(file)]
    headers = data[0]
    rows = list(filter(lambda x: len(x) == len(headers), filter(lambda x: all([len(e) > 0 for e in x]), data[1:])))
    print(headers)
    print(rows)

