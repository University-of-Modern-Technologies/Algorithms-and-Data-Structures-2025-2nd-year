from seed_data import all_feeds
from divide_and_conquer import merge_k_feeds
from collections import defaultdict


# Імітація Mapper (Агент)
def mapper(agent_data):
    # Кожен агент видає новини з ключем 'дата'
    output = []
    for post in agent_data:
        key = post["timestamp"].date()
        output.append((key, post))
    return output


# Shuffle фаза - групування за ключами
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


# Імітація Reducer
def reducer(key, lists_to_merge):
    # lists_to_merge - масив відсортованих списків від агентів
    return merge_k_feeds(lists_to_merge)


# MapReduce workflow
def map_reduce_pipeline(feeds):
    # 1. MAP: кожен агент генерує пари (key, value)
    mapped_by_agent = []
    for agent_feed in feeds:
        mapped = mapper(agent_feed)
        mapped_by_agent.append(mapped)

    print(f"MAP фаза: {len(feeds)} агентів згенерували пари (key, value)")
    for agent_idx, agent_mapped in enumerate(mapped_by_agent):
        print(f"  Агент {agent_idx}: {len(agent_mapped)} пар (key, value)")

    # 2. SHUFFLE: групуємо за датами, зберігаючи окремі потоки від агентів
    grouped = shuffle(mapped_by_agent)
    print(f"SHUFFLE фаза: згруповано в {len(grouped)} унікальних дат")
    print(f"Ключі після shuffle: {list(grouped.keys())}")
    for key in sorted(grouped.keys()):
        total_news = sum(len(feed) for feed in grouped[key])
        print(f"  Дата {key}: {total_news} новин від {len(grouped[key])} агентів")

    # 3. REDUCE: використовуємо merge_k_feeds для кожної дати
    results = {}
    for key, feeds_to_merge in grouped.items():
        results[key] = reducer(key, feeds_to_merge)
        print(f"REDUCE фаза: дата {key} -> {len(feeds_to_merge)} потоків об'єднано")

    return results


if __name__ == "__main__":
    print("=" * 60)
    print("MapReduce Pipeline з merge_k_feeds")
    print("=" * 60)
    results = map_reduce_pipeline(all_feeds)

    for date, news_list in sorted(results.items()):
        print(f"\n📅 Дата: {date}")
        for news in news_list:
            print(
                f"  {news['timestamp'].strftime('%H:%M')} | {news['source']} | {news['category']}: {news['content']}"
            )
