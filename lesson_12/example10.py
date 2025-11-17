from collections import deque

import networkx as nx
import matplotlib.pyplot as plt


def dfs_recursive(graph, vertex, visited=None, order=None):
    if visited is None:
        visited = set()
    if order is None:
        order = []
    visited.add(vertex)
    order.append(vertex)
    print(vertex, end=" ")  # Відвідуємо вершину
    for neighbor in graph[vertex]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited, order)


def bfs_iterative(graph, start_vertex):
    visited = set()
    queue = deque([start_vertex])
    order = []

    while queue:
        vertex = queue.popleft()
        if vertex in visited:
            continue
        print(vertex, end=" ")
        visited.add(vertex)
        order.append(vertex)
        for neighbor in graph[vertex]:
            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)
    return order


graph = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E"],
}

G = nx.Graph(graph)  # type: ignore

print("\n=== Порівняння DFS ===")
dfs_tree = nx.dfs_tree(G, "A")
print(f"NetworkX порядок вузлів : {list(dfs_tree.nodes())}")
print(f"NetworkX ребра дерева   : {list(dfs_tree.edges())}")
print("Наш рекурсивний порядок :", end=" ")
dfs_order = []
dfs_recursive(graph, "A", order=dfs_order)
print(f"\nНаш список              : {dfs_order}\n")

print("=== Порівняння BFS ===")
bfs_tree = nx.bfs_tree(G, "A")
print(f"NetworkX порядок вузлів : {list(bfs_tree.nodes())}")
print(f"NetworkX ребра дерева   : {list(bfs_tree.edges())}")
print("Наш ітеративний порядок :", end=" ")

bfs_order = bfs_iterative(graph, "A")
print(f"\nНаш список              : {bfs_order}\n")

plt.figure(figsize=(6, 6))
pos = nx.spring_layout(G, seed=42)
nx.draw_networkx(
    G,
    pos,
    with_labels=True,
    node_size=800,
    node_color="lightblue",
    font_size=16,
    font_weight="bold",
)
plt.show()
