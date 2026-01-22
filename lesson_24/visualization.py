import matplotlib.pyplot as plt
import networkx as nx
import importlib.util
import sys


def visualize_graph(graph, coloring):
    """Візуалізує граф з розфарбуванням вершин"""
    G = nx.Graph()

    # Додаємо вершини та ребра
    for vertex, neighbors in graph.items():
        G.add_node(vertex)
        for neighbor in neighbors:
            if not G.has_edge(vertex, neighbor):
                G.add_edge(vertex, neighbor)

    # Кольори для вершин - яскраві контрастні кольори
    color_map = ["#FF0000", "#0000FF", "#00FF00", "#FFFF00", "#FF00FF", "#FF8800"]
    node_colors = [color_map[coloring[node] % len(color_map)] for node in G.nodes()]

    # Позиціонування вершин
    pos = nx.spring_layout(G, seed=42)

    # Створення візуалізації
    plt.figure(figsize=(10, 8))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2000,
        font_size=16,
        font_weight="bold",
        edge_color="gray",
        width=2,
        alpha=0.7,
    )

    # Додаємо легенду з кольорами
    legend_elements = []
    unique_colors = set(coloring.values())
    for color_idx in sorted(unique_colors):
        legend_elements.append(
            plt.Rectangle(
                (0, 0),
                1,
                1,
                facecolor=color_map[color_idx % len(color_map)],
                label=f"Колір {color_idx}",
            )
        )

    plt.legend(handles=legend_elements, loc="upper left", fontsize=12)
    plt.title("Розфарбування графа", fontsize=16, fontweight="bold", pad=20)
    plt.show()


if __name__ == "__main__":
    # Імпорт функції з файлу, що починається з цифри
    spec = importlib.util.spec_from_file_location(
        "graph_coloring", "01_graph_coloring.py"
    )
    graph_coloring = importlib.util.module_from_spec(spec)
    sys.modules["graph_coloring"] = graph_coloring
    spec.loader.exec_module(graph_coloring)
    color_graph = graph_coloring.color_graph
    # Приклад графа
    graph = {
        "A": ["B", "C"],
        "B": ["A", "C", "D"],
        "C": ["A", "B", "D"],
        "D": ["B", "C"],
    }

    # Кількість кольорів
    num_colors = 3

    # Виклик функції для розфарбування
    solution = color_graph(graph, num_colors)
    if solution:
        print("Знайдене розфарбування графа:", solution)
        visualize_graph(graph, solution)
    else:
        print("Розфарбування графа неможливе з даною кількістю кольорів.")
