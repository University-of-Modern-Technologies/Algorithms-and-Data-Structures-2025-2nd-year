# Знайдемо два рядки, які дають колізію
table_size = 10
keys = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Heidi', 'Ivan', 'Judy']

print(f"Розподіл ключів по таблиці (розмір {table_size}):")
indexes = {}
for key in keys:
    index = hash(key) % table_size
    
    # Додаємо в словник, щоб згрупувати ключі за індексами
    if index not in indexes:
        indexes[index] = []
    indexes[index].append(key)

print("\nРозподіл ключів:")
print("-" * 50)
for index in sorted(indexes.keys()):
    keys_at_index = indexes[index]
    collision_info = f" (колізія: {len(keys_at_index)} ключів)" if len(keys_at_index) > 1 else ""
    print(f"Індекс {index:2d}: {keys_at_index}{collision_info}")
print("-" * 50)
