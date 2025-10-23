def bubble_sort(lst): # для вісортованих O(n)
    _lst = lst.copy()
    n = len(_lst)
    for i in range(n - 1):
        flag = False
        for j in range(0, n - i - 1):
            if _lst[j] > _lst[j + 1]:
                _lst[j], _lst[j + 1] = _lst[j + 1], _lst[j]
                flag = True
        if not flag:
            break
    return _lst


if __name__ == '__main__':
    # numbers = [1, 2, 3, 4, 5]
    numbers = [5, 3, 8, 4, 2]
    r = bubble_sort(numbers)
    print(numbers, r)