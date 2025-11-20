import sympy as sp


def analyze_link_torsion(link_name, relator_str):
    """
    AEG 2.0: 双变量链环挠率分析
    验证 Blanchfield Pairing 迹象与多变量亚历山大多项式结构。
    """
    # 1. 定义双变量
    t1, t2 = sp.symbols('t1 t2')

    # 2. 定义对称仿射表示 (Symmetric Affine Representation)
    # 假设: 两个生成元都是"缩放+平移"算子，分别携带 t1, t2
    # M = [[t, 1], [0, 1]] -> x' = t*x + 1

    M_a = sp.Matrix([[t1, 1], [0, 1]])
    M_b = sp.Matrix([[t2, 1], [0, 1]])

    # 计算逆矩阵
    M_A = M_a.inv()  # a^-1
    M_B = M_b.inv()  # b^-1

    # 映射表
    ops = {
        'a': M_a, 'b': M_b,
        'A': M_A, 'B': M_B
    }

    print(f"--- 分析链环: {link_name} ---")
    print(f"Relator: {relator_str}")
    print(f"表示假设: a -> Aff(t1, 1), b -> Aff(t2, 1)")

    # 3. 计算正向路径 Evaluation p(t1, t2)
    M_p = sp.eye(2)
    # 注意矩阵乘法顺序：从左到右处理字符串 (对应函数最内层到最外层?
    # 修正: 按照之前的逻辑，字符串首字符是最外层函数，即最左边的矩阵)
    # 让我们保持与单变量实验一致的逻辑: M_total = M_char0 * M_char1...

    for char in relator_str:
        if char in ops:
            M_p = M_p * ops[char]

    p_val = sp.simplify(M_p[0, 1])
    # 提取通分后的分子分母，便于观察
    p_num, p_den = sp.fraction(sp.together(p_val))

    print(f"\n[1] 正向路径 p(t1, t2):")
    print(p_val)

    # 4. 计算反向路径 q(t1, t2)
    rev_relator = relator_str[::-1]
    M_q = sp.eye(2)
    for char in rev_relator:
        if char in ops:
            M_q = M_q * ops[char]

    q_val = sp.simplify(M_q[0, 1])
    print(f"\n[2] 反向路径 q(t1, t2):")
    print(q_val)

    # 5. 计算互挠率 / 全局挠率
    tau = sp.simplify(p_val - q_val)
    print(f"\n[3] 互挠率 tau = p - q:")
    print(tau)

    print(f"\n[4] 因子分析 (寻找 Alexander Polynomial):")
    factorized = sp.factor(tau)
    print(factorized)

    # 6. 验证是否包含 (t1-1) 或 (t2-1) 这种分圆因子
    # 对于 Whitehead Link, Delta(x,y) = (x-1)(y-1)
    print(f"\n[5] 结构特征检查:")
    check_poly = (t1 - 1) * (t2 - 1)
    if sp.simplify(tau / check_poly).is_polynomial(t1, t2):
        print(f"发现核心结构: (t1-1)(t2-1) 是 tau 的因子！")
    else:
        # 尝试其他可能的因子
        pass


# --- 执行实验 ---

# 1. Hopf Link (最简单的链环)
# Relator: Commutator [a, b] = a b A B
# 预期: 应该非常简单，可能与 (t1-1)(t2-1) 有关
analyze_link_torsion("Hopf Link", "abAB")

print("\n" + "=" * 30 + "\n")

# 2. Whitehead Link (5^2_1)
# Group Relator: a b a^-1 b^-1 a^-1 b a b^-1
# 字符串: a b A B A b a B
# 这是最经典的 Whitehead Link 表示
analyze_link_torsion("Whitehead Link", "abABAbab")  # 注意大小写 A=a^-1, B=b^-1