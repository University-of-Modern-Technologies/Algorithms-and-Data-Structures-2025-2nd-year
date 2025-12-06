from BTrees.IOBTree import IOBTree
import random
import sys
import timeit


# функції для вимірювання продуктивності
def measure_operation(operation, iterations=1):
    """Вимірює час виконання операції з використанням timeit для точності"""
    if iterations == 1:
        return timeit.timeit(operation, number=1)
    else:
        return timeit.timeit(operation, number=iterations) / iterations


def measure_search(data_structure, key, iterations=1000):
    """Вимірює час пошуку ключа в структурі даних"""
    return timeit.timeit(lambda: key in data_structure, number=iterations) / iterations


def demo_btree_capabilities():
    """
    Оновлена демонстрація B-tree з порівнянням з Python dict
    """
    print("=== ПОРІВНЯННЯ B-TREE VS PYTHON DICT ===\n")

    # Створюємо структури даних
    db_index = IOBTree()  # B-дерево
    python_dict = {}  # Python dictionary

    print("--- 1. Генерація та вставка даних ---")
    data_size = 50000  # Зменшено для швидшої демонстрації
    print(f"Генеруємо {data_size} записів...")

    # Генерація даних
    test_data = []
    for i in range(data_size):
        random_id = random.randint(1, 1000000)
        test_data.append((random_id, f"User_Data_{random_id}"))

    btree_insert_time = measure_operation(
        lambda: [db_index.__setitem__(key, value) for key, value in test_data]
    )

    dict_insert_time = measure_operation(
        lambda: [python_dict.__setitem__(key, value) for key, value in test_data]
    )

    print(f"B-дерево вставка: {btree_insert_time:.4f} сек ({len(db_index)} елементів)")
    print(f"Dict вставка: {dict_insert_time:.4f} сек ({len(python_dict)} елементів)")
    print(
        f"Співвідношення швидкості (B-tree/dict): {btree_insert_time/dict_insert_time:.2f}x"
    )

    # Отримуємо діапазон ключів
    min_k, max_k = db_index.minKey(), db_index.maxKey()
    print(f"Діапазон ключів у дереві: від {min_k} до {max_k}")

    print("\n--- 2. Пошук за ключем ---")
    test_keys = [min_k, max_k, random.choice(list(db_index.keys()))]

    print("Порівняння швидкості пошуку:")
    for key in test_keys:
        btree_search_time = measure_search(db_index, key, iterations=1000)
        dict_search_time = measure_search(python_dict, key, iterations=1000)

        print(
            f"  Ключ {key}: B-tree {btree_search_time:.6f}s, Dict {dict_search_time:.6f}s"
        )

    print("\n--- 3. ДІАПАЗОННІ ЗАПИТИ (КЛЮЧОВА ПЕРЕВАГА B-TREE) ---")
    start_range = 100000
    end_range = 100500

    print(f"Шукаємо записи в діапазоні ID: {start_range} - {end_range}")

    btree_range_time = measure_operation(
        lambda: list(db_index.items(start_range, end_range))
    )
    btree_result = list(db_index.items(start_range, end_range))
    """
    Це ілюстрація того, чому SELECT fullname FROM users WHERE id BETWEEN 100 AND 200 працює швидко в базах даних: SQL-движок використовує саме такий механізм обходу B-дерева, як показано в коді вище.
    """

    dict_range_time = measure_operation(
        lambda: [
            (k, v) for k, v in python_dict.items() if start_range <= k <= end_range
        ]
    )
    dict_result = [
        (k, v) for k, v in python_dict.items() if start_range <= k <= end_range
    ]

    print(
        f"B-дерево діапазонний запит: {btree_range_time:.6f} сек ({len(btree_result)} результатів)"
    )
    print(
        f"Dict діапазонний запит: {dict_range_time:.6f} сек ({len(dict_result)} результатів)"
    )

    if dict_range_time > 0 and btree_range_time > 0:
        print(f"B-tree швидше в: {dict_range_time/btree_range_time:.1f} разів!")
    elif btree_range_time == 0 and dict_range_time > 0:
        print(f"B-tree миттєво швидший за Dict ({dict_range_time:.6f}s)")
    elif dict_range_time == 0 and btree_range_time > 0:
        print(f"Dict миттєво швидший за B-tree ({btree_range_time:.6f}s)")

    print(f"\nЗнайдені записи:")
    for i, (k, v) in enumerate(btree_result[:5]):  # Показати перші 5
        print(f"  [{i+1}] Key: {k} -> Value: {v}")
    if len(btree_result) > 5:
        print(f"  ... та ще {len(btree_result)-5} записів")

    print("\n--- 4. СОРТУВАННЯ ТА ПОРЯДОК ---")
    print("B-дерево автоматично підтримує відсортований порядок:")

    btree_sort_time = measure_operation(lambda: list(db_index.keys()))
    btree_sorted = list(db_index.keys())

    dict_sort_time = measure_operation(lambda: sorted(python_dict.keys()))
    dict_sorted = sorted(python_dict.keys())

    print(f"B-дерево відсортовані ключі: {btree_sort_time:.6f} сек")
    print(f"Dict сортування ключів: {dict_sort_time:.6f} сек")
    print(f"B-tree швидше в: {dict_sort_time/btree_sort_time:.1f} разів!")

    # Перевірка чи результати однакові
    print(f"Результати однакові: {btree_sorted == dict_sorted}")

    print("\n--- 5. АНАЛІЗ ВИКОРИСТАННЯ ПАМ'ЯТІ ---")

    btree_memory = sys.getsizeof(db_index) + len(db_index) * 64  # Приблизна оцінка
    dict_memory = sys.getsizeof(python_dict) + len(python_dict) * 72  # Приблизна оцінка

    print(f"B-дерево пам'ять (приблизно): {btree_memory/1024:.1f} KB")
    print(f"Dict пам'ять (приблизно): {dict_memory/1024:.1f} KB")
    print(f"Ефективність пам'яті B-tree: {(dict_memory/btree_memory):.2f}x краще")


if __name__ == "__main__":
    demo_btree_capabilities()
