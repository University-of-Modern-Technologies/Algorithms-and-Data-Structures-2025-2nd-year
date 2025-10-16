# архітектура Space Invaders

Цей документ описує загальну архітектуру системи, розташування компонентів, їх відповідальність та правила взаємодії. Архітектура слідує чистому архітектурному принципу з розділенням відповідальності: залежності спрямовані від зовнішніх шарів до внутрішніх.

## 1. принципи архітектури

### 1.1 шарист (layered) підхід

```
┌─────────────────────────────────────────┐
│         UI шар (ui)                     │  ← взаємодія з користувачем
├─────────────────────────────────────────┤
│    Інфраструктура (infra)               │  ← адаптери, утиліти
├─────────────────────────────────────────┤
│    Ядро логіки (core)                   │  ← основна ігрова логіка
├─────────────────────────────────────────┤
│    Бізнес-домен (domain)                │  ← моделі, правила
└─────────────────────────────────────────┘
```

### 1.2 правила залежностей

- **Domain** не залежить від нічого → максимально переносима
- **Core** залежить від Domain, не залежить від UI/Infra
- **Infra** постачає адаптери та утиліти, залежить від Domain/Core
- **UI** зовнішній шар, може залежати від всіх інших

### 1.3 напрями зв'язків

```
ui → core → domain
ui → infra → domain
infra → core
```

---

## 2. структура модулів

```
src/game/
├── __init__.py
├── core/                    # ядро гри (фізика, логіка, ввід)
│   ├── __init__.py
│   ├── physics.py          # детектор зіткнень (AABB, еліпс, круг)
│   ├── input.py            # обробник вводу (клавіатура + геймпад)
│   ├── update.py           # головна функція оновлення логіки
│   └── render.py           # підготовка команд для рендерингу
│
├── domain/                  # бізнес-логіка, моделі
│   ├── __init__.py
│   ├── entities.py         # Player, Enemy, Projectile, Shield, Wave, BonusShip
│   ├── scoring.py          # ScoreManager, система очок
│   ├── game_state.py       # GameState, состояния гри, Difficulty
│   └── difficulty.py       # параметри складності, баланс
│
├── infra/                   # адаптери, утиліти, ресурси
│   ├── __init__.py
│   ├── timing.py           # GameTimer, синхронізація 60 FPS
│   ├── logging.py          # логер, запис у файл
│   ├── config.py           # ConfigManager, збереження налаштувань
│   ├── i18n.py             # Translator, локалізація
│   ├── assets.py           # AssetLoader, завантаження ресурсів
│   └── audio.py            # AudioManager, управління звуком
│
└── ui/                      # користувацький інтерфейс
    ├── __init__.py
    ├── scenes.py           # Scene, MenuScene, GameScene, etc.
    ├── components.py       # Widget, Button, Label, Slider, RadioButton
    ├── renderer.py         # PygameRenderer, рендеринг спрайтів
    └── hud.py              # HUD, відображення інформації

src/
└── main.py                  # точка входу, головний ігровий цикл
```

---

## 3. опис пакетів

### 3.1 domain

**Назначення**: Бізнес-логіка гри, повністю незалежна від UI та Infra.

**Основні сутності**:

- `Player` — корабель гравця (позиція, HP, щити, ширина)
- `Enemy` — ворог (позиція, швидкість, HP, тип)
- `Projectile` — снаряд (позиція, швидкість, власник)
- `Shield` — щит (позиція, сегменти зі станом)
- `BonusShip` — рідкісний ворог (позиція, швидкість, бонусний бал)
- `Wave` — хвиля ворогів (список, активні, загибель)

**Основні сервіси**:

- `ScoreManager` — накопленням балів, зберігання рекорду
- `GameState` — глобальний стан (MENU, PLAYING, PAUSED, GAME_OVER, SETTINGS)
- `DifficultyParams` — параметри складності (EASY, NORMAL, HARD)

**Правило**: Всі класи мають типові анотації, немає прямого звернення до pygame.

---

### 3.2 core

**Назначення**: Ядро гри — основна логіка, фізика, ввід.

**Підмодулі**:

#### 3.2.1 physics.py

```python
class CollisionDetector:
    def check_rect_rect(rect1, rect2) -> bool
    def check_circle_rect(circle, rect) -> bool
    def check_ellipse_circle(ellipse, circle) -> bool

class CollisionEvent:
    type: str  # "enemy_projectile", "player_enemy", etc.
    subject: Entity
    object: Entity
```

#### 3.2.2 input.py

```python
class InputHandler:
    def update() -> None
    def is_key_pressed(key) -> bool
    def get_axis(axis) -> float  # для геймпада
    def get_movement() -> Tuple[float, float]
    def is_shoot_pressed() -> bool
    def is_pause_pressed() -> bool
```

#### 3.2.3 update.py

