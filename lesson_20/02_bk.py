def binomial_coefficient(n: int, k: int) -> int:  # O(n * k)
    dp = [[0 for _ in range(k + 1)] for _ in range(n + 1)]  # O(n * k)

    for i in range(n + 1):
        for j in range(min(i, k) + 1):
            if j == 0 or j == i:
                dp[i][j] = 1
            else:
                dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j]

    return dp[n][k]


if __name__ == "__main__":
    print(binomial_coefficient(5, 2))
