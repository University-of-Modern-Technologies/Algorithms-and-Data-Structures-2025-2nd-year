import matplotlib.pyplot as plt
import networkx as nx

# Матриця суміжності (список списків) — рядок відповідає вершині,
# а значення в кожному стовпці показує, чи існує ребро до іншої вершини (1 або 0).
adj_matrix = [
    [0, 1, 0, 1],  # Вершина A
    [1, 0, 1, 0],  # Вершина B
    [0, 1, 0, 1],  # Вершина C
    [1, 0, 1, 0],  # Вершина D
]

# Список суміжності описує граф як словник: ключ — вершина, значення — всі суміжні вершини.
adj_list = {
    "A": ["B", "D"],
    "B": ["A", "C"],
    "C": ["B", "D"],
    "D": ["A", "C"],
}

# Список ребер — окреме представлення графа у вигляді пар вершин (u, v), що утворюють ребро.
edge_list = [
    ("A", "B"),
    ("A", "D"),
    ("B", "C"),
    ("C", "D"),
]


print("Матриця суміжності:")
print(adj_matrix)

print("\nСписок суміжності:")
print(adj_list)

print("\nСписок ребер (пари вершин):")
print(edge_list)

# Побудова графа
graph = nx.Graph()
graph.add_edges_from(edge_list)

pos = nx.spring_layout(graph, seed=42)
nx.draw(
    graph,
    pos,
    with_labels=True,
    node_size=1500,
    node_color="#9bd4ff",
    font_size=14,
    font_weight="bold",
    edge_color="#555555",
)
plt.title("Візуалізація графа")
plt.show()
