import networkx as nx
import matplotlib.pyplot as plt
from dijkstra import graph

# Створення зваженого графа NetworkX
G = nx.Graph()

# Додавання ребер з вагами
for node, neighbors in graph.items():
    for neighbor, weight in neighbors.items():
        G.add_edge(node, neighbor, weight=weight)

# Задання початкової вершини
start_vertex = "A"

# Обчислення найкоротших шляхів від start_vertex до всіх вершин
shortest_paths = nx.single_source_dijkstra_path(G, start_vertex)
shortest_distances = nx.single_source_dijkstra_path_length(G, start_vertex)

print("Найкоротші шляхи:", shortest_paths)
print("Найкоротші відстані:", shortest_distances)

# Створення візуалізації
plt.figure(figsize=(12, 8))

# Позиціонування вершин
pos = nx.spring_layout(G, seed=42)

# Отримання ваг ребер для відображення
edge_labels = {(u, v): d["weight"] for u, v, d in G.edges(data=True)}

# Малювання всіх ребер
nx.draw_networkx_edges(G, pos, edge_color="gray", width=1.5, alpha=0.5)

# Малювання вершин
nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=1500, alpha=0.9)

# Малювання міток вершин з відстанями
node_labels = {node: f"{node}\n({shortest_distances[node]})" for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10, font_weight="bold")

# Малювання ваг на ребрах
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

# Підсвітка найкоротших шляхів від start_vertex
for target in shortest_paths:
    if target != start_vertex:
        path = shortest_paths[target]
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(
            G, pos, edgelist=path_edges, edge_color="red", width=2.5, alpha=0.7
        )

# Заголовок
plt.title(
    f"Візуалізація графа Дейкстри від вершини {start_vertex}\n"
    f"(Червоним виділено найкоротші шляхи, у дужках - відстані)",
    fontsize=14,
    fontweight="bold",
    pad=20,
)

plt.axis("off")
plt.tight_layout()
output_filename = f"graph_dijkstra_{start_vertex}.png"
plt.savefig(output_filename, dpi=300, bbox_inches="tight")
plt.show()

print(f"Граф збережено як '{output_filename}'")
print(f"\nНайкоротші відстані від {start_vertex}:")
for node, distance in sorted(shortest_distances.items()):
    print(f"  {start_vertex} -> {node}: {distance}")
