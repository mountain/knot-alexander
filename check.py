import snappy

from sage.all import *


def check(depth, knot_name):
    R = PolynomialRing(QQ, 'a')
    t = R.gen()

    M = snappy.Manifold(knot_name)
    M.randomize()
    a = M.alexander_polynomial()

    g = M.fundamental_group()
    if not g.num_generators() == 2:
        print('Knot:', knot_name)
        print("Fundamental group:\n", g)
        return

    r = M.fundamental_group().relators()[0]

    if depth > 2048:
        # print('Knot:', knot_name)
        # print("Fundamental group:\n", g)
        return

    cond_a = r.count('a') - r.count('A') == 0
    cond_b = r.count('b') - r.count('B') == 0

    p = 0
    if cond_a or cond_b:
        for ch in reversed(r):
            if cond_a:
                if ch == 'a':
                    p = p * t
                if ch == 'A':
                    p = p / t
                if ch == 'b':
                    p = p + 1
                if ch == 'B':
                    p = p - 1
            if cond_b:
                if ch == 'b':
                    p = p * t
                if ch == 'B':
                    p = p / t
                if ch == 'a':
                    p = p + 1
                if ch == 'A':
                    p = p - 1

        result = False
        for factor, _ in list(p.factor()):
            if factor == a or factor == - a:
                result = True
                break
        if result:
            pass
            print('----------------------------------------------')
            print('Knot:', knot_name)
            print("Fundamental group:\n", g)
            print("Alexander polynomial:", a)
            print("Calculated result:",p)
            print('Check result:', result)
    else:
        check(depth + 1, knot_name)


# All Rolfsen tables
knots = []
for i, j in zip(range(3, 15), [1, 1, 2, 3, 7, 21, 49, 165, 552, 2176, 9988, 46972, 253293]):
    for k in range(1, j + 1):
        knots.append('%d_%d' % (i, k))

# Check all knots
for k in knots:
    check(0, k)
