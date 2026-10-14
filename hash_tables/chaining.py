class SeparateChainingHashTable:
    def __init__(self, capacity: int = 2**18):
        self.capacity = capacity
        self.mask = capacity - 1
        self.table = [[] for _ in range(capacity)]
        self.size = 0

    def _hash(self, key: int) -> int:
        return hash(key) & self.mask

    def put(self, key: int, value) -> int:
        idx = self._hash(key)
        probes = 0
        for item in self.table[idx]:
            probes += 1
            if item[0] == key:
                item[1] = value
                return probes
        
        self.table[idx].append([key, value])
        self.size += 1
        return probes + len(self.table[idx])

    def get(self, key: int) -> tuple[any, int]:
        idx = self._hash(key)
        probes = 0
        for item in self.table[idx]:
            probes += 1
            if item[0] == key:
                return item[1], probes
        return None, probes