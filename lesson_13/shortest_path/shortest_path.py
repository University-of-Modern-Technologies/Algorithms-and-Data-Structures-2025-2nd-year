import networkx as nx

G = nx.Graph()

edges = [
    ('A', 'B'), ('A', 'C'),
    ('B', 'D'), ('C', 'E'), ('C', 'G'),
    ('D', 'F'), ('E', 'G'),
    ('F', 'H'), ('G', 'I'),
    ('H', 'I'), ('H', 'J'), ('D', 'J'), ('E', 'J')
]
G.add_edges_from(edges)

path = nx.shortest_path(G, source='A', target='J')
print("Найкоротший шлях:", " -> ".join(path))

all_nodes = list(nx.bfs_tree(G, source='A'))
print("Всі вершини:", all_nodes)
print("Всі вершини", G.nodes())

all_edges = list(nx.bfs_edges(G, source='A'))
print("Всі ребра:", all_edges)
print("Всі ребра", G.edges())

all_paths = nx.single_source_shortest_path(G, source='A')
print("Всі шляхи:", all_paths)

