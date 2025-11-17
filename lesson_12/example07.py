# Камеральна розкладка (Shell Layout)
import networkx as nx
import matplotlib.pyplot as plt

G = nx.complete_graph(8)

# 1. Визначаємо "камери" (shells) - вкладені списки вузлів
shells = [[0, 1, 2], [3, 4], [5, 6, 7]]

# 2. Розраховуємо позиції
# Вузли [0,1,2] будуть на внутрішньому колі
# Вузли [3,4] - на середньому
# Вузли [5,6,7] - на зовнішньому
pos = nx.shell_layout(G, shells)

# 3. Малюємо граф
nx.draw(G, pos, with_labels=True, node_color="lightcoral", node_size=1000)
plt.title("Shell Layout")
plt.show()
