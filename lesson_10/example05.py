from collections import defaultdict

class SimpleHashTable:
    """
    Реалізує хеш-таблицю з методом ланцюжків.
    """
    def __init__(self, size=10):
        self.size = size
        self.table = defaultdict(list)

    def _hash(self, key):  # O(1)
        """Приватний метод для обчислення індексу."""
        return hash(key) % self.size

    def __str__(self):  # O(size + n)
        output = "--- Хеш-таблиця ---\n"
        for index in range(self.size):
            bucket = self.table[index]
            output += f"Індекс {index}: {bucket}\n"
        return output + "--------------------"

    def put(self, key, value):  # Average O(1), Worst O(n)
        """Додає або оновлює пару ключ-значення."""
        index = self._hash(key)
        bucket = self.table[index]
        
        # Перевіряємо, чи ключ вже існує (для оновлення)
        for i, (existing_key, existing_value) in enumerate(bucket):
            if existing_key == key:
                # Ключ знайдено, оновлюємо значення і виходимо
                bucket[i] = (key, value)
                print(f"Оновлено: {key}")
                return
                
        # Ключ новий, додаємо в кінець ланцюжка (списку)
        bucket.append((key, value))
        print(f"Додано: {key}")

    def get(self, key):  # Average O(1), Worst O(n)
        """Отримує значення за ключем."""
        index = self._hash(key)
        bucket = self.table[index]
        
        # Шукаємо ключ у ланцюжку (кошику)
        for existing_key, value in bucket:
            if existing_key == key:
                return value
                
        # Якщо цикл завершився, а ключ не знайдено
        raise KeyError(f"Ключ '{key}' не знайдено")

    def delete(self, key):  # Average O(1), Worst O(n)
        """Видаляє ключ з таблиці."""
        index = self._hash(key)
        bucket = self.table[index]
        
        # Шукаємо ключ у ланцюжку
        for existing_key, existing_value in bucket:
            if existing_key == key:
                bucket.remove((existing_key, existing_value))
                print(f"Видалено: {key}")
                return
                
        # Якщо ключ не знайдено
        raise KeyError(f"Ключ '{key}' не знайдено")

# --- Демонстрація нашого класу ---
print("Створюємо нашу SimpleHashTable...\n")
my_book = SimpleHashTable(size=5) # Малий розмір для гарантованих колізій

# Додаємо дані
my_book.put('Alice', '555-1234')
my_book.put('Bob', '555-5678')
my_book.put('Charlie', '555-9876')
my_book.put('Heidi', '555-1111') 
print(my_book)

# Оновлюємо існуючий ключ
my_book.put('Alice', '555-0000')
print(my_book)

# Отримуємо дані
print(f"\nНомер Alice: {my_book.get('Alice')}")

# Видаляємо ключі
my_book.delete('Bob')
print(my_book)

# Перевіряємо, що видалені ключі не знайдені
print("\nСпроба отримати видалені ключі:")
try:
    my_book.get('Bob')
except KeyError as e:
    print(e)