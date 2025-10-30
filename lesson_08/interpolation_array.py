import matplotlib.pyplot as plt
import numpy as np


def show_piecewise_interpolation():
    # Набір точок (відсортований масив)
    x_points = [1, 2, 4, 7, 8, 10]
    y_points = [2, 5, 4, 7, 9, 8]

    plt.figure(figsize=(12, 8))

    # Малюємо основні точки
    plt.scatter(x_points, y_points, c="red", s=100, label="Точки масиву")

    # Малюємо ламану лінію інтерполяції
    plt.plot(x_points, y_points, "b-", label="Ламана інтерполяції")

    # Додаємо кілька прикладів інтерпольованих точок
    x_interp = [1.5, 3, 7.5]  # приклади точок для інтерполяції

    for x in x_interp:
        # Знаходимо відрізок для інтерполяції
        for i in range(len(x_points) - 1):
            if x_points[i] <= x <= x_points[i + 1]:
                # Лінійна інтерполяція на цьому відрізку
                x1, x2 = x_points[i], x_points[i + 1]
                y1, y2 = y_points[i], y_points[i + 1]
                y = y1 + (x - x1) * (y2 - y1) / (x2 - x1)

                # Малюємо точку
                plt.scatter([x], [y], c="green", s=100)
                plt.vlines([x], 0, y, "g", linestyles="--")
                plt.annotate(
                    f"x={x}, y={y:.1f}",
                    (x, y),
                    xytext=(5, 5),
                    textcoords="offset points",
                )
                break

    # Додаємо пояснення
    explanation = (
        "Принцип кускової лінійної інтерполяції:\n"
        + "1. Масив точок розбиває область на відрізки\n"
        + "2. На кожному відрізку [x₁,x₂] застосовуємо\n"
        + "   формулу лінійної інтерполяції:\n"
        + "   y = y₁ + (x-x₁)·(y₂-y₁)/(x₂-x₁)\n"
        + "3. Всі відрізки разом утворюють ламану"
    )

    plt.text(
        0.02,
        0.98,
        explanation,
        transform=plt.gca().transAxes,
        fontsize=10,
        bbox=dict(facecolor="white", alpha=0.8),
        verticalalignment="top",
    )

    plt.title("Кускова лінійна інтерполяція на масиві точок")
    plt.xlabel("X координата")
    plt.ylabel("Y значення")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    show_piecewise_interpolation()
