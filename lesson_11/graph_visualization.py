import networkx as nx
import matplotlib.pyplot as plt

graph = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E"],
}

edges = [
    ("A", "B"),
    ("A", "C"),
    ("B", "A"),
    ("B", "D"),
    ("B", "E"),
    ("C", "A"),
    ("C", "F"),
    ("D", "B"),
    ("E", "B"),
    ("E", "F"),
    ("F", "C"),
    ("F", "E"),
]
G = nx.Graph(edges)

pos = nx.spring_layout(G)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=1500,
    node_color="skyblue",
    font_size=15,
    font_weight="bold",
)
plt.title("Graph Visualization")
plt.savefig("graph.png")
plt.show()
