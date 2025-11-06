import hashlib

text1 = "Hello, world" 
text2 = "Hello, world!"

hash1 = hashlib.sha256(text1.encode('utf-8')).hexdigest()
hash2 = hashlib.sha256(text2.encode('utf-8')).hexdigest()

# Виводимо хеші - лавинний ефект
print(f"'{text1}' -> {hash1}")
print(f"'{text2}' -> {hash2}")