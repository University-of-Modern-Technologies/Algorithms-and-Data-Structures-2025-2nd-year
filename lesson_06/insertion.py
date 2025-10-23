def insertion_sort(_lst):
    _lst = _lst[:]  # lst = lst.copy()
    for i in range(1, len(_lst)):
        key = _lst[i]
        j = i - 1
        while j >= 0 and key < _lst[j]:
            _lst[j + 1] = _lst[j]
            j -= 1
        _lst[j + 1] = key
    return _lst


def insertion_sort_steps(lst):
    """Повертає список кроків (масив, активні індекси) для візуалізації"""
    steps = [(lst.copy(), [])]
    _lst = lst[:]
    for i in range(1, len(_lst)):
        key = _lst[i]
        j = i - 1
        steps.append((_lst.copy(), [i]))  # показуємо який елемент вставляємо
        while j >= 0 and key < _lst[j]:
            _lst[j + 1] = _lst[j]
            steps.append((_lst.copy(), [j, j + 1]))
            j -= 1
        _lst[j + 1] = key
        steps.append((_lst.copy(), [j + 1]))
    steps.append((_lst.copy(), []))
    return steps


if __name__ == '__main__':
    lst = [5, 3, 8, 4, 2]
    r = insertion_sort(lst)
    print(lst, r)