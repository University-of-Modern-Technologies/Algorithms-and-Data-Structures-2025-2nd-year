from trie import Trie
from utils.trie_visualizer import visualize_trie

trie = Trie()
words = [
    "apple",
    "application",
    "appetizer",
    "banana",
    "band",
    "banner",
    "ball",
    "bat",
    "battery",
]

# Додаємо слова до Trie
for index, word in enumerate(words):
    trie.put(word, index)


# Функція автозаповнення
def autocomplete(trie, prefix):
    return trie.keys_with_prefix(prefix)


# Приклад використання автозаповнення
user_input = "app"
suggestions = autocomplete(trie, user_input)
print(f"Пропозиції для '{user_input}': {suggestions[:2]}")
visualize_trie(trie)
