class LinearProbingTable:
    """
    Реалізує хеш-таблицю з відкритею адресацією
    (лінійне зондування).
    
    Для простоти, ми будемо зберігати кортежі (key, value).
    Спеціальне значення (None) означає порожню комірку.
    """
    def __init__(self, size=10):
        self.size = size
        # Просто список, заповнений "порожніми" значеннями
        self.table = [None] * self.size

    def _hash(self, key):
        return hash(key) % self.size
        
    def __str__(self):
        output = "--- Linear Probing Table ---\n"
        for index, item in enumerate(self.table):
            output += f"Індекс {index}: {item}\n"
        return output + "-------------------------"

    def put(self, key, value):
        index = self._hash(key)
        original_index = index
        
        # Починаємо з нашого "ідеального" індексу
        for i in range(self.size):
            # Рахуємо індекс зі зсувом
            current_index = (index + i) % self.size 
            
            # Якщо комірка порожня (None) АБО ключ той самий (оновлення)
            if self.table[current_index] is None or \
               self.table[current_index][0] == key:
               
                self.table[current_index] = (key, value)
                if i == 0:
                    print(f"Помістили '{key}' в індекс {current_index} (без колізій)")
                else:
                    print(f"Помістили '{key}' в індекс {current_index} (КОЛІЗІЯ! хеш={original_index}, зсув={i})")
                return
        
        # Якщо ми пройшли весь цикл і не знайшли місця
        raise OverflowError("Хеш-таблиця заповнена!")

    def get(self, key):
        index = self._hash(key)
        
        for i in range(self.size):
            current_index = (index + i) % self.size
            item = self.table[current_index]
            
            # 1. Якщо ми натрапили на порожню комірку, ключа точно немає
            if item is None:
                raise KeyError(f"Ключ '{key}' не знайдено (знайшли None)")
            
            # 2. Якщо ми знайшли наш ключ
            if item[0] == key:
                return item[1]
        
        # 3. Якщо пройшли всю таблицю, а ключ не знайшли
        raise KeyError(f"Ключ '{key}' не знайдено (повний обхід)")


# --- Демонстрація ---
table = LinearProbingTable(size=5) # Малий розмір для колізій!

# Показуємо хеш-індекси
keys = ['Alice', 'Bob', 'Heidi', 'Chris', 'Charlie']
print("Хеш-індекси ключів:")
for key in keys:
    print(f"  {key}: hash() % 5 = {hash(key) % 5}")

print("\nДодаємо елементи:\n")
table.put('Alice', '555-1111') 
table.put('Bob', '555-2222') 
table.put('Heidi', '555-3333')
table.put('Chris', '555-4444')

print(f"\n{table}")

# Пошук
print("Пошук елементів:")
print(f"Шукаємо 'Heidi': {table.get('Heidi')}")
print(f"Шукаємо 'Chris': {table.get('Chris')}")
print(f"Шукаємо 'Alice': {table.get('Alice')}")
print(f"Шукаємо 'Bob': {table.get('Bob')}")
try:
    print(f"Шукаємо 'Charlie': {table.get('Charlie')}") 
except KeyError as e:
    print(e)
