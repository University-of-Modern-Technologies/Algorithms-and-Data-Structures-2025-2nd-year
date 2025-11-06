from argon2 import PasswordHasher
import time

# Це вже текстовий пароль
password = "MySecurePassword123"

# === РЕЄСТРАЦІЯ ===
print("--- Реєстрація з Argon2 ---")
start_time = time.perf_counter()

# 1. Створюємо "хешер" з налаштуваннями за замовчуванням
#    (Вони вже включають хороші параметри time_cost, memory_cost, parallelism)
ph = PasswordHasher()

# 2. Хешуємо пароль. Він сам генерує сіль.
hashed_password = ph.hash(password)
end_time = time.perf_counter()

print(f"Витрачено часу на хешування: {end_time - start_time:.4f} секунд")
print(f"Пароль: {password}")
print(f"Збережений хеш: {hashed_password}")
print("\n")


# === ЛОГІН ===
print("--- Перевірка логіну з Argon2 ---")
login_attempt = "MySecurePassword123"

# 1. Перевірка
start_time = time.perf_counter()
try:
    # 2. ph.verify() перевіряє хеш
    #    Він також витягує всі параметри (сіль, пам'ять, час) із самого хешу.
    if ph.verify(hashed_password, login_attempt):
        print("Успішний вхід!")

except Exception as e:
    # Викликає виняток, якщо хеш невірний
    print(f"Неправильний пароль (помилка верифікації: {e})")

end_time = time.perf_counter()
print(f"Витрачено часу на перевірку: {end_time - start_time:.4f} секунд")

# --- Перевірка неправильного пароля ---
print("\nПеревірка 'WrongPass':")
try:
    ph.verify(hashed_password, "WrongPass")
except Exception as e:
    print(f"Провал верифікації (це очікувано): {e}")