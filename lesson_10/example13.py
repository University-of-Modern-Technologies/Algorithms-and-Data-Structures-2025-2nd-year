import hashlib

def get_file_hash(filename):
    hash = hashlib.md5()
    
    try:
        with open(filename, "rb") as f: # 'rb' - читати як байти
            # Читаємо файл шматками по 4КБ, щоб не завантажувати файли в пам'ять
            while chunk := f.read(4096):
                hash.update(chunk)
        return hash.hexdigest()
    except FileNotFoundError:
        return f"Файл '{filename}' не знайдено."

# --- Створимо тестові файли ---
with open("file1.txt", "w") as f:
    f.write("Це вміст файлу.")

with open("file2.txt", "w") as f:
    f.write("Це вміст файлу.") # Точна копія

with open("file3.txt", "w") as f:
    f.write("Це вміст файлу...") # Змінений (додали крапки)

# --- Обчислимо хеші ---
hash1 = get_file_hash("file1.txt")
hash2 = get_file_hash("file2.txt")
hash3 = get_file_hash("file3.txt")

print(f"Хеш file1.txt: {hash1}")
print(f"Хеш file2.txt: {hash2}")
print(f"Хеш file3.txt: {hash3}")

# Перевірка
print(f"\nfile1 == file2 ? {hash1 == hash2}")
print(f"file1 == file3 ? {hash1 == hash3}")

# Очистимо файли 
import os
os.remove("file1.txt")
os.remove("file2.txt")
os.remove("file3.txt")