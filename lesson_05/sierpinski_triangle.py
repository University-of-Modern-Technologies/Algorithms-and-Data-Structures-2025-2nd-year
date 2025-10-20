import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

def sierpinski_recursive(ax, vertices, depth, color='blue'):
    """
    Рекурсивно малює трикутник Серпиньского, поділяючи трикутник на менші.

    Args:
        ax: Вісь matplotlib для малювання
        vertices (list): Список вершин трикутника [[x1,y1], [x2,y2], [x3,y3]]
        depth (int): Глибина рекурсії
        color (str): Колір для малювання
    """
    if depth == 0:
        # Малюємо базовий трикутник
        triangle = patches.Polygon(vertices, closed=True, edgecolor=color, facecolor=color, alpha=0.8)
        ax.add_patch(triangle)
        return

    # Знаходимо середини сторін
    mid1 = [(vertices[0][0] + vertices[1][0]) / 2, (vertices[0][1] + vertices[1][1]) / 2]
    mid2 = [(vertices[1][0] + vertices[2][0]) / 2, (vertices[1][1] + vertices[2][1]) / 2]
    mid3 = [(vertices[2][0] + vertices[0][0]) / 2, (vertices[2][1] + vertices[0][1]) / 2]

    # Рекурсивно малюємо три менші трикутники (без центрального)
    sierpinski_recursive(ax, [vertices[0], mid1, mid3], depth - 1, color)
    sierpinski_recursive(ax, [vertices[1], mid1, mid2], depth - 1, color)
    sierpinski_recursive(ax, [vertices[2], mid2, mid3], depth - 1, color)

def sierpinski_probabilistic(vertices, num_points=10000, color='red'):
    """
    Генерує трикутник Серпиньского за допомогою ймовірнісного методу (chaos game).

    Args:
        vertices (list): Список вершин трикутника [[x1,y1], [x2,y2], [x3,y3]]
        num_points (int): Кількість точок для генерації
        color (str): Колір точок

    Returns:
        list: Список згенерованих точок [[x1,y1], [x2,y2], ...]
    """
    # Починаємо з випадкової точки
    current_point = [random.uniform(0, 1), random.uniform(0, 1)]

    points = [current_point.copy()]

    for _ in range(num_points - 1):
        # Випадково обираємо вершину
        vertex = random.choice(vertices)

        # Рухаємося на половину відстані до вершини
        current_point[0] = (current_point[0] + vertex[0]) / 2
        current_point[1] = (current_point[1] + vertex[1]) / 2

        points.append(current_point.copy())

    return points

def plot_sierpinski_recursive(depth=6, size=10):
    """
    Відображає трикутник Серпиньского, намальований рекурсивним методом.

    Args:
        depth (int): Глибина рекурсії
        size (float): Розмір трикутника
    """
    # Створюємо базовий трикутник
    height = size * np.sqrt(3) / 2
    vertices = [
        [0, 0],           # Нижня ліва
        [size, 0],        # Нижня права
        [size/2, height]  # Верхня
    ]

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_aspect('equal')
    ax.set_xlim(-1, size + 1)
    ax.set_ylim(-1, height + 1)

    # Малюємо рекурсивний трикутник Серпиньского
    sierpinski_recursive(ax, vertices, depth, 'navy')

    plt.title(f'Трикутник Серпиньского (рекурсивний метод, глибина {depth})',
              fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('sierpinski_recursive.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_sierpinski_probabilistic(num_points=50000, size=10):
    """
    Відображає трикутник Серпиньского, згенерований ймовірнісним методом.

    Args:
        num_points (int): Кількість точок для генерації
        size (float): Розмір трикутника
    """
    # Створюємо базовий трикутник
    height = size * np.sqrt(3) / 2
    vertices = [
        [0, 0],           # Нижня ліва
        [size, 0],        # Нижня права
        [size/2, height]  # Верхня
    ]

    # Генеруємо точки
    points = sierpinski_probabilistic(vertices, num_points)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_aspect('equal')
    ax.set_xlim(-1, size + 1)
    ax.set_ylim(-1, height + 1)

    # Розділяємо координати для малювання
    x_coords, y_coords = zip(*points)

    # Малюємо точки
    ax.scatter(x_coords, y_coords, s=0.1, c='crimson', alpha=0.6)

    # Малюємо базовий трикутник для референсу
    triangle = patches.Polygon(vertices, closed=True, edgecolor='black',
                              facecolor='none', linewidth=2, linestyle='--')
    ax.add_patch(triangle)

    plt.title(f'Трикутник Серпиньского (ймовірнісний метод, {num_points} точок)',
              fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('sierpinski_probabilistic.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_comparison(depth=5, num_points=30000, size=10):
    """
    Порівнює обидва методи на одному графіку.

    Args:
        depth (int): Глибина для рекурсивного методу
        num_points (int): Кількість точок для ймовірнісного методу
        size (float): Розмір трикутника
    """
    height = size * np.sqrt(3) / 2
    vertices = [
        [0, 0],
        [size, 0],
        [size/2, height]
    ]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Рекурсивний метод
    ax1.set_aspect('equal')
    ax1.set_xlim(-1, size + 1)
    ax1.set_ylim(-1, height + 1)
    sierpinski_recursive(ax1, vertices, depth, 'navy')
    ax1.set_title(f'Рекурсивний метод (глибина {depth})', fontsize=14, fontweight='bold')
    ax1.axis('off')

    # Ймовірнісний метод
    points = sierpinski_probabilistic(vertices, num_points)
    x_coords, y_coords = zip(*points)

    ax2.set_aspect('equal')
    ax2.set_xlim(-1, size + 1)
    ax2.set_ylim(-1, height + 1)
    ax2.scatter(x_coords, y_coords, s=0.05, c='crimson', alpha=0.8)
    triangle = patches.Polygon(vertices, closed=True, edgecolor='black',
                              facecolor='none', linewidth=2, linestyle='--')
    ax2.add_patch(triangle)
    ax2.set_title(f'Ймовірнісний метод ({num_points} точок)', fontsize=14, fontweight='bold')
    ax2.axis('off')

    plt.suptitle('Порівняння методів генерації трикутника Серпиньского',
                 fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.savefig('sierpinski_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """
    Головна функція для демонстрації трикутника Серпиньского.
    """
    print("Генерація трикутника Серпиньского...")

    # Демонструємо рекурсивний метод
    print("Рекурсивний метод...")
    plot_sierpinski_recursive(depth=7)

    # Демонструємо ймовірнісний метод
    print("Ймовірнісний метод...")
    plot_sierpinski_probabilistic(num_points=80000)

    # Порівняння
    print("Порівняння методів...")
    plot_comparison()

    print("Зображення збережено як 'sierpinski_recursive.png', 'sierpinski_probabilistic.png' та 'sierpinski_comparison.png'")

if __name__ == "__main__":
    main()
