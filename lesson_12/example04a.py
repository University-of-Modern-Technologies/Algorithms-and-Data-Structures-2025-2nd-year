"""Додатковий приклад показуємо знаходження мостів та критичних вершин"""

import networkx as nx
import matplotlib.pyplot as plt


def build_supply_graph() -> nx.Graph:
    graph = nx.Graph()
    cluster_one = ["A", "B", "C"]
    cluster_two = ["D", "E"]

    graph.add_nodes_from(cluster_one, region="Кластер 1")
    graph.add_nodes_from(cluster_two, region="Кластер 2")

    graph.add_edges_from([("A", "B"), ("B", "C"), ("A", "C")])  # щільна трійка
    graph.add_edges_from([("D", "E")])  # невеликий ланцюжок
    graph.add_edge("C", "D", relation="ключовий міст")
    return graph


def describe_components(graph: nx.Graph, label: str) -> None:
    components = list(nx.connected_components(graph))
    print(f"\n{label}: {len(components)} компонент(и)")
    for idx, component in enumerate(components, 1):
        members = ", ".join(sorted(component))
        print(f"  {idx}) {members}")


def plot_graph(graph: nx.Graph, title: str) -> None:
    plt.figure(figsize=(6, 4.5))
    pos = nx.spring_layout(graph, seed=4)
    colors = [
        "#6EC6FF" if graph.nodes[node]["region"] == "Кластер 1" else "#FFD96A"
        for node in graph.nodes
    ]
    nx.draw_networkx(
        graph,
        pos,
        node_color=colors,
        with_labels=True,
        node_size=1100,
        font_weight="bold",
    )
    bridge_labels = nx.get_edge_attributes(graph, "relation")
    if bridge_labels:
        nx.draw_networkx_edge_labels(
            graph, pos, edge_labels=bridge_labels, font_color="firebrick"
        )
    plt.title(title)
    plt.axis("off")
    plt.show()


def main() -> None:
    graph = build_supply_graph()

    print("=== Крок 1. Єдина мережа ===")
    describe_components(graph, "Перед збоєм")
    plot_graph(graph, "Вузол C-D тримає всі склади в єдиному ланцюгу")
    print(
        "\nПеревірка самим NetworkX: критичні ребра (bridges) =",
        list(nx.bridges(graph)),
    )
    print(
        "Критичні вершини (articulation points) =",
        list(nx.articulation_points(graph)),
    )
    print("\n=== Крок 2. Втрачаємо міст C-D ===")
    # broken_graph = graph.copy()
    graph.remove_edge("C", "D")
    describe_components(graph, "Після втрати мосту")
    plot_graph(graph, "Без мосту: мережа розпалась на 2 компоненти")


if __name__ == "__main__":
    main()
