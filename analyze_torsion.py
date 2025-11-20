import sympy as sp


def verify_aeg_torsion(knot_name, relator_str):
    """
    验证 AEG 理论中的算术挠率结构与理性假设。

    参数:
        knot_name: 纽结名称 (如 "4_1")
        relator_str: 纽结群的 Relator 字符串 (如 "abbbaBAAB")
    """
    # 1. 定义符号与矩阵生成元
    t = sp.symbols('t')

    # 定义生成元矩阵 (Aff(1, C) 表示)
    # a: 乘法 (t), b: 加法 (1)
    # 注意：AEG 符号从右向左作用 (f o g)，但矩阵乘法 M_f * M_g 也是从右向左作用于向量 x。
    # 论文中 "a(b(x))" 对应的矩阵顺序是 M_a * M_b

    M_a = sp.Matrix([[t, 0], [0, 1]])
    M_b = sp.Matrix([[1, 1], [0, 1]])
    M_A = sp.Matrix([[t ** -1, 0], [0, 1]])  # a^-1
    M_B = sp.Matrix([[1, -1], [0, 1]])  # b^-1

    ops = {
        'a': (M_a, 0, 1),  # (Matrix, additive_delta, multiplicative_exp)
        'b': (M_b, 1, 0),
        'A': (M_A, 0, -1),
        'B': (M_B, -1, 0)
    }

    print(f"--- 分析纽结: {knot_name} ---")
    print(f"Relator: {relator_str}")

    # 2. 计算 p(t): 正向路径 Evaluation
    # 对应矩阵乘积 M_total = M_last * ... * M_first (根据函数复合顺序)
    # 论文例子: a(b(b...)) -> a 是最外层函数，即最后乘上去的左矩阵

    # 为了匹配论文 derivation [cite: 2851]，字符串 "abbba..." 中第一个字符 'a' 是最外层函数。
    # 所以矩阵乘积顺序应该是 M_char0 * M_char1 * ...

    M_p = sp.eye(2)
    for char in relator_str:
        if char in ops:
            M_p = M_p * ops[char][0]

    p_t = sp.simplify(M_p[0, 1])  # 矩阵右上角元素即为 total translation (evaluation)
    print(f"\n[1] 正向路径 p(t) (Alexander Polynomial term):")
    print(p_t)

    # 3. 计算 q(t): 反向路径 Evaluation
    # 反向路径即字符串逆序: "BAAB..."
    rev_relator = relator_str[::-1]
    M_q = sp.eye(2)
    for char in rev_relator:
        if char in ops:
            M_q = M_q * ops[char][0]

    q_t = sp.simplify(M_q[0, 1])
    print(f"\n[2] 反向路径 q(t):")
    print(q_t)

    # 4. 计算全局算术挠率 tau(t) 并因式分解
    tau = sp.simplify(p_t - q_t)
    print(f"\n[3] 全局算术挠率 tau(t) = p(t) - q(t):")
    print(tau)

    print(f"\n[4] tau(t) 的因式分解 (验证 (t^K - 1) 结构):")
    factorized_tau = sp.factor(tau)
    print(factorized_tau)

    # 5. 验证“对偶求和公式” (Hypothesis Structural Verification)
    # 公式: Sum( delta_k * (t^Ek - t^-Ek) )
    # 我们需要重新遍历路径来收集 delta (加法贡献) 和 Ek (前缀乘法指数)

    theoretical_sum = 0

    # 正向遍历以收集每一项的贡献
    # 注意：矩阵 M_total = M_0 * M_1 * ... * M_n
    # 第 k 项 M_k 的加法贡献 delta_k 会被其左边的所有矩阵缩放。
    # 左边累积的缩放因子即为 t^Ek。

    current_scale_exponent = 0

    # 我们从左向右扫描字符串 (即从最外层函数向内层)
    # 字符串: c0 c1 c2 ...
    # 矩阵: M_c0 * M_c1 ...
    # 当处理 M_ck 时，它被左边的 M_c0...M_c(k-1) 缩放

    for char in relator_str:
        mat, delta, exp_change = ops[char]

        if delta != 0:
            # 这是一个加法项
            # 它的贡献是 delta * t^(current_scale_exponent)
            # 在对偶假设中，它对应的反向项贡献是 delta * t^(-current_scale_exponent)
            term = delta * (t ** current_scale_exponent - t ** (-current_scale_exponent))
            theoretical_sum += term

        # 更新累积缩放指数
        current_scale_exponent += exp_change

    theoretical_sum = sp.simplify(theoretical_sum)

    print(f"\n[5] 验证对偶求和假设 (Sum(delta * (t^E - t^-E))):")
    print(f"理论构造值: {theoretical_sum}")

    check = sp.simplify(tau - theoretical_sum)
    if check == 0:
        print(">>> 验证成功！挠率完美符合对偶结构！ <<<")
    else:
        print(f">>> 验证差异: {check}")


# --- 执行测试 ---
# 测试用例 1: Figure Eight Knot (4_1)
# Relator 来源: knots_01.pdf
relator_4_1 = "abABaBabABaBAbAb"
verify_aeg_torsion("8_10", relator_4_1)

# 你可以尝试取消注释下面的行来测试其他 Relator (如果已知)
# 例如 Trefoil (3_1) 的 Relator 通常是 a^3 = b^2 -> a a a B B
# verify_aeg_torsion("3_1", "aaaBB")