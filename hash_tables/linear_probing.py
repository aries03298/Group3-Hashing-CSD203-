EMPTY = 0
OCCUPIED = 1
TOMBSTONE = 2


class LinearProbingHashTable:
    def __init__(self, capacity=2**18):
        if capacity <= 0 or capacity & (capacity - 1):
            raise ValueError("capacity phải là lũy thừa của 2")

        self.capacity = capacity
        self.mask = capacity - 1

        self.keys = [None] * capacity
        self.values = [None] * capacity
        self.states = [EMPTY] * capacity

        self.size = 0
        self.slots = self.keys

    def _hash(self, key):
        return hash(key) & self.mask

    def put(self, key, value):
        i = self._hash(key)
        first_tombstone = -1

        for probes in range(1, self.capacity + 1):

            if self.states[i] == OCCUPIED:
                if self.keys[i] == key:
                    self.values[i] = value
                    return probes

            elif self.states[i] == TOMBSTONE:
                if first_tombstone == -1:
                    first_tombstone = i

            else:
                if first_tombstone != -1:
                    i = first_tombstone

                self.keys[i] = key
                self.values[i] = value
                self.states[i] = OCCUPIED
                self.size += 1

                return probes

            i = (i + 1) & self.mask

        if first_tombstone != -1:
            i = first_tombstone

            self.keys[i] = key
            self.values[i] = value
            self.states[i] = OCCUPIED
            self.size += 1

            return self.capacity

        raise OverflowError("Bảng băm đã đầy")

    def get(self, key):
        i = self._hash(key)

        for probes in range(1, self.capacity + 1):

            if self.states[i] == EMPTY:
                return None, probes

            if self.states[i] == OCCUPIED:
                if self.keys[i] == key:
                    return self.values[i], probes

            i = (i + 1) & self.mask

        return None, self.capacity

    def remove(self, key):
        i = self._hash(key)

        for probes in range(1, self.capacity + 1):

            if self.states[i] == EMPTY:
                return False, probes

            if self.states[i] == OCCUPIED:
                if self.keys[i] == key:
                    self.keys[i] = None
                    self.values[i] = None
                    self.states[i] = TOMBSTONE
                    self.size -= 1

                    return True, probes

            i = (i + 1) & self.mask

        return False, self.capacity

    def get_value(self, key):
        i = self._hash(key)
        start = i

        while True:
            if self.states[i] == EMPTY:
                return None

            if self.states[i] == OCCUPIED:
                if self.keys[i] == key:
                    return self.values[i]

            i = (i + 1) & self.mask
            if i == start:
                return None

    def max_cluster(self):
        if self.size == self.capacity:
            return self.capacity

        start = 0

        while self.states[start] == OCCUPIED:
            start += 1

        longest = 0
        current = 0

        for step in range(1, self.capacity + 1):
            i = (start + step) & self.mask

            if self.states[i] == OCCUPIED:
                current += 1
                longest = max(longest, current)
            else:
                current = 0

        return longest

