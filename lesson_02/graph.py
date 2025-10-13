import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_node("Ivan")
G.add_node("Veronika")
G.add_node("Fedir")
G.add_node("Dmytro")
G.add_node("Marta")
G.add_node("Tamara")
G.add_node("Yehor")
G.add_node("Serhii")
G.add_node("Viktoriia")
G.add_node("Maksym")
G.add_node("Ihor")
G.add_node("Roman")


G.add_edge("Ivan", "Veronika")
G.add_edge("Ivan", "Dmytro")
G.add_edge("Yehor", "Viktoriia")
G.add_edge("Yehor", "Serhii")
G.add_edge("Serhii", "Viktoriia")
G.add_edge("Serhii", "Maksym")
G.add_edge("Serhii", "Roman")
G.add_edge("Serhii", "Ihor")
G.add_edge("Serhii", "Tamara")
G.add_edge("Serhii", "Marta")
G.add_edge("Tamara", "Fedir")
G.add_edge("Veronika", "Fedir")

plt.figure(figsize=(6, 6))
nx.draw_networkx(
    G,
    with_labels=True,
    font_weight="bold",
    font_size=16,
    node_color="lightblue",
    edge_color="gray",
)
plt.axis("off")
plt.show()
