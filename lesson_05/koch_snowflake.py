import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def koch_snowflake_recursive(ax, start_point, end_point, depth, color='blue'):
    """
    Рекурсивно генерує криву Коха між двома точками.

    Args:
        ax: Вісь matplotlib для малювання
        start_point (tuple): Початкова точка (x, y)
        end_point (tuple): Кінцева точка (x, y)
        depth (int): Глибина рекурсії
        color (str): Колір лінії
    """
    if depth == 0:
        # Малюємо пряму лінію
        ax.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]],
                color=color, linewidth=1)
        return

    # Обчислюємо точки для кривої Коха
    dx = end_point[0] - start_point[0]
    dy = end_point[1] - start_point[1]

    # Точки поділу: ділимо лінію на 3 частини
    p1 = start_point
    p2 = (start_point[0] + dx/3, start_point[1] + dy/3)
    p4 = (start_point[0] + 2*dx/3, start_point[1] + 2*dy/3)
    
    # Обчислюємо вершину трикутника (p3)
    # Вершина знаходиться на відстані length/3 від p2, під кутом 60° до лінії
    angle = np.arctan2(dy, dx)  # Кут лінії
    
    # Обертаємо вектор від p2 до p4 на 60 градусів проти годинникової стрілки
    p3_x = p2[0] + (p4[0] - p2[0]) * np.cos(np.pi/3) - (p4[1] - p2[1]) * np.sin(np.pi/3)
    p3_y = p2[1] + (p4[0] - p2[0]) * np.sin(np.pi/3) + (p4[1] - p2[1]) * np.cos(np.pi/3)
    
    p3 = (p3_x, p3_y)

    # Рекурсивно генеруємо 4 сегменти
    koch_snowflake_recursive(ax, p1, p2, depth - 1, color)
    koch_snowflake_recursive(ax, p2, p3, depth - 1, color)
    koch_snowflake_recursive(ax, p3, p4, depth - 1, color)
    koch_snowflake_recursive(ax, p4, end_point, depth - 1, color)

def generate_koch_snowflake_vertices(size=10, depth=4):
    """
    Генерує вершини для сніжинки Коха на основі рівностороннього трикутника.

    Args:
        size (float): Розмір сніжинки
        depth (int): Глибина рекурсії

    Returns:
        list: Список сегментів для малювання [(start, end), ...]
    """
    # Створюємо початковий рівносторонній трикутник
    height = size * np.sqrt(3) / 2

    vertices = [
        (0, 0),                    # Нижня ліва
        (size, 0),                 # Нижня права
        (size/2, height),          # Верхня
        (0, 0)                     # Повертаємося до початку
    ]

    segments = []

    # Генеруємо криву Коха для кожної сторони
    for i in range(3):  # Три сторони трикутника
        start = vertices[i]
        end = vertices[i+1]

        # Рекурсивно генеруємо точки для цієї сторони
        side_segments = []

        def collect_segments(s, e, d):
            if d == 0:
                side_segments.append((s, e))
                return

            dx = e[0] - s[0]
            dy = e[1] - s[1]

            p1 = s
            p2 = (s[0] + dx/3, s[1] + dy/3)
            p4 = (s[0] + 2*dx/3, s[1] + 2*dy/3)

            # Обчислюємо вершину трикутника (обертаємо вектор p2->p4 на 60°)
            p3_x = p2[0] + (p4[0] - p2[0]) * np.cos(np.pi/3) - (p4[1] - p2[1]) * np.sin(np.pi/3)
            p3_y = p2[1] + (p4[0] - p2[0]) * np.sin(np.pi/3) + (p4[1] - p2[1]) * np.cos(np.pi/3)
            p3 = (p3_x, p3_y)

            collect_segments(p1, p2, d - 1)
            collect_segments(p2, p3, d - 1)
            collect_segments(p3, p4, d - 1)
            collect_segments(p4, e, d - 1)

        collect_segments(start, end, depth)
        segments.extend(side_segments)

    return segments

def plot_koch_snowflake_simple(depth=4, size=10):
    """
    Малює сніжинку Коха простим методом (крок за кроком).

    Args:
        depth (int): Глибина рекурсії
        size (float): Розмір сніжинки
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')

    # Центруємо сніжинку
    height = size * np.sqrt(3) / 2
    offset_x = -size/2
    offset_y = -height/2

    # Створюємо початковий трикутник
    vertices = [
        (offset_x, offset_y),
        (offset_x + size, offset_y),
        (offset_x + size/2, offset_y + height)
    ]

    # Малюємо криву Коха для кожної сторони
    for i in range(3):
        start = vertices[i]
        end = vertices[(i + 1) % 3]
        koch_snowflake_recursive(ax, start, end, depth, 'navy')

    plt.title(f'Сніжинка Коха (глибина {depth})', fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('koch_snowflake_simple.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_koch_snowflake_advanced(depth=5, size=8):
    """
    Малює сніжинку Коха з покращеною візуалізацією.

    Args:
        depth (int): Глибина рекурсії
        size (float): Розмір сніжинки
    """
    # Генеруємо вершини
    segments = generate_koch_snowflake_vertices(size, depth)

    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_aspect('equal')

    # Центруємо сніжинку
    height = size * np.sqrt(3) / 2
    offset_x = -size/2
    offset_y = -height/2

    # Малюємо всі сегменти
    for start, end in segments:
        # Компенсуємо зміщення
        start = (start[0] + offset_x, start[1] + offset_y)
        end = (end[0] + offset_x, end[1] + offset_y)

        ax.plot([start[0], end[0]], [start[1], end[1]],
                color='darkblue', linewidth=0.8, alpha=0.9)

    # Додаємо коло для краси
    circle = patches.Circle((0, 0), size/2, facecolor='none',
                           edgecolor='lightblue', linewidth=2, linestyle='--', alpha=0.3)
    ax.add_patch(circle)

    plt.title(f'Сніжинка Коха (глибина {depth})', fontsize=18, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('koch_snowflake_advanced.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_koch_evolution(depths=[0, 1, 2, 3, 4, 5], size=6):
    """
    Показує еволюцію сніжинки Коха з різними глибинами рекурсії.

    Args:
        depths (list): Список глибин для відображення
        size (float): Розмір сніжинки
    """
    n_plots = len(depths)
    cols = 3
    rows = (n_plots + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(15, 5*rows))
    if rows == 1:
        axes = axes.reshape(1, -1)
    elif n_plots == 1:
        axes = np.array([[axes]])

    for i, depth in enumerate(depths):
        row, col = i // cols, i % cols
        ax = axes[row, col]

        # Генеруємо сегменти для цієї глибини
        segments = generate_koch_snowflake_vertices(size, depth)

        # Центруємо
        height = size * np.sqrt(3) / 2
        offset_x = -size/2
        offset_y = -height/2

        # Малюємо
        for start, end in segments:
            start = (start[0] + offset_x, start[1] + offset_y)
            end = (end[0] + offset_x, end[1] + offset_y)

            ax.plot([start[0], end[0]], [start[1], end[1]],
                    color='navy', linewidth=1)

        ax.set_aspect('equal')
        ax.set_title(f'Глибина {depth}', fontsize=12, fontweight='bold')
        ax.axis('off')

    # Ховаємо порожні subplot'и
    for i in range(n_plots, rows * cols):
        row, col = i // cols, i % cols
        axes[row, col].set_visible(False)

    plt.suptitle('Еволюція сніжинки Коха', fontsize=20, fontweight='bold')
    plt.tight_layout()
    plt.savefig('koch_evolution.png', dpi=300, bbox_inches='tight')
    plt.show()

def calculate_koch_length(depth, initial_length=1):
    """
    Обчислює загальну довжину кривої Коха для заданої глибини.

    Args:
        depth (int): Глибина рекурсії
        initial_length (float): Початкова довжина сторони

    Returns:
        float: Загальна довжина кривої
    """
    if depth == 0:
        return initial_length

    # Кожна сторона поділяється на 4 сегменти, кожен 1/3 від початкової довжини
    # Але з кожним рівнем довжина множиться на 4/3
    return initial_length * (4/3) ** depth

def main():
    """
    Головна функція для демонстрації сніжинки Коха.
    """
    print("Генерація сніжинки Коха...")

    # Простий варіант
    print("Простий варіант...")
    plot_koch_snowflake_simple(depth=5)

    # Покращений варіант
    print("Покращений варіант...")
    plot_koch_snowflake_advanced(depth=6)

    # Еволюція
    print("Еволюція...")
    plot_koch_evolution()

    # Обчислюємо довжину для демонстрації
    print("Обчислення довжини...")
    for depth in range(6):
        length = calculate_koch_length(depth, 3)  # 3 сторони по 1 одиниці
        print(f"Глибина {depth}: довжина = {length:.2f}")

    print("Зображення збережено як 'koch_snowflake_simple.png', 'koch_snowflake_advanced.png' та 'koch_evolution.png'")

if __name__ == "__main__":
    main()
