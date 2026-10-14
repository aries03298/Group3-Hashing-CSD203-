class Tombstone:
    pass

class LinearProbingHashTable:
    def __init__(self, capacity: int = 2**18):
        self.capacity = capacity
        self.mask = capacity - 1
        self.keys = [None] * capacity
        self.values = [None] * capacity
        self.tombstone_obj = Tombstone()
        self.size = 0

    def _hash(self, key: int) -> int:
        return hash(key) & self.mask

    def put(self, key: int, value) -> int:
        idx = self._hash(key)
        probes = 0
        first_tombstone = -1

        while self.keys[idx] is not None:
            probes += 1
            if self.keys[idx] is self.tombstone_obj:
                if first_tombstone == -1:
                    first_tombstone = idx
            elif self.keys[idx] == key:
                self.values[idx] = value
                return probes
            idx = (idx + 1) & self.mask
            if probes >= self.capacity:
                raise Exception("Hash table full")

        target_idx = first_tombstone if first_tombstone != -1 else idx
        if first_tombstone == -1:
            self.size += 1

        self.keys[target_idx] = key
        self.values[target_idx] = value
        return probes

    def get(self, key: int) -> tuple[any, int]:
        idx = self._hash(key)
        probes = 0

        while self.keys[idx] is not None:
            probes += 1
            if self.keys[idx] is not self.tombstone_obj and self.keys[idx] == key:
                return self.values[idx], probes
            idx = (idx + 1) & self.mask
            if probes >= self.capacity:
                break
        return None, probes