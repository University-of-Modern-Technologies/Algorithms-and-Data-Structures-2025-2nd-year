"""Тести для перевірки правильності алгоритмів сортування"""
from bubble import bubble_sort_steps
from insertion import insertion_sort_steps
from selection import selection_sort_steps


def test_algorithm(name, sort_func, test_cases):
    """Тестує алгоритм на різних тестових випадках"""
    print(f"\n{'='*50}")
    print(f"Тестування {name}")
    print('='*50)
    
    all_passed = True
    for i, test_case in enumerate(test_cases, 1):
        steps = sort_func(test_case)
        start_data, start_indices = steps[0]
        end_data, end_indices = steps[-1]
        expected = sorted(test_case)
        
        passed = end_data == expected
        all_passed = all_passed and passed
        
        status = "✓" if passed else "✗"
        print(f"{status} Тест {i}: {start_data} -> {end_data} ({len(steps)} кроків)")
        
        if not passed:
            print(f"  Очікувалось: {expected}")
    
    if all_passed:
        print(f"\n✓ Всі тести пройдено!")
    else:
        print(f"\n✗ Деякі тести не пройшли!")
    
    return all_passed


def main():
    # Різні тестові випадки
    test_cases = [
        [5, 3, 8, 4, 2],           # базовий
        [1, 2, 3, 4, 5],           # вже відсортований
        [5, 4, 3, 2, 1],           # зворотний порядок
        [1],                        # один елемент
        [3, 3, 3, 3],              # всі однакові
        [9, 1, 5, 3, 7, 2, 8, 4, 6], # більший масив
        [2, 1],                     # два елементи
    ]
    
    results = []
    results.append(test_algorithm("Bubble Sort", bubble_sort_steps, test_cases))
    results.append(test_algorithm("Insertion Sort", insertion_sort_steps, test_cases))
    results.append(test_algorithm("Selection Sort", selection_sort_steps, test_cases))
    
    print(f"\n{'='*50}")
    print("ПІДСУМОК")
    print('='*50)
    
    algorithms = ["Bubble Sort", "Insertion Sort", "Selection Sort"]
    for alg, passed in zip(algorithms, results):
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{alg}: {status}")
    
    if all(results):
        print("\n✓ Всі алгоритми працюють правильно!")
    else:
        print("\n✗ Деякі алгоритми мають помилки!")


if __name__ == '__main__':
    main()

