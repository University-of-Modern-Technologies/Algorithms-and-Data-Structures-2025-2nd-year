"""
Longest Common Subsequence (LCS) - найдовша спільна підпослідовність
ПОСТАНОВКА ЗАДАЧІ:
Дано: два рядки X і Y
Мета: знайти найдовшу підпослідовність, яка присутня в обох рядках
Приклад:
X = "ABCDGH"
Y = "AEDFHR"
LCS = "ADH" (довжина 3)
Підпослідовність - це послідовність символів, що зберігає порядок, але не обов'язково йде підряд
"""


def lcs_dp(X, Y):
    m, n = len(X), len(Y)  # O(1)

    # Створюємо DP таблицю
    dp = [[0] * (n + 1) for _ in range(m + 1)]  # O(m * n)

    # Заповнюємо таблицю
    for i in range(1, m + 1):  # O(m)
        for j in range(1, n + 1):  # O(n)
            if X[i - 1] == Y[j - 1]:  # O(1)
                dp[i][j] = dp[i - 1][j - 1] + 1  # O(1)
            else:  # O(1)
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])  # O(1)

    # Відновлюємо саму послідовність
    lcs = []  # O(1)
    i, j = m, n  # O(1)
    while i > 0 and j > 0:  # O(m + n)
        if X[i - 1] == Y[j - 1]:  # O(1)
            lcs.append(X[i - 1])  # O(1)
            i -= 1  # O(1)
            j -= 1  # O(1)
        elif dp[i - 1][j] > dp[i][j - 1]:  # O(1)
            i -= 1  # O(1)
        else:  # O(1)
            j -= 1  # O(1)

    return dp[m][n], "".join(reversed(lcs))  # O(m + n)


if __name__ == "__main__":
    # Демонстрація
    X = "ABCDGHKLM"
    Y = "AEDFHRHLM"
    length, sequence = lcs_dp(X, Y)
    print(f"Рядок 1: {X}")
    print(f"Рядок 2: {Y}")
    print(f"LCS довжина: {length}")
    print(f"LCS: {sequence}")
