from pathlib import Path

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

CASE_TITLE = "Case Study про соціальну мережу ніндзя з селища Листя"
REPORT_PATH = Path("naruto_ninja_report.md")

characters = [
    {
        "name": "Naruto Uzumaki",
        "house": "Джинчуурікі",
        "role": "Джинчуурікі Дев'ятихвостого",
        "priority": "Стати Хокаге та захистити друзів",
    },
    {
        "name": "Sasuke Uchiha",
        "house": "Клан Uchiha",
        "role": "Ніндзя-втікач",
        "priority": "Помста та відновлення клану",
    },
    {
        "name": "Sakura Haruno",
        "house": "Команда 7",
        "role": "Медичний ніндзя",
        "priority": "Захист друзів та розвиток навичок",
    },
    {
        "name": "Kakashi Hatake",
        "house": "Сенсеї",
        "role": "Джонін, сенсей команди 7",
        "priority": "Навчання та захист учнів",
    },
    {
        "name": "Hinata Hyuga",
        "house": "Клан Hyuga",
        "role": "Ніндзя клану Hyuga",
        "priority": "Підтримка Naruto та розвиток",
    },
    {
        "name": "Shikamaru Nara",
        "house": "Команда 10",
        "role": "Тактик та стратег",
        "priority": "Захист селища та друзів",
    },
    {
        "name": "Ino Yamanaka",
        "house": "Команда 10",
        "role": "Сенсор та медичний ніндзя",
        "priority": "Розвиток команди та дружба",
    },
    {
        "name": "Choji Akimichi",
        "house": "Команда 10",
        "role": "Ніндзя-бойовик",
        "priority": "Захист друзів та команди",
    },
    {
        "name": "Gaara",
        "house": "Джинчуурікі",
        "role": "Казаге Піску",
        "priority": "Захист селища Піску та дружба з Naruto",
    },
    {
        "name": "Rock Lee",
        "house": "Команда Guy",
        "role": "Ніндзя-бойовик",
        "priority": "Стати сильним без технік",
    },
    {
        "name": "Neji Hyuga",
        "house": "Клан Hyuga",
        "role": "Геній клану Hyuga",
        "priority": "Захист Hinata та клану",
    },
]

interactions = [
    ("Naruto Uzumaki", "Sasuke Uchiha", 10, "найкращі друзі та суперники"),
    ("Naruto Uzumaki", "Sakura Haruno", 9, "члени команди 7"),
    ("Naruto Uzumaki", "Kakashi Hatake", 9, "учень-вчитель"),
    ("Naruto Uzumaki", "Hinata Hyuga", 10, "романтичні відносини"),
    ("Naruto Uzumaki", "Shikamaru Nara", 8, "найкращі друзі"),
    ("Naruto Uzumaki", "Gaara", 9, "дружба джинчуурікі"),
    ("Sasuke Uchiha", "Sakura Haruno", 10, "романтичні відносини"),
    ("Sasuke Uchiha", "Kakashi Hatake", 8, "учень-вчитель"),
    ("Sakura Haruno", "Ino Yamanaka", 8, "найкращі подруги"),
    ("Sakura Haruno", "Kakashi Hatake", 7, "учень-вчитель"),
    ("Hinata Hyuga", "Neji Hyuga", 7, "родинні зв'язки"),
    ("Hinata Hyuga", "Naruto Uzumaki", 10, "романтичні відносини"),
    ("Shikamaru Nara", "Ino Yamanaka", 9, "члени команди 10"),
    ("Shikamaru Nara", "Choji Akimichi", 10, "найкращі друзі"),
    ("Ino Yamanaka", "Choji Akimichi", 9, "члени команди 10"),
    ("Rock Lee", "Neji Hyuga", 8, "члени команди Guy"),
    ("Gaara", "Naruto Uzumaki", 9, "дружба джинчуурікі"),
    ("Neji Hyuga", "Hinata Hyuga", 7, "родинні зв'язки"),
]

