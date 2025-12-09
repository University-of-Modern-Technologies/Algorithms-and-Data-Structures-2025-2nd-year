from trie import Trie
from utils.trie_visualizer import visualize_trie
import re


class TagSystem(Trie):
    def __init__(self):

        super().__init__()
        self.separator = "/"

    def add_tag(self, tag_path, description=None):
        """
        Додає ієрархічний тег до системи
        tag_path: "технологія/програмування/python"
        description: опис тега
        """
        if not isinstance(tag_path, str) or not tag_path:
            raise TypeError("tag_path must be a non-empty string")

        # Нормалізуємо шлях (прибираємо подвійні слеші)
        normalized_path = self.separator.join(
            [part.strip() for part in tag_path.split(self.separator) if part.strip()]
        )

        tag_info = {
            "path": normalized_path,
            "description": description or f"Тег: {normalized_path}",
            "level": len(normalized_path.split(self.separator)),
            "children_count": 0,
        }

        self.put(normalized_path, tag_info)
        print(f"✅ Додано тег: '{normalized_path}'")

        # Оновлюємо лічильник дочірніх елементів для батьківських тегів
        self._update_parent_children_count(normalized_path)

    def _update_parent_children_count(self, tag_path):
        """Оновлює кількість дочірніх елементів для батьківських тегів"""
        parts = tag_path.split(self.separator)
        for i in range(len(parts) - 1):
            parent_path = self.separator.join(parts[: i + 1])
            parent_info = self.get(parent_path)
            if parent_info:
                parent_info["children_count"] += 1

    def get_all_child_tags(self, parent_path):
        """
        Повертає всі дочірні теги для вказаного батьківського тега
        """
        if not parent_path:
            # Якщо батьківський шлях порожній, повертаємо всі теги
            return self.keys()

        return self.keys_with_prefix(parent_path)

    def suggest_tags(self, partial_path):
        """
        Автодоповнення тегів на основі часткового шляху
        """
        suggestions = self.keys_with_prefix(partial_path)

        # Якщо немає точних збігів, пробуємо знайти теги що містять частковий шлях
        if not suggestions:
            all_tags = self.keys()
            suggestions = [tag for tag in all_tags if partial_path in tag]

        return suggestions[:10]  # Обмежуємо кількість пропозицій

    def get_tag_hierarchy(self, tag_path):
        """
        Повертає повну ієрархію тега від кореня
        """
        parts = tag_path.split(self.separator)
        hierarchy = []

        for i in range(1, len(parts) + 1):
            current_path = self.separator.join(parts[:i])
            tag_info = self.get(current_path)
            if tag_info:
                hierarchy.append(
                    {
                        "path": current_path,
                        "description": tag_info["description"],
                        "level": tag_info["level"],
                    }
                )

        return hierarchy

    def search_by_keyword(self, keyword):
        """
        Пошук тегів за ключовим словом в описі
        """
        results = []
        all_tags = self.keys()

        for tag_path in all_tags:
            tag_info = self.get(tag_path)
            if tag_info and keyword.lower() in tag_info["description"].lower():
                results.append(
                    {
                        "path": tag_path,
                        "description": tag_info["description"],
                        "level": tag_info["level"],
                    }
                )

        return results

    def get_tags_by_level(self, level):
        """
        Повертає всі теги певного рівня ієрархії
        """
        results = []
        all_tags = self.keys()

        for tag_path in all_tags:
            tag_info = self.get(tag_path)
            if tag_info and tag_info["level"] == level:
                results.append(
                    {"path": tag_path, "description": tag_info["description"]}
                )

        return results

    def print_tree_structure(self, root_path=""):
        """
        Друкує структуру тегів у вигляді дерева
        """
        if not root_path:
            # Показуємо теги першого рівня
            level_1_tags = self.get_tags_by_level(1)
            for tag in sorted(level_1_tags, key=lambda x: x["path"]):
                self._print_subtree(tag["path"], "")
        else:
            self._print_subtree(root_path, "")

    def _print_subtree(self, tag_path, indent=""):
        """Рекурсивний друк піддерева"""
        tag_info = self.get(tag_path)
        if not tag_info:
            return

        # Визначаємо чи це листок
        is_leaf = tag_info["children_count"] == 0
        prefix = "📁" if not is_leaf else "📄"

        print(f"{indent}{prefix} {tag_path.split('/')[-1]}")
        if tag_info["description"]:
            print(f"{indent}   └─ {tag_info['description']}")

        # Рекурсивно друкуємо дочірні елементи
        children = self.get_all_child_tags(tag_path)
        # Видаляємо сам батьківський елемент зі списку
        children = [
            child
            for child in children
            if child != tag_path and child.startswith(tag_path + self.separator)
        ]

        # Сортуємо і групуємо за першим рівнем вкладеності
        for child in sorted(children):
            if child.count(self.separator) == tag_path.count(self.separator) + 1:
                self._print_subtree(child, indent + "   ")


