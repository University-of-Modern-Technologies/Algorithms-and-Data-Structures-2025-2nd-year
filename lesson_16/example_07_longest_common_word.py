from trie import Trie


class LongestCommonWord(Trie):
    def find_longest_common_word(self, words):
        if not words or not all(isinstance(word, str) for word in words):
            raise TypeError("words must be a non-empty list of strings")

        for i, word in enumerate(words):
            self.put(word, i)

        current = self.root
        common_prefix = []

        while len(current.children) == 1:
            char = max(current.children, key=current.children.get)
            # char, next_node = next(iter(current.children.items()))
            common_prefix.append(char)
            current = current.children[char]  # next_node  #

        return "".join(common_prefix)


if __name__ == "__main__":
    trie = LongestCommonWord()
    words = ["сонце", "сонячний", "сонечко", "соняшник"]
    print(trie.find_longest_common_word(words))
