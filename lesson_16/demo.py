from insert import Trie
from utils.trie_visualizer import visualize_trie


def main():
    """Демонстрація візуалізації префіксного дерева"""

    # Створення та заповнення дерева з розширеним прикладом
    trie = Trie()

    # Оригінальні слова з insert.py
    trie.put("cat", 2)
    trie.put("dog", 3)
    trie.put("cats", 4)

    # Додаткові слова для кращої візуалізації структури
    trie.put("car", 5)
    trie.put("cart", 6)
    trie.put("do", 7)
    trie.put("door", 8)
    trie.put("apple", 9)
    trie.put("app", 10)

    print("Префіксне дерево створено зі словами:")
    print("- 'cat' -> 2")
    print("- 'cats' -> 4")
    print("- 'car' -> 5")
    print("- 'cart' -> 6")
    print("- 'dog' -> 3")
    print("- 'do' -> 7")
    print("- 'door' -> 8")
    print("- 'apple' -> 9")
    print("- 'app' -> 10")
    print(f"\nЗагальна кількість унікальних слів: {trie.size}")
    print("\nЗапускаю візуалізацію...")

    # Показ візуалізації у вікні
    visualize_trie(trie, figsize=(14, 10))

    # Опціонально: збереження у файл
    # visualize_trie(trie, save_path="trie_visualization.png", show=False)
    # print("Візуалізацію збережено у файл 'trie_visualization.png'")


if __name__ == "__main__":
    main()
