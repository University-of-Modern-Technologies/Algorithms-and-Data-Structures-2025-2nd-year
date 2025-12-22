"""
Activity Selection Problem - задача планування активностей

ПОСТАНОВКА ЗАДАЧІ:

Дано: n активностей, кожна має час початку s[i] та закінчення f[i]
Мета: вибрати максимальну кількість непересічних активностей
Приклад: Активності: [(1,4), (3,5), (0,6), (5,7), (8,9), (5,9)]
Оптимальний вибір: (1,4), (5,7), (8,9) = 3 активності

ЖАДІБНА СТРАТЕГІЯ:
    Сортуємо активності за часом закінчення f[i]
    Завжди вибираємо активність що закінчується найраніше
    Пропускаємо всі що конфліктують з вибраною
"""


def activity_selection_greedy(activities):
    if not activities:
        return []

    # Сортуємо за часом закінчення
    sorted_activities = sorted(activities, key=lambda x: x[1])

    selected = [sorted_activities[0]]  # Завжди беремо першу
    last_finish_time = sorted_activities[0][1]

    # Жадібно вибираємо непересічні активності
    for i in range(1, len(sorted_activities)):
        start_time, finish_time = sorted_activities[i]

        if start_time >= last_finish_time:  # Немає конфлікту
            selected.append((start_time, finish_time))
            last_finish_time = finish_time

    return selected


# Демонстрація
activities = [(1, 4), (3, 5), (0, 6), (5, 7), (8, 9), (5, 9)]
result = activity_selection_greedy(activities)
print("Вибрані активності:", result)
