import bcrypt
import time

password = b"SuperDifficultPassword!@#" # bcrypt працює з байтами

# === РЕЄСТРАЦІЯ ===
print("--- Реєстрація з bcrypt ---")
start_time = time.perf_counter()

# 1. Генеруємо сіль. bcrypt.gensalt() автоматично
#    включає "cost factor" (фактор складності).
#    Чим він вищий, тим повільніше. '12' - хороший дефолт.
salt = bcrypt.gensalt(rounds=10)

# 2. Хешуємо пароль
hashed_password = bcrypt.hashpw(password, salt)
end_time = time.perf_counter()

print(f"Витрачено часу на хешування: {end_time - start_time:.4f} секунд")
print(f"Пароль: {password.decode()}")
print(f"Збережений хеш: {hashed_password.decode()}")
print("\n")

# --- ЛОГІН ---
print("--- Перевірка логіну з bcrypt ---")
login_attempt = b"SuperDifficultPassword!@#"

# bcrypt розумний. Йому не потрібна окрема сіль.
# Він сам витягує сіль і cost factor із повного хешу.
start_time = time.perf_counter()
if bcrypt.checkpw(login_attempt, hashed_password):
    print("Успішний вхід!")
else:
    print("Неправильний пароль.")
end_time = time.perf_counter()
print(f"Витрачено часу на перевірку: {end_time - start_time:.4f} секунд")

# --- Перевірка неправильного пароля ---
print(f"\nПеревірка 'WrongPass': {bcrypt.checkpw(b'WrongPass', hashed_password)}")