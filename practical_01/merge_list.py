def merge_lists(list1, list2):
    i, j = 0, 0
    result_list = []
    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            result_list.append(list1[i])
            i += 1
        else:
            result_list.append(list2[j])
            j += 1

    result_list.extend(list1[i:])
    result_list.extend(list2[j:])
    return result_list

def merge_k_lists(lists: list[list[int]]):
    if not lists:
        return []

    result_list  = lists[0]
    for i in range(1, len(lists)):
        result_list = merge_lists(result_list, lists[i])
    return result_list


if __name__ == "__main__":
    # Приклад виклику функції
    lists: list[list[int]] = [[1, 4, 5], [1, 3, 4], [2, 6]]
    merged_list = merge_k_lists(lists)
    print("Відсортований список:", merged_list)
