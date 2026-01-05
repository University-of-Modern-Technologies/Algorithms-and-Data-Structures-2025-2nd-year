"""
Композитні ключі в MapReduce: паралелізація через вибірковий Reduce

КЛЮЧОВА ІДЕЯ:
Використовуючи композитний ключ (дата, категорія), ми можемо:
1. Запустити MAP+SHUFFLE один раз
2. Викликати REDUCE тільки для потрібних категорій/дат
3. Паралелізувати обробку різних категорій незалежно

ВІДМІННІСТЬ від простого MapReduce:
- Простий: ключ = дата → reduce обробляє ВСІ новини цього дня
- Композитний: ключ = (дата, категорія) → reduce тільки для потрібних топіків

Це дозволяє не завантажувати зайві дані та паралелізувати роботу сильніше.
"""

from seed_data import all_feeds
from divide_and_conquer import merge_k_feeds
from collections import defaultdict


# Mapper зі складеним ключем
def composite_mapper(agent_data):
    output = []
    for post in agent_data:
        # Ключ тепер - це пара (дата, категорія)
        key = (post["timestamp"].date(), post["category"])
        output.append((key, post))
    return output


# Shuffle фаза з композитними ключами
def shuffle(mapped_by_agent):
    # Спочатку групуємо за ключами, зберігаючи окремі потоки від агентів
    temp_grouped = defaultdict(lambda: defaultdict(list))
    for agent_idx, agent_mapped in enumerate(mapped_by_agent):
        for key, value in agent_mapped:
            temp_grouped[key][agent_idx].append(value)

    # Одразу перетворюємо в list of lists (відсортованих потоків)
    grouped = {}
    for key, agents_data in temp_grouped.items():
        grouped[key] = [agents_data[idx] for idx in sorted(agents_data.keys())]

    return grouped


# Reducer (той самий)
def reducer(key, lists_to_merge):
    # lists_to_merge - масив відсортованих списків від агентів
    return merge_k_feeds(lists_to_merge)


# MAP + SHUFFLE (без Reduce)
def map_and_shuffle(feeds):
    # 1. MAP: кожен агент генерує пари ((date, category), news)
    mapped_by_agent = []
    for agent_feed in feeds:
        mapped = composite_mapper(agent_feed)
        mapped_by_agent.append(mapped)

    print(
        f"MAP фаза: {len(feeds)} агентів згенерували пари з композитним ключем (date, category)"
    )

    # 2. SHUFFLE: групуємо за (дата, категорія)
    grouped = shuffle(mapped_by_agent)
    print(
        f"SHUFFLE фаза: згруповано в {len(grouped)} унікальних комбінацій (дата, категорія)"
    )
    print("\nДані групуються НЕ просто за днем, а за КОЖНИМ топіком окремо:")
    for key in sorted(grouped.keys()):
        date, category = key
        total_news = sum(len(feed) for feed in grouped[key])
        print(
            f"  ({date}, {category}): {total_news} новин від {len(grouped[key])} агентів"
        )

    print("\n" + "=" * 60)
    print("ПОВНА СТРУКТУРА ДАНИХ В grouped:")
    print("=" * 60)
    for key, item in sorted(grouped.items()):
        date, category = key
        print(f"\n🔑 Ключ: (date={date}, category='{category}')")
        print(f"   Структура item: list of lists (кількість агентів={len(item)})")
        print(f"   Повний вміст:")
        for i, agent_feed in enumerate(item):
            print(f"   ├── Агент {i + 1}: {len(agent_feed)} новин")
            for news in agent_feed:
                print(f"   │   ├── {news['source']}: {news['content']}")
        print()

    return grouped


# REDUCE тільки для вибраних ключів
def reduce_selected(shuffled_data, key_filter=None):
    """
    key_filter - функція, яка повертає True для ключів, які треба обробити
    Якщо None - обробляємо всі ключі
    """
    if key_filter is None:
        relevant_keys = shuffled_data.keys()
    else:
        relevant_keys = [k for k in shuffled_data.keys() if key_filter(k)]

    print(f"REDUCE фаза: обробляємо {len(relevant_keys)} з {len(shuffled_data)} ключів")

    results = {}
    for key in relevant_keys:
        feeds_to_merge = shuffled_data[key]
        results[key] = reducer(key, feeds_to_merge)
        date, category = key
        print(f"  ✓ ({date}, {category}) -> {len(feeds_to_merge)} потоків об'єднано")

    return results


# Фільтри для вибіркового reduce
def filter_by_category(target_category):
    """Повертає функцію-фільтр для категорії"""
    return lambda key: key[1] == target_category


def filter_by_date(target_date):
    """Повертає функцію-фільтр для дати"""
    return lambda key: key[0] == target_date


def filter_by_date_and_category(target_date, target_category):
    """Повертає функцію-фільтр для дати ТА категорії"""
    return lambda key: key[0] == target_date and key[1] == target_category


if __name__ == "__main__":
    from datetime import date as dt

    print("=" * 60)
    print("Composite Key MapReduce: (дата, категорія)")
    print("=" * 60)

    # MAP + SHUFFLE (один раз для всіх)
    shuffled = map_and_shuffle(all_feeds)

    # Демонстрація 1: Reduce для ВСІХ категорій
    print("=" * 60)
    print("Сценарій 1: Повний звіт (всі категорії)")
    print("=" * 60)
    all_results = reduce_selected(shuffled)

    for (date, category), news_list in sorted(all_results.items()):
        print(f"\n📅 {date} | 📂 {category}")
        for news in news_list:
            print(
                f"  {news['timestamp'].strftime('%H:%M')} | {news['source']}: {news['content']}"
            )

    # Демонстрація 2: Reduce ТІЛЬКИ для Tech (паралелізація!)
    print("\n" + "=" * 60)
    print("Сценарій 2: Reduce тільки для Tech новин")
    print("=" * 60)
    tech_results = reduce_selected(shuffled, filter_by_category("Tech"))

    for (date, category), news_list in sorted(tech_results.items()):
        print(f"\n📅 {date} | 📂 {category}")
        for news in news_list:
            print(
                f"  {news['timestamp'].strftime('%H:%M')} | {news['source']}: {news['content']}"
            )

    # Демонстрація 3: Reduce для Sport за конкретну дату
    target_date = dt(2026, 1, 5)

    print("\n" + "=" * 60)
    print(f"Сценарій 3: Reduce тільки для Sport за {target_date}")
    print("=" * 60)
    sport_date_results = reduce_selected(
        shuffled, filter_by_date_and_category(target_date, "Sport")
    )

    for (date, category), news_list in sorted(sport_date_results.items()):
        print(f"\n📅 {date} | 📂 {category}")
        for news in news_list:
            print(
                f"  {news['timestamp'].strftime('%H:%M')} | {news['source']}: {news['content']}"
            )
