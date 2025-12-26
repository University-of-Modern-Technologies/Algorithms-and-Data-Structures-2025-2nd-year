"""
Rod Cutting Problem - оптимальне розрізання стрижня

ПОСТАНОВКА ЗАДАЧІ:

Дано: стрижень довжини n, масив цін prices[i] для відрізка довжини i+1

Мета: розрізати стрижень щоб максимізувати прибуток

Приклад:

У нас є стрижень довжини 4 і прайс-лист:

    Відрізок довжини 1 ціна 1
    Відрізок довжини 2 ціна 5
    Відрізок довжини 3 ціна 8
    Відрізок довжини 4 ціна 9

Як можна розрізати стрижень довжини 4:

    Не різати: залишити 1 шматок довжини 4 прибуток = 9
    Розрізати 1+3: 2 шматки (довжини 1 і 3) прибуток = 1 + 8 = 9
    Розрізати 2+2: 2 шматки (обидва довжини 2) прибуток = 5 + 5 = 10
    Розрізати 1+1+2: 3 шматки прибуток = 1 + 1 + 5 = 7
    Розрізати 1+1+1+1: 4 шматки прибуток = 1 + 1 + 1 + 1 = 4

Найкращий варіант: розрізати 2+2, отримаємо прибуток 10.
"""


def rod_cutting_greedy_wrong(length, prices):
    """
    ЖАДІБНИЙ ПІДХІД:
    ────────────────────────────────────────────────────────────
    Стратегія: завжди вибираємо відрізок з найкращою ціною за одиницю
    Проблема: локально оптимальний вибір не дає глобального оптимуму
    """
    # Обчислюємо ціну за одиницю для кожної довжини
    unit_prices = [(prices[i] / (i + 1), i + 1) for i in range(len(prices))]
    unit_prices.sort(reverse=True)  # Сортуємо за спаданням ціни за одиницю

    total_profit = 0
    remaining = length
    cuts = []

    for unit_price, cut_length in unit_prices:
        while remaining >= cut_length:
            cuts.append(cut_length)
            total_profit += prices[cut_length - 1]
            remaining -= cut_length

    return total_profit, cuts


def rod_cutting_dp(length, prices):
    """
    ДИНАМІЧНЕ ПРОГРАМУВАННЯ:
    ────────────────────────────────────────────────────────────
    dp[i] = максимальний прибуток для стрижня довжини i

    Рекурентне співвідношення:
    dp[i] = max(prices[j] + dp[i-j-1]) для всіх j від 0 до i-1
    """
    dp = [0] * (length + 1)
    cuts_dp = [[] for _ in range(length + 1)]

    for i in range(1, length + 1):
        for j in range(i):
            if prices[j] + dp[i - j - 1] > dp[i]:
                dp[i] = prices[j] + dp[i - j - 1]
                cuts_dp[i] = cuts_dp[i - j - 1] + [j + 1]
    print(cuts_dp)
    return dp[length], cuts_dp[length]


if __name__ == "__main__":
    # Демонстрація
    length = 5
    prices = [2, 5, 7, 8, 10]  # для довжин 1,2,3,4,5

    print(f"Довжина стрижня: {length}")
    print(f"Ціни: {prices}")

    greedy_profit, greedy_cuts = rod_cutting_greedy_wrong(length, prices)
    dp_profit, dp_cuts = rod_cutting_dp(length, prices)

    print(f"\nЖадібний підхід: прибуток = {greedy_profit}, розрізи = {greedy_cuts}")
    print(f"ДП підхід: прибуток = {dp_profit}, розрізи = {dp_cuts}")

    # Приклад де жадібний алгоритм помиляється
    print(f"\n{'=' * 50}")
    length2 = 4
    prices2 = [1, 5, 8, 9]  # для довжин 1,2,3,4

    print(f"Довжина стрижня: {length2}")
    print(f"Ціни: {prices2}")

    greedy_profit2, greedy_cuts2 = rod_cutting_greedy_wrong(length2, prices2)
    dp_profit2, dp_cuts2 = rod_cutting_dp(length2, prices2)

    print(f"\nЖадібний підхід: прибуток = {greedy_profit2}, розрізи = {greedy_cuts2}")
    print(f"ДП підхід: прибуток = {dp_profit2}, розрізи = {dp_cuts2}")


# Жадібний: O(n⋅log n) - сортування

# ДП: O(n^2) - подвійний цикл
