import hashlib

text = "MyPassword123"
text_bytes = text.encode('utf-8')

print(f"Текст: {text}\n")

# MD5 - НЕБЕЗПЕЧНИЙ (rainbow tables)
md5_hash = hashlib.md5(text_bytes).hexdigest()
print(f"\nMD5:        {md5_hash}")
print(f"Довжина хешу: {len(md5_hash)} символів (128 біт / 4 = 32 символи)")

# SHA-1 - НЕБЕЗПЕЧНИЙ (зламаний)
sha1_hash = hashlib.sha1(text_bytes).hexdigest()
print(f"\nSHA-1:      {sha1_hash}")
print(f"Довжина хешу: {len(sha1_hash)} символів (160 біт / 4 = 40 символів)")

# SHA-256 - безпечний
sha256_hash = hashlib.sha256(text_bytes).hexdigest()
print(f"\nSHA-256:    {sha256_hash}")
print(f"Довжина хешу: {len(sha256_hash)} символів (256 біт / 4 = 64 символи)")

# SHA-512 - безпечний
sha512_hash = hashlib.sha512(text_bytes).hexdigest()
print(f"\nSHA-512:    {sha512_hash}")
print(f"Довжина хешу: {len(sha512_hash)} символів (512 біт / 4 = 128 символів)")

# BLAKE2b - безпечний, швидкий
blake2b_hash = hashlib.blake2b(text_bytes).hexdigest()
print(f"\nBLAKE2b:    {blake2b_hash}")
print(f"Довжина хешу: {len(blake2b_hash)} символів (512 біт / 4 = 128 символів)")

# SHA3-256 - безпечний, сучасний
sha3_256_hash = hashlib.sha3_256(text_bytes).hexdigest()
print(f"\nSHA3-256:   {sha3_256_hash}")
print(f"Довжина хешу: {len(sha3_256_hash)} символів (256 біт / 4 = 64 символи)")

print(f"\nВсі доступні алгоритми:")
print(sorted(hashlib.algorithms_available))