import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.left_node: Node | None = None
        self.right_node: Node | None = None


class SplayTree:
    def __init__(self):
        self.root: Node | None = None

    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
        else:
            self._insert_node(data, self.root)

    def _insert_node(self, data, current_node):
        if data < current_node.data:
            if current_node.left_node:
                self._insert_node(data, current_node.left_node)
            else:
                current_node.left_node = Node(data, current_node)
        else:
            if current_node.right_node:
                self._insert_node(data, current_node.right_node)
            else:
                current_node.right_node = Node(data, current_node)

    def find(self, data):
        node = self.root
        while node is not None:
            if data < node.data:
                node = node.left_node
            elif data > node.data:
                node = node.right_node
            else:
                self._splay(node)
                return node.data
        return None

    def _splay(self, node):
        while node.parent is not None:
            if node.parent.parent is None:
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif (
                node == node.parent.left_node
                and node.parent == node.parent.parent.left_node
            ):
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif (
                node == node.parent.right_node
                and node.parent == node.parent.parent.right_node
            ):
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else:
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_right(self, node):
        left_child = node.left_node
        if left_child is None:
            return
        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left_node:
            node.parent.left_node = left_child
        else:
            node.parent.right_node = left_child
        left_child.right_node = node
        node.parent = left_child

    def _rotate_left(self, node):
        right_child = node.right_node
        if right_child is None:
            return
        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child
        right_child.left_node = node
        node.parent = right_child

    def visualize(self):
        """Візуалізує дерево за допомогою бібліотеки networkx у вигляді дерева."""
        if self.root is None:
            print("Дерево порожнє.")
            return

        # Побудова графу
        graph = nx.DiGraph()
        self._add_edges(self.root, graph)

        # Отримання позицій вузлів для дерева
        pos = self._hierarchical_layout(self.root)

        # Малювання графу
        nx.draw(graph, pos, with_labels=True, node_size=3000, font_size=12)
        plt.title("Splay Tree Visualization")
        plt.show()

    def _add_edges(self, node, graph):
        """Рекурсивно додає вузли та ребра до графу."""
        if node.left_node:
            graph.add_edge(node.data, node.left_node.data)
            self._add_edges(node.left_node, graph)
        if node.right_node:
            graph.add_edge(node.data, node.right_node.data)
            self._add_edges(node.right_node, graph)

    def _hierarchical_layout(
        self, root, x=0, y=0, level_gap=1.5, sibling_gap=1.5, pos=None
    ):
        """
        Коректно розташовує вузли дерева у вигляді ієрархії.
        """
        if pos is None:
            pos = {}

        # Додаємо поточний вузол
        pos[root.data] = (x, y)

        # Визначаємо позицію для лівого дочірнього вузла
        if root.left_node:
            pos = self._hierarchical_layout(
                root.left_node,
                int(x - sibling_gap),  # Розташування ліворуч
                int(y - level_gap),  # Розташування нижче
                level_gap,
                sibling_gap,
                pos,
            )

        # Визначаємо позицію для правого дочірнього вузла
        if root.right_node:
            pos = self._hierarchical_layout(
                root.right_node,
                int(x + sibling_gap),  # Розташування праворуч
                int(y - level_gap),  # Розташування нижче
                level_gap,
                sibling_gap,
                pos,
            )

        return pos

    def print_tree(self, node=None, level=0):
        """Рекурсивно друкує дерево у вигляді тексту."""
        if node is None:
            node = self.root

        if node and node.right_node:
            self.print_tree(node.right_node, level + 1)

        if node is not None:
            print(" " * 4 * level + "->", node.data)

        if node and node.left_node:
            self.print_tree(node.left_node, level + 1)


if __name__ == "__main__":
    splay_tree = SplayTree()
    splay_tree.insert(10)
    splay_tree.insert(8)
    splay_tree.insert(3)
    splay_tree.insert(7)
    splay_tree.visualize()
    print("Accessing 7:", splay_tree.find(7))
    splay_tree.visualize()
    print("Accessing 3:", splay_tree.find(3))
    splay_tree.visualize()
    print("Accessing 8:", splay_tree.find(8))
    splay_tree.visualize()
    print("Accessing 3:", splay_tree.find(3))
    splay_tree.visualize()

    if splay_tree.root:
        splay_tree.print_tree()
        print("Root after operations:", splay_tree.root.data)
