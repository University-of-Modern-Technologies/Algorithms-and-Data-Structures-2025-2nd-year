from datetime import datetime

# Дані від Агентів (кожен список уже відсортований за timestamp всередині)
agent_1_results = [
    {
        "timestamp": datetime(2026, 1, 5, 8, 0),
        "source": "Agent_1",
        "category": "Tech",
        "content": "Новий прорив у квантових обчисленнях.",
    },
    {
        "timestamp": datetime(2026, 1, 5, 10, 30),
        "source": "Agent_1",
        "category": "Politics",
        "content": "Саміт G20: обговорення кліматичних змін.",
    },
    {
        "timestamp": datetime(2026, 1, 5, 14, 0),
        "source": "Agent_1",
        "category": "Tech",
        "content": "Вихід нової версії популярної ОС.",
    },
]

agent_2_results = [
    {
        "timestamp": datetime(2026, 1, 5, 9, 15),
        "source": "Agent_2",
        "category": "Sport",
        "content": "Результати нічних матчів НБА.",
    },
    {
        "timestamp": datetime(2026, 1, 5, 11, 45),
        "source": "Agent_2",
        "category": "Tech",
        "content": "Анонс нового смартфона з гнучким екраном.",
    },
    {
        "timestamp": datetime(2026, 1, 5, 15, 30),
        "source": "Agent_2",
        "category": "Sport",
        "content": "Підготовка збірної до чемпіонату світу.",
    },
]

agent_3_results = [
    {
        "timestamp": datetime(2026, 1, 5, 7, 45),
        "source": "Agent_3",
        "category": "Politics",
        "content": "Вибори в ЄС: перші прогнози екзит-полів.",
    },
    {
        "timestamp": datetime(2026, 1, 5, 12, 0),
        "source": "Agent_3",
        "category": "Sport",
        "content": "Тенісний турнір: сенсаційна перемога аутсайдера.",
    },
    {
        "timestamp": datetime(2026, 1, 5, 16, 20),
        "source": "Agent_3",
        "category": "Politics",
        "content": "Новий законопроєкт про цифрові активи.",
    },
]

agent_4_results = [
    {
        "timestamp": datetime(2026, 1, 5, 10, 0),
        "source": "Agent_4",
        "category": "Tech",
        "content": "Штучний інтелект навчився писати музику.",
    },
    {
        "timestamp": datetime(2026, 1, 5, 13, 15),
        "source": "Agent_4",
        "category": "Sport",
        "content": "Трансферні новини європейського футболу.",
    },
    {
        "timestamp": datetime(2026, 1, 5, 17, 0),
        "source": "Agent_4",
        "category": "Tech",
        "content": "Огляд найкращих гаджетів року.",
    },
]

agent_5_results = [
    {
        "timestamp": datetime(2026, 1, 5, 8, 30),
        "source": "Agent_5",
        "category": "Politics",
        "content": "Дипломатичний візит до Вашингтона.",
    },
    {
        "timestamp": datetime(2026, 1, 5, 11, 0),
        "source": "Agent_5",
        "category": "Tech",
        "content": "Кібербезпека: поради щодо захисту даних.",
    },
    {
        "timestamp": datetime(2026, 1, 5, 14, 45),
        "source": "Agent_5",
        "category": "Politics",
        "content": "Економічний форум у Давосі стартує завтра.",
    },
]

# Загальний масив джерел
all_feeds = [
    agent_1_results,
    agent_2_results,
    agent_3_results,
    agent_4_results,
    agent_5_results,
]
