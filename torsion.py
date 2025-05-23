import sys
import snappy as sp

from sage.all import *


sys.setrecursionlimit(8912)


def claculate_polynomial_by_a(t, p, ch):
    if ch == 'a':
        p = p * t
    if ch == 'A':
        p = p / t
    if ch == 'b':
        p = p + 1
    if ch == 'B':
        p = p - 1
    return p


def claculate_polynomial_by_b(t, p, ch):
    if ch == 'b':
        p = p * t
    if ch == 'B':
        p = p / t
    if ch == 'a':
        p = p + 1
    if ch == 'A':
        p = p - 1

    return p


def calculate(knot_name, R, g, t, r, a_poly, chosen_function, mapping_description):
    p_val, q_val = QQ(0), QQ(0)

    for char_in_relator in reversed(r):
        p_val = chosen_function(t, p_val, char_in_relator)

    for char_in_relator in r:
        q_val = chosen_function(t, q_val, char_in_relator)

    a_result = []
    for a_factor, a_order in list(a_poly.factor()):
        a_result.append(False)
        for factor, order in list(p_val.factor()):
            if factor == a_factor or factor == - a_factor and order >= a_order:
                a_result[-1] = True

    torsion_poly = p_val - q_val

    result = all(a_result)
    if result:
        print('----------------------------------------------')
        print('Knot:', knot_name)
        print("Fundamental group (generators: a,b):\n", g)  # g.generators() might be better
        print("Relator used:", r)
        print(f"Mapping chosen: {mapping_description}")
        print("Alexander polynomial (variable 'a'):", a_poly)
        print("Calculated p (nu(S_R)(0,a)):", p_val)
        print("Calculated q (nu(S_R_rev)(0,a)):", q_val)
        print("Calculated Torsion (p-q):", torsion_poly)
        if torsion_poly != 0:
            print("Calculated Torsion (p-q) factors:", list(torsion_poly.factor()))
        else:
            print("Calculated factors: []")


def check(depth, knot_name):
    R = PolynomialRing(QQ, 'a')
    t = R.gen()

    M = sp.Manifold(knot_name)
    M.randomize()
    a = M.alexander_polynomial()

    g = M.fundamental_group()
    if not g.num_generators() == 2:
        # print('Knot:', knot_name)
        # print("Fundamental group:\n", g)
        return

    r = M.fundamental_group().relators()[0]

    if depth > 8192:
        # print('Knot:', knot_name)
        # print("Fundamental group:\n", g)
        return

    cond_a = r.count('a') - r.count('A') == 0
    cond_b = r.count('b') - r.count('B') == 0
    if cond_a:
        chosen_function = claculate_polynomial_by_a
        mapping_description = "'a' as multiplicative, 'b' as additive"
    elif cond_b:  # Use elif to ensure only one mapping is chosen
        chosen_function = claculate_polynomial_by_b
        mapping_description = "'b' as multiplicative, 'a' as additive"

    if cond_a or cond_b:
        calculate(knot_name, R, g, t, r, a, chosen_function, mapping_description)
    else:
        check(depth + 1, knot_name)


# All Rolfsen tables
knots = []
for i, j in zip(range(3, 12), [1, 1, 2, 3, 7, 21, 49, 165, 552, 2176]):
    for k in range(1, j + 1):
        knots.append('%d_%d' % (i, k))

# Check all knots
for k in knots:
    check(0, k)
