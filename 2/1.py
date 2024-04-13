import re


s = input()
c = re.findall(r'code\d+', s)
for i in c:
    s = s.replace(i, '???')
print(s)