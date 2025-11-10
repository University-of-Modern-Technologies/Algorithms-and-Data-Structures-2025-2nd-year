import mmh3


class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def add(self, item: str):
        for i in range(self.num_hashes):
            index = mmh3.hash(item, i) % self.size
            self.bit_array[index] = 1

    def contains(self, item: str):
        for i in range(self.num_hashes):
            index = mmh3.hash(item, i) % self.size
            if self.bit_array[index] == 0:
                return False
        return True

    def visualize(self):
        return "".join(["x" if bit == 1 else "0" for bit in self.bit_array])

if __name__ == "__main__":
    bloom_filter = BloomFilter(1000, 3)
    bloom_filter.add("apple")
    print(bloom_filter.visualize())
    bloom_filter.add("banana")
    print(bloom_filter.visualize())
    bloom_filter.add("orange")
    print(bloom_filter.visualize())

    print(bloom_filter.contains("apple"))
    print(bloom_filter.contains("banana"))
    print(bloom_filter.contains("orange"))
    print(bloom_filter.contains("grape"))
    print(bloom_filter.contains("kiwi"))

