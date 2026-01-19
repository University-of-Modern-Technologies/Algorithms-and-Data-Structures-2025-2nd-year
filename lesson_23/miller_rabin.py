import random


def is_prime(n, k=20):  # k - кількість ітерацій (20 для надійності) 1/4^k
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True

    # Знаходимо r та d
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    # Проводимо k тестів
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


if __name__ == "__main__":
    # Приклад використання:
    test_numbers = [
        (2, True),
        (3, True),
        (17, True),
        (561, False),  # Число Кармайкла (3 × 11 × 17)
        (1009, True),
        (1000, False),
    ]

    print("Тест Міллера-Рабіна:")
    for n, expected in test_numbers:
        result = is_prime(n)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {n}: {'просте' if result else 'не просте'}")
