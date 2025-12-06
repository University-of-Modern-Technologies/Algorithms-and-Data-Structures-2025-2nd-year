from BTrees.IOBTree import IOBTree
import random
import timeit


def measure_operation(operation, iterations=1):
    """Вимірює час виконання операції з використанням timeit для точності"""
    if iterations == 1:
        return timeit.timeit(operation, number=1)
    else:
        return timeit.timeit(operation, number=iterations) / iterations


def performance_comparison():
    """
    Детальне порівняння продуктивності
    """
    print("\n\n=== DETАЛЬНЕ ПОРІВНЯННЯ ПРОДУКТИВНОСТІ ===\n")

    sizes = [100000, 500000, 1000000]

    for size in sizes:
        print(f"--- Тест для {size} елементів ---")

        # Генерація даних
        test_data = [(random.randint(1, 1000000), f"data_{i}") for i in range(size)]

        btree = IOBTree()
        btree_time = measure_operation(
            lambda: [btree.__setitem__(k, v) for k, v in test_data]
        )
        for k, v in test_data:
            btree[k] = v

        py_dict = {}
        dict_time = measure_operation(
            lambda: [py_dict.__setitem__(k, v) for k, v in test_data]
        )
        for k, v in test_data:
            py_dict[k] = v

        # Діапазонний запит (10% даних)
        test_keys = sorted([k for k, _ in test_data])
        range_start = test_keys[len(test_keys) // 10]
        range_end = test_keys[len(test_keys) // 10 + len(test_keys) // 20]

        btree_range_time = measure_operation(
            lambda: list(btree.items(range_start, range_end))
        )
        btree_range = list(btree.items(range_start, range_end))

        dict_range_time = measure_operation(
            lambda: [
                (k, v) for k, v in py_dict.items() if range_start <= k <= range_end
            ]
        )
        dict_range = [
            (k, v) for k, v in py_dict.items() if range_start <= k <= range_end
        ]

        if dict_time > 0:
            print(
                f"  Вставка - B-tree: {btree_time:.4f}s, Dict: {dict_time:.4f}s ({btree_time/dict_time:.2f}x)"
            )
        else:
            print(
                f"  Вставка - B-tree: {btree_time:.4f}s, Dict: {dict_time:.4f}s (Dict миттєвий)"
            )
        print(
            f"  Діапазон - B-tree: {btree_range_time:.6f}s ({len(btree_range)}), Dict: {dict_range_time:.6f}s ({len(dict_range)})"
        )
        if dict_range_time > 0 and btree_range_time > 0:
            print(f"  Перевага діапазону: {dict_range_time/btree_range_time:.1f}x")
        elif btree_range_time == 0 and dict_range_time > 0:
            print(
                f"  Перевага діапазону: B-tree миттєвий за Dict ({dict_range_time:.6f}s)"
            )
        elif dict_range_time == 0 and btree_range_time > 0:
            print(
                f"  Перевага діапазону: Dict миттєвий за B-tree ({btree_range_time:.6f}s)"
            )
        else:
            print(f"  Обидві структури миттєві")


if __name__ == "__main__":
    performance_comparison()
