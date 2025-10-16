# Space Invaders

Класична аркадна гра Space Invaders, реалізована на Python з використанням pygame-ce.

## Вимоги

- **Python**: 3.12+
- **ОС**: Windows 10+, Linux (Ubuntu 20.04+)
- **uv**: Менеджер залежностей та пакетів

## Встановлення

### 1. Установка залежностей

```bash
uv sync
```

Це встановить всі залежності, визначені в `pyproject.toml`.

### 2. Запуск гри

#### Способ 1: Безпосередній запуск

```bash
uv run python -m game
```

#### Способ 2: Запуск через main.py

```bash
cd src
python main.py
```

#### Способ 3: Запуск через точку входу (після встановлення)

```bash
space-invaders
```

## Розробка

### Запуск тестів

```bash
uv run pytest
```

### Перевірка типів

```bash
uv run mypy src/
```

### Лінтинг та форматування

```bash
uv run ruff check src/
uv run ruff format src/
uv run black src/
```

### Збірка автономного .exe (Windows)

```bash
uv run pyinstaller space_invaders.spec
```

Виконуваний файл буде в `dist/space_invaders/`.

## Структура проекту

```
space-invaders/
├── docs/                    # Документація
│   ├── requirements.md      # Вимоги до гри
│   ├── arch_rules.md        # Архітектурні правила
│   ├── architecture.md      # Опис архітектури
│   └── plan.md              # План розробки
├── src/
│   ├── main.py              # Точка входу
│   └── game/                # Основний пакет гри
│       ├── __init__.py
│       ├── __main__.py
│       ├── core/            # Ядро логіки
│       ├── domain/          # Бізнес-логіка
│       ├── infra/           # Інфраструктура
│       └── ui/              # Користувацький інтерфейс
├── assets/                  # Ресурси гри
│   ├── images/
│   ├── sounds/
│   ├── fonts/
│   └── data/
├── tests/                   # Тести
│   ├── unit/
│   └── integration/
├── logs/                    # Логи гри
├── pyproject.toml           # Конфіг проекту
├── mypy.ini                 # Конфіг типізації
├── ruff.toml                # Конфіг лінтингу
├── pytest.ini               # Конфіг тестування
└── space_invaders.spec      # Конфіг PyInstaller
```

## Архітектура

Проект слідує чистій архітектурі з 4 основними шарами:

1. **Domain** — бізнес-логіка (сутності, правила)
2. **Core** — ядро гри (фізика, логіка, ввід)
3. **Infra** — інфраструктура (адаптери, утиліти)
4. **UI** — користувацький інтерфейс

Детальний опис див. в `docs/architecture.md`.

## Управління

- **Стрілки / A-D**: Рух коробля
- **Пробіл**: Постріл
- **P**: Пауза
- **Esc**: Меню

## Ліцензія

MIT
