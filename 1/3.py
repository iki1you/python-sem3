a11, a21, a31 = [16, 19, 14, 18], [16, 18, 18, 16], [17, 18, 18, 16]
a12, a22, a32 = [16.35, 14.9, 19.8, 14.9], [19.35, 19.35, 20.8, 16.35], [21.25, 16.9, 19.25, 16.9]
#a11, a21, a31 = [10, 8, 7, 10], [8, 12, 14, 12], [15, 8, 10, 10]
#a12, a22, a32 = [12, 8, 8, 7], [12, 13, 11, 14], [13, 15, 12, 10]

a = [[a11, a21, a31],
     [a12, a22, a32]]

print(a)
print(sum(a11), sum(a21), sum(a31))
print(sum(a12), sum(a22), sum(a32))
Q = (sum(a11) + sum(a21) + sum(a31) + sum(a12) + sum(a22) + sum(a32))
print('Q', Q)
Q_B1 = sum(a11) + sum(a21) + sum(a31)
Q_B2 = sum(a12) + sum(a22) + sum(a32)
print('Q_B', Q_B1, Q_B2)
Q_A1 = sum(a11) + sum(a12)
Q_A2 = sum(a21) + sum(a22)
Q_A3 = sum(a31) + sum(a32)
print('Q_A', Q_A1, Q_A2, Q_A3)
X_med = Q / (2 * 3 * 4)
print('X_med', X_med)
X_med_B_1, X_med_B_2 = Q_B1 / (3 * 4), Q_B2 / (3 * 4)
print('X_med_B', X_med_B_1, X_med_B_2)
X_med_A_1, X_med_A_2, X_med_A_3 = Q_A1 / (2 * 4), Q_A2 / (2 * 4), Q_A3 / (2 * 4)
print('X_med_A', X_med_A_1, X_med_A_2, X_med_A_3)
x11_med, x21_med, x31_med = sum(a11) / 4, sum(a21) / 4, sum(a31) / 4
x12_med, x22_med, x32_med = sum(a12) / 4, sum(a22) / 4, sum(a32) / 4
SS_A = (4 * 2 * (
    (X_med_A_1 - X_med)**2 + (X_med_A_2 - X_med)**2 + (X_med_A_3 - X_med)**2
))
SS_B = (4 * 3 * (
    (X_med_B_1 - X_med)**2 + (X_med_B_2 - X_med)**2
))
print('SS_A', SS_A)
print('SS_B', SS_B)
SS_AB = 4 * (
    (sum(a11) / 4 - X_med_A_1 - X_med_B_1 + X_med)**2 +
    (sum(a21) / 4 - X_med_A_2 - X_med_B_1 + X_med)**2 +
    (sum(a31) / 4 - X_med_A_3 - X_med_B_1 + X_med)**2 +
    (sum(a12) / 4 - X_med_A_1 - X_med_B_2 + X_med)**2 +
    (sum(a22) / 4 - X_med_A_2 - X_med_B_2 + X_med)**2 +
    (sum(a32) / 4 - X_med_A_3 - X_med_B_2 + X_med)**2
)
print('SS_AB', SS_AB)
SS_R = 0
for i in range(2):
    for j in range(3):
        for k in range(4):
            SS_R += (a[i][j][k] - sum(a[i][j]) / 4)**2
print('SS_R', SS_R)
SS_0 = SS_A + SS_B + SS_AB + SS_R
print('SS_0', SS_0)
print('Оценка дисперсии', SS_A / 2, SS_B / 1, SS_AB / 2, SS_R / 18)
print('F_A', (SS_A / 2) / (SS_R / 18))
print('F_B', (SS_B / 1) / (SS_R / 18))
print('F_AB', (SS_AB / 2) / (SS_R / 18))
print('Критическое значение критерия', 3.555, 4.414, 3.555)
