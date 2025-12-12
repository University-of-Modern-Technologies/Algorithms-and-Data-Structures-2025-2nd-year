# Custom Objects in Heap - Об'єкти в купі

## Проблема

`heapq` добре працює з числами:

```python
heap = [5, 3, 7, 1]
heapq.heapify(heap)  # ✅ Працює
```

Але що з об'єктами?

```python
class Task:
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description

heap = [Task(1, "Важливо"), Task(2, "Менш важливо")]
heapq.heapify(heap)  # 💥 TypeError: '<' not supported
```

**Проблема:** Python не знає як порівнювати наші об'єкти!

## Рішення: `@dataclass(order=True)`

### Базовий приклад

```python
from dataclasses import dataclass

@dataclass(order=True)
class Task:
    priority: int
    description: str
```

**Що робить `order=True`:**

- Автоматично створює методи порівняння: `__lt__`, `__le__`, `__gt__`, `__ge__`, `__eq__`
- Порівнює об'єкти **по всім полям** зверху вниз

```python
task1 = Task(1, "AAA")
task2 = Task(2, "BBB")
task3 = Task(1, "ZZZ")

task1 < task2  # True (1 < 2)
task1 < task3  # True (1 == 1, але "AAA" < "ZZZ")
```

### Проблема: Небажане порівняння

Якщо `priority` однаковий, Python порівнює `description`! Це не те, що ми хочемо.

```python
heap = []
heappush(heap, Task(1, "Завдання A"))
heappush(heap, Task(1, "Завдання B"))
# Порівнюється не тільки priority, але й description! 😕
```

## Рішення: `field(compare=False)`

```python
from dataclasses import dataclass, field

@dataclass(order=True)
class Task:
    priority: int
    description: str = field(compare=False)  # ← НЕ використовується для порівняння
```

**Тепер порівнюється ТІЛЬКИ `priority`!**

```python
task1 = Task(1, "AAA")
task2 = Task(1, "ZZZ")

task1 < task2  # False (1 == 1, description ігнорується)
task1 == task2  # True (однаковий priority)
```

## Детальний розбір параметрів

### `order=True`

```python
@dataclass(order=True)
class Task:
    priority: int
```

**Генерує автоматично:**

```python
# Еквівалентно написанню вручну:
def __lt__(self, other):
    return self.priority < other.priority

def __le__(self, other):
    return self.priority <= other.priority

def __gt__(self, other):
    return self.priority > other.priority

def __ge__(self, other):
    return self.priority >= other.priority

def __eq__(self, other):
    return self.priority == other.priority
```

### `field(compare=False)`

```python
@dataclass(order=True)
class Task:
    priority: int           # compare=True (за замовчуванням)
    description: str = field(compare=False)
    created_at: datetime = field(compare=False, default_factory=datetime.now)
```

**Параметри `field()`:**

| Параметр          | Значення     | Опис                              |
| ----------------- | ------------ | --------------------------------- |
| `compare`         | `True/False` | Чи використовувати для порівняння |
| `default`         | будь-яке     | Значення за замовчуванням         |
| `default_factory` | функція      | Функція для генерації значення    |

### Порядок полів важливий!

```python
@dataclass(order=True)
class Event:
    timestamp: float       # Спочатку порівнюється час
    priority: int          # Потім пріоритет (якщо час однаковий)
    name: str = field(compare=False)
```

```python
event1 = Event(10.0, 1, "A")
event2 = Event(10.0, 2, "B")
event3 = Event(5.0, 5, "C")

event1 < event2  # False (timestamp однаковий, priority: 1 < 2 → True, але timestamp головний)
event3 < event1  # True (5.0 < 10.0)
```

## Приклад 1: Менеджер завдань

```python
@dataclass(order=True)
class Task:
    priority: int  # 1 = найважливіше
    description: str = field(compare=False)
    created_at: datetime = field(compare=False, default_factory=datetime.now)

# Використання:
tasks = []
heappush(tasks, Task(3, "Написати звіт"))
heappush(tasks, Task(1, "ТЕРМІНОВО: Виправити баг"))
heappush(tasks, Task(2, "Зателефонувати клієнту"))

while tasks:
    task = heappop(tasks)
    print(f"[P{task.priority}] {task.description}")

# Вихід (за пріоритетом):
# [P1] ТЕРМІНОВО: Виправити баг
# [P2] Зателефонувати клієнту
# [P3] Написати звіт
```

## Приклад 2: Швидка допомога (Triage)

```python
@dataclass(order=True)
class Patient:
    severity: int  # 1=критичний, 2=серйозний, 3=середній, 4=легкий
    arrival_time: float = field(compare=False)
    name: str = field(compare=False)
    symptoms: str = field(compare=False)

# Використання:
patients = []
heappush(patients, Patient(4, 0.0, "Іванов", "Легкий кашель"))
heappush(patients, Patient(2, 5.0, "Петренко", "Біль в грудях"))
heappush(patients, Patient(1, 10.0, "Коваленко", "Серцевий напад"))
heappush(patients, Patient(3, 8.0, "Сидоренко", "Перелом руки"))

# Обробка за серйозністю (не за часом прибуття!):
while patients:
    patient = heappop(patients)
    print(f"{patient.name}: {patient.symptoms}")

# Вихід:
# Коваленко: Серцевий напад        (severity=1)
# Петренко: Біль в грудях          (severity=2)
# Сидоренко: Перелом руки          (severity=3)
# Іванов: Легкий кашель            (severity=4)
```

