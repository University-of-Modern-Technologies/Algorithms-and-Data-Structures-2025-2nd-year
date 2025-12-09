import matplotlib.pyplot as plt
import networkx as nx
from typing import Optional, Dict, Tuple


def _hierarchical_layout(G: nx.DiGraph) -> Dict:
    """
    Створює ієрархічне розташування вузлів для графа.

    Args:
        G: Направлений граф

    Returns:
        Словник з позиціями вузлів {node_id: (x, y)}
    """
    pos = {}
    levels = {}  # {level: [nodes]}

    # Знаходимо корінь (вузол без вхідних ребер)
    root = None
    for node in G.nodes():
        if G.in_degree(node) == 0:
            root = node
            break

    if root is None:
        # Якщо корінь не знайдено, використовуємо spring_layout
        return nx.spring_layout(G, k=3, iterations=50, seed=42)

    # Рекурсивна функція для визначення рівнів вузлів
    def assign_levels(node, level=0):
        if level not in levels:
            levels[level] = []
        levels[level].append(node)

        # Рекурсивно обходимо дочірні вузли
        for child in G.successors(node):
            assign_levels(child, level + 1)

    # Призначаємо рівні для всіх вузлів
    assign_levels(root)

    # Розташовуємо вузли по рівнях
    level_height = 2.0  # Відстань між рівнями
    base_y = len(levels) * level_height

    for level, nodes in levels.items():
        y = base_y - level * level_height
        level_width = max(len(nodes), 1) * 1.5
        start_x = -level_width / 2

        for i, node in enumerate(sorted(nodes)):
            x = (
                start_x + (i * level_width / max(len(nodes) - 1, 1))
                if len(nodes) > 1
                else 0
            )
            pos[node] = (x, y)

    return pos


def visualize_trie(
    trie, save_path: Optional[str] = None, show: bool = True, figsize: tuple = (12, 8)
):
    """
    Візуалізує префіксне дерево (Trie) за допомогою networkx та matplotlib.

    Args:
        trie: Об'єкт Trie для візуалізації
        save_path: Шлях для збереження зображення (опціонально)
        show: Чи показувати вікно з візуалізацією
        figsize: Розмір фігури (ширина, висота)
    """
    # Створення направленого графу
    G = nx.DiGraph()

    # Рекурсивна функція для обходу дерева
    def add_nodes_and_edges(node, node_id, path=""):
        # Додавання вузла з міткою
        if node_id == 0:  # Корінь
            label = "root"
        else:
            label = path[-1] if path else ""
            if node.value is not None:
                label += f"\n({node.value})"

        # Визначення кольору вузла
        if node_id == 0:
            color = "lightblue"
        elif node.value is not None:
            color = "lightgreen"
        else:
            color = "lightgray"

        G.add_node(node_id, label=label, color=color)

        # Рекурсивне додавання дочірніх вузлів
        child_id = node_id + 1
        for char, child_node in node.children.items():
            child_node_id = (
                node_id * 100 + len(list(node.children.keys())) * 10 + ord(char)
            )
            G.add_edge(node_id, child_node_id, label=char)
            add_nodes_and_edges(child_node, child_node_id, path + char)

    # Побудова графа з кореня
    add_nodes_and_edges(trie.root, 0)

    # Налаштування візуалізації
    plt.figure(figsize=figsize)

    # Ієрархічне розташування вузлів
    pos = _hierarchical_layout(G)

    # Отримання кольорів та міток
    node_colors = [G.nodes[node]["color"] for node in G.nodes()]
    node_labels = {node: G.nodes[node]["label"] for node in G.nodes()}
    edge_labels = {(u, v): G.edges[u, v]["label"] for u, v in G.edges()}

    # Малювання графа
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1500, alpha=0.8)
    nx.draw_networkx_labels(
        G, pos, labels=node_labels, font_size=10, font_weight="bold"
    )
    nx.draw_networkx_edges(
        G, pos, edge_color="gray", arrows=True, arrowsize=20, arrowstyle="->", width=2
    )
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, font_color="red", font_size=9
    )

    # Додавання легенди
    from matplotlib.patches import Patch

    legend_elements = [
        Patch(facecolor="lightblue", label="Корінь"),
        Patch(facecolor="lightgreen", label="Кінцевий вузол (зі значенням)"),
        Patch(facecolor="lightgray", label="Проміжний вузол"),
    ]
    plt.legend(handles=legend_elements, loc="upper right")

    plt.title("Візуалізація префіксного дерева (Trie)", fontsize=16, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()

    # Збереження або показ
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Зображення збережено: {save_path}")

    if show:
        plt.show()
    else:
        plt.close()
