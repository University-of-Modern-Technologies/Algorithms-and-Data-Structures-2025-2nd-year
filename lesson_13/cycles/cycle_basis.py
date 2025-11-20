import networkx as nx
import matplotlib.pyplot as plt

# Неорієнтований граф
G = nx.Graph()
G.add_edges_from(
    [
        ("A", "B"),
        ("B", "C"),
        ("C", "A"),  # цикл A-B-C-A
        ("C", "D"),
        ("D", "E"),
        ("E", "C"),  # цикл C-D-E-C
    ]
)

cycles = nx.cycle_basis(G)
print("Цикли у неорієнтованому графі:", cycles)

# Візуалізація графа
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, seed=42)

# Малювання всіх ребер (сірим кольором)
nx.draw_networkx_edges(G, pos, edge_color="gray", width=1.5, alpha=0.3)

# Підсвітка циклів різними кольорами
colors = ["red", "blue", "green", "orange", "purple"]
for idx, cycle in enumerate(cycles):
    if len(cycle) > 1:
        cycle_edges = []
        for i in range(len(cycle)):
            cycle_edges.append((cycle[i], cycle[(i + 1) % len(cycle)]))

        color = colors[idx % len(colors)]
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=cycle_edges,
            edge_color=color,
            width=3,
            alpha=0.8,
            style="dashed",
        )

# Малювання вершин та міток
nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=1500, alpha=0.9)
nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")

cycle_info = ", ".join(["-".join(cycle) + "-" + cycle[0] for cycle in cycles])
plt.title(
    f"Неорієнтований граф з базисом циклів\nЗнайдено циклів у базисі: {len(cycles)}\n{cycle_info}",
    fontsize=12,
    fontweight="bold",
    pad=20,
)

plt.axis("off")
plt.tight_layout()
plt.show()
