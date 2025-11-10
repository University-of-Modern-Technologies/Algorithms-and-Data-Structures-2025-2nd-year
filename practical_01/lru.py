from typing import Optional


class Node:
    def __init__(self, key, value):
        self.data = (key, value)
        self.next: Optional["Node"] = None
        self.prev: Optional["Node"] = None


class DoublyLinkedList:
    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None

    def push(self, key, value):
        new_node = Node(key, value)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        else:
            self.tail = new_node
        self.head = new_node
        return new_node

    def remove(self, node: Node) -> None:
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = None
        node.next = None

    def move_to_front(self, node: Node) -> None:
        if node != self.head:
            self.remove(node)
            node.next = self.head
            if self.head:
                self.head.prev = node
            self.head = node

    def remove_last(self) -> Optional[Node]:
        if self.tail:
            last = self.tail
            self.remove(last)
            return last
        return None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.list = DoublyLinkedList()
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self.list.move_to_front(node)
        return node.data[1]
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # якщо ключ вже існує, оновлюємо значення та переміщуємо вузол до початку списку
            node = self.cache[key]
            node.data = (key, value)
            self.list.move_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                last = self.list.remove_last()
                if last:
                    del self.cache[last.data[0]]
            new_node = self.list.push(key, value)
            self.cache[key] = new_node


def explain(cache: LRUCache):
    print("-----------------------")
    if cache.list.head:
        print("HEAD: ", cache.list.head.data)
    else:
        print("HEAD: None")
    if cache.list.tail:
        print("TAIL: ", cache.list.tail.data)
    else:
        print("TAIL: None")
    current = cache.list.head
    while current:
        print(f"{current.data[0]}: {current.data[1]}")
        current = current.next
    print("-----------------------")


if __name__ == "__main__":
    cache = LRUCache(3)
    cache.put(1, "Банан")
    explain(cache)
    cache.put(2, "Груша")
    explain(cache)
    cache.put(3, "Яблуко")
    explain(cache)
    print(cache.get(1))  # виведе "Банан"
    explain(cache)
    cache.put(4, "Диня")
    explain(cache)
    print(cache.get(2))  # виведе -1 (не знайдено)