```python
def update(dt: float, game_state: GameState) -> List[Command]:
    # 1. Обробка вводу
    # 2. Оновлення позицій і анімацій
    # 3. Перевірка зіткнень
    # 4. Генерація команд
    # Повертає список команд для обробки
```

#### 3.2.4 render.py

```python
def render(game_state: GameState) -> List[RenderCommand]:
    # Повертає список об'єктів для рисування у правильному Z-порядку
```

**Правило**: Core не знає про pygame, окрім абстракцій введення-виведення від Infra.

---

### 3.3 infra

**Назначення**: Адаптери для ресурсів, утиліти, інтеграція з OS.

#### 3.3.1 timing.py

```python
class GameTimer:
    FIXED_DT = 1 / 60  # 60 FPS

    def tick(target_fps=60) -> Tuple[float, bool]:
        # Повертає (dt, should_render)
        # dt завжди 1/60
        # should_render = True якщо час для кадру
```

#### 3.3.2 logging.py

```python
class Logger:
    def info(msg: str) -> None
    def error(msg: str, exc: Exception = None) -> None
    # Записує в logs/game.log
```

#### 3.3.3 config.py

```python
class ConfigManager:
    def load() -> Dict[str, Any]
    def save(config: Dict[str, Any]) -> None
    # ~/.space_invaders/config.json
```

#### 3.3.4 i18n.py

```python
class Translator:
    def get(key: str, lang: str = "uk") -> str
    def set_language(lang: str) -> None
    # assets/data/locales.json
```

#### 3.3.5 assets.py

```python
class AssetLoader:
    def load_image(path: str) -> pygame.Surface
    def load_sound(path: str) -> pygame.mixer.Sound
    def load_font(name: str, size: int) -> pygame.font.Font
    # Кешування, fallback'и
```

#### 3.3.6 audio.py

```python
class AudioManager:
    def play_sfx(name: str, volume: float) -> None
    def play_music(name: str, loop: int = -1) -> None
    def set_volume(category: str, volume: float) -> None
    # категорії: "music", "sfx"
```

**Правило**: Infra — це "адаптерні шари" між Core/Domain та зовнішніми бібліотеками.

---

### 3.4 ui

**Назначення**: Користувацький інтерфейс, сцени, компоненти, рендеринг.

#### 3.4.1 scenes.py

```python
class Scene(ABC):
    def update(dt: float) -> None
    def render(renderer: Renderer) -> None
    def handle_input(input_handler: InputHandler) -> None
    def transition_to(scene_type: Type[Scene]) -> None

class MenuScene(Scene):
    # Головне меню з кнопками

class GameScene(Scene):
    # Основна ігрова сцена

class PauseScene(Scene):
    # Екран паузи

class GameOverScene(Scene):
    # Екран завершення з рекордом

class SettingsScene(Scene):
    # Налаштування гри
```

#### 3.4.2 components.py

```python
class Widget(ABC):
    def render(renderer: Renderer) -> None
    def update(dt: float) -> None
    def on_click() -> None
    def on_hover() -> None

class Button(Widget):
    text: str
    on_click_callback: Callable

class Label(Widget):
    text: str

class Slider(Widget):
    min_value: float
    max_value: float
    value: float

class RadioButton(Widget):
    options: List[str]
    selected: int
```

#### 3.4.3 renderer.py

```python
class Renderer:
    def clear() -> None
    def draw_sprite(sprite: Sprite, pos: Tuple[int, int]) -> None
    def draw_rect(rect: Rect, color: Tuple[int, int, int]) -> None
    def draw_text(text: str, font: Font, pos: Tuple[int, int]) -> None
    def present() -> None
```

#### 3.4.4 hud.py

```python
class HUD:
    def render(renderer: Renderer, game_state: GameState) -> None
    #렌더 очки, рекорд, HP, складність, хвилю
```

**Правило**: UI взаємодіє з Core/Domain через інтерфейси, а не прямо.

---

## 4. головний ігровий цикл

```python
# src/main.py

def main():
    # 1. Ініціалізація
    timer = GameTimer()
    config = ConfigManager.load()
    assets = AssetLoader()
    renderer = Renderer(1280, 720)

    # 2. Ініціалізація сцен
    scene = MenuScene()
    game_state = GameState(state=State.MENU)

    # 3. Головний цикл
    running = True
    accumulator = 0.0

    while running:
        # Синхронізація часу
        dt, should_render = timer.tick()
        accumulator += dt

        # Обробка вводу (завжди)
        input_handler.update()
        scene.handle_input(input_handler)

        # Фіксований крок оновлення логіки
        while accumulator >= timer.FIXED_DT:
            if game_state.state == State.PLAYING:
                commands = core.update(timer.FIXED_DT, game_state)
                apply_commands(commands, game_state)

            scene.update(timer.FIXED_DT)
            accumulator -= timer.FIXED_DT

        # Рендеринг (за потреби)
        if should_render:
            renderer.clear()
            scene.render(renderer)
            renderer.present()

        # Перевірка завершення
        running = not input_handler.is_quit()

    renderer.close()
```