house_colors = {
    "Джинчуурікі": "#FF6B6B",
    "Клан Uchiha": "#4ECDC4",
    "Команда 7": "#95E1D3",
    "Сенсеї": "#F38181",
    "Клан Hyuga": "#AA96DA",
    "Команда 10": "#FCBAD3",
    "Команда Guy": "#FFD93D",
}

label_shifts = {
    "Naruto Uzumaki": (0, 0.1),
    "Sasuke Uchiha": (0, -0.12),
    "Sakura Haruno": (0, 0.1),
    "Kakashi Hatake": (0, -0.12),
    "Hinata Hyuga": (0, 0.1),
    "Shikamaru Nara": (0, -0.12),
    "Ino Yamanaka": (0, 0.1),
    "Choji Akimichi": (0, -0.12),
    "Gaara": (0, 0.1),
    "Rock Lee": (0, -0.12),
    "Neji Hyuga": (0, 0.1),
}


def build_graph() -> nx.Graph:
    graph = nx.Graph(title=CASE_TITLE)
    for character in characters:
        graph.add_node(
            character["name"],
            house=character["house"],
            role=character["role"],
            priority=character["priority"],
        )

    for source, target, weight, relation in interactions:
        graph.add_edge(
            source,
            target,
            weight=weight,
            relation=relation,
            distance=1 / weight,  # сильний зв'язок -> менша дистанція
        )
    return graph


def describe_graph(graph: nx.Graph) -> None:
    houses = {data["house"] for _, data in graph.nodes(data=True)}
    print(f"\n{CASE_TITLE}")
    print("-" * len(CASE_TITLE))
    print(f"Вузлів: {graph.number_of_nodes()} | Ребер: {graph.number_of_edges()}")
    print(f"Групи та клани в аналізі: {', '.join(sorted(houses))}")


def report_influence(graph: nx.Graph) -> None:
    print("\n1) Вимірюємо вплив та силу зв'язків у селищі ніндзя")
    deg_centrality = nx.degree_centrality(graph)
    betweenness = nx.betweenness_centrality(graph, weight="distance")
    weighted_strength = {
        node: sum(data["weight"] for _, _, data in graph.edges(node, data=True))
        for node in graph.nodes
    }
    header = f"{'Персонаж':<25} {'Група/Клан':<18} {'Degree':<8} {'Betweenness':<12} {'Сила зв\'язків':<16}"
    print(header)
    print("-" * len(header))
    for node in sorted(graph.nodes, key=lambda n: weighted_strength[n], reverse=True):
        house = graph.nodes[node]["house"]
        print(
            f"{node:<25} {house:<18} "
            f"{deg_centrality[node]:<8.2f} {betweenness[node]:<12.2f} {weighted_strength[node]:<16}"
        )
    highlight_bridges(betweenness)


def highlight_bridges(betweenness: dict[str, float]) -> None:
    sensitive_bridge = 0.30
    print(f"\nКлючові посередники селища (betweenness > {sensitive_bridge}):")
    bridges = [node for node, score in betweenness.items() if score > sensitive_bridge]
    if not bridges:
        print("  У графі немає яскраво виражених посередників.")
        return
    for node in bridges:
        print(f"  * {node} — критичний для соціальної мережі, ризик розпаду зв'язків в разі відсутності")


def generate_character_report(graph: nx.Graph) -> None:
    deg_centrality = nx.degree_centrality(graph)
    weighted_strength = {
        node: sum(data["weight"] for _, _, data in graph.edges(node, data=True))
        for node in graph.nodes
    }

    md_lines = [
        f"# {CASE_TITLE}",
        "",
        "## Соціальна довідка по ніндзя",
        "",
        "| Персонаж | Група/Клан | Роль | Стратегічний пріоритет | Degree | Сила зв'язків |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    detailed_blocks: list[str] = []

    for node, data in sorted(
        graph.nodes(data=True),
        key=lambda item: weighted_strength[item[0]],
        reverse=True,
    ):
        house = data["house"]
        partners = sorted(graph.neighbors(node))
        partner_rows = []
        for partner in partners:
            relation = graph[node][partner]["relation"]
            weight = graph[node][partner]["weight"]
            partner_rows.append(
                f"| {partner} | {graph.nodes[partner]['house']} | {relation} | {weight} |"
            )

        md_lines.append(
            "| {node} | {house} | {role} | {priority} | {degree:.2f} | {strength} |".format(
                node=node,
                house=house,
                role=data["role"],
                priority=data["priority"],
                degree=deg_centrality[node],
                strength=weighted_strength[node],
            )
        )

        detailed_blocks.extend(
            [
                f"### {node}",
                "",
                f"- Група/Клан: {house}",
                f"- Роль: {data['role']}",
                f"- Стратегічний пріоритет: {data['priority']}",
                f"- Degree centrality: {deg_centrality[node]:.2f}",
                f"- Сумарна сила зв'язків: {weighted_strength[node]}",
                "",
                "#### Взаємодії з іншими ніндзя",
            ]
        )
        if partner_rows:
            detailed_blocks.append("| Партнер | Група/Клан | Тип взаємодії | Вага |")
            detailed_blocks.append("| --- | --- | --- | --- |")
            detailed_blocks.extend(partner_rows)
        else:
            detailed_blocks.append("_Наразі немає активних зв'язків._")
        detailed_blocks.append("")

    md_lines.extend(["", "## Детальна розшифровка", ""] + detailed_blocks)

    REPORT_PATH.write_text("\n".join(md_lines), encoding="utf-8")


def draw_graph(graph: nx.Graph) -> None:
    node_colors = [
        house_colors.get(graph.nodes[node]["house"], "#CCCCCC") for node in graph.nodes
    ]
    deg_centrality = nx.degree_centrality(graph)
    node_sizes = [
        2000 if score == max(deg_centrality.values()) else 1200
        for score in deg_centrality.values()
    ]
    layout = nx.circular_layout(graph)
    weights = [graph[u][v]["weight"] * 0.4 for u, v in graph.edges()]

    fig, ax = plt.subplots(figsize=(12, 7.5))
    ax.set_title("Соціальна мережа ніндзя з селища Листя", pad=15)
    nx.draw_networkx_edges(graph, layout, width=weights, alpha=0.7, ax=ax)
    nx.draw_networkx_nodes(
        graph,
        layout,
        node_color=node_colors,
        node_size=node_sizes,
        edgecolors="black",
        linewidths=1.2,
        ax=ax,
    )
    edge_labels = nx.get_edge_attributes(graph, "relation")
    nx.draw_networkx_edge_labels(
        graph,
        layout,
        edge_labels=edge_labels,
        font_size=7,
        ax=ax,
    )
    
    # Розраховуємо позиції міток радіально назовні від центру кола
    label_positions = {}
    center = np.array([0.0, 0.0])
    offset_distance = 0.15  # відстань від вузла до мітки
    
    for node in graph.nodes:
        node_pos = np.array(layout[node])
        # Обчислюємо напрямок від центру до вузла
        direction = node_pos - center
        if np.linalg.norm(direction) > 0:
            direction = direction / np.linalg.norm(direction)
        else:
            direction = np.array([1.0, 0.0])
        
        # Зміщуємо мітку назовні від вузла
        label_pos = node_pos + direction * offset_distance
        label_positions[node] = tuple(label_pos)
    
    nx.draw_networkx_labels(graph, label_positions, font_weight="bold", font_size=9, ax=ax)

    ax.axis("off")
    ax.margins(0.25)
    plt.tight_layout()
    plt.show()


def main() -> None:
    graph = build_graph()
    describe_graph(graph)
    report_influence(graph)
    generate_character_report(graph)

    draw_graph(graph)


if __name__ == "__main__":
    main()

