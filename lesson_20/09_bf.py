import sys
from typing import List, Tuple


def shortest_path(graph: List[List[Tuple[int, int]]], start: int, end: int) -> int:
    """
    Алгоритм Беллмана-Форда (Bellman-Ford) - пошук найкоротшого шляху в графі.
    """
    n = len(graph)
    distances = [sys.maxsize] * n
    distances[start] = 0
    print(distances)
    for _ in range(n - 1):
        for u in range(n):
            for v, weight in graph[u]:
                if distances[u] != sys.maxsize and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
    print(distances)
    return distances[end]


# Приклад графа: [[(сусід, вага), ...], ...]
graph = [[(1, 4), (2, 1)], [(3, 1)], [(1, 2), (3, 5)], [(4, 3)], []]

print(shortest_path(graph, 0, 4))
