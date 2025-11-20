import networkx as nx
import matplotlib.pyplot as plt
from bfs_shortest_path import G, bfs_shortest_path

# Задання початкової та кінцевої вершин
start_vertex = 'A'
goal_vertex = 'H'

# Створення візуалізації графа
plt.figure(figsize=(12, 8))

# Знаходження найкоротшого шляху для підсвітки
# shortest_path = bfs_shortest_path(G, start_vertex, goal_vertex)
shortest_path = nx.shortest_path(G, source=start_vertex, target=goal_vertex)

# Створення списку ребер найкоротшого шляху
path_edges = []
if shortest_path:
    for i in range(len(shortest_path) - 1):
        path_edges.append((shortest_path[i], shortest_path[i + 1]))

# Позиціонування вершин
pos = nx.spring_layout(G,  seed=42)

# Малювання всіх ребер (сірим кольором)
nx.draw_networkx_edges(G, pos, edge_color='gray', width=1, alpha=0.3)

# Малювання ребер найкоротшого шляху (червоним кольором)
if path_edges:
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, alpha=0.8)

# Малювання вершин
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000, alpha=0.9)

# Малювання міток вершин
nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')

# Малювання міток ребер (опціонально)
# nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): '' for u, v in G.edges()})

# Додавання заголовка
if shortest_path:
    plt.title(f'Візуалізація графа з найкоротшим шляхом {start_vertex} -> {goal_vertex}: {" -> ".join(shortest_path)}', 
              fontsize=14, fontweight='bold', pad=20)
else:
    plt.title(f'Візуалізація графа (шлях від {start_vertex} до {goal_vertex} не знайдено)', 
              fontsize=14, fontweight='bold', pad=20)

plt.axis('off')
plt.tight_layout()
output_filename = f'graph_visualization_{start_vertex}_to_{goal_vertex}.png'
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
plt.show()

print(f"Граф збережено як '{output_filename}'")
if shortest_path:
    print(f"Найкоротший шлях: {' -> '.join(shortest_path)}")

