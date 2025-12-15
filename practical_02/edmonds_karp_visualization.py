"""
Візуалізація алгоритму Едмондса-Карпа - максимально просто
"""

import matplotlib.pyplot as plt
import networkx as nx
from collections import deque, defaultdict
from matplotlib.widgets import Button
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


class EdmondsKarp:
    def __init__(self):
        self.graph = defaultdict(dict)
        self.original = {}
        self.steps = []
        self.flow = defaultdict(lambda: defaultdict(int))  # Фактичний потік

    def add_edge(self, u, v, cap):
        self.graph[u][v] = cap
        self.original[(u, v)] = cap
        if v not in self.graph:
            self.graph[v] = {}

    def bfs(self, src, sink, parent):
        """BFS - пошук найкоротшого шляху"""
        visited = {src}
        queue = deque([src])

        while queue:
            u = queue.popleft()
            for v in self.graph[u]:
                if v not in visited and self.graph[u][v] > 0:
                    visited.add(v)
                    queue.append(v)
                    parent[v] = u
                    if v == sink:
                        return True
        return False

    def run(self, src, sink):
        parent = {}
        max_flow = 0
        iteration = 0

        # Початковий стан
        self.steps.append(
            {
                "iter": 0,
                "title": "ПОЧАТКОВИЙ СТАН",
                "desc": "Всі ребра мають початкові пропускні здатності.\n"
                "Мітки на ребрах: використано/загальна пропускна здатність.\n\n"
                "S (зелена) = джерело (source) - звідки йде потік\n"
                "T (рожева) = стік (sink) - куди йде потік\n\n"
                "Зараз всі ребра показують 0/X (нічого не використано).\n"
                "Знайдемо шлях від S до T і пропустимо через нього потік.",
                "path": [],
                "min_cap": 0,
                "total": 0,
                "flow": {k: dict(v) for k, v in self.flow.items()},
            }
        )

        while self.bfs(src, sink, parent):
            iteration += 1

            # Шлях та мінімальна пропускна здатність
            path = []
            min_cap = float("inf")
            v = sink
            while v != src:
                u = parent[v]
                path.append((u, v))
                min_cap = min(min_cap, self.graph[u][v])
                v = u
            path.reverse()

            # Оновлюємо граф і потік
            v = sink
            while v != src:
                u = parent[v]

                # Перевіряємо чи це оригінальне ребро чи зворотне
                if (u, v) in self.original:
                    # Оригінальне ребро - збільшуємо потік
                    self.flow[u][v] += min_cap
                else:
                    # Зворотне ребро - зменшуємо потік на оригінальному
                    self.flow[v][u] -= min_cap

                # Оновлюємо залишковий граф
                self.graph[u][v] -= min_cap
                if u not in self.graph[v]:
                    self.graph[v][u] = 0
                self.graph[v][u] += min_cap
                v = u

            max_flow += min_cap

            # Пояснення для зворотніх ребер
            has_reverse = any((u, v) not in self.original for (u, v) in path)
            reverse_note = ""
            if has_reverse:
                reverse_note = "\n[!] Цей шлях використовує зворотне ребро!\n(Алгоритм 'відміняє' частину попереднього потоку)"

            # Детальний опис змін на ребрах
            changes_desc = "\n\n─── Зміни на ребрах ───\n"
            for u, v in path:
                if (u, v) in self.original:
                    prev = (
                        self.steps[-1]["flow"].get(u, {}).get(v, 0)
                        if len(self.steps) > 0
                        else 0
                    )
                    new = self.flow[u][v]
                    changes_desc += f"{u} → {v}: {prev} → {new} (+{min_cap})\n"

            self.steps.append(
                {
                    "iter": iteration,
                    "title": f"ІТЕРАЦІЯ {iteration}",
                    "desc": f'Знайдено шлях (ЧЕРВОНІ стрілки): {" → ".join(str(e[0]) for e in path)} → {path[-1][1]}\n\n'
                    f"Мінімальна пропускна здатність на шляху: {min_cap}\n"
                    f"(найменше значення серед ребер на шляху)\n\n"
                    f"Додаємо потік +{min_cap} до кожного ребра шляху.\n"
                    f"Червоні мітки показують (+приріст).{reverse_note}"
                    f"{changes_desc}\n"
                    f"Загальний акумульований потік: {max_flow}",
                    "path": path,
                    "min_cap": min_cap,
                    "total": max_flow,
                    "flow": {k: dict(v) for k, v in self.flow.items()},
                }
            )
            parent = {}

        # Підраховуємо скільки ребер використано
        used_edges = sum(1 for (u, v) in self.original.keys() if self.flow[u][v] > 0)
        total_edges = len(self.original)

        edge_note = ""
        if used_edges == total_edges:
            edge_note = f"\n\n[!] В цьому графі ВСІ {total_edges} ребра використовуються!\nТому всі стрілки зелені - це нормально."
        else:
            edge_note = f"\n\n{used_edges} з {total_edges} ребер використовуються (зелені).\nСірі ребра не беруть участі в потоці."

        # Фінальний стан
        self.steps.append(
            {
                "iter": len(self.steps),
                "title": "РЕЗУЛЬТАТ",
                "desc": f"Більше немає шляхів від S до T.\n"
                f"Алгоритм завершено.\n\n"
                f"═══ МАКСИМАЛЬНИЙ ПОТІК = {max_flow} ═══\n\n"
                f"ЗЕЛЕНІ СТРІЛКИ = ребра через які йде потік (> 0)\n"
                f"Товщина стрілки пропорційна потоку\n"
                f"СІРІ стрілки = ребра без потоку{edge_note}\n\n"
                f"Потік виходить з джерела S = {max_flow}\n"
                f"Потік входить в стік T = {max_flow}",
                "path": [],
                "min_cap": 0,
                "total": max_flow,
                "flow": {k: dict(v) for k, v in self.flow.items()},
            }
        )

        return max_flow

    def visualize_interactive(self):
        """Інтерактивна візуалізація з кнопками"""
        self.current_step = 0

        self.fig = plt.figure(figsize=(16, 12))
        self.fig.canvas.manager.set_window_title("Алгоритм Едмондса-Карпа")

        # Кнопки ВГОРІ (прямо під заголовком вікна)
        ax_prev = plt.axes([0.35, 0.95, 0.12, 0.035])
        ax_next = plt.axes([0.53, 0.95, 0.12, 0.035])

        self.btn_prev = Button(ax_prev, "← Назад")
        self.btn_next = Button(ax_next, "Далі →")

        self.btn_prev.on_clicked(self.prev_step)
        self.btn_next.on_clicked(self.next_step)

        # Граф займає верхню частину (трохи нижче кнопок)
        self.ax_graph = plt.subplot2grid((6, 3), (0, 0), rowspan=3, colspan=3)

        # Пояснення займає частину знизу
        self.ax_text = plt.subplot2grid((6, 3), (3, 0), rowspan=3, colspan=3)
        self.ax_text.axis("off")

        self.update_plot()
        plt.show()

    def update_plot(self):
        """Оновлює графік для поточного кроку"""
        step = self.steps[self.current_step]

        self.ax_graph.clear()
        self.ax_text.clear()
        self.ax_text.axis("off")

        # Створюємо граф
        G = nx.DiGraph()
        all_nodes = set()
        for u, v in self.original.keys():
            all_nodes.add(u)
            all_nodes.add(v)
        G.add_nodes_from(all_nodes)

        # Позиції вершин
        if len(all_nodes) == 4:
            pos = {"S": (0, 1), "A": (1, 1.5), "B": (1, 0.5), "T": (2, 1)}
        else:
            pos = nx.spring_layout(G, k=3, iterations=100, seed=42)

        # Малюємо вершини
        node_colors = []
        for node in G.nodes():
            if node == "S":
                node_colors.append("#90EE90")
            elif node == "T":
                node_colors.append("#FFB6C6")
            else:
                node_colors.append("#87CEEB")

        nx.draw_networkx_nodes(
            G, pos, node_color=node_colors, node_size=1500, ax=self.ax_graph
        )
        nx.draw_networkx_labels(
            G, pos, font_size=16, font_weight="bold", ax=self.ax_graph
        )

        # Малюємо ребра
        is_final_step = step["title"] == "РЕЗУЛЬТАТ"

        for (u, v), orig_cap in self.original.items():
            # Використовуємо flow замість різниці graph
            flow_value = step["flow"].get(u, {}).get(v, 0)

            is_in_path = (u, v) in step["path"]

            # Отримуємо попередній потік для показу приросту
            if step["iter"] > 0 and not is_final_step:
                prev_flow = self.steps[step["iter"] - 1]["flow"].get(u, {}).get(v, 0)
                flow_delta = flow_value - prev_flow
            else:
                flow_delta = 0

            # На фінальному кроці виділяємо всі ребра з потоком
            if is_final_step and flow_value > 0:
                # Товщина пропорційна потоку
                width = 2 + (flow_value / orig_cap) * 4
                color = "#00AA00"  # зелений для ребер з потоком
            elif is_in_path:
                color = "#FF0000"
                width = 4
            else:
                # Сірий якщо немає потоку, темніший якщо є
                if flow_value > 0:
                    color = "#555555"
                else:
                    color = "#AAAAAA"
                width = 2

            self.ax_graph.annotate(
                "",
                xy=pos[v],
                xycoords="data",
                xytext=pos[u],
                textcoords="data",
                arrowprops=dict(
                    arrowstyle="-|>",
                    color=color,
                    lw=width,
                    connectionstyle="arc3,rad=0.15",
                    shrinkA=20,
                    shrinkB=20,
                ),
            )

            mid_x = (pos[u][0] + pos[v][0]) / 2
            mid_y = (pos[u][1] + pos[v][1]) / 2

            # Показуємо приріст якщо є
            if is_in_path and flow_delta > 0:
                label = f"{flow_value}/{orig_cap}\n(+{flow_delta})"
            else:
                label = f"{flow_value}/{orig_cap}"

            # На фінальному кроці виділяємо ребра з потоком
            if is_final_step and flow_value > 0:
                bbox_color = "#90EE90"  # світло-зелений
                edge_color = "#00AA00"
            elif is_in_path:
                bbox_color = "yellow"
                edge_color = color
            else:
                if flow_value > 0:
                    bbox_color = "#E8E8E8"
                else:
                    bbox_color = "white"
                edge_color = color

            bbox_props = dict(
                boxstyle="round,pad=0.3",
                facecolor=bbox_color,
                edgecolor=edge_color,
                lw=2 if (is_in_path or (is_final_step and flow_value > 0)) else 1,
            )

            self.ax_graph.text(
                mid_x,
                mid_y,
                label,
                fontsize=10,
                fontweight="bold",
                ha="center",
                va="center",
                bbox=bbox_props,
            )

        title = f"{step['title']} (Крок {self.current_step}/{len(self.steps)-1})"
        self.ax_graph.set_title(title, fontsize=18, fontweight="bold", pad=20)
        self.ax_graph.axis("off")
        self.ax_graph.set_xlim(-0.3, 2.3)
        self.ax_graph.set_ylim(0, 2)

        # Додаємо легенду
        is_final_step = step["title"] == "РЕЗУЛЬТАТ"

        if is_final_step:
            legend_elements = [
                Patch(facecolor="#90EE90", label="S = Джерело"),
                Patch(facecolor="#FFB6C6", label="T = Стік"),
                Patch(facecolor="#87CEEB", label="Проміжні"),
                Line2D(
                    [0],
                    [0],
                    color="#00AA00",
                    linewidth=4,
                    label="Ребра з потоком > 0",
                ),
                Line2D(
                    [0], [0], color="#AAAAAA", linewidth=2, label="Ребра без потоку"
                ),
            ]
        else:
            legend_elements = [
                Patch(facecolor="#90EE90", label="S = Джерело"),
                Patch(facecolor="#FFB6C6", label="T = Стік"),
                Patch(facecolor="#87CEEB", label="Проміжні"),
                Line2D(
                    [0],
                    [0],
                    color="#FF0000",
                    linewidth=3,
                    label="Поточний шлях (+приріст)",
                ),
                Line2D([0], [0], color="#555555", linewidth=2, label="Ребра з потоком"),
                Line2D(
                    [0], [0], color="#AAAAAA", linewidth=2, label="Ребра без потоку"
                ),
            ]

        self.ax_graph.legend(
            handles=legend_elements, loc="upper left", fontsize=9, framealpha=0.9
        )

        # Підраховуємо потік з джерела для показу
        if step["total"] > 0:
            total_flow_from_s = 0
            for (u, v), orig_cap in self.original.items():
                if u == "S":
                    flow_value = step["flow"].get(u, {}).get(v, 0)
                    total_flow_from_s += flow_value

            # Показуємо загальний потік біля джерела
            self.ax_graph.text(
                -0.25,
                0.85,
                f"Потік з S:\n{total_flow_from_s}",
                fontsize=12,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgreen", alpha=0.8),
                ha="center",
            )

            # Показуємо загальний потік біля стоку
            total_flow_to_t = 0
            for (u, v), orig_cap in self.original.items():
                if v == "T":
                    flow_value = step["flow"].get(u, {}).get(v, 0)
                    total_flow_to_t += flow_value

            self.ax_graph.text(
                2.25,
                0.85,
                f"Потік в T:\n{total_flow_to_t}",
                fontsize=12,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.5", facecolor="#FFB6C6", alpha=0.8),
                ha="center",
            )

        # Пояснення
        desc_text = step["desc"]

        # Додаємо детальну інформацію про потік на фінальному кроці
        if is_final_step:
            desc_text += "\n\n─── Детальний розподіл потоку ───\n"
            for (u, v), orig_cap in self.original.items():
                flow_value = step["flow"].get(u, {}).get(v, 0)
                if flow_value > 0:
                    desc_text += f"{u} → {v}: потік {flow_value}\n"

        self.ax_text.text(
            0.5,
            0.5,
            desc_text,
            fontsize=11,
            ha="center",
            va="center",
            transform=self.ax_text.transAxes,
            bbox=dict(boxstyle="round,pad=1", facecolor="lightyellow", alpha=0.8),
        )

        # Оновлюємо стан кнопок
        self.btn_prev.ax.set_visible(self.current_step > 0)
        self.btn_next.ax.set_visible(self.current_step < len(self.steps) - 1)

        self.fig.canvas.draw()

    def next_step(self, event):
        """Наступний крок"""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.update_plot()

    def prev_step(self, event):
        """Попередній крок"""
        if self.current_step > 0:
            self.current_step -= 1
            self.update_plot()


