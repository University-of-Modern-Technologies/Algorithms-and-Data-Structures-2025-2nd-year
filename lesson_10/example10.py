import hashlib
import os
import time

password = "MySecurePassword123"

# --- РЕЄСТРАЦІЯ КОРИСТУВАЧА (Зберігаємо пароль) ---

# 1. Генеруємо випадкову "сіль"
salt = os.urandom(16) # 16 байт випадкових даних

# 2. Створюємо хеш за допомогою PBKDF2 (Password-Based Key Derivation Function 2 with HMAC)
# 'sha256' - алгоритм
# password.encode() - наш пароль
# salt - наша сіль
# 100000 - кількість ітерацій (робить процес повільним для хакера)
start_time = time.perf_counter()
pass_hash = hashlib.pbkdf2_hmac(
    'sha256', 
    password.encode('utf-8'), 
    salt, 
    100000
)
pbkdf2_time = time.perf_counter() - start_time

print("--- Реєстрація ---")
print(f"Пароль: {password}")
print(f"Сіль (в hex):   {salt.hex()}")
print(f"Хеш (в hex): {pass_hash.hex()}")
print(f"Час PBKDF2 (100,000 ітерацій): {pbkdf2_time:.4f} секунд")

# У базі даних ми зберігаємо salt І pass_hash

# --- ЛОГІН КОРИСТУВАЧА (Перевіряємо пароль) ---
print("\n--- Перевірка логіну ---")
login_attempt = "MySecurePassword123"

# 1. Беремо з бази даних сіль, яку ми зберегли для цього користувача
stored_salt = salt 
stored_hash = pass_hash

# 2. Виконуємо ТУ САМУ операцію з паролем, що намагається увійти
attempt_hash = hashlib.pbkdf2_hmac(
    'sha256',
    login_attempt.encode('utf-8'),
    stored_salt, # Використовуючи ту саму сіль!
    100000
)

# 3. Порівнюємо хеші
if attempt_hash == stored_hash:
    print("Успішний вхід!")
else:
    print("Неправильний пароль!")

# Перевірка з неправильним паролем
wrong_attempt_hash = hashlib.pbkdf2_hmac('sha256', "WrongPassword".encode(), stored_salt, 100000)
print(f"Порівняння з неправильним паролем: {wrong_attempt_hash == stored_hash}")