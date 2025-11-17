from pathlib import Path

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

CASE_TITLE = "Case Study про соціальну мережу персонажів Теорії великого вибуху"
REPORT_PATH = Path("big_bang_theory_report.md")

characters = [
    {
        "name": "Sheldon Cooper",
        "house": "Фізики",
        "role": "Фізик-теоретик",
        "priority": "Розвиток теорії струн та квантової механіки",
    },
    {
        "name": "Leonard Hofstadter",
        "house": "Фізики",
        "role": "Фізик-експериментатор",
        "priority": "Баланс між наукою та особистим життям",
    },
    {
        "name": "Penny",
        "house": "Актори",
        "role": "Актриса та офіціантка",
        "priority": "Побудова акторської кар'єри",
    },
    {
        "name": "Howard Wolowitz",
        "house": "Інженери",
        "role": "Інженер-астронавт",
        "priority": "Розробка космічних технологій",
    },
    {
        "name": "Rajesh Koothrappali",
        "house": "Астрофізики",
        "role": "Астрофізик",
        "priority": "Дослідження космосу та знаходження кохання",
    },
    {
        "name": "Bernadette Rostenkowski",
        "house": "Біологи",
        "role": "Мікробіолог",
        "priority": "Наукові дослідження та сім'я",
    },
    {
        "name": "Amy Farrah Fowler",
        "house": "Біологи",
        "role": "Нейробіолог",
        "priority": "Дослідження мозку та розвиток відносин",
    },
    {
        "name": "Stuart Bloom",
        "house": "Бізнес",
        "role": "Власник комікс-магазину",
        "priority": "Розвиток бізнесу та соціалізація",
    },
    {
        "name": "Barry Kripke",
        "house": "Фізики",
        "role": "Фізик-теоретик",
        "priority": "Конкуренція з Sheldon та наукові досягнення",
    },
]

interactions = [
    ("Sheldon Cooper", "Leonard Hofstadter", 10, "кімнати та найкращі друзі"),
    ("Sheldon Cooper", "Amy Farrah Fowler", 9, "романтичні відносини"),
    ("Sheldon Cooper", "Penny", 7, "сусідські стосунки"),
    ("Sheldon Cooper", "Howard Wolowitz", 6, "наукові дискусії"),
    ("Sheldon Cooper", "Rajesh Koothrappali", 6, "наукові дискусії"),
    ("Leonard Hofstadter", "Penny", 10, "романтичні відносини"),
    ("Leonard Hofstadter", "Howard Wolowitz", 8, "дружба"),
    ("Leonard Hofstadter", "Rajesh Koothrappali", 8, "дружба"),
    ("Leonard Hofstadter", "Amy Farrah Fowler", 7, "дружба через Sheldon"),
    ("Penny", "Amy Farrah Fowler", 9, "найкращі подруги"),
    ("Penny", "Bernadette Rostenkowski", 9, "найкращі подруги"),
    ("Penny", "Rajesh Koothrappali", 5, "одностороння симпатія"),
    ("Howard Wolowitz", "Rajesh Koothrappali", 10, "найкращі друзі"),
    ("Howard Wolowitz", "Bernadette Rostenkowski", 10, "шлюб"),
    ("Rajesh Koothrappali", "Stuart Bloom", 7, "дружба через комікси"),
    ("Bernadette Rostenkowski", "Amy Farrah Fowler", 8, "дружба"),
    ("Stuart Bloom", "Sheldon Cooper", 6, "дружба через комікси"),
    ("Stuart Bloom", "Leonard Hofstadter", 6, "дружба через комікси"),
    ("Stuart Bloom", "Howard Wolowitz", 5, "дружба через комікси"),
    ("Barry Kripke", "Sheldon Cooper", 4, "наукова конкуренція"),
    ("Barry Kripke", "Leonard Hofstadter", 6, "колеги-фізики"),
    ("Barry Kripke", "Amy Farrah Fowler", 5, "наукові дискусії"),
]

house_colors = {
    "Фізики": "#4169E1",
    "Інженери": "#FF6347",
    "Астрофізики": "#9370DB",
    "Біологи": "#32CD32",
    "Актори": "#FFD700",
    "Бізнес": "#FFA500",
}

label_shifts = {
    "Sheldon Cooper": (0, 0.1),
    "Leonard Hofstadter": (0, -0.12),
    "Penny": (0, 0.1),
    "Howard Wolowitz": (0, -0.12),
    "Rajesh Koothrappali": (0, 0.1),
    "Bernadette Rostenkowski": (0, -0.12),
    "Amy Farrah Fowler": (0, 0.1),
    "Stuart Bloom": (0, -0.12),
    "Barry Kripke": (0, 0.1),
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
    print(f"Професійні групи в аналізі: {', '.join(sorted(houses))}")


def report_influence(graph: nx.Graph) -> None:
    print("\n1) Вимірюємо вплив та силу зв'язків у групі друзів")
    deg_centrality = nx.degree_centrality(graph)
    betweenness = nx.betweenness_centrality(graph, weight="distance")
    weighted_strength = {
        node: sum(data["weight"] for _, _, data in graph.edges(node, data=True))
        for node in graph.nodes
    }
    header = f"{'Персонаж':<25} {'Професійна група':<18} {'Degree':<8} {'Betweenness':<12} {'Сила зв\'язків':<16}"
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
    print(f"\nКлючові посередники групи (betweenness > {sensitive_bridge}):")
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
        "## Соціальна довідка по персонажах",
        "",
        "| Персонаж | Професійна група | Роль | Стратегічний пріоритет | Degree | Сила зв'язків |",
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
                f"- Професійна група: {house}",
                f"- Роль: {data['role']}",
                f"- Стратегічний пріоритет: {data['priority']}",
                f"- Degree centrality: {deg_centrality[node]:.2f}",
                f"- Сумарна сила зв'язків: {weighted_strength[node]}",
                "",
                "#### Взаємодії з іншими персонажами",
            ]
        )
        if partner_rows:
            detailed_blocks.append("| Партнер | Професійна група | Тип взаємодії | Вага |")
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
    ax.set_title("Соціальна мережа персонажів Теорії великого вибуху", pad=15)
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

