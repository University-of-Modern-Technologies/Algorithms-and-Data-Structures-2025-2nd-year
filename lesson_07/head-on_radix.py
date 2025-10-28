from collections import defaultdict
from typing import List, Optional


def radix_sort(arr: List[int]) -> List[int]:
    if not arr:
        return []

    max_num = max(arr)
    pos = 1

    result = arr[:]
    while max_num // pos > 0:
        # створюємо словник позицій
        buckets = defaultdict(list)
        # {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}

        # заповнюємо його
        for x in result:
            d = (x // pos) % 10
            buckets[d].append(x)

        # збираємо назад у правильному порядку цифр
        result = [x for d in range(10) for x in buckets[d]]
        pos *= 10

    return result


arr = [3, 89, 67, 254, 9, 21, 185, 4, 62]
print(radix_sort(arr))
