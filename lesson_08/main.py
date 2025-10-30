import time
import random
from binary_search import binary_search as binary_search_simple
from binary_search_upper import binary_search as binary_search_upper, binary_search_low
from index_linear_search import indexed_sequential_search, create_index_table
from interpolation import interpolation_search


def linear_search(arr, x):
    """Звичайний лінійний пошук для порівняння"""
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1


def measure_time(search_func, arr, x, iterations=1000, **kwargs):
    """Вимірює середній час виконання функції пошуку"""
    start = time.perf_counter()
    for _ in range(iterations):
        search_func(arr, x, **kwargs)
    end = time.perf_counter()
    return (end - start) / iterations * 1_000_000  # мікросекунди


def test_search_algorithms():
    # Розміри масивів для тестування
    sizes = [100, 1_000, 10_000, 100_000]
    
    print("=" * 80)
    print("ПОРІВНЯННЯ АЛГОРИТМІВ ПОШУКУ")
    print("=" * 80)
    
    for size in sizes:
        print(f"\n{'=' * 80}")
        print(f"Розмір масиву: {size:,} елементів")
        print(f"{'=' * 80}")
        
        # Створюємо відсортований масив
        arr = sorted(random.sample(range(size * 10), size))
        
        # Вибираємо три типи елементів для пошуку
        test_cases = [
            ("Елемент на початку", arr[5]),
            ("Елемент в середині", arr[size // 2]),
            ("Елемент в кінці", arr[-5]),
            ("Неіснуючий елемент", size * 10 + 1000)
        ]
        
        for case_name, target in test_cases:
            print(f"\n{case_name}: {target}")
            print("-" * 80)
            
            results = {}
            
            # 1. Лінійний пошук
            time_linear = measure_time(linear_search, arr, target)
            results["Лінійний пошук"] = time_linear
            
            # 2. Бінарний пошук (простий)
            time_binary = measure_time(binary_search_simple, arr, target)
            results["Бінарний пошук"] = time_binary
            
            # 3. Бінарний пошук з верхньою границею
            time_binary_upper = measure_time(
                lambda a, x: binary_search_upper(a, x), arr, target
            )
            results["Бінарний (upper bound)"] = time_binary_upper
            
            # 4. Бінарний пошук через low
            time_binary_low = measure_time(
                lambda a, x: binary_search_low(a, x), arr, target
            )
            results["Бінарний (low)"] = time_binary_low
            
            # 5. Індексно-послідовний пошук
            step = 10  # фіксований крок, як в оригіналі
            index_table = create_index_table(arr, step)
            time_indexed = measure_time(
                lambda a, x: indexed_sequential_search(a, index_table, x),
                arr, target
            )
            results["Індексно-послідовний"] = time_indexed
            
            # 6. Інтерполяційний пошук
            time_interp = measure_time(interpolation_search, arr, target)
            results["Інтерполяційний"] = time_interp
            
            # Виводимо результати відсортовані за швидкістю
            sorted_results = sorted(results.items(), key=lambda x: x[1])
            
            print(f"{'Алгоритм':<30} {'Час (мкс)':<15} {'Відносна швидкість'}")
            print("-" * 80)
            
            fastest_time = sorted_results[0][1]
            for name, exec_time in sorted_results:
                relative = exec_time / fastest_time
                print(f"{name:<30} {exec_time:>10.3f} мкс   {relative:>6.2f}x")
    
    print("\n" + "=" * 80)
    print("ВИСНОВКИ")
    print("=" * 80)
    print("""
1. Лінійний пошук: O(n) - найповільніший, але працює на несортованих масивах
2. Бінарний пошук: O(log n) - класичний вибір для відсортованих масивів
3. Інтерполяційний: O(log log n) - найшвидший на рівномірно розподілених даних
4. Індексно-послідовний: O(log n) - бінарний пошук + лінійний в малому діапазоні
    """)


def detailed_test():
    """Детальний тест на невеликому масиві"""
    print("\n" + "=" * 80)
    print("ДЕТАЛЬНИЙ ТЕСТ НА МАЛОМУ МАСИВІ")
    print("=" * 80)
    
    arr = [2, 3, 4, 10, 40, 50, 60, 70, 80, 90, 100]
    test_values = [10, 39, 100, 101]
    
    print(f"\nМасив: {arr}")
    
    for x in test_values:
        print(f"\n{'=' * 80}")
        print(f"Шукаємо елемент: {x}")
        print(f"{'=' * 80}")
        
        # Лінійний
        result = linear_search(arr, x)
        print(f"Лінійний пошук:           індекс = {result}")
        
        # Бінарний простий
        result = binary_search_simple(arr, x)
        print(f"Бінарний пошук:           індекс = {result}")
        
        # Бінарний з верхньою границею
        value, status = binary_search_upper(arr, x)
        status_names = {
            0: "масив пустий",
            1: "точне значення",
            2: "верхня границя",
            3: "більше за максимум"
        }
        print(f"Бінарний (upper bound):   значення = {value}, статус = {status_names[status]}")
        
        # Бінарний через low
        value, status = binary_search_low(arr, x)
        print(f"Бінарний (low):           значення = {value}, статус = {status_names[status]}")
        
        # Індексно-послідовний
        index_table = create_index_table(arr, 3)
        result = indexed_sequential_search(arr, index_table, x)
        print(f"Індексно-послідовний:     індекс = {result}")
        
        # Інтерполяційний
        result = interpolation_search(arr, x)
        print(f"Інтерполяційний пошук:    індекс = {result}")


if __name__ == "__main__":
    # Спочатку детальний тест
    detailed_test()
    
    # Потім порівняльний аналіз продуктивності
    print("\n\n")
    test_search_algorithms()

