class No_Perturb_Hash_Table:
    def __init__(self, capacity=2**18):
        self.capacity = capacity
        self.mask = capacity - 1
        self.slots = [None] * capacity
        self.values = [None] * capacity
        self.count = 0
    def _hash(self, key):
        return hash(key)
    def put(self, key, value):
        hash_val = self._hash(key)
        i = hash_val & self.mask
        probes = 1
        while self.slots[i] is not None and self.slots[i] != "TOMBSTONE":
            if self.slots[i] == key:
                self.values[i] = value
                return probes
            i = (i + 1) & self.mask
            probes += 1
            if probes > self.capacity:  
                raise Exception("Hash table full")
        self.slots[i] = key
        self.values[i] = value
        self.count += 1
        return probes
    def lookup(self, key):
        hash_val = self._hash(key)
        i = hash_val & self.mask
        probes = 1
        while self.slots[i] is not None:
            if self.slots[i] == key:
                return self.values[i], probes
            i = (i + 1) & self.mask
            probes += 1
        return None, probes