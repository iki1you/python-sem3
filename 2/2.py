n = int(input())
height = input().split()
books = dict()
for i in height:
    if i not in books:
        books[i] = 1
    else:
        books[i] += 1
print(len(books))
print(*sorted(books.values()))