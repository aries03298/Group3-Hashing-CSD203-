class Perturbation_Probing_Hash_Table:
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.mask = capacity - 1
        self.slots = [None] * capacity  
        self.values = [None] * capacity
        self.count = 0

    def _hash(self, key):
        return hash(key)

    def insert(self, key, value):
        hash_val = self._hash(key)
        perturb = hash_val if hash_val >= 0 else -hash_val
        i = hash_val & self.mask
        
        probes = 1
        first_tombstone = -1

        for _ in range(self.capacity):
            if self.slots[i] is None:
                target = first_tombstone if first_tombstone != -1 else i
                self.slots[target] = key
                self.values[target] = value
                self.count += 1
                return probes

            if self.slots[i] == key:
                self.values[i] = value
                return probes

            if self.slots[i] == "TOMBSTONE":
                if first_tombstone == -1:
                    first_tombstone = i

            perturb >>= 5
            i = (5 * i + perturb + 1) & self.mask
            probes += 1

        if first_tombstone != -1:
            self.slots[first_tombstone] = key
            self.values[first_tombstone] = value
            self.count += 1
            return probes

        raise OverflowError("Bảng băm đã đầy hoàn toàn!")

    def lookup(self, key):
        hash_val = self._hash(key)
        perturb = hash_val if hash_val >= 0 else -hash_val
        i = hash_val & self.mask
        probes = 1

        for _ in range(self.capacity):
            if self.slots[i] is None:
                return None, probes
            if self.slots[i] == key:
                return self.values[i], probes
            perturb >>= 5
            i = (5 * i + perturb + 1) & self.mask
            probes += 1

        return None, probes

    def remove(self, key):
        hash_val = self._hash(key)
        perturb = hash_val if hash_val >= 0 else -hash_val
        i = hash_val & self.mask

        for _ in range(self.capacity):
            if self.slots[i] is None:
                return False
            if self.slots[i] == key:
                self.slots[i] = "TOMBSTONE"
                self.values[i] = None
                self.count -= 1
                return True
            perturb >>= 5
            i = (5 * i + perturb + 1) & self.mask

        return False