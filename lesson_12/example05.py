# Кругова розкладка (Circular Layout)
import networkx as nx
import matplotlib.pyplot as plt

# Створюємо повний граф з 8 вузлами
G = nx.complete_graph(8)

# 1. Розраховуємо позиції вузлів
# Вузли розміщуються по колу
pos = nx.circular_layout(G)

# 2. Малюємо граф, передаючи йому позиції
nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=1000)
plt.title("Circular Layout")
plt.show()
