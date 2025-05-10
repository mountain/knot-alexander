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


def get_canonical_path_string_A_then_M(relator_str, mapping_description):
    """
    Generates a canonical path string from the original relator string based on the given mapping
    (all additive-type operations first, then all multiplicative-type operations).
    This preserves the relative order of operations within each type.

    Args:
        relator_str (str): The original relator string (e.g., "aaBAbbbAB").
        mapping_description (str): A string describing the mapping, e.g.,
                                   "'a' as multiplicative, 'b' as additive".

    Returns:
        str: The canonical path string with additions/subtractions first,
             followed by multiplications/divisions.
    """
    additive_chars_list = []
    multiplicative_chars_list = []

    # Determine the current mapping type ('a' is multiplicative or 'b' is multiplicative)
    is_a_multiplicative = "'a' as multiplicative" in mapping_description

    for char_code in relator_str:
        if is_a_multiplicative:
            if char_code.lower() == 'a':  # 'a' or 'A' are multiplicative
                multiplicative_chars_list.append(char_code)
            elif char_code.lower() == 'b':  # 'b' or 'B' are additive
                additive_chars_list.append(char_code)
        else:  # 'b' is the multiplicative generator in the mapping
            if char_code.lower() == 'b':  # 'b' or 'B' are multiplicative
                multiplicative_chars_list.append(char_code)
            elif char_code.lower() == 'a':  # 'a' or 'A' are additive
                additive_chars_list.append(char_code)

    # Concatenate: all original additive characters first, then all original multiplicative characters.
    # This method preserves the original relative order within each category of operations.
    canonical_path_str = "".join(additive_chars_list) + "".join(multiplicative_chars_list)
    return canonical_path_str


def get_canonical_path_string_M_then_A(relator_str, mapping_description):
    """
    Generates a canonical path string (all multiplicative-type operations first,
    then all additive-type operations).
    Preserves relative order within each type.
    """
    additive_chars_list = []
    multiplicative_chars_list = []

    is_a_multiplicative = "'a' as multiplicative" in mapping_description

    for char_code in relator_str:
        if is_a_multiplicative:
            if char_code.lower() == 'a':
                multiplicative_chars_list.append(char_code)
            elif char_code.lower() == 'b':
                additive_chars_list.append(char_code)
        else:
            if char_code.lower() == 'b':
                multiplicative_chars_list.append(char_code)
            elif char_code.lower() == 'a':
                additive_chars_list.append(char_code)

    # Concatenate: all original multiplicative chars first, then all original additive chars.
    canonical_path_str = "".join(multiplicative_chars_list) + "".join(additive_chars_list)
    return canonical_path_str


def calculate(knot_name, R_poly_ring, g, t_var, relator_str, alex_poly, chosen_eval_function, mapping_description):
    # Ensure starting from the zero element of the polynomial ring for correct symbolic calculations
    p_val = R_poly_ring(0)
    q_C_val = R_poly_ring(0)  # To store the evaluation of the canonical path gamma_C
    q_C_prime_val = R_poly_ring(0)  # Initialize correctly

    # 1. Calculate p_val (evaluation of the original relator path gamma_R)
    # In your script, iterating through reversed(relator_str) means chosen_eval_function
    # applies operations one by one, effectively from right to left of the composed function.
    # This corresponds to the calculation of nu(gamma_R)(0,t): op_n(...op_2(op_1(initial_val))...)
    # where the first character in the string represents the first operation op_1.
    for char_in_relator in reversed(relator_str):
        p_val = chosen_eval_function(t_var, p_val, char_in_relator)

    # 2. Generate the canonical path string (all additions first, then all multiplications)
    canonical_path_A_then_M_str = get_canonical_path_string_A_then_M(relator_str, mapping_description)
    canonical_path_M_then_A_str = get_canonical_path_string_M_then_A(relator_str, mapping_description)

    # 3. Calculate q_C_val (evaluation of the canonical path gamma_C = gamma_{A->M})
    # The evaluation method should be consistent with p_val, so we also use reversed()
    for char_in_relator_canonical in reversed(canonical_path_A_then_M_str):
        q_C_val = chosen_eval_function(t_var, q_C_val, char_in_relator_canonical)

    for char_in_relator_canonical_prime in reversed(canonical_path_M_then_A_str):
        q_C_prime_val = chosen_eval_function(t_var, q_C_prime_val, char_in_relator_canonical_prime)

    # 4. Calculate the new "torsion" or difference
    new_torsion_poly = p_val - q_C_val
    new_torsion_prime_poly = p_val - q_C_prime_val

    # --- Output Results ---
    # (You can keep your original validation logic for p_val against alex_poly if needed)
    # I noticed your original a_result check was quite complex.
    # To focus on our current goal, p_val - q_C_val, I'll simplify the output logic here.
    # If you need to retain the complex validation of p_val against alex_poly, you can add it back.
    # For now, we will directly print the calculated values.

    print('----------------------------------------------')
    print('Knot:', knot_name)
    # g.generators() is usually better for just listing generators,
    # g itself prints the full group presentation.
    print("Fundamental group (generators specified in mapping):\n", g)
    print("Relator used (for p_val):", relator_str)
    print(f"Mapping chosen: {mapping_description}")
    print("Alexander polynomial (variable 'a'):", alex_poly)  # Your script names t_var as 'a' in PolynomialRing
    print("Calculated p_val (nu(gamma_R)(0,a)):", p_val)
    print("Canonical path (Additions then Multiplications) string (for q_C_val):", canonical_path_A_then_M_str)
    print("Calculated q_C_val (nu(gamma_A->M)(0,a)):", q_C_val)  # The new q
    print("New 'Torsion' (p_val - q_C_val):", new_torsion_poly)

    if new_torsion_poly != 0:
        # Try to print factors as a list if new_torsion_poly is a Sage object
        factored_torsion_list = []
        if hasattr(new_torsion_poly, 'factor_list'):  # For Sage symbolic expressions
            factored_torsion_list = new_torsion_poly.factor_list()
        elif new_torsion_poly != 0:  # For non-zero QQ elements or other cases
            try:
                factored_torsion_list = list(factor(new_torsion_poly))  # Sage global factor function
            except Exception:  # If it cannot be factored this way
                factored_torsion_list = [(new_torsion_poly, 1)]  # Output as is
        print("New 'Torsion' (p_val - q_C_val) factors:", factored_torsion_list)
    else:
        print("New 'Torsion' factors: []")

    print("Canonical path (Multiplications then Additions) string (for q_C_prime_val):", canonical_path_M_then_A_str)
    print("Calculated q_C_prime_val (nu(gamma_M->A)(0,a)):", q_C_prime_val)
    print("New 'Torsion Prime' (p_val - q_C_prime_val):", new_torsion_prime_poly)

    if new_torsion_prime_poly != 0:
        factored_torsion_prime_list = []
        if hasattr(new_torsion_prime_poly, 'factor_list'):
             factored_torsion_prime_list = new_torsion_prime_poly.factor_list()
        elif new_torsion_prime_poly != 0 :
            try:
                factored_torsion_prime_list = list(factor(new_torsion_prime_poly))
            except Exception:
                 factored_torsion_prime_list = [(new_torsion_prime_poly, 1)]
        print("New 'Torsion Prime' (p_val - q_C_prime_val) factors:", factored_torsion_prime_list)
    else:
        print("New 'Torsion Prime' factors: []")


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
