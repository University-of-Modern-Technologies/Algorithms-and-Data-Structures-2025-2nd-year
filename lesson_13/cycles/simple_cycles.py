import networkx as nx
import matplotlib.pyplot as plt

# Орієнтований граф
DG = nx.DiGraph()
DG.add_edges_from(
    [
        ("A", "B"),
        ("B", "C"),
        ("C", "A"),  # цикл A → B → C → A
        ("C", "D"),
        ("D", "C"),  # цикл C → D → C
    ]
)

directed_cycles = list(nx.simple_cycles(DG))
print("Цикли в орієнтованому графі:", directed_cycles)

# Візуалізація графа
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(DG, seed=42)

# Малювання всіх ребер (сірим кольором)
nx.draw_networkx_edges(
    DG,
    pos,
    edge_color="gray",
    width=1.5,
    alpha=0.3,
    arrows=True,
    arrowsize=20,
    arrowstyle="->",
    connectionstyle="arc3,rad=0.1",
    node_size=1500,
)

# Підсвітка циклів різними кольорами
colors = ["red", "blue", "green", "orange", "purple"]
for idx, cycle in enumerate(directed_cycles):
    if len(cycle) > 1:
        cycle_edges = []
        for i in range(len(cycle)):
            cycle_edges.append((cycle[i], cycle[(i + 1) % len(cycle)]))

        color = colors[idx % len(colors)]
        nx.draw_networkx_edges(
            DG,
            pos,
            edgelist=cycle_edges,
            edge_color=color,
            width=3,
            alpha=0.8,
            arrows=True,
            arrowsize=25,
            arrowstyle="->",
            style="dashed",
            connectionstyle="arc3,rad=0.1",
            node_size=1500,
        )

# Малювання вершин та міток
nx.draw_networkx_nodes(DG, pos, node_color="lightblue", node_size=1500, alpha=0.9)
nx.draw_networkx_labels(DG, pos, font_size=12, font_weight="bold")

cycle_info = ", ".join(
    [" → ".join(cycle) + " → " + cycle[0] for cycle in directed_cycles]
)
plt.title(
    f"Орієнтований граф з циклами\nЗнайдено циклів: {len(directed_cycles)}\n{cycle_info}",
    fontsize=12,
    fontweight="bold",
    pad=20,
)

plt.axis("off")
plt.tight_layout()
plt.show()