**Важливо:** Пацієнти обробляються НЕ за часом прибуття, а за серйозністю стану!

## Приклад 3: Ігрові події

```python
@dataclass(order=True)
class Event:
    timestamp: float        # Час події (секунди від початку гри)
    event_type: str = field(compare=False)
    data: dict = field(compare=False, default_factory=dict)

# Використання:
events = []
heappush(events, Event(5.5, "SPAWN_ENEMY", {"type": "goblin"}))
heappush(events, Event(3.2, "PLAYER_JUMP", {}))
heappush(events, Event(0.0, "GAME_START", {"level": 1}))
heappush(events, Event(7.8, "COLLECT_COIN", {"value": 10}))

# Обробка подій у хронологічному порядку:
while events:
    event = heappop(events)
    print(f"t={event.timestamp:.1f}s: {event.event_type}")

# Вихід:
# t=0.0s: GAME_START
# t=3.2s: PLAYER_JUMP
# t=5.5s: SPAWN_ENEMY
# t=7.8s: COLLECT_COIN
```

## Альтернативні підходи

### 1. Кортежі (старий спосіб)

```python
# Замість:
heappush(heap, Task(1, "Важливо"))

# Використовуємо:
heappush(heap, (1, "Важливо"))  # (priority, task)

# Проблеми:
# - Немає назв полів (що означає 1?)
# - Складно читати код
# - Легко помилитися в порядку
```

### 2. Ручна реалізація `__lt__`

```python
class Task:
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description

    def __lt__(self, other):
        return self.priority < other.priority

    def __le__(self, other):
        return self.priority <= other.priority

    # ... ще 3 методи

# Проблеми:
# - Багато коду
# - Легко забути якийсь метод
# - Треба підтримувати вручну
```

### 3. `@dataclass(order=True)` ✅ (найкращий)

```python
@dataclass(order=True)
class Task:
    priority: int
    description: str = field(compare=False)

# Переваги:
# ✅ Мало коду
# ✅ Автоматична генерація методів
# ✅ Явно вказано що порівнюється
# ✅ Легко читати і підтримувати
```

## Комбінування критеріїв сортування

### Пріоритет + час (якщо пріоритет однаковий)

```python
@dataclass(order=True)
class Task:
    priority: int           # Спочатку за пріоритетом
    created_at: float       # Потім за часом
    description: str = field(compare=False)

task1 = Task(1, 10.0, "A")
task2 = Task(1, 5.0, "B")   # Той самий пріоритет, але раніше
task3 = Task(2, 1.0, "C")

# Сортування:
# task2 (p=1, t=5.0)  ← Найвищий пріоритет + найраніший
# task1 (p=1, t=10.0) ← Той самий пріоритет, але пізніший
# task3 (p=2, t=1.0)  ← Нижчий пріоритет
```

## Типові помилки

### ❌ Помилка 1: Забули `compare=False`

```python
@dataclass(order=True)
class Task:
    priority: int
    description: str  # ← Буде порівнюватись!

task1 = Task(1, "AAA")
task2 = Task(1, "ZZZ")

# Непередбачуване порівняння рядків!
```

### ❌ Помилка 2: Неправильний порядок полів

```python
@dataclass(order=True)
class Task:
    description: str = field(compare=False)
    priority: int  # ← Має бути ПЕРШИМ!
```

### ❌ Помилка 3: Порівняння змінних даних

```python
@dataclass(order=True)
class Task:
    priority: int
    completed: bool  # ← Змінюється! Купа зламається!

# Якщо змінити completed, купа стане невалідною!
```

## Ключові моменти

1. **`order=True`** - автоматично генерує методи порівняння
2. **`compare=False`** - виключає поле з порівняння
3. **Порядок полів важливий** - спочатку головні критерії
4. **Не змінюйте поля** - після додавання в купу, об'єкти мають бути незмінними
5. **Читабельність** - dataclass набагато зрозуміліший за кортежі

## Коли використовувати?

✅ **Використовуйте custom objects:**

- Коли об'єктів багато полів (>2)
- Коли важлива читабельність коду
- Коли потрібна типізація
- Коли логіка порівняння складна

❌ **Використовуйте кортежі:**

- Для простих випадків (priority, item)
- Для швидких прототипів
- Коли продуктивність критична (кортежі трохи швидші)

## Завдання для практики

1. Створіть клас `Job` для черги друку з пріоритетом та кількістю сторінок
2. Реалізуйте клас `Email` який сортується за важливістю та датою
3. Створіть систему планування завдань з дедлайнами та пріоритетами
