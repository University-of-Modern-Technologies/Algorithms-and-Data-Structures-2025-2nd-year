# Випадкова розкладка (Random Layout)
import networkx as nx
import matplotlib.pyplot as plt

G = nx.complete_graph(8)

# 1. Розраховуємо позиції вузлів
# Вузли розміщуються у випадкових точках
pos = nx.random_layout(G)

# 2. Малюємо граф
nx.draw(G, pos, with_labels=True, node_color="lightgreen", node_size=1000)
plt.title("Random Layout")
plt.show()
