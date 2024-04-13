n = int(input())
possible_dates = []
for i in range(n):
    date_get, date_work, date_end = map(int, input().split())
    date_final = date_get + date_work
    possible_dates.append(tuple(range(date_final, date_end + 1)))

sorted_data = sorted(possible_dates, key=lambda x: (len(x), x))
exist = []
for date in sorted_data:
    if len(date) == 0:
        print('NO')
        break
    for j in date:
        if j not in exist:
            exist.append(j)
            break
    else:
        print('NO')
        break
else:
    print('YES')