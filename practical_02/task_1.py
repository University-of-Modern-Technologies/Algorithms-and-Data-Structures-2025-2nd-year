import networkx as nx
from collections import deque

# Створення графа
G = nx.DiGraph()

# Додавання ребер з пропускними здатностями
edges = [
    ("Термінал 1", "Склад 1", 25),
    ("Термінал 1", "Склад 2", 20),
    ("Термінал 1", "Склад 3", 15),
    ("Термінал 2", "Склад 3", 15),
    ("Термінал 2", "Склад 4", 30),
    ("Термінал 2", "Склад 2", 10),
    ("Склад 1", "Магазин 1", 15),
    ("Склад 1", "Магазин 2", 10),
    ("Склад 1", "Магазин 3", 20),
    ("Склад 2", "Магазин 4", 15),
    ("Склад 2", "Магазин 5", 10),
    ("Склад 2", "Магазин 6", 25),
    ("Склад 3", "Магазин 7", 20),
    ("Склад 3", "Магазин 8", 15),
    ("Склад 3", "Магазин 9", 10),
    ("Склад 4", "Магазин 10", 20),
    ("Склад 4", "Магазин 11", 10),
    ("Склад 4", "Магазин 12", 15),
    ("Склад 4", "Магазин 13", 5),
    ("Склад 4", "Магазин 14", 10),
]

# Додавання ребер до графа
G.add_weighted_edges_from(edges, weight="capacity")


# Функція для пошуку збільшуючого шляху (BFS)
def bfs(capacity, flow, source, sink, parent):
    visited = {node: False for node in G.nodes}
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()

        for neighbor in G.neighbors(current_node):
            residual_capacity = capacity[current_node][neighbor] - flow[
                current_node
            ].get(neighbor, 0)
            if not visited[neighbor] and residual_capacity > 0:
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)
    return False


# Основна функція для обчислення максимального потоку (Алгоритм Едмондса-Карпа)
def edmonds_karp(G, source, sink):
    capacity = nx.get_edge_attributes(G, "capacity")
    max_flow = 0
    parent = {}

    # Преобразуємо capacity у зручний для роботи формат
    capacity_matrix = {node: {} for node in G.nodes}
    for u, v, cap in G.edges.data("capacity"):
        capacity_matrix[u][v] = cap

    # Ініціалізація потоку
    flow_matrix = {node: {} for node in G.nodes}

    # Поки є збільшуючий шлях, додаємо потік
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        # Знаходимо мінімальну пропускну здатність уздовж знайденого шляху (вузьке місце)
        path_flow = float("Inf")
        s = sink
        while s != source:
            path_flow = min(
                path_flow,
                capacity_matrix[parent[s]][s] - flow_matrix[parent[s]].get(s, 0),
            )
            s = parent[s]

        # Оновлюємо потік уздовж шляху
        v = sink
        while v != source:
            u = parent[v]
            if v not in flow_matrix[u]:
                flow_matrix[u][v] = 0
            if u not in flow_matrix[v]:
                flow_matrix[v][u] = 0
            flow_matrix[u][v] += path_flow
            flow_matrix[v][u] -= path_flow
            v = parent[v]

        # Збільшуємо загальний потік
        max_flow += path_flow

    return max_flow


terminals = [node for node in G.nodes if "Термінал" in node]
stores = [node for node in G.nodes if "Магазин" in node]
print(" Таблиця з результатами")
print("|--------------|-------------|----------------|")
print("| Термінал     | Магазин     | Потік(одиниць) |")
print("|--------------|-------------|----------------|")
for terminal in terminals:
    for store in stores:
        max_flow = edmonds_karp(G, terminal, store)
        print(f"| {terminal:<12} | {store:<11} | {max_flow:<14} |")
