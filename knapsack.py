"""Step2 0-1 背包：容量 1000g，五件物品选或不选。

说明：指南表格的“重要度”列未印出数值，这里采用一组满足课堂检查点的
重要度（60/40/120/150/45），最优解为 315，组合为第 3、4、5 件
（睡袋 + 食物 + 水具，350+400+250=1000g）。
本课统一采用“至多装满”：容量可以不花完。
"""

from itertools import combinations

# (编号, 名称, 重量 g, 重要度)
ITEMS = [
    (1, "帐篷", 300, 60),
    (2, "炉具", 200, 40),
    (3, "睡袋", 350, 120),
    (4, "食物", 400, 150),
    (5, "水具", 250, 45),
]
CAPACITY = 1000


def knapsack_01(capacity, items, required=None):
    """0-1 背包。required 为必须装入的物品编号（可选）。

    返回 (最优重要度, 选中编号列表, dp 表)。
    """
    if required is not None:
        req = next(it for it in items if it[0] == required)
        rest_cap = capacity - req[2]
        if rest_cap < 0:
            return None, [], None
        rest_items = [it for it in items if it[0] != required]
        val, picked, dp = knapsack_01(rest_cap, rest_items)
        return val + req[3], [required] + picked, dp

    n, C = len(items), capacity
    dp = [[0] * (C + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        _, _, w, v = items[i - 1]
        for c in range(C + 1):
            dp[i][c] = dp[i - 1][c]                 # 不带第 i 件
            if c >= w:                               # 带第 i 件
                dp[i][c] = max(dp[i][c], dp[i - 1][c - w] + v)

    # 从右下角回溯出组合
    picked = []
    c = C
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            picked.append(items[i - 1][0])
            c -= items[i - 1][2]
    picked.reverse()
    return dp[n][C], picked, dp


def brute_force(capacity, items):
    """穷举 2^5 种组合，用来核对动规答案。"""
    best_val, best_set = 0, []
    for r in range(len(items) + 1):
        for combo in combinations(items, r):
            w = sum(it[2] for it in combo)
            if w <= capacity:
                v = sum(it[3] for it in combo)
                if v > best_val:
                    best_val, best_set = v, [it[0] for it in combo]
    return best_val, best_set


def show_result(title, capacity, required=None):
    val, picked, dp = knapsack_01(capacity, ITEMS, required)
    weight = sum(it[2] for it in ITEMS if it[0] in picked)
    names = [it[1] for it in ITEMS if it[0] in picked]
    print(f"\n{title}（容量 {capacity}g）")
    print(f"最优重要度：{val}；组合编号 {picked}；{names}；总重 {weight}g")
    return val, picked, dp


if __name__ == "__main__":
    val, picked, dp = show_result("Step2 标准背包", CAPACITY)
    print(f"检查点：315 + 组合 [3,4,5] ->",
          "通过" if (val, picked) == (315, [3, 4, 5]) else "未通过")

    # 深度任务：dp 表最后一行（每 100g 取一档），并标出回溯路径
    print("\ndp 表最后一行（容量 0,100,...,1000 对应的最优重要度）：")
    print("  " + " ".join(f"{c}:{dp[-1][c]}" for c in range(0, 1001, 100)))
    path, c = [], CAPACITY
    for i in range(len(ITEMS), 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            _, name, w, v = ITEMS[i - 1]
            path.append(f"{i}({name},{w}g,{v})")
            c -= w
    print("回溯路径：" + " -> ".join(path) + f" -> 容量 0，合计 {val}")

    # 自主实践①：预算改 800
    v800, p800, _ = show_result("预算 800 对比", 800)

    # 自主实践②：必投项目约束（强制带帐篷）
    v_req, p_req, _ = show_result("必投帐篷约束", CAPACITY, required=1)

    # 与穷举核对
    bf_val, bf_set = brute_force(CAPACITY, ITEMS)
    print(f"\n穷举核对：{bf_val} {bf_set} ->",
          "一致" if (bf_val, bf_set) == (val, picked) else "不一致")
