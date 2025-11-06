# Наші дані
phone_book = [
    ('Alice', '555-1234'),
    ('Bob', '555-5678'),
    ('Charlie', '555-9876'),
    ('David', '555-4321'),
    # ... тут мільйон записів
]

def find_in_list(book, name_to_find): # O(n)
    for name, number in book:
        if name == name_to_find:
            return number
    return -1


print(f"Знайдено: {find_in_list(phone_book, 'Charlie')}\n")
print(f"Знайдено: {find_in_list(phone_book, 'Zoe')}") 