import heapq


def merge_k_lists(lists):
    # Ініціалізуємо мінімальну купу
    min_heap = []
    # Ініціалізуємо ітератори для кожного списку
    iterators = [iter(x) for x in lists]

    # Додаємо перший елемент кожного списку в купу разом з індексом списку і ітератором
    for list_idx, it in enumerate(iterators):
        first_element = next(it, None)
        if first_element is not None:
            heapq.heappush(min_heap, (first_element, list_idx, it))
    # print(min_heap)
    # Ініціалізуємо результат
    result = []

    # Поки купа не порожня, витягуємо найменший елемент і додаємо його до результату
    while min_heap:
        val, list_idx, it = heapq.heappop(min_heap)
        result.append(val)
        # Беремо наступний елемент з того ж списку та додаємо його до купи
        next_element = next(it, None)
        if next_element is not None:
            heapq.heappush(min_heap, (next_element, list_idx, it))

    return result


if __name__ == "__main__":
    lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
    merged_list = merge_k_lists(lists)
    print("Відсортований список:", merged_list)
