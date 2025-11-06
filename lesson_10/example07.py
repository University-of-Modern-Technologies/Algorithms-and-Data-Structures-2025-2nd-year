import hashlib

# 1. Створюємо об'єкт хешування
h = hashlib.sha256()

# 2. .update() приймає ТІЛЬКИ байти!
text = "Hello, world!"
h.update(text.encode('utf-8')) 

# 3. Отримуємо результат у вигляді 16-кового рядка
hex_digest = h.hexdigest()

print(f"Рядок: '{text}'")
print(f"SHA-256: {hex_digest}")
print(f"Довжина хешу: {len(hex_digest)} символів (256 біт / 4 = 64 символи)")

# Той самий рядок ЗАВЖДИ дає той самий хеш
h2 = hashlib.sha256()
h2.update("Hello, world!".encode('utf-8'))
print(f"\nПовторний хеш: {h2.hexdigest()}")