import timeit
from functools import lru_cache


def fibonacci_memo(n, memo=None):
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        memo[n] = n
        return n
    else:
        memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
        return memo[n]


@lru_cache(maxsize=None)
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_pure(n):
    if n <= 1:
        return n
    else:
        return fibonacci_pure(n - 1) + fibonacci_pure(n - 2)


# print(fibonacci_pure(37))
# print(fibonacci(37))
# print(fibonacci_memo(37))

n = 70

# time_pure = timeit.timeit("fibonacci_pure(n)", globals=globals(), number=10)
time_lru = timeit.timeit("fibonacci(n)", globals=globals(), number=10)
time_memo = timeit.timeit("fibonacci_memo(n)", globals=globals(), number=10)


# print(f"pure: {time_pure:.6f}")
print(f"lru: {time_lru:.6f}")
print(f"memo: {time_memo:.6f}")
