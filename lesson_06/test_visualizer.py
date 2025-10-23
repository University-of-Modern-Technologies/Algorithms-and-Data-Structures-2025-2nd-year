"""Тестовий скрипт для перевірки візуалізації без input()"""
from bubble import bubble_sort_steps
from insertion import insertion_sort_steps
from selection import selection_sort_steps
from visualizer import StepVisualizer


def test_bubble():
    data = [5, 3, 8, 4, 2]
    steps = bubble_sort_steps(data)
    print(f"Bubble Sort: {len(steps)} steps")
    visualizer = StepVisualizer(steps, "Bubble Sort")
    visualizer.show()


def test_insertion():
    data = [5, 3, 8, 4, 2]
    steps = insertion_sort_steps(data)
    print(f"Insertion Sort: {len(steps)} steps")
    visualizer = StepVisualizer(steps, "Insertion Sort")
    visualizer.show()


def test_selection():
    data = [5, 3, 8, 4, 2]
    steps = selection_sort_steps(data)
    print(f"Selection Sort: {len(steps)} steps")
    visualizer = StepVisualizer(steps, "Selection Sort")
    visualizer.show()


if __name__ == '__main__':
    print("Тестування Bubble Sort...")
    test_bubble()
    # Розкоментуйте для тестування інших:
    # test_insertion()
    # test_selection()

