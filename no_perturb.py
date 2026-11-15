TOMBSTONE = "TOMBSTONE"


class No_Perturb_Hash_Table:
    """Giống dict của CPython nhưng BỎ perturb: i = (5*i + 1) & mask.

    Dùng để đối chứng: khóa cùng ô băm đầu sẽ đi theo đúng một chuỗi dò.
    Số lượt dò đếm từ 1 và tính cả ô cuối cùng được xét.
    """

    def __init__(self, capacity=2**18):
        if capacity <= 0 or capacity & (capacity - 1):
            raise ValueError("capacity phải là lũy thừa của 2")
        self.capacity = capacity
        self.mask = capacity - 1
        self.slots = [None] * capacity
        self.keys = self.slots
        self.values = [None] * capacity
        self.count = 0
        self.size = 0

    def _next(self, i):
        return (5 * i + 1) & self.mask

    def put(self, key, value):
        i = hash(key) & self.mask
        first_tombstone = -1
        probes = 1
        while self.slots[i] is not None:
            slot = self.slots[i]
            if isinstance(slot, str) and slot == TOMBSTONE:
                if first_tombstone == -1:
                    first_tombstone = i
            elif slot == key:
                self.values[i] = value
                return probes
            if probes >= self.capacity:
                if first_tombstone == -1:
                    raise OverflowError("Bảng băm đã đầy")
                i = first_tombstone
                break
            i = self._next(i)
            probes += 1
        if first_tombstone != -1:
            i = first_tombstone
        self.slots[i] = key
        self.values[i] = value
        self.count += 1
        self.size = self.count
        return probes

    def lookup(self, key):
        i = hash(key) & self.mask
        probes = 1
        while self.slots[i] is not None:
            slot = self.slots[i]
            if not (isinstance(slot, str) and slot == TOMBSTONE) and slot == key:
                return self.values[i], probes
            if probes >= self.capacity:
                return None, probes
            i = self._next(i)
            probes += 1
        return None, probes

    get = lookup
