def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def selection_sort_steps(lst):
    """Повертає список кроків (масив, активні індекси) для візуалізації"""
    steps = [(lst.copy(), [])]
    arr = lst.copy()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            # Показуємо який елемент перевіряємо
            steps.append((arr.copy(), [min_idx, j]))
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            # Показуємо перед обміном
            steps.append((arr.copy(), [i, min_idx]))
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            # Показуємо після обміну
            steps.append((arr.copy(), [i, min_idx]))
    steps.append((arr.copy(), []))
    return steps


if __name__ == '__main__':
    numbers = [5, 3, 8, 4, 2]
    r = selection_sort(numbers.copy())
    print(numbers, r)