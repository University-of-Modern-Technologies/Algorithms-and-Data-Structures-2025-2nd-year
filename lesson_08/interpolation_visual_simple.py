import matplotlib.pyplot as plt


def show_interpolation_principle():
    # Базові точки
    x1, y1 = 1, 10  # точка A
    x2, y2 = 5, 50  # точка B
    x_target = 3  # шукана точка X

    # Формула лінійної інтерполяції:
    # y = y1 + (x - x1) * (y2 - y1)/(x2 - x1)
    y_target = y1 + (x_target - x1) * (y2 - y1) / (x2 - x1)

    # Візуалізація
    plt.figure(figsize=(12, 8))

    # Малюємо основну лінію інтерполяції
    plt.plot([x1, x2], [y1, y2], "b-", label="Лінія інтерполяції")

    # Точки A і B
    plt.scatter([x1, x2], [y1, y2], c="red", s=100, label="Відомі точки (A, B)")

    # Шукана точка X
    plt.scatter(
        [x_target], [y_target], c="green", s=100, label="Інтерпольована точка (X)"
    )

    # Допоміжні лінії
    plt.vlines([x_target], 0, y_target, "g", linestyles="--")
    plt.hlines([y_target], 0, x_target, "g", linestyles="--")

    # Підписи точок
    plt.annotate(
        f"A({x1},{y1})", (x1, y1), xytext=(-10, 10), textcoords="offset points"
    )
    plt.annotate(
        f"B({x2},{y2})", (x2, y2), xytext=(-10, 10), textcoords="offset points"
    )
    plt.annotate(
        f"X({x_target},{y_target:.1f})",
        (x_target, y_target),
        xytext=(-10, 10),
        textcoords="offset points",
    )

    # Додаємо формулу як текст
    formula = r"$y = y_1 + (x - x_1)\cdot\frac{y_2 - y_1}{x_2 - x_1}$"
    plt.text(
        0.05,
        0.95,
        "Формула інтерполяції:\n" + formula,
        transform=plt.gca().transAxes,
        fontsize=12,
        bbox=dict(facecolor="white", alpha=0.8),
    )

    # Пояснення принципу
    explanation = (
        "Принцип:\n"
        + "1. Беремо дві відомі точки A і B\n"
        + "2. Проводимо пряму між ними\n"
        + "3. Для будь-якої точки x між A і B\n"
        + "   знаходимо y за формулою\n"
        + "4. Це і є інтерпольоване значення"
    )
    plt.text(
        0.05,
        0.75,
        explanation,
        transform=plt.gca().transAxes,
        fontsize=10,
        bbox=dict(facecolor="white", alpha=0.8),
    )

    plt.title("Принцип лінійної інтерполяції")
    plt.xlabel("X координата")
    plt.ylabel("Y значення")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    show_interpolation_principle()
