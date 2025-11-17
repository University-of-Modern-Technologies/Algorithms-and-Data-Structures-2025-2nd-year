from pathlib import Path

import networkx as nx
import matplotlib.pyplot as plt

CASE_TITLE = "Case Study про стратегію Братства Персня перед битвою за Мордор"
REPORT_PATH = Path("fellowship_priorities_report.md")

characters = [
    {
        "name": "Aragorn",
        "house": "Люди",
        "role": "Майбутній король Гондору",
        "priority": "Об'єднати людські королівства",
    },
    {
        "name": "Gandalf",
        "house": "Майя",
        "role": "Білий Чародій",
        "priority": "Координувати опір Саурону",
    },
    {
        "name": "Frodo",
        "house": "Хобіти",
        "role": "Носій Персня",
        "priority": "Знищити Перстень у вогнях Мордору",
    },
    {
        "name": "Legolas",
        "house": "Ельфи",
        "role": "Ельфійський лучник",
        "priority": "Захистити Братство",
    },
    {
        "name": "Gimli",
        "house": "Гноми",
        "role": "Воїн гномів",
        "priority": "Відновити честь гномів",
    },
    {
        "name": "Boromir",
        "house": "Люди",
        "role": "Командир Гондору",
        "priority": "Захистити Гондор",
    },
    {
        "name": "Saruman",
        "house": "Майя",
        "role": "Зрадник",
        "priority": "Послабити Братство",
    },
]

interactions = [
    ("Aragorn", "Gandalf", 10, "стратегічний союз"),
    ("Aragorn", "Legolas", 9, "боєва дружба"),
    ("Aragorn", "Gimli", 9, "побратимство"),
    ("Aragorn", "Boromir", 7, "військове командування"),
    ("Gandalf", "Frodo", 10, "наставництво"),
    ("Gandalf", "Legolas", 8, "мудрі поради"),
    ("Frodo", "Legolas", 6, "захист Братства"),
    ("Frodo", "Gimli", 6, "взаємна підтримка"),
    ("Legolas", "Gimli", 10, "незламна дружба"),
    ("Boromir", "Frodo", 5, "напруженість через Перстень"),
    ("Saruman", "Gandalf", 2, "відкритий конфлікт"),
    ("Saruman", "Aragorn", 1, "ворожість"),
]

house_colors = {
    "Люди": "#4A90E2",
    "Майя": "#FFFFFF",
    "Хобіти": "#8B7355",
    "Ельфи": "#90EE90",
    "Гноми": "#8B4513",
}

label_shifts = {
    "Aragorn": (0, 0.1),
    "Gandalf": (0, -0.12),
    "Frodo": (0, 0.1),
    "Legolas": (0, -0.12),
    "Gimli": (0, 0.1),
    "Boromir": (0, -0.12),
    "Saruman": (0, 0.1),
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
    print(f"Раси та фракції в аналізі: {', '.join(sorted(houses))}")


def report_influence(graph: nx.Graph) -> None:
    print("\n1) Вимірюємо вплив та силу зв'язків у Братстві")
    deg_centrality = nx.degree_centrality(graph)
    betweenness = nx.betweenness_centrality(graph, weight="distance")
    weighted_strength = {
        node: sum(data["weight"] for _, _, data in graph.edges(node, data=True))
        for node in graph.nodes
    }
    header = f"{'Персонаж':<22} {'Раса/Фракція':<15} {'Degree':<8} {'Betweenness':<12} {'Сила зв\'язків':<16}"
    print(header)
    print("-" * len(header))
    for node in sorted(graph.nodes, key=lambda n: weighted_strength[n], reverse=True):
        house = graph.nodes[node]["house"]
        print(
            f"{node:<22} {house:<15} "
            f"{deg_centrality[node]:<8.2f} {betweenness[node]:<12.2f} {weighted_strength[node]:<16}"
        )
    highlight_bridges(betweenness)


def highlight_bridges(betweenness: dict[str, float]) -> None:
    sensitive_bridge = 0.30
    print(f"\nКлючові посередники Братства (betweenness > {sensitive_bridge}):")
    bridges = [node for node, score in betweenness.items() if score > sensitive_bridge]
    if not bridges:
        print("  У графі немає яскраво виражених посередників.")
        return
    for node in bridges:
        print(f"  * {node} — критичний для єдності Братства, ризик розпаду в разі втрати")


def generate_character_report(graph: nx.Graph) -> None:
    deg_centrality = nx.degree_centrality(graph)
    weighted_strength = {
        node: sum(data["weight"] for _, _, data in graph.edges(node, data=True))
        for node in graph.nodes
    }

    md_lines = [
        f"# {CASE_TITLE}",
        "",
        "## Тактична довідка по членах Братства Персня",
        "",
        "| Персонаж | Раса/Фракція | Роль | Стратегічний пріоритет | Degree | Сила зв'язків |",
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
                f"- Раса/Фракція: {house}",
                f"- Роль: {data['role']}",
                f"- Стратегічний пріоритет: {data['priority']}",
                f"- Degree centrality: {deg_centrality[node]:.2f}",
                f"- Сумарна сила зв'язків: {weighted_strength[node]}",
                "",
                "#### Взаємодії з іншими членами Братства",
            ]
        )
        if partner_rows:
            detailed_blocks.append("| Партнер | Раса/Фракція | Тип взаємодії | Вага |")
            detailed_blocks.append("| --- | --- | --- | --- |")
            detailed_blocks.extend(partner_rows)
        else:
            detailed_blocks.append("_Наразі немає активних зв'язків у Братстві._")
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
    layout = nx.spring_layout(graph, seed=42)
    weights = [graph[u][v]["weight"] * 0.4 for u, v in graph.edges()]

    fig, ax = plt.subplots(figsize=(12, 7.5))
    ax.set_title("Соціальна мережа Братства Персня: стратегічні зв'язки перед битвою за Мордор", pad=15)
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
        font_size=8,
        ax=ax,
    )
    label_positions = {
        node: (
            layout[node][0] + label_shifts.get(node, (0.0, 0.0))[0],
            layout[node][1] + label_shifts.get(node, (0.0, 0.0))[1],
        )
        for node in graph.nodes
    }
    nx.draw_networkx_labels(graph, label_positions, font_weight="bold", ax=ax)

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

