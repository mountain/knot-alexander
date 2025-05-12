import sys
import snappy as sp

from sage.all import *


sys.setrecursionlimit(8912)


knot2checker = {}
knot2relators = {}


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
        print('--' * 80)
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
    if depth > 8192:
        return

    if knot_name not in knot2relators:
        knot2relators[knot_name] = {}
    if knot_name not in knot2checker:
        knot2checker[knot_name] = {}
    relators = knot2relators[knot_name]
    checker = knot2checker[knot_name]

    R = PolynomialRing(QQ, 'a')
    t = R.gen()

    M = sp.Manifold(knot_name)
    M.randomize()
    a = M.alexander_polynomial()

    g = M.fundamental_group()
    if not g.num_generators() == 2:
        return

    r = M.fundamental_group().relators()[0]
    if r in checker:
        return
    checker[r] = True

    cond_a = r.count('a') - r.count('A') == 0
    cond_b = r.count('b') - r.count('B') == 0
    if cond_b:
        r = r.replace('a', 'c')
        r = r.replace('A', 'C')
        r = r.replace('b', 'a')
        r = r.replace('B', 'A')
        r = r.replace('c', 'b')
        r = r.replace('C', 'B')
    if cond_a or cond_b:
        relators[r] = True
        chosen_function = claculate_polynomial_by_a
        mapping_description = "'a' as multiplicative, 'b' as additive"
        calculate(knot_name, R, g, t, r, a, chosen_function, mapping_description)
        print('--' * 80)
        print('relator index:', len(relators))

    check(depth + 1, knot_name)


knot2relators['9_11'] = {}
while len(knot2relators['9_11']) < 1000:
    check(0, '9_11')
