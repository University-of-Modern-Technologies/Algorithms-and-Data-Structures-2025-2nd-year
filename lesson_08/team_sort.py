def insertion_sort(arr, left, right):
    """Insertion sort для малих підмасивів"""
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def merge(arr, left, mid, right):
    """Злиття двох відсортованих підмасивів"""
    left_part = arr[left:mid + 1]
    right_part = arr[mid + 1:right + 1]
    
    i = j = 0
    k = left
    
    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
            arr[k] = left_part[i]
            i += 1
        else:
            arr[k] = right_part[j]
            j += 1
        k += 1
    
    while i < len(left_part):
        arr[k] = left_part[i]
        i += 1
        k += 1
    
    while j < len(right_part):
        arr[k] = right_part[j]
        j += 1
        k += 1


def tim_sort(arr):
    """
    TimSort - гібридний алгоритм сортування
    Поєднує Insertion Sort для малих блоків та Merge Sort для злиття
    Використовується в Python's sorted() та list.sort()
    
    Складність: O(n log n) в середньому та гірших випадках
    O(n) в кращому випадку (для майже відсортованих даних)
    """
    n = len(arr)
    MIN_RUN = 32  # Мінімальний розмір блоку для insertion sort
    
    # Сортуємо окремі блоки розміром MIN_RUN
    for start in range(0, n, MIN_RUN):
        end = min(start + MIN_RUN - 1, n - 1)
        insertion_sort(arr, start, end)
    
    # Злиття відсортованих блоків
    size = MIN_RUN
    while size < n:
        for start in range(0, n, size * 2):
            mid = start + size - 1
            end = min(start + size * 2 - 1, n - 1)
            
            if mid < end:
                merge(arr, start, mid, end)
        
        size *= 2
    
    return arr


def tim_sort_with_runs(arr):
    """
    TimSort з автоматичним визначенням природних runs
    (послідовностей що вже відсортовані)
    """
    n = len(arr)
    MIN_RUN = 32
    
    def find_run(start):
        """Знаходить природний run (зростаючий або спадний)"""
        if start >= n - 1:
            return start
        
        end = start + 1
        
        # Перевіряємо, зростаючий чи спадний run
        if arr[end] < arr[start]:
            # Спадний run
            while end < n and arr[end] < arr[end - 1]:
                end += 1
            # Реверсуємо спадний run
            arr[start:end] = reversed(arr[start:end])
        else:
            # Зростаючий run
            while end < n and arr[end] >= arr[end - 1]:
                end += 1
        
        return end - 1
    
    runs = []
    i = 0
    
    # Знаходимо всі runs
    while i < n:
        run_end = find_run(i)
        
        # Якщо run занадто малий, розширюємо його
        if run_end - i + 1 < MIN_RUN:
            run_end = min(i + MIN_RUN - 1, n - 1)
            insertion_sort(arr, i, run_end)
        
        runs.append((i, run_end))
        i = run_end + 1
    
    # Злиття runs
    while len(runs) > 1:
        new_runs = []
        for i in range(0, len(runs), 2):
            if i + 1 < len(runs):
                left_start, left_end = runs[i]
                right_start, right_end = runs[i + 1]
                merge(arr, left_start, left_end, right_end)
                new_runs.append((left_start, right_end))
            else:
                new_runs.append(runs[i])
        runs = new_runs
    
    return arr


if __name__ == '__main__':
    # Тестування базового TimSort
    test_arr = [5, 2, 9, 1, 7, 6, 3, 8, 4]
    print(f"Original: {test_arr}")
    tim_sort(test_arr.copy())
    print(f"Sorted (basic TimSort): {test_arr}")
    
    # Тестування з великим масивом
    import random
    large_arr = [random.randint(1, 1000) for _ in range(100)]
    print(f"\nLarge array (first 10): {large_arr[:10]}")
    tim_sort(large_arr)
    print(f"Sorted (first 10): {large_arr[:10]}")
    print(f"Is sorted: {large_arr == sorted(large_arr)}")
    
    # Тестування з природними runs
    partly_sorted = [1, 2, 3, 4, 9, 8, 7, 5, 10, 11, 12]
    print(f"\nPartly sorted: {partly_sorted}")
    tim_sort_with_runs(partly_sorted)
    print(f"Sorted (with runs): {partly_sorted}")
    
    # Порівняння швидкості
    import time
    
    test_sizes = [100, 1000, 5000]
    print("\n--- Performance comparison ---")
    
    for size in test_sizes:
        arr = [random.randint(1, 10000) for _ in range(size)]
        
        # TimSort
        arr_copy = arr.copy()
        start = time.perf_counter()
        tim_sort(arr_copy)
        tim_time = time.perf_counter() - start
        
        # Python's built-in sort (also TimSort)
        arr_copy = arr.copy()
        start = time.perf_counter()
        arr_copy.sort()
        builtin_time = time.perf_counter() - start
        
        print(f"Size {size}:")
        print(f"  Custom TimSort: {tim_time*1000:.3f}ms")
        print(f"  Built-in sort:  {builtin_time*1000:.3f}ms")
