import networkx as nx
import matplotlib.pyplot as plt

# Створення Орієнтованого графа ---
DG = nx.DiGraph()

# Додавання вузлів з атрибутами ---
# Додаємо вузли з атрибутом 'type', який ми ВИКОРИСТАЄМО
DG.add_node("A", type="Hub")  # Головний транспортний вузол
DG.add_node("B", type="Local")  # Звичайне перехрестя
DG.add_node("C", type="Local")  # Звичайне перехрестя
DG.add_node("D", type="Exit")  # Виїзд з міста

# --- 3. Додавання ребер з атрибутами ---
# Додаємо ребра (дороги) з 'weight' (час у дорозі)
DG.add_edge("A", "B", weight=10)  # A -> B займає 10 хв
DG.add_edge("A", "C", weight=2)  # A -> C займає 2 хв
DG.add_edge("B", "D", weight=3)  # B -> D займає 3 хв
DG.add_edge("C", "D", weight=8)  # C -> D займає 8 хв


# --- 4. АТРИБУТИ ВУЗЛІВ У ДІЇ (Функція) ---
print("\n--- Використання Атрибутів Вузлів ---")
# Створимо логіку: ми хочемо різні кольори для різних типів вузлів
# Словник "тип -> колір"
color_map = {"Hub": "red", "Local": "skyblue", "Exit": "green"}

# Тепер пройдемося по вузлах і створимо список кольорів
# Вузол "А" має тип "Hub", отже, він буде "red"
# Вузли "B", "C" мають тип "Local" -> "skyblue" і т.д.

# Отут атрибут 'type' виконує свою функцію:
node_colors = [color_map[DG.nodes[node]["type"]] for node in DG.nodes()]

print(f"Згенеровано список кольорів на основі 'type': {node_colors}")


# Візуалізація
print("\nМалюємо граф...")
pos = nx.spring_layout(DG, seed=42)

nx.draw(
    DG,
    pos,
    with_labels=True,
    node_color=node_colors,
    node_size=2000,
    font_weight="bold",
    font_color="black",
    arrowsize=20,
)

# Покажемо також вагу ребер
edge_labels = nx.get_edge_attributes(DG, "weight")
nx.draw_networkx_edge_labels(DG, pos, edge_labels=edge_labels)

plt.show()
