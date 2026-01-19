import random
from collections import defaultdict

import matplotlib.pyplot as plt

nums = 10_000_000

counts = defaultdict(int)

for _ in range(nums):
    dice = random.randint(1, 6)
    # dice_two = random.randint(1, 6)
    counts[dice] += 1  # counts[dice + dice_two] += 1

probabilities = {key: count / nums for key, count in counts.items()}
print(probabilities)
print("Кубик | Ймовірність")
print("------|------------")
for dice, prob in probabilities.items():
    print(f"{dice}     | {prob:.2%}")


plt.bar(list(probabilities.keys()), list(probabilities.values()))  # noqa
plt.xlabel("Грань кубика")
plt.ylabel("Ймовірність")
plt.title("Кидання кубика - розподіл ймовірностей")
plt.xticks(range(1, 7))
plt.grid(True, alpha=0.3, axis="y")
plt.show()
