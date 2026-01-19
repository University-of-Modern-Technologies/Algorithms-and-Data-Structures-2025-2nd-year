import numpy as np
import matplotlib.pyplot as plt

"""
КРОК 1: Базовий PageRank

Ідея: важливість сайту = сума важливостей сайтів що на нього посилаються
"""

# Граф: 3 сайти в інтернеті
labels = ["Wikipedia", "GitHub", "Medium"]

# Хто на кого посилається:
# Wikipedia → GitHub, Medium
# GitHub → Medium
# Medium → Wikipedia

print("=" * 60)
print("БАЗОВИЙ PAGERANK - ОЦІНКА ВАЖЛИВОСТІ САЙТІВ")
print("=" * 60)
print("Граф посилань між сайтами:")
print("  Wikipedia → GitHub, Medium")
print("  GitHub    → Medium")
print("  Medium    → Wikipedia")
print()
print("Питання: який сайт найважливіший?")
print()

# Матриця переходів
# Рядок i = з якого сайту, стовпець j = на який сайт
# P[i,j] = ймовірність переходу з i на j

P = np.array(
    [
        [0, 0.5, 0.5],  # Wikipedia: 50% на GitHub, 50% на Medium
        [0, 0, 1.0],  # GitHub: 100% на Medium
        [1.0, 0, 0],  # Medium: 100% на Wikipedia
    ]
)

print("Матриця переходів P:")
print("                Wikipedia  GitHub  Medium")
for i, label in enumerate(labels):
    print(f"  {label:12s}  {P[i]}")
print()

# Початковий розподіл: всі сайти рівноцінні
rank = np.array([1 / 3, 1 / 3, 1 / 3])

print("Початковий PageRank:")
print("  Wikipedia = 0.333, GitHub = 0.333, Medium = 0.333")
print()

# Ітерації
num_iterations = 20
history = [rank.copy()]

for i in range(num_iterations):
    rank = rank @ P  # Множимо вектор на матрицю
    history.append(rank.copy())

history = np.array(history)

# Результат
print("=" * 60)
print("РЕЗУЛЬТАТ ПІСЛЯ 20 ІТЕРАЦІЙ:")
print("=" * 60)
for i, label in enumerate(labels):
    bar = "█" * int(rank[i] * 60)
    print(f"  {label:12s}: {rank[i]:.6f}  {bar}")
print()
print(f"Сума: {rank.sum():.6f}")
print()

# Пояснення
print("=" * 60)
print("ЩО ВІДБУЛОСЯ:")
print("=" * 60)
print("✓ Всі сайти отримали однаковий PageRank!")
print("✓ Причина: циклічна структура Wikipedia→GitHub→Medium→Wikipedia")
print("✓ Кожен сайт рівноцінний в цьому графі")
print()
print("У реальному інтернеті структура набагато складніша!")
print("=" * 60)

# Візуалізація збіжності
plt.figure(figsize=(12, 6))

for i, label in enumerate(labels):
    plt.plot(
        history[:, i], marker="o", linewidth=2, markersize=5, label=label, alpha=0.8
    )

plt.xlabel("Ітерація", fontsize=12)
plt.ylabel("PageRank", fontsize=12)
plt.title("Збіжність PageRank - оцінка важливості сайтів", fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
