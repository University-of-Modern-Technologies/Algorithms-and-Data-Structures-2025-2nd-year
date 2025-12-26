from itertools import permutations
from math import sqrt

# Визначити координати для 5 міст
cities = {"A": (0, 0), "B": (1, 5), "C": (2, 2), "D": (3, 3), "E": (5, 1)}


# Функція для обчислення відстані між двома містами
def distance(first_city_name, second_city_name):
    x1, y1 = cities[first_city_name]
    x2, y2 = cities[second_city_name]
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def total_distance_with_return(tour):
    # Загальна відстань, включаючи повернення до початкової точки
    return sum(distance(tour[i], tour[i + 1]) for i in range(len(tour) - 1)) + distance(
        tour[-1], tour[0]
    )


# Знайти найкоротший маршрут
all_tours = permutations(cities.keys())
# print(list(all_tours))
shortest_tour = min(all_tours, key=total_distance_with_return)
# Переобчислити відстань найкоротшого маршруту з урахуванням зворотного шляху
shortest_distance_with_return = total_distance_with_return(shortest_tour)

print(shortest_tour, shortest_distance_with_return)
