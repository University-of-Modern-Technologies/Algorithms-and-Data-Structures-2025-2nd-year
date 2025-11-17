# Аналіз Мережі
import networkx as nx
import matplotlib.pyplot as plt

# Створення графа
G = nx.Graph()
G.add_edges_from([("A", "B"), ("A", "C"), ("B", "C"), ("B", "D")])

# --- 2. Додавання Атрибутів 'weight' (Вага/Час) ---
G.edges["A", "B"]["weight"] = 1  # A-B = 1 хв
G.edges["A", "C"]["weight"] = 5  # A-C = 5 хв
G.edges["B", "C"]["weight"] = 1  # B-C = 1 хв
G.edges["B", "D"]["weight"] = 1  # B-D = 1 хв


# -Аналіз центральності

# Ступінь (Degree): Скільки у вузла "друзів"?
deg_centrality = nx.degree_centrality(
    G
)  # Нормалізований показник: degree(node) / (N - 1)
print(f"Ступінь центральності (Degree): {deg_centrality}")

# Посередництво (Betweenness): Через кого пролягає більшість шляхів?
bet_centrality = nx.betweenness_centrality(G)
print(f"Центральність посередництва (Betweenness): {bet_centrality}")
bet_centrality_weighted = nx.betweenness_centrality(G, weight="weight")
print(
    f"Центральність посередництва (Betweenness) враховуючи вагу: {bet_centrality_weighted}"
)

# Близькість (Closeness): Наскільки вузол "близький" до всіх інших?
close_centrality = nx.closeness_centrality(G)
print(f"Центральність близькості (Closeness): {close_centrality}")
close_centrality_weighted = nx.closeness_centrality(G, distance="weight")
print(
    f"Центральність близькості (Closeness) враховуючи вагу: {close_centrality_weighted}"
)

# --- 4. Пошук найкоротших шляхів (АТРИБУТ В ДІЇ) ---
print("\n--- Пошук Найкоротших Шляхів ---")

# Шлях 1: Ігноруючи вагу (за замовчуванням)
# Шукає шлях з найменшою кількістю "кроків"
path_by_hops = nx.shortest_path(G, source="A", target="C")
print(f"Найкоротший шлях (по кроках) з A до C: {path_by_hops}")


# Шлях 2: Використовуючи вагу (weight)
# Шукаємо "найшвидший" шлях, використовуючи наш атрибут 'weight'
path_by_weight = nx.shortest_path(G, source="A", target="C", weight="weight")

print(f"\nНайшвидший шлях (по вазі/часу) з A до C: {path_by_weight}")

# Шлях 3: Середня довжина шляху (за лекцією)
# Розраховує середню відстань між УСІМА парами вузлів
avg_path_len = nx.average_shortest_path_length(G)
print(f"Середня довжина найкоротшого шляху : {avg_path_len}")

# Розраховує середню відстань між УСІМА парами вузлів (враховуючи вагу)
avg_path_len = nx.average_shortest_path_length(G, weight="weight")
print(f"Середня довжина 'найшвидшого' шляху : {avg_path_len}")
# Візуалізація
print("\nМалюємо граф...")
pos = nx.spring_layout(G, seed=42)
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="skyblue",
    node_size=1500,
    font_weight="bold",
    width=2,
)

# Малюємо мітки з нашою "вагою" (часом)
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.show()
