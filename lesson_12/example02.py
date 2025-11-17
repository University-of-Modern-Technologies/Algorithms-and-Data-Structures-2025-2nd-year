# Атрибути та Орієнтовані Графи
import networkx as nx
import matplotlib.pyplot as plt

# Створення Орієнтованого графа
# Використовуємо DiGraph (Directed Graph)
# Тепер ребро A -> B не те саме, що B -> A
DG = nx.DiGraph()

# 2. Додавання вузлів з атрибутами
# Додамо перехрестя (вузли)
# Ми можемо додати атрибути (дані) прямо при створенні
DG.add_node("A", type="Roundabout")  # Перехрестя А - кільце
DG.add_node("B", type="Crossroads")  # Перехрестя B - звичайне
DG.add_node("C", type="Industrial")  # Виїзд у промислову зону
DG.add_node("D", type="Residential")  # В'їзд у житловий район
DG.add_node("E", type="Highway")  # В'їзд на трасу
DG.add_node("F", type="Mall")  # Торговий центр з парковкою

# Додавання ребер з атрибутами
# Моделюємо вулиці (ребра)
# Додаємо атрибути 'weight' (вага/час) та 'label' (назва)

# Вулиця з A до B (одностороння), час 5 хв
DG.add_edge("A", "B", weight=5, label="Main St")

# Вулиця з B до C (одностороння), час 3 хв
DG.add_edge("B", "C", weight=3, label="Oak Ave")

# Вулиця між C і D (двостороння)
# В DiGraph двосторонній рух моделюється ДВОМА окремими ребрами
DG.add_edge("C", "D", weight=2, label="Side Rd")
DG.add_edge("D", "C", weight=2, label="Side Rd")

# Трасу з A до Е (виїзд на кільцеву дорогу)
DG.add_edge("A", "E", weight=4, label="Ring Rd")
# В'їзд з траси до торгового центру
DG.add_edge("E", "F", weight=6, label="Mall Expwy")
# З торгового центру можна повернутися в житловий район
DG.add_edge("F", "D", weight=5, label="Market Blvd")
# Додамо дорогу з житлового району до перехрестя B
DG.add_edge("D", "B", weight=7, label="Elm St")

# --- 4. Доступ до атрибутів ---
print("\n--- Доступ до атрибутів ---")

# Отримуємо атрибут вузла "A"
print(f"Тип вузла 'A': {DG.nodes['A']['type']}")

# Отримуємо атрибути ребра "A" -> "B"
print(f"Вулиця A->B: {DG.edges['A', 'B']['label']}")
print(f"Час у дорозі A->B: {DG['A']['B']['weight']} хв")


# Перевіряємо різницю: чи є шлях з B до A?
print(f"Чи існує ребро B -> A? {'Так' if DG.has_edge('B', 'A') else 'Ні'}")
print(f"Чи існує ребро A -> B? {'Так' if DG.has_edge('A', 'B') else 'Ні'}")

# --- 5. Візуалізація DiGraph ---
print("\nМалюємо орієнтований граф...")
# Для DiGraph важливо показати стрілки

# Використовуємо spring_layout для кращого розташування
pos = nx.spring_layout(DG, seed=42)

nx.draw(
    DG,
    pos,
    with_labels=True,
    node_color="lightgreen",
    node_size=1500,
    font_weight="bold",
    width=2,
    arrowsize=10,  # Розмір стрілок
)

# Додамо мітки ребер (назви вулиць)
edge_labels = nx.get_edge_attributes(DG, "weight")
nx.draw_networkx_edge_labels(DG, pos, edge_labels=edge_labels)

plt.show()
