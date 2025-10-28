import timeit
import random

from merge_sort import merge_sort
from quick_sort import quicksort
from radix_sort import radix_sort


# Створення випадкового масиву
arr = [random.randint(0, 10_000) for _ in range(100_000)]

time_merge = timeit.timeit(lambda: merge_sort(arr[:]), number=10)
time_quick = timeit.timeit(lambda: quicksort(arr[:]), number=10)
time_radix = timeit.timeit(lambda: radix_sort(arr[:]), number=10)
time_sorted = timeit.timeit(lambda: sorted(arr), number=10)
time_sort = timeit.timeit(lambda: arr[:].sort(), number=10)

print(f"Sorted: {time_sorted} seconds")
print(f"Sort: {time_sort} seconds")
print(f"Merge sort: {time_merge} seconds")
print(f"Quick sort: {time_quick} seconds")
print(f"Radix sort: {time_radix} seconds")
