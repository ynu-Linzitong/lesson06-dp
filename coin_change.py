"""Step1 凑硬币：贪心 vs 动态规划

面额 [1, 5, 11]，目标 15。
检查点：贪心 5 枚（11+1+1+1+1），动规 3 枚（5+5+5）。
"""

COINS = [1, 5, 11]
AMOUNT = 15


def coin_greedy(coins, amount):
    """贪心：每一步取不超过余额的最大面额，不回头。"""
    coins = sorted(coins, reverse=True)
    picked = []
    rest = amount
    for c in coins:
        while rest >= c:
            picked.append(c)
            rest -= c
    return len(picked), picked


def coin_dp(coins, amount):
    """动规：dp[c] = 1 + min(dp[c-coin])，并记录选择用于回溯。"""
    INF = amount + 1
    dp = [INF] * (amount + 1)
    choice = [0] * (amount + 1)
    dp[0] = 0
    for c in range(1, amount + 1):
        for coin in coins:
            if coin <= c and dp[c - coin] + 1 < dp[c]:
                dp[c] = dp[c - coin] + 1
                choice[c] = coin
    # 回溯出组合
    picked = []
    c = amount
    while c > 0:
        picked.append(choice[c])
        c -= choice[c]
    return dp[amount], picked


if __name__ == "__main__":
    g_count, g_picked = coin_greedy(COINS, AMOUNT)
    d_count, d_picked = coin_dp(COINS, AMOUNT)
    print(f"面额 {COINS}，目标 {AMOUNT}")
    print(f"贪心：{g_count} 枚，组合 {g_picked}")
    print(f"动规：{d_count} 枚，组合 {d_picked}")
    print("检查点：贪心 5 枚 vs 动规 3 枚 ->",
          "通过" if (g_count, d_count) == (5, 3) else "未通过")
