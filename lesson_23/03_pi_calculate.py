import os
from concurrent.futures import ProcessPoolExecutor

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np

nums = 100_000


def estimate_pi(n):
    x = np.random.uniform(-1, 1, n)
    y = np.random.uniform(-1, 1, n)
    inside_circle = x**2 + y**2 <= 1
    pi_estimate = 4 * np.sum(inside_circle) / n
    return pi_estimate


def visualize_pi(n):
    x = np.random.uniform(-1, 1, n)
    y = np.random.uniform(-1, 1, n)
    inside_circle = x**2 + y**2 <= 1
    pi_estimate = 4 * np.sum(inside_circle) / n

    plt.figure(figsize=(8, 8))
    plt.scatter(
        x[inside_circle],
        y[inside_circle],
        color="blue",
        s=1,
        label=f"Всередині: {np.sum(inside_circle)}",
    )
    plt.scatter(
        x[~inside_circle],
        y[~inside_circle],
        color="red",
        s=1,
        label=f"Поза: {np.sum(~inside_circle)}",
    )

    # Draw circle
    circle = Circle(
        (0, 0), 1, color="green", fill=False, linewidth=2, label="Коло (r=1)"
    )
    plt.gca().add_patch(circle)

    # Draw square
    plt.plot([-1, 1, 1, -1, -1], [-1, -1, 1, 1, -1], "k-", linewidth=2, label="Квадрат")

    plt.xlim(-1.1, 1.1)
    plt.ylim(-1.1, 1.1)
    plt.axis("equal")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.title(f"Обчислення π методом Монте-Карло\nπ ≈ {pi_estimate:.6f} (n={n:,})")
    plt.show()
    return pi_estimate


def main():
    num_for_process = 100_000
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(estimate_pi, num_for_process) for _ in range(1000)]  # noqa
        pi_estimates = [future.result() for future in futures]
        pi = np.mean(pi_estimates)
        print(pi)


if __name__ == "__main__":
    # Візуалізація методу (одна симуляція)
    pi = visualize_pi(nums)
    print(pi)

    # Паралельні обчислення для точності
    print(os.cpu_count())
    main()
