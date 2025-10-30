import matplotlib.pyplot as plt
import numpy as np


def visualize_array_interpolation(arr):
    """Visualize array points and the linear interpolation line
    between the first and last points (as used in interpolation search).
    X-axis: indices, Y-axis: values.
    """

    if not arr:
        raise ValueError("Array must be non-empty")

    plt.figure(figsize=(12, 8))

    # Scatter original points (index -> value)
    indices = list(range(len(arr)))
    plt.scatter(indices, arr, color="blue", s=100, label="Array points (i, arr[i])")

    # Annotate points
    for i, val in enumerate(arr):
        plt.annotate(
            f"({i}, {val})", (i, val), xytext=(5, 5), textcoords="offset points"
        )

    # Interpolation line ONLY between first and last points
    x1, y1 = 0, arr[0]
    x2, y2 = len(arr) - 1, arr[-1]

    # Guard against division by zero if x2 == x1 (only 1 element)
    if x2 > x1:
        x_line = np.linspace(x1, x2, 200)
        y_line = y1 + (x_line - x1) * (y2 - y1) / (x2 - x1)
        plt.plot(x_line, y_line, "r-", label="Linear interpolation: first ↔ last")
    else:
        # Single element: just mark the point
        plt.scatter([x1], [y1], color="red", s=120, label="Single point")

    plt.grid(True)
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.title("Array with interpolation between first and last points")
    plt.legend()

    plt.show()


if __name__ == "__main__":
    arr = [2, 3, 4, 10, 40, 50, 60, 70, 80, 90, 100]
    visualize_array_interpolation(arr)

