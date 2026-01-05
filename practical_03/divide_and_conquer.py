from seed_data import all_feeds


def merge_two_feeds(feed1, feed2):
    result = []
    i = j = 0
    while i < len(feed1) and j < len(feed2):
        if feed1[i]["timestamp"] <= feed2[j]["timestamp"]:
            result.append(feed1[i])
            i += 1
        else:
            result.append(feed2[j])
            j += 1
    result.extend(feed1[i:])
    result.extend(feed2[j:])
    return result


def merge_k_feeds(feeds):
    if not feeds:
        return []
    if len(feeds) == 1:
        return feeds[0]

    mid = len(feeds) // 2
    left = merge_k_feeds(feeds[:mid])
    right = merge_k_feeds(feeds[mid:])

    return merge_two_feeds(left, right)


if __name__ == "__main__":
    print("=" * 60)
    print("Divide & Conquer: merge_k_feeds")
    print("=" * 60)
    result = merge_k_feeds(all_feeds)

    # Групуємо за датами для зручного виводу
    from collections import defaultdict

    grouped = defaultdict(list)
    for news in result:
        grouped[news["timestamp"].date()].append(news)

    for date, news_list in sorted(grouped.items()):
        print(f"\n📅 Дата: {date}")
        for news in news_list:
            print(
                f"  {news['timestamp'].strftime('%H:%M')} | {news['source']} | {news['category']}: {news['content']}"
            )
