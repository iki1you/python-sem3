n, k = map(int, input().strip().split())
prices = list(map(int, input().strip().split()))
days = []
fish = 0
cost = 0
pref = 0

for i in range(n):
    local = i
    if 1 <= i < pref:
        local = pref
        pref = i
    else:
        end = min(i + k - 1, n - 1)
        l_min = prices[i]
        l_i = i
        for j in range(i + 1, end + 1):
            if prices[j] < l_min:
                l_min = prices[j]
                l_i = i + j
                break
        local = l_i
    fish -= 1
    if local - i == 0:
        buy_fish = min(k, n - 1 - fish - i)
    else:
        buy_fish = local - i
    fish += buy_fish
    cost += buy_fish * prices[i]
    days.append(buy_fish)

print(cost)
print(*days)