def main():
    print("\n" + "=" * 70)
    print(" АЛГОРИТМ ЕДМОНДСА-КАРПА - ПОКРОКОВЕ ПОЯСНЕННЯ")
    print("=" * 70 + "\n")

    print("ПРИНЦИП РОБОТИ:")
    print("-" * 70)
    print("1. Шукаємо будь-який шлях від джерела S до стоку T (через BFS)")
    print("2. Знаходимо мінімальну пропускну здатність на цьому шляху")
    print("3. Пропускаємо максимальний можливий потік через цей шлях")
    print("4. Оновлюємо залишкові пропускні здатності")
    print("5. Повторюємо поки є шляхи від S до T")
    print("-" * 70)

    print("\nПРОСТИЙ ПРИКЛАД:")
    print("-" * 70)

    ek = EdmondsKarp()

    # Дуже простий граф: 4 вершини
    # S -> A -> T
    # S -> B -> T
    # A -> B (допоміжне ребро)

    ek.add_edge("S", "A", 10)
    ek.add_edge("S", "B", 8)
    ek.add_edge("A", "B", 3)
    ek.add_edge("A", "T", 5)
    ek.add_edge("B", "T", 10)

    print("Граф:")
    print("  S → A: пропускна здатність 10")
    print("  S → B: пропускна здатність 8")
    print("  A → B: пропускна здатність 3")
    print("  A → T: пропускна здатність 5")
    print("  B → T: пропускна здатність 10")
    print()

    max_flow = ek.run("S", "T")

    print("-" * 70)
    print(f"МАКСИМАЛЬНИЙ ПОТІК: {max_flow}")
    print("-" * 70)
    print(f"\nКількість ітерацій: {len(ek.steps) - 2}")  # без початку та кінця
    print()

    print("ПОКАЗУЮ ІНТЕРАКТИВНУ ВІЗУАЛІЗАЦІЮ...")
    print("(Використовуй кнопки 'Назад' і 'Далі' для навігації)")
    print("-" * 70)

    ek.visualize_interactive()

    print("-" * 70)
    print("\nГОТОВО!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