if __name__ == "__main__":
    print("🏷️  Система ієрархічних тегів\n")

    tag_system = TagSystem()

    # Додаємо теги
    tags_to_add = [
        ("технологія/програмування/python", "Мова програмування Python"),
        ("технологія/програмування/javascript", "Мова програмування JavaScript"),
        ("технологія/програмування/java", "Мова програмування Java"),
        ("технологія/веб/розробка", "Веб розробка"),
        ("технологія/веб/дизайн", "Веб дизайн"),
        ("технологія/бази/даних/sql", "SQL бази даних"),
        ("технологія/бази/даних/nosql", "NoSQL бази даних"),
        ("наука/математика/алгебра", "Алгебра та лінійна алгебра"),
        ("наука/математика/геометрія", "Геометрія"),
        ("наука/фізика/квантова", "Квантова фізика"),
        ("наука/фізика/класична", "Класична фізика"),
        ("мистецтво/музика/класична", "Класична музика"),
        ("мистецтво/музика/сучасна", "Сучасна музика"),
        ("мистецтво/живопис", "Живопис та малярство"),
    ]

    for tag_path, description in tags_to_add:
        tag_system.add_tag(tag_path, description)

    print(f"\n📊 Всього тегів у системі: {tag_system.size}")

    # Приклад 1: Автодоповнення
    print("\n🔍 Автодоповнення для 'технологія/п':")
    suggestions = tag_system.suggest_tags("технологія/п")
    for suggestion in suggestions:
        print(f"  • {suggestion}")

    # Приклад 2: Дочірні теги
    print("\n🌳 Дочірні теги для 'технологія':")
    children = tag_system.get_all_child_tags("технологія")
    for child in sorted(children):
        info = tag_system.get(child)
        if info:
            print(f"  • {child} ({info['description']})")

    # Приклад 3: Ієрархія тега
    print("\n📋 Ієрархія тега 'технологія/програмування/python':")
    hierarchy = tag_system.get_tag_hierarchy("технологія/програмування/python")
    for level, item in enumerate(hierarchy, 1):
        print(f"  Рівень {level}: {item['path']} - {item['description']}")

    # Приклад 4: Пошук за ключовим словом
    print("\n🔎 Пошук тегів за словом 'програмування':")
    results = tag_system.search_by_keyword("програмування")
    for result in results:
        print(f"  • {result['path']} - {result['description']}")

    # Приклад 5: Теги за рівнем
    print("\n📊 Теги 2-го рівня ієрархії:")
    level_2_tags = tag_system.get_tags_by_level(2)
    for tag in sorted(level_2_tags, key=lambda x: x["path"]):
        print(f"  • {tag['path']} - {tag['description']}")

    # Приклад 6: Візуалізація структури
    print("\n🌳 Повна структура тегів:")
    tag_system.print_tree_structure()

    # Візуалізація trie
    print("\n🎨 Візуалізація структури trie:")
    # visualize_trie(tag_system)
