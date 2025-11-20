import networkx as nx


# Матриця пропускної здатності для каналів у мережі (capacity_matrix)
capacity_matrix = [
    [0, 0, 15, 10, 0, 0, 0],  # Джерело 1
    [0, 0, 20, 0, 0, 0, 0],  # Джерело 2
    [0, 0, 0, 0, 10, 5, 0],  # Проміжний Вузол 1
    [0, 0, 0, 0, 0, 0, 15],  # Проміжний Вузол 2
    [0, 0, 0, 0, 0, 0, 0],  # Споживач 1
    [0, 0, 0, 0, 0, 0, 0],  # Споживач 2
    [0, 0, 0, 0, 0, 0, 0],  # Споживач 3
]

source = 0  # Джерело 1
sink = 6  # Споживач 3

G = nx.DiGraph()

n = len(capacity_matrix)

for u in range(n):
    for v in range(n):
        if capacity_matrix[u][v] > 0:
            G.add_edge(u, v, capacity=capacity_matrix[u][v])

flow_value, flow_dict = nx.maximum_flow(
    G, source, sink, flow_func=nx.algorithms.flow.edmonds_karp
)

print("Максимальний потік:", flow_value)
print("Розподіл потоків:", flow_dict)
