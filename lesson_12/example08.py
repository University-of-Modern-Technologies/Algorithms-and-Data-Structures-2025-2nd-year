# Силова розкладка (Spring Layout)
import networkx as nx
import matplotlib.pyplot as plt

print("--- Приклад 4.4: Силова розкладка (Spring Layout) ---")

G = nx.complete_graph(8)

# Це найпопулярніший layout. Він імітує фізику:
# ребра - це пружини, вузли - об'єкти, що відштовхуються.
# Він "знаходить" природне положення графа.
# використовується за замовчуванням
pos = nx.spring_layout(G)

# 2. Малюємо граф
nx.draw(G, pos, with_labels=True, node_color="gold", node_size=1000)
plt.title("Spring Layout (Default)")
plt.show()
