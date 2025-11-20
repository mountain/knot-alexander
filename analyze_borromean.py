import sympy as sp


def analyze_borromean_rings():
    """
    AEG 3.0: 三变量博罗梅安环 (Borromean Rings) 验证
    目标: 验证是否能捕捉到 (t1-1)(t2-1)(t3-1) 这种三体纠缠结构。
    """
    # 1. 定义三变量
    t1, t2, t3 = sp.symbols('t1 t2 t3')

    # 2. 对称仿射表示 (Symmetric Affine Representation)
    # 假设: 三个组件都在同一个 1D 空间上作用，但携带不同的缩放因子
    M_a = sp.Matrix([[t1, 1], [0, 1]])
    M_b = sp.Matrix([[t2, 1], [0, 1]])
    M_c = sp.Matrix([[t3, 1], [0, 1]])

    # 逆矩阵
    M_A = M_a.inv()
    M_B = M_b.inv()
    M_C = M_c.inv()

    ops = {
        'a': M_a, 'b': M_b, 'c': M_c,
        'A': M_A, 'B': M_B, 'C': M_C
    }

    # 3. 构造 Relator: [a, [b, c^-1]]
    # 这是一个典型的 Brunnian 链接的 Relator 形式
    # [b, C] = b C B c
    # [a, [b, C]] = a (b C B c) A (b C B c)^-1
    #             = a b C B c A C b c B

    relator_str = "abCBcACbcB"

    print(f"--- 分析对象: Borromean Rings (6^3_2) ---")
    print(f"Relator: {relator_str} (来源于换位子 [a, [b, c^-1]])")
    print(f"表示: a->(t1,1), b->(t2,1), c->(t3,1)")

    # 4. 计算正向路径 p
    M_p = sp.eye(2)
    for char in relator_str:
        M_p = M_p * ops[char]
    p_val = sp.simplify(M_p[0, 1])

    print(f"\n[1] 正向路径 p(t1, t2, t3):")
    # 只是为了打印好看一点，不做 fully expansion 因为太长
    print(p_val)

    # 5. 计算反向路径 q
    rev_relator = relator_str[::-1]
    M_q = sp.eye(2)
    for char in rev_relator:
        M_q = M_q * ops[char]
    q_val = sp.simplify(M_q[0, 1])

    # 6. 计算互挠率
    tau = sp.simplify(p_val - q_val)
    print(f"\n[2] 互挠率 tau = p - q:")
    # print(tau) # 可能太长，先不打印原始值

    # 7. 核心验证: 是否包含亚历山大多项式因子 (t1-1)(t2-1)(t3-1)
    print(f"\n[3] 因子分析 (寻找 Borromean 核心结构):")

    # 预期核心
    core_poly = (t1 - 1) * (t2 - 1) * (t3 - 1)

    # 试除
    ratio = sp.simplify(tau / core_poly)

    if ratio.is_polynomial(t1, t2, t3) or ratio.as_numer_denom()[1] == t1:
        # 允许分母是 t1 (类似之前的 Whitehead link 结果)
        print(f">>> 成功捕获核心因子 (t1-1)(t2-1)(t3-1)！ <<<")
        print("剩余因子结构 (Residual):")
        print(sp.factor(ratio))
    else:
        print("未直接发现完整的三元因子，尝试部分因式分解...")
        print(sp.factor(tau))


# --- 运行 ---
analyze_borromean_rings()