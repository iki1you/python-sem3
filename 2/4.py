from itertools import combinations


n, m, gw = map(int, input().split())
interesting = list(map(int, input().split()))
gw_list = list(map(int, input().split()))
pairs = sorted([tuple(map(int, input().split())) for i in range(m)])
interest_chains = []
chain = []
exist = set()
for i in pairs:
    exist.add(i[0])
    exist.add(i[1])
for i in pairs:
    if len(chain) == 0:
        chain.append(i)
        continue
    if chain[-1][1] == i[0]:
        chain.append(i)
    else:
        interest_chains.append(chain)
        chain = [i]
if len(chain) != 0:
    interest_chains.append(chain)
interest_chains = [list(range(i[0][0], i[-1][1] + 1)) for i in interest_chains]
tuples_interest = []
for chain in interest_chains:
    value = 0
    interest = 0
    for i in chain:
        interest += interesting[i - 1]
        value += gw_list[i - 1]
    tuples_interest.append((interest, value))
tuples_interest = sorted(tuples_interest, key=lambda x: (-x[0], x[1]))
comb = []
for i in range(1, len(tuples_interest) + 1):
    comb += combinations(tuples_interest, i)
for i in range(n):
    if i + 1 not in exist:
        comb.append(((interesting[i], gw_list[i]),))
max_interest = 0
for i in comb:
    x1 = sum([j[0] for j in i])
    x2 = sum([j[1] for j in i])
    if x2 <= gw:
        max_interest = max(x1, max_interest)
print(max_interest)