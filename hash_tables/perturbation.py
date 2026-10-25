class Perturbation_Probing_Hash_Table:
    def __init__(self, capacity: int = 2**18):
        self.capacity = capacity
        self.mask = capacity - 1
        self.slots = [None] * capacity  
        self.values = [None] * capacity
        self.slots = self.keys
        self.tombstone_obj = object()
        self.size = 0
    def put(self, key: int, value) -> int:
        h = hash(key)
        idx = h & self.mask
        probes = 0
        first_tombstone = -1
        perturb = h
        while self.keys[idx] is not None:
            probes += 1
            if self.keys[idx] is self.tombstone_obj:
                if first_tombstone == -1:
                    first_tombstone = idx
            elif self.keys[idx] == key:
                self.values[idx] = value
                return probes
            idx = (5 * idx + 1 + perturb) & self.mask
            perturb >>= 5
            if probes >= self.capacity:
                raise Exception("Hash table full")
        target_idx = first_tombstone if first_tombstone != -1 else idx
        if first_tombstone == -1:
            self.size += 1
        self.keys[target_idx] = key
        self.values[target_idx] = value
        return probes
    def get(self, key: int) -> tuple[any, int]:
        h = hash(key)
        idx = h & self.mask
        probes = 0
        perturb = h
        while self.keys[idx] is not None:
            probes += 1
            if self.keys[idx] is not self.tombstone_obj and self.keys[idx] == key:
                return self.values[idx], probes
            idx = (5 * idx + 1 + perturb) & self.mask
            perturb >>= 5
            if probes >= self.capacity:
                break
        return None, probes
