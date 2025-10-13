from functools import lru_cache


@lru_cache(maxsize=3)
def sum(a, b):
    print(f"sum({a}, {b})")
    return a + b


print(sum(1, 2))
print(sum(1, 2))
print(sum(3, 4))
print(sum(3, 4))
print(sum(5, 6))
print(sum(1, 2))
print(sum(1, 1))
print(sum(1, 2))
