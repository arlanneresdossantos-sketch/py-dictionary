from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.75) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size: int = 0
        self.table: list[list[Node]] = [[] for _ in range(self.capacity)]

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0
        for bucket in old_table:
            for node in bucket:
                index = hash(node.key) % self.capacity
                self.table[index].append(node)
                self.size += 1

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()
        index = self._hash(key)
        for node in self.table[index]:
            if node.key == key:
                node.value = value
                return
        self.table[index].append(Node(key, value))
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        index = self._hash(key)
        for node in self.table[index]:
            if node.key == key:
                return node.value
        raise KeyError(f"Key '{key}' not found.")

    def __delitem__(self, key: Any) -> None:
        index = self._hash(key)
        for i, node in enumerate(self.table[index]):
            if node.key == key:
                del self.table[index][i]
                self.size -= 1
                return
        raise KeyError(f"Key '{key}' not found.")

    def __len__(self) -> int:
        return self.size
