x = [6, 6, 7, 6, 3, 6, 6, 5, 5, 4, 5, 2, 4, 4, 5, 5, 5, 6, 5, 3, 5, 7, 5, 5, 2, 6, 4, 4, 3, 6, 4, 4, 4, 3, 5, 4, 6, 5, 4, 6, 5, 5, 5, 5, 5, 5, 7, 4, 4, 6]
d = dict()
for i in x:
    if i not in d:
        d[i] = 1
    else:
        d[i] += 1
print(d)
print(sum(x) / len(x))
print(sum(map(lambda i: i**2, x)) / len(x))
print(sum(map(lambda i: i**2, x)) / len(x) - (sum(x) / len(x))**2)
print((sum(map(lambda i: i**2, x)) / len(x) - (sum(x) / len(x))**2)**0.5)