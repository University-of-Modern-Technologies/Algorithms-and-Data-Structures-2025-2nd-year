"""
[1, [2, 3], 4, [5, 6, [7, 8, [9]]]] -> [1, 2, 3, 4, 5, 6, 7, 8, 9]
"""

def flatten(arr: list) -> list:
    result = []
    for i in arr:
        if isinstance(i, list):
            result += flatten(i)
        else:
            result.append(i)
    return result


test = [1, [2, 3], 4, [5, 6, [7, 8, [9]]]]
print(flatten(test))