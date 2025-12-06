class AVLNode:
    """Вузол AVL дерева"""

    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

    def __str__(self, level=0, prefix="Root: "):
        """Візуалізація вузла та його нащадків"""
        ret = (
            "\t" * level
            + prefix
            + str(self.key)
            + " Height: "
            + str(self.height)
            + "\n"
        )
        if self.left:
            ret += self.left.__str__(level + 1, "L--- ")
        if self.right:
            ret += self.right.__str__(level + 1, "R--- ")
        return ret


class AVLTree:
    """Клас AVL дерева з інкапсуляцією всіх операцій"""

    def __init__(self, duplicate_strategy="ignore"):
        """
        Ініціалізація AVL дерева

        Args:
            duplicate_strategy: стратегія обробки дублікатів
                'ignore' - ігнорувати дублікати (за замовчуванням)
                'update' - оновити існуючий вузол
                'count' - зберігати лічильник дублікатів
        """
        self.root = None
        self.duplicate_strategy = duplicate_strategy
        self._size = 0

    @staticmethod
    def _get_height(node):
        """Отримати висоту вузла"""
        if not node:
            return 0
        return node.height

    @staticmethod
    def _get_balance(node):
        """Отримати баланс factor вузла"""
        if not node:
            return 0
        return AVLTree._get_height(node.left) - AVLTree._get_height(node.right)

    @staticmethod
    def _left_rotate(z):
        """Лівий поворот"""
        y = z.right
        T2 = y.left

        # Виконуємо поворот
        y.left = z
        z.right = T2

        # Оновлюємо висоти
        z.height = 1 + max(AVLTree._get_height(z.left), AVLTree._get_height(z.right))
        y.height = 1 + max(AVLTree._get_height(y.left), AVLTree._get_height(y.right))

        return y

    @staticmethod
    def _right_rotate(y):
        """Правий поворот"""
        x = y.left
        T3 = x.right

        # Виконуємо поворот
        x.right = y
        y.left = T3

        # Оновлюємо висоти
        y.height = 1 + max(AVLTree._get_height(y.left), AVLTree._get_height(y.right))
        x.height = 1 + max(AVLTree._get_height(x.left), AVLTree._get_height(x.right))

        return x

    def _min_value_node(self, node):
        """Знайти вузол з мінімальним значенням в піддереві"""
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _max_value_node(self, node):
        """Знайти вузол з максимальним значенням в піддереві"""
        current = node
        while current.right is not None:
            current = current.right
        return current

    def _insert_recursive(self, root, key):
        """Рекурсивна вставка з обробкою дублікатів"""
        if not root:
            self._size += 1
            return AVLNode(key)

        if key < root.key:
            root.left = self._insert_recursive(root.left, key)
        elif key > root.key:
            root.right = self._insert_recursive(root.right, key)
        else:  # Дублікат
            return self._handle_duplicate(root)

        # Оновлюємо висоту предка
        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))

        # Отримуємо баланс factor
        balance = self._get_balance(root)

        # Якщо вузol стає небалансованим, виконуємо відповідні ротации

        # Left Left Case
        if balance > 1 and key < root.left.key:
            return self._right_rotate(root)

        # Right Right Case
        if balance < -1 and key > root.right.key:
            return self._left_rotate(root)

        # Left Right Case
        if balance > 1 and key > root.left.key:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)

        # Right Left Case
        if balance < -1 and key < root.right.key:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)

        return root

    def _handle_duplicate(self, root):
        """Обробка дублікатів згідно зі стратегією"""
        if self.duplicate_strategy == "ignore":
            return root  # Ігноруємо дублікат
        elif self.duplicate_strategy == "update":
            return root  # Існуючий вузол залишається (можна додати логіку оновлення)
        elif self.duplicate_strategy == "count":
            # Тут можна реалізувати лічильник, але для простості ігноруємо
            return root
        else:
            return root

    def _delete_recursive(self, root, key):
        """Рекурсивне видалення"""
        if not root:
            return root

        # Стандартне видалення BST
        if key < root.key:
            root.left = self._delete_recursive(root.left, key)
        elif key > root.key:
            root.right = self._delete_recursive(root.right, key)
        else:
            # Вузол з одним нащадком або без нащадків
            if root.left is None:
                temp = root.right
                root = None
                if temp:
                    self._size -= 1
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                if temp:
                    self._size -= 1
                return temp

            # Вузол з двома нащадками: отримуємо successor (мінімум у правому піддереві)
            temp = self._min_value_node(root.right)
            root.key = temp.key
            root.right = self._delete_recursive(root.right, temp.key)
            self._size -= 1

        # Якщо дерево мало лише один вузол
        if not root:
            return root

        # Оновлюємо висоту предка
        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))

        # Отримуємо баланс factor
        balance = self._get_balance(root)

        # Балансуємо дерево

        # Left Left Case
        if balance > 1 and self._get_balance(root.left) >= 0:
            return self._right_rotate(root)

        # Left Right Case
        if balance > 1 and self._get_balance(root.left) < 0:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)

        # Right Right Case
        if balance < -1 and self._get_balance(root.right) <= 0:
            return self._left_rotate(root)

        # Right Left Case
        if balance < -1 and self._get_balance(root.right) > 0:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)

        return root

    def insert(self, key):
        """
        Вставити ключ в дерево

        Args:
            key: ключ для вставки

        Returns:
            bool: True якщо вставлено успішно, False якщо дублікат проігноровано
        """
        if not isinstance(key, (int, float)):
            raise ValueError("Ключ повинен бути числом")

        old_size = self._size
        self.root = self._insert_recursive(self.root, key)
        return self._size > old_size

    def delete(self, key):
        """
        Видалити ключ з дерева

        Args:
            key: ключ для видалення

        Returns:
            bool: True якщо ключ знайдено та видалено, False інакше
        """
        if not isinstance(key, (int, float)):
            raise ValueError("Ключ повинен бути числом")

        old_size = self._size
        self.root = self._delete_recursive(self.root, key)
        return self._size < old_size

    def search(self, key):
        """
        Пошук ключа в дереві

        Args:
            key: ключ для пошуку

        Returns:
            bool: True якщо ключ знайдено, False інакше
        """
        if not isinstance(key, (int, float)):
            raise ValueError("Ключ повинен бути числом")

        current = self.root
        while current:
            if key == current.key:
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return False

    def get_min(self):
        """Отримати мінімальне значення в дереві"""
        if not self.root:
            raise ValueError("Дерево порожнє")
        return self._min_value_node(self.root).key

    def get_max(self):
        """Отримати максимальне значення в дереві"""
        if not self.root:
            raise ValueError("Дерево порожнє")
        return self._max_value_node(self.root).key

    def size(self):
        """Отримати розмір дерева"""
        return self._size

    def is_empty(self):
        """Перевірити чи дерево порожнє"""
        return self.root is None

    def inorder_traversal(self):
        """Симетричний обхід дерева (в порядку зростання)"""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        """Допоміжна функція для симетричного обходу"""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.key)
            self._inorder_recursive(node.right, result)

    def preorder_traversal(self):
        """Прямий обхід дерева"""
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        """Допоміжна функція для прямого обходу"""
        if node:
            result.append(node.key)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def postorder_traversal(self):
        """Зворотний обхід дерева"""
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node, result):
        """Допоміжна функція для зворотного обходу"""
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.key)

    def get_height(self):
        """Отримати висоту дерева"""
        return self._get_height(self.root)

    def is_balanced(self):
        """Перевірити чи дерево збалансоване"""
        return self._is_balanced_recursive(self.root)

    def _is_balanced_recursive(self, node):
        """Рекурсивна перевірка балансу"""
        if not node:
            return True

        balance = self._get_balance(node)
        if abs(balance) > 1:
            return False

        return self._is_balanced_recursive(node.left) and self._is_balanced_recursive(
            node.right
        )

    def __str__(self):
        """Візуалізація дерева"""
        if not self.root:
            return "Empty AVL Tree"
        return str(self.root)

    def __len__(self):
        """Отримати розмір дерева через len()"""
        return self._size


if __name__ == "__main__":
    # Демонстрація покращеної реалізації AVL дерева

    print("=== Тестування AVL дерева ===\n")

    # Створюємо AVL дерево
    avl = AVLTree()

    # Тестування вставки
    print("1. Тестування вставки:")
    keys = [10, 20, 30, 25, 28, 27, -1, 5, 15, 35]
    for key in keys:
        success = avl.insert(key)
        print(
            f"Вставлено {key}: {'Успішно' if success else 'Проігноровано (дублікат)'}"
        )

    print(f"\nAVL Дерево (розмір: {avl.size()}):")
    print(avl)
    print(f"Висота дерева: {avl.get_height()}")
    print(f"Дерево збалансоване: {avl.is_balanced()}")

    # Тестування обходів
    print(f"\n2. Обходи дерева:")
    print(f"In-order (симетричний): {avl.inorder_traversal()}")
    print(f"Pre-order (прямий): {avl.preorder_traversal()}")
    print(f"Post-order (зворотний): {avl.postorder_traversal()}")

    # Тестування пошуку
    print(f"\n3. Тестування пошуку:")
    search_keys = [25, 99, -1, 10]
    for key in search_keys:
        found = avl.search(key)
        print(f"Пошук {key}: {'Знайдено' if found else 'Не знайдено'}")

    # Тестування min/max
    print(f"\n4. Мінімум та максимум:")
    print(f"Мінімальне значення: {avl.get_min()}")
    print(f"Максимальне значення: {avl.get_max()}")

    # Тестування видалення
    print(f"\n5. Тестування видалення:")
    keys_to_delete = [10, 27, 99]  # 99 не існує
    for key in keys_to_delete:
        success = avl.delete(key)
        print(f"Видалено {key}: {'Успішно' if success else 'Не знайдено'}")

    print(f"\nAVL Дерево після видалення (розмір: {avl.size()}):")
    print(avl)
    print(f"Дерево збалансоване: {avl.is_balanced()}")

    # Тестування обробки дублікатів
    print(f"\n6. Тестування обробки дублікатів:")
    avl_duplicates = AVLTree(duplicate_strategy="ignore")
    duplicate_keys = [5, 10, 5, 15, 10, 20, 5]

    for key in duplicate_keys:
        success = avl_duplicates.insert(key)
        print(
            f"Вставлено {key}: {'Успішно' if success else 'Проігноровано (дублікат)'}"
        )

    print(f"\nДерево з дублікатами (розмір: {avl_duplicates.size()}):")
    print(avl_duplicates)
    print(f"In-order traversal: {avl_duplicates.inorder_traversal()}")

    # Тестування валідації
    print(f"\n7. Тестування валідації:")
    try:
        avl.insert("не число")
    except ValueError as e:
        print(f"Помилка валідації: {e}")

    try:
        avl.search("не число")
    except ValueError as e:
        print(f"Помилка валідації: {e}")

    print(f"\n=== Тестування завершено ===")
