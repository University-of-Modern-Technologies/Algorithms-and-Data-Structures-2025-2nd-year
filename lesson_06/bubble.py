def bubble_sort(lst):
    _lst = lst.copy()
    n = len(_lst)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if _lst[j] > _lst[j + 1]:
                _lst[j], _lst[j + 1] = _lst[j + 1], _lst[j]
    return _lst


def bubble_sort_steps(lst):
    """Повертає список кроків (масив, активні індекси) для візуалізації"""
    steps = [(lst.copy(), [])]  # початковий стан без активних елементів
    _lst = lst.copy()
    n = len(_lst)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            # Показуємо які елементи порівнюємо
            steps.append((_lst.copy(), [j, j + 1]))
            if _lst[j] > _lst[j + 1]:
                _lst[j], _lst[j + 1] = _lst[j + 1], _lst[j]
                # Показуємо після обміну
                steps.append((_lst.copy(), [j, j + 1]))
    steps.append((_lst.copy(), []))  # фінальний стан
    return steps


if __name__ == '__main__':
    numbers = [5, 3, 8, 4, 2]
    r = bubble_sort(numbers)
    print(numbers, r)