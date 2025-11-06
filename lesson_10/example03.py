# Приклад 1: Рядки
key1 = 'Alice'
key2 = 'Bob'
key3 = 'Charlie'

print(f"hash('{key1}') = {hash(key1)}")
print(f"hash('{key2}') = {hash(key2)}")
print(f"hash('{key3}') = {hash(key3)}")

# Приклад 2: Детермінізм
print(f"\nПовторний виклик: hash('Alice') = {hash('Alice')}")
print(f"Повторний виклик: hash('Bob') = {hash('Bob')}")
print(f"Повторний виклик: hash('Charlie') = {hash('Charlie')}")

# Приклад 3: Числа
print(f"\nhash(123) = {hash(123)}")
print(f"hash(256) = {hash(256)}")
print(f"hash(123.45) = {hash(123.45)}")
print(f"hash(256.5) = {hash(256.5)}")

# Приклад 4: Малий масив ("таблиця")
# Ми не можемо мати масив великого розміру 
# Нам потрібен індекс для масиву, скажімо, з 10 слотів.
table_size = 10
index1 = hash(key1) % table_size
index2 = hash(key2) % table_size
index3 = hash(key3) % table_size

print(f"\nДля таблиці розміром {table_size}:")
print(f"'{key1}' -> хеш {hash(key1)} -> індекс {index1}")
print(f"'{key2}' -> хеш {hash(key2)} -> індекс {index2}")
print(f"'{key3}' -> хеш {hash(key3)} -> індекс {index3}")