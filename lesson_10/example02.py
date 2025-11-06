phone_book = {
    'Alice': '555-1234',
    'Bob': '555-5678',
    'Charlie': '555-9876',
    'David': '555-4321',
}

def find_in_dict(book, name_to_find): # O(1)
    return book.get(name_to_find, -1)

# Демонстрація миттєвого пошуку
print(f"Знайдено: {find_in_dict(phone_book, 'Charlie')}\n")
print(f"Знайдено: {find_in_dict(phone_book, 'Zoe')}")