def retro(m):
    a = m
    s = 0
    for v in a:
        s += 1. / v
    mar = s - 1
    return [1. / x / s for x in a]


a = retro([3.35, 3.52, 2.22])
a1 = a[0] + a[1] * a[0] / (a[0] + a[2])
a2 = a[02] + a[1] * a[2] / (a[0] + a[2])
print([a1, a2])

print retro([2.35, 1.55])
