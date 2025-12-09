from collections import deque
from typing import List, Tuple

from trie import Trie
from utils.trie_visualizer import visualize_trie


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Обчислює редакційну відстань Левенштейна між двома рядками.
    Повна реалізація з урахуванням вставок, видалень та замін.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    # Ініціалізація матриці для динамічного програмування
    previous_row = list(range(len(s2) + 1))

    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def get_corrections(trie: Trie, word: str, max_distance: int = 1) -> List[str]:
    """
    Покращений алгоритм пошуку можливих виправлень для слова з помилкою.
    Використовує правильну редакційну відстань Левенштейна.

    Args:
        trie: Префіксне дерево зі словами
        word: Слово з помилкою для виправлення
        max_distance: Максимальна редакційна відстань

    Returns:
        Список можливих варіантів виправлення
    """
    corrections = []

    # Отримуємо всі слова з дерева
    all_words = trie.keys()

    # Перевіряємо кожне слово
    for candidate in all_words:
        distance = levenshtein_distance(candidate, word)

        # Якщо відстань в межах ліміту і слово не дорівнює цільовому
        if 0 < distance <= max_distance:
            corrections.append(candidate)

    # Сортуємо результати за відстанню (спочатку найближчі)
    def get_distance(w):
        return levenshtein_distance(w, word)

    corrections.sort(key=get_distance)

    return corrections


if __name__ == "__main__":
    # Ініціалізація Trie та вставка слів у словник
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

    # Приклад використання пошуку виправлень
    word_with_typo = "battary"
    corrections = get_corrections(trie, word_with_typo, max_distance=2)
    print(f"Можливі варіанти виправлення для '{word_with_typo}': {corrections}")

    # visualize_trie(trie)
