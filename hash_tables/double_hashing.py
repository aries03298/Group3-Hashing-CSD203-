class DoubleHashingHashTable:
    """Bảng băm kép (Double Hashing), địa chỉ mở.

    Quy ước đếm lượt dò giống LinearProbingHashTable: probes = số ô đã xem,
    tính cả ô cuối cùng (ô trống hoặc ô chứa khóa cần tìm).
    """

    def __init__(self, capacity=2**18):
        if capacity <= 0 or capacity & (capacity - 1):
            raise ValueError("capacity phải là lũy thừa của 2")

        self.capacity = capacity
        self.mask = capacity - 1
        self.keys = [None] * capacity
        self.values = [None] * capacity
        self.size = 0

    def _hash1(self, key):
        # Ô xuất phát (giống Linear Probing).
        return hash(key) & self.mask

    def _hash2(self, key):
        # Độ dài bước. "| 1" ép thành số lẻ để bước đi hết mọi ô
        # (bảng có số ô là lũy thừa của 2).
        return (hash(key) % self.mask) | 1

    def put(self, key, value):
        i = self._hash1(key)
        step = self._hash2(key)

        for probes in range(1, self.capacity + 1):
            if self.keys[i] is None:            # ô trống: thêm vào đây
                self.keys[i] = key
                self.values[i] = value
                self.size += 1
                return probes

            if self.keys[i] == key:             # đã có khóa: ghi đè
                self.values[i] = value
                return probes

            i = (i + step) & self.mask          # nhảy một bước dài

        raise OverflowError("Bảng băm đã đầy")

    def get(self, key):
        i = self._hash1(key)
        step = self._hash2(key)

        for probes in range(1, self.capacity + 1):
            if self.keys[i] is None:
                return None, probes

            if self.keys[i] == key:
                return self.values[i], probes

            i = (i + step) & self.mask

        return None, self.capacity
