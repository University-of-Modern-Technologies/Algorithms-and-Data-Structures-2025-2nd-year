"""
MEDIAN FINDER - Пошук медіани в потоці даних

Цей приклад демонструє продвинуте використання куп для вирішення класичної задачі:
знаходження медіани в потоці даних, що постійно надходять.

ЩО РОБИТЬ:
- Використовує ДВІ купи одночасно (max heap + min heap)
- Знаходить медіану за O(1), додає числа за O(log n)
- Підтримує баланс між двома купами для швидкого доступу

ДЛЯ ЧОГО:
- Моніторинг метрик в реальному часі (ціни, час відгуку)
- Аналіз потокових даних без збереження всього масиву
- Демонстрація комбінації min та max heap для складних задач

ПРИКЛАДИ ВИКОРИСТАННЯ:
1. Моніторинг медіанної ціни акцій
2. Відстеження медіанного часу відгуку сервера
"""

import heapq


class MedianFinder:
    """
    Знаходить медіану в потоці даних за O(log n) для додавання
    та O(1) для отримання медіани.

    Використовує дві купи:
    - small (max heap): зберігає меншу половину чисел
    - large (min heap): зберігає більшу половину чисел
    """

    def __init__(self):
        self.small = []  # max heap (інвертовані значення для Python)
        self.large = []  # min heap

    def add_num(self, num: int):
        """Додає число до структури"""
        # Завжди спочатку додаємо в small
        heapq.heappush(self.small, -num)

        # Переміщуємо найбільший елемент з small в large
        heapq.heappush(self.large, -heapq.heappop(self.small))

        # Балансуємо розміри: small має бути >= large
        if len(self.small) < len(self.large):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def find_median(self) -> float:
        """Повертає поточну медіану"""
        if len(self.small) > len(self.large):
            # Логіка: При непарній кількості елементів,
            # медіана - це найбільший елемент з меншої половини (вершина small).
            return -self.small[0]  # непарна кількість елементів
        # Логіка: При парній кількості, медіана - це середнє двох центральних елементів:
        #    Найбільший з меншої половини: -small[0]
        #    Найменший з більшої половини: large[0]
        return (-self.small[0] + self.large[0]) / 2  # парна кількість


def demo_stock_prices():
    """Приклад: моніторинг медіанної ціни акцій в реальному часі"""
    print("=== Моніторинг медіанної ціни акцій ===\n")

    mf = MedianFinder()
    prices = [100, 102, 98, 105, 97, 110, 95, 108]

    for i, price in enumerate(prices, 1):
        mf.add_num(price)
        median = mf.find_median()
        print(f"День {i}: ціна ${price}, медіанна ціна: ${median:.2f}")


def demo_response_times():
    """Приклад: моніторинг медіанного часу відгуку сервера"""
    print("\n=== Моніторинг часу відгуку сервера (мс) ===\n")

    mf = MedianFinder()
    response_times = [45, 120, 38, 250, 42, 48, 350, 40, 55, 43]

    for i, time in enumerate(response_times, 1):
        mf.add_num(time)
        median = mf.find_median()
        status = "⚠️ ПОВІЛЬНО" if median > 100 else "✓ OK"
        print(f"Запит {i:2d}: {time:3d}мс | Медіана: {median:6.1f}мс {status}")


if __name__ == "__main__":
    demo_stock_prices()
    demo_response_times()
