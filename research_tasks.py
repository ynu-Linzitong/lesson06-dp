"""独立研究任务的验证小程序（选做）

① n 皇后：8 皇后一共有 92 个解。
② 完全背包：把 0-1 的“上一行”改成“本行”，物品可重复选。
"""

ITEMS = [
    (1, "帐篷", 300, 60),
    (2, "炉具", 200, 40),
    (3, "睡袋", 350, 120),
    (4, "食物", 400, 150),
    (5, "水具", 250, 45),
]


def solve_n_queens(n):
    """回溯法求 n 皇后解的数量。"""
    count = 0
    cols, diag1, diag2 = set(), set(), set()

    def dfs(row):
        nonlocal count
        if row == n:
            count += 1
            return
        for col in range(n):
            if col in cols or row - col in diag1 or row + col in diag2:
                continue
            cols.add(col); diag1.add(row - col); diag2.add(row + col)
            dfs(row + 1)
            cols.remove(col); diag1.remove(row - col); diag2.remove(row + col)

    dfs(0)
    return count


def complete_knapsack(capacity, items):
    """完全背包：一维 dp，容量从小到大遍历（同一件可反复取）。"""
    dp = [0] * (capacity + 1)
    for _, _, w, v in items:
        for c in range(w, capacity + 1):   # 正序：本行结果可再次使用
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]


if __name__ == "__main__":
    print(f"8 皇后解的数量：{solve_n_queens(8)}")
    print(f"完全背包 1000g 最优：{complete_knapsack(1000, ITEMS)}")
    print(f"完全背包 800g 最优：{complete_knapsack(800, ITEMS)}")
