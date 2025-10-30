from math import isclose

def binary_search(arr, x):
    """
    Повертає кортеж (value, status), де:
    status це:
    - 0 якщо масив пустий
    - 1 якщо знайдено точне значення
    - 2 якщо знайдена верхня границя
    - 3 якщо значення більше за максимум
    """
    if not arr:  # пустий масив
        return None, 0

    if x > arr[-1]:  # більше за максимум
        return None, 3

    low = 0
    high = len(arr) - 1
    upper_bound = None

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == x:
            return arr[mid], 1  # точне значення
        if arr[mid] < x:
            low = mid + 1
        else:
            upper_bound = arr[mid]  # запам'ятовуємо поточну верхню границю
            high = mid - 1

    return upper_bound, 2  # повертаємо збережену верхню границю


def binary_search_low(arr, x):
    """
    Альтернативний варіант пошуку через low.
    Повертає кортеж (value, status), де:
    status це:
    - 0 якщо масив пустий
    - 1 якщо знайдено точне значення
    - 2 якщо знайдена верхня границя
    - 3 якщо значення більше за максимум
    """
    if not arr:  # пустий масив
        return None, 0

    if x > arr[-1]:  # більше за максимум
        return None, 3

    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == x:
            return arr[mid], 1  # точне значення
        if arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1

    # low тепер вказує на позицію першого елемента, який >= x
    return arr[low], 2


if __name__ == "__main__":
    # Демонстрація / швидкі тести з дробовими числами
    tests = [
        ([1.1, 2.2, 3.3, 4.4, 5.5], 3.3),  # точний збіг
        ([1.1, 2.2, 3.3, 4.4, 5.5], 3.0),  # між 2.2 і 3.3 -> верхня границя
        ([1.1, 2.2, 3.3, 4.4, 5.5], 6.0),  # більше за максимум
        ([1.1, 2.2, 3.3, 4.4, 5.5], 0.5),  # менше за мінімум
        ([], 2.0),  # порожній масив
    ]

    status_messages = {
        0: "масив пустий",
        1: "точне значення",
        2: "верхня границя",
        3: "більше за максимум",
    }

    print("=== Варіант через upper_bound ===")
    for arr, x in tests:
        value, status = binary_search(arr, x)
        print(f"arr={arr} x={x} -> value={value}, тип={status_messages[status]}")

    print("\n=== Варіант через low ===")
    for arr, x in tests:
        value, status = binary_search_low(arr, x)
        print(f"arr={arr} x={x} -> value={value}, тип={status_messages[status]}")
