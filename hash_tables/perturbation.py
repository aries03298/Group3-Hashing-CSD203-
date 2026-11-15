class Perturbation_Probing_Hash_Table:
    PERTURB_SHIFT = 5
    def __init__(self, capacity: int = 2**18):
        if capacity <= 0 or capacity & (capacity - 1):
            raise ValueError("capacity phải là lũy thừa của 2")
        self.capacity = capacity
        self.mask = capacity - 1
        self.keys = [None] * capacity
        self.values = [None] * capacity
        self.slots = self.keys
        self.tombstone_obj = object()
        self.size = 0
    def put(self, key, value) -> int:
        h = hash(key)
        idx = h & self.mask
        perturb = h & 0xFFFFFFFFFFFFFFFF   # số không dấu như CPython
        probes = 1
        first_tombstone = -1
        while self.keys[idx] is not None:
            if self.keys[idx] is self.tombstone_obj:
                if first_tombstone == -1:
                    first_tombstone = idx
            elif self.keys[idx] == key:
                self.values[idx] = value
                return probes
            if probes >= self.capacity:
                if first_tombstone == -1:
                    raise OverflowError("Bảng băm đã đầy")
                idx = first_tombstone
                break
            perturb >>= self.PERTURB_SHIFT
            idx = (5 * idx + perturb + 1) & self.mask
            probes += 1
        target = first_tombstone if first_tombstone != -1 else idx
        self.keys[target] = key
        self.values[target] = value
        self.size += 1
        return probes
    def get(self, key):
        h = hash(key)
        idx = h & self.mask
        perturb = h & 0xFFFFFFFFFFFFFFFF
        probes = 1
        while self.keys[idx] is not None:
            if self.keys[idx] is not self.tombstone_obj and self.keys[idx] == key:
                return self.values[idx], probes
            if probes >= self.capacity:
                return None, probes
            perturb >>= self.PERTURB_SHIFT
            idx = (5 * idx + perturb + 1) & self.mask
            probes += 1
        return None, probes
