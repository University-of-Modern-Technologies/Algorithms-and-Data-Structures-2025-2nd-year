import random

from miller_rabin import is_prime


class UniversalHashFunction:
    """
    Універсальна хеш-функція з сімейства ((ax + b) mod p) mod m

    Властивості:
    - p - просте число > max_key
    - a ∈ [1, p-1], b ∈ [0, p-1] вибираються випадково
    - Ймовірність колізії для будь-яких x ≠ y: P(h(x) = h(y)) ≤ 1/m
    """

    def __init__(self, m, max_key):
        """
        m: розмір хеш-таблиці
        max_key: максимальне значення ключа
        """
        self.m = m
        self.p = self._next_prime(max_key)
        self.a = random.randint(1, self.p - 1)
        self.b = random.randint(0, self.p - 1)

    def _next_prime(self, n):
        """Знаходить наступне просте число після n (Miller-Rabin)"""
        candidate = n + 1
        while not is_prime(candidate):
            candidate += 1
        return candidate

    def hash(self, key):
        """Обчислює хеш ключа"""
        if key < 0:
            raise ValueError(f"Key must be non-negative, got {key}")
        return ((self.a * key + self.b) % self.p) % self.m


# Приклад використання: демонстрація розподілу
if __name__ == "__main__":
    print("=" * 60)
    print("УНІВЕРСАЛЬНЕ ХЕШУВАННЯ")
    print("=" * 60)

    # Створюємо хеш-функцію
    m = 10  # розмір таблиці
    max_key = 1000
    hasher = UniversalHashFunction(m, max_key)

    print(f"\nПараметри:")
    print(f"  Розмір таблиці (m): {m}")
    print(f"  Просте число (p): {hasher.p}")
    print(f"  Коефіцієнти: a={hasher.a}, b={hasher.b}")
    print(f"  Формула: h(k) = ((a*k + b) mod p) mod m")

    # Тестуємо на прикладах
    print(f"\nПриклади:")
    test_keys = [123, 456, 789, 1000, 55, 66, 77]
    for key in test_keys:
        print(f"  h({key}) = {hasher.hash(key)}")

    # Демонстрація розподілу
    print(f"\n{'='*60}")
    print("АНАЛІЗ РОЗПОДІЛУ (1000 випадкових ключів)")
    print("=" * 60)

    buckets = [0] * m
    num_keys = 1000

    for _ in range(num_keys):
        key = random.randint(0, max_key)
        bucket = hasher.hash(key)
        buckets[bucket] += 1

    print("\nРозподіл по корзинам:")
    for i, count in enumerate(buckets):
        bar = "█" * (count // 10)
        print(f"  Корзина {i}: {count:3d} {bar}")

    # Статистика
    avg = num_keys / m
    max_bucket = max(buckets)
    min_bucket = min(buckets)

    print(f"\nСтатистика:")
    print(f"  Ідеальний розподіл: {avg:.1f} ключів/корзина")
    print(f"  Мін: {min_bucket}, Макс: {max_bucket}")
    print(f"  Відхилення: {max_bucket - min_bucket}")
    print(f"  Якість: {'✓ Хороший' if max_bucket - min_bucket < avg else '✗ Поганий'}")
