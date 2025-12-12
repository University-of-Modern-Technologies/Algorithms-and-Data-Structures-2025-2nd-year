"""
CUSTOM OBJECTS IN HEAP - Користувацькі об'єкти в купі

Цей приклад показує як використовувати купи не тільки з числами,
але й зі складними об'єктами (класами).

ЩО РОБИТЬ:
- Використовує @dataclass(order=True) для автоматичного порівняння об'єктів
- Показує field(compare=False) для виключення полів з порівняння
- Демонструє різні реальні сценарії використання

ДЛЯ ЧОГО:
- Менеджер завдань з різними пріоритетами
- Система сортування пацієнтів швидкої допомоги (triage)
- Черга подій в грі, що обробляються за часом

КЛЮЧОВА КОНЦЕПЦІЯ:
heapq порівнює об'єкти, тому потрібно визначити як вони сортуються.
dataclass(order=True) автоматично створює __lt__, __le__, __gt__, __ge__
на основі полів, які мають compare=True (за замовчуванням).

ПРИКЛАДИ ВИКОРИСТАННЯ:
1. Task - завдання з пріоритетами (1=найважливіше)
2. Patient - пацієнти за серйозністю стану
3. Event - події в грі за часом виконання
"""

import heapq
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass(order=True)
class Task:
    """
    Завдання з пріоритетом для черги.
    order=True автоматично генерує методи порівняння.
    """

    priority: int
    description: str = field(compare=False)  # не використовується для порівняння
    created_at: datetime = field(compare=False, default_factory=datetime.now)

    def __repr__(self):
        return f"Task(p={self.priority}, '{self.description}')"


@dataclass(order=True)
class Patient:
    """Пацієнт в системі сортування швидкої допомоги"""

    severity: int  # 1=критичний, 2=серйозний, 3=середній, 4=легкий
    arrival_time: float = field(compare=False)
    name: str = field(compare=False)
    symptoms: str = field(compare=False)

    def __repr__(self):
        severity_name = {1: "КРИТИЧНИЙ", 2: "СЕРЙОЗНИЙ", 3: "СЕРЕДНІЙ", 4: "ЛЕГКИЙ"}[
            self.severity
        ]
        return f"{self.name} [{severity_name}]: {self.symptoms}"


def demo_task_manager():
    """Приклад: менеджер завдань з пріоритетами"""
    print("=== Менеджер завдань ===\n")

    tasks = []

    heapq.heappush(tasks, Task(3, "Написати звіт"))
    heapq.heappush(tasks, Task(1, "ТЕРМІНОВО: Виправити баг в продакшені"))
    heapq.heappush(tasks, Task(2, "Зателефонувати клієнту"))
    heapq.heappush(tasks, Task(5, "Оновити документацію"))
    heapq.heappush(tasks, Task(1, "ТЕРМІНОВО: Backup бази даних"))
    heapq.heappush(tasks, Task(4, "Code review"))

    print("Виконання завдань за пріоритетом:\n")
    position = 1
    while tasks:
        task = heapq.heappop(tasks)
        print(f"{position}. [P{task.priority}] {task.description}")
        position += 1


def demo_emergency_room():
    """Приклад: система сортування пацієнтів швидкої допомоги"""
    print("\n=== Відділення швидкої допомоги ===\n")

    patients = []
    current_time = 0

    # Пацієнти прибувають
    heapq.heappush(patients, Patient(4, current_time, "Іванов", "Легкий кашель"))
    current_time += 5
    heapq.heappush(
        patients, Patient(2, current_time, "Петренко", "Сильний біль в грудях")
    )
    current_time += 3
    heapq.heappush(patients, Patient(3, current_time, "Сидоренко", "Перелом руки"))
    current_time += 2
    heapq.heappush(patients, Patient(1, current_time, "Коваленко", "Серцевий напад"))
    current_time += 7
    heapq.heappush(patients, Patient(4, current_time, "Мельник", "Подряпина"))
    current_time += 1
    heapq.heappush(patients, Patient(1, current_time, "Шевченко", "Важка травма"))

    print("Порядок прийому пацієнтів:\n")
    position = 1
    while patients:
        patient = heapq.heappop(patients)
        print(f"{position}. {patient}")
        position += 1


@dataclass(order=True)
class Event:
    """Події для ігрового циклу"""

    timestamp: float
    event_type: str = field(compare=False)
    data: dict = field(compare=False, default_factory=dict)


def demo_game_events():
    """Приклад: ігрова черга подій"""
    print("\n=== Ігрова черга подій ===\n")

    events = []

    heapq.heappush(events, Event(0.0, "GAME_START", {"level": 1}))
    heapq.heappush(events, Event(5.5, "SPAWN_ENEMY", {"type": "goblin", "x": 100}))
    heapq.heappush(events, Event(3.2, "PLAYER_JUMP", {}))
    heapq.heappush(events, Event(7.8, "COLLECT_COIN", {"value": 10}))
    heapq.heappush(events, Event(2.1, "PLAY_SOUND", {"sound": "footstep.wav"}))
    heapq.heappush(events, Event(10.0, "SPAWN_ENEMY", {"type": "orc", "x": 250}))

    print("Обробка подій у хронологічному порядку:\n")
    while events:
        event = heapq.heappop(events)
        print(f"t={event.timestamp:4.1f}s: {event.event_type:15s} {event.data}")


if __name__ == "__main__":
    demo_task_manager()
    demo_emergency_room()
    demo_game_events()
