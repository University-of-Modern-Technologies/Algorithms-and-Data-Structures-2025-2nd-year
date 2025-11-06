# Швидка перевірка унікальності (O(n))
def has_duplicates_set(items):
    # set автоматично прибирає дублікати
    # Якщо довжини не збігаються - є дублікати
    return len(items) != len(set(items))

test_cases = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 1],
    [1, 2, 3],
    [1, 1, 2]
]

for test in test_cases:
    print(f"{test}: {has_duplicates_set(test)}")