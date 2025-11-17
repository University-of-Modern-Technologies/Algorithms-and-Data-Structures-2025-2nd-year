import networkx as nx
import matplotlib.pyplot as plt

print("--- Приклад 5: Обхід графа (DFS та BFS) ---")

# Граф поданий у вигляді словника суміжності
graph_dict = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E"],
}

G = nx.Graph(graph_dict)  # type: ignore
# Встановимо початкову позицію, щоб усі 3 графіки були однаковими
pos = nx.spring_layout(G, seed=42)

# --- 2. Демонстрація DFS (Обхід у глибину) ---
print("\n--- DFS (Обхід у глибину) ---")
# Ця функція повертає ОРІЄНТОВАНЕ дерево,
# яке показує шлях обходу
dfs_tree = nx.dfs_tree(G, source="A")

print(f"Ребра, знайдені DFS: {list(dfs_tree.edges())}")


# --- 3. Демонстрація BFS (Обхід у ширину) ---
print("\n--- BFS (Обхід у ширину) ---")
# Ця функція також повертає ОРІЄНТОВАНЕ дерево
bfs_tree = nx.bfs_tree(G, source="A")

print(f"Ребра, знайдені BFS: {list(bfs_tree.edges())}")


# --- 4. Візуалізація для порівняння ---
print("\nМалюємо 3 графіки для порівняння...")

plt.figure(figsize=(15, 5))

# Графік 1: Оригінальний граф
plt.subplot(1, 3, 1)
plt.title("Оригінальний Граф")
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="skyblue",
    node_size=1000,
    width=2,
    font_weight="bold",
)

# Графік 2: DFS Дерево
plt.subplot(1, 3, 2)
plt.title("DFS (Обхід у глибину)")
nx.draw(
    dfs_tree,
    pos,  # Використовуємо ту саму 'pos'
    with_labels=True,
    node_color="lightcoral",
    node_size=1000,
    font_weight="bold",
)  # Показуємо стрілки обходу

# Графік 3: BFS Дерево
plt.subplot(1, 3, 3)
plt.title("BFS (Обхід у ширину)")
nx.draw(
    bfs_tree,
    pos,  # Використовуємо ту саму 'pos'
    with_labels=True,
    node_color="lightgreen",
    node_size=1000,
    font_weight="bold",
)  # Показуємо стрілки обходу

plt.tight_layout()
plt.show()