---

## 5. потоки даних

### 5.1 ввід → логіка

```
User Input
    ↓
InputHandler (core.input)
    ↓
core.update() ← GameState (domain)
    ↓
Commands (внутрішні команди)
    ↓
apply_commands() → GameState
```

### 5.2 логіка → рендеринг

```
GameState (domain)
    ↓
core.render() → RenderCommands
    ↓
Scene.render(renderer)
    ↓
Renderer → pygame Surface
    ↓
Display
```

### 5.3 синхронізація часу

```
System Clock
    ↓
GameTimer.tick()
    ↓
dt = 1/60 (фіксовано)
    ↓
Accumulator Pattern
```

---

## 6. об'єкти значення та команди

### 6.1 Value Objects (нечутливі до часу)

```python
# Позиція
class Position:
    x: float
    y: float

# Розміри
class Size:
    width: float
    height: float

# Колір
class Color:
    r: int
    g: int
    b: int
```

### 6.2 Commands (imperatives)

```python
# Команди для застосування результатів зіткнень
@dataclass
class KillEntityCommand:
    entity_id: int

@dataclass
class DamageCommand:
    entity_id: int
    damage: int

@dataclass
class ScoreCommand:
    amount: int

@dataclass
class ChangeStateCommand:
    new_state: GameState
```

---

## 7. інтеграція модулів

### 7.1 ініціалізація при старті

```
main.py
├─ ConfigManager.load() → config dict
├─ AssetLoader.load_all() → cache sprites, sounds, fonts
├─ InputHandler() → initialize pygame.event listeners
├─ GameTimer() → set up clock
├─ MenuScene() → create first scene
└─ Game Loop →

    for each frame:
    ├─ timer.tick() → dt
    ├─ input_handler.update() → collect events
    ├─ scene.handle_input() → process UI interactions
    ├─ core.update() → process game logic
    ├─ scene.update() → update scene state
    ├─ core.render() → prepare draw commands
    ├─ scene.render() → draw UI
    └─ renderer.present() → flip display
```

### 7.2 управління сценами

```
Scene Manager (у main):
├─ current_scene
├─ scene_queue
└─ transition(scene_type)
    ├─ Cleanup current scene
    ├─ Create new scene
    └─ Set as current
```

---

## 8. розширення та розвиток

### 8.1 додавання нової механіки

Приклад: додати "Power-ups"

1. **Domain**: `domain/entities.py` → додати `PowerUp` клас
2. **Core**: `core/update.py` → обробка зіткнення з PowerUp
3. **Core**: `core/physics.py` → додати тип зіткнення
4. **Infra**: `infra/assets.py` → завантажити спрайт
5. **UI**: `ui/hud.py` → показати активний PowerUp

Залежності йдуть знизу вгору (від Domain до UI).

### 8.2 додавання нового типу сцени

1. Наслідувати `Scene` із `ui/scenes.py`
2. Реалізувати `update()`, `render()`, `handle_input()`
3. Додати в меню перехід на нову сцену
4. Використати наявні компоненти або створити нові

---

## 9. критичні інваріанти

1. **Domain** ніколи не імпортує з `ui` або `infra`
2. **Core** ніколи не створює pygame об'єкти напряму
3. **Детермінізм**: одна послідовність вводу → одна послідовність результатів
4. **Атомарність команд**: всі команди застосовуються разом, не поступово
5. **Фіксований dt**: ввід і рендеринг можуть пропускатися, логіка ні
6. **Типізація**: всі публічні функції мають type hints

---

## 10. залежності третіх сторін

| Модуль  | Залежність  | Версія | Використання          |
| ------- | ----------- | ------ | --------------------- |
| game.\* | pygame-ce   | 2.3+   | Графіка, звук, ввід   |
| game.\* | mypy        | 1.5+   | Type checking         |
| tests   | pytest      | 7.0+   | Тестування            |
| \*      | ruff        | 0.1+   | Лінтинг, форматування |
| \*      | black       | 23.0+  | Форматування          |
| build   | pyinstaller | 6.0+   | Збірка .exe           |

---

## 11. відповідність архітектурним правилам

| Правило                         | Реалізація                                       |
| ------------------------------- | ------------------------------------------------ |
| `core` без деталей pygame       | Абстракції InputHandler, Renderer                |
| `domain` незалежна              | Немає імпортів з інших модулів                   |
| Залежності спрямовані всередину | Розділення на шари                               |
| Фіксований ігровий крок         | GameTimer з dt = 1/60                            |
| Команди замість подій           | Команди застосовуються атомарно                  |
| Типізація                       | Type hints у всіх публічних API                  |
| Тести                           | Юніт тести для core, domain; інтеграційні для ui |
