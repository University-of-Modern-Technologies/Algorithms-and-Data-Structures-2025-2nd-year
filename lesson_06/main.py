from bubble import bubble_sort_steps
from insertion import insertion_sort_steps
from selection import selection_sort_steps
from visualizer import StepVisualizer


def main():
    # Тестовий масив
    data = [5, 3, 8, 4, 2, 7, 1, 6]
    
    print("Виберіть алгоритм сортування:")
    print("1 - Bubble Sort")
    print("2 - Insertion Sort")
    print("3 - Selection Sort")
    
    choice = input("Ваш вибір (1-3): ").strip()
    
    if choice == '1':
        steps = bubble_sort_steps(data)
        algorithm_name = "Bubble Sort"
    elif choice == '2':
        steps = insertion_sort_steps(data)
        algorithm_name = "Insertion Sort"
    elif choice == '3':
        steps = selection_sort_steps(data)
        algorithm_name = "Selection Sort"
    else:
        print("Невірний вибір!")
        return
    
    print(f"\nПочатковий масив: {data}")
    print(f"Кількість кроків: {len(steps) - 1}")
    print(f"\nЗапуск візуалізації {algorithm_name}...")
    
    # Створення та запуск візуалізації
    visualizer = StepVisualizer(steps, algorithm_name)
    visualizer.show()


if __name__ == '__main__':
    main()

