from hash_tables.linear_probing import LinearProbingHashTable


table = LinearProbingHashTable(8)

# 1. Thêm các khóa cùng vị trí băm ban đầu.
table.put(0, 100)
table.put(8, 200)
table.put(16, 300)

assert table.get(16) == (300, 3)

# 2. Xóa khóa giữa chuỗi, vẫn tìm được khóa phía sau.
assert table.remove(8)[0] is True
assert table.get(16)[0] == 300

# 3. Cập nhật khóa sau Tombstone, không thêm bản sao.
table.put(16, 999)

assert table.get(16)[0] == 999
assert table.size == 2

# 4. Dùng lại ô đã xóa.
table.put(24, 400)

assert table.keys[1] == 24
assert table.size == 3

# 5. Xóa khóa không có.
before = (
    table.keys.copy(),
    table.values.copy(),
    table.states.copy(),
    table.size,
)

assert table.remove(1000)[0] is False

assert before == (
    table.keys,
    table.values,
    table.states,
    table.size,
)

# 6. Dò vòng từ cuối mảng về đầu.
table = LinearProbingHashTable(8)
table.put(7, 100)
table.put(15, 200)

assert table.keys[7] == 7
assert table.keys[0] == 15

# 7. Truy vết theo đề: M = 16.
table = LinearProbingHashTable(16)

for probes, key in enumerate([0, 16, 32, 48], start=1):
    assert table.put(key, key) == probes
    print("Khóa:", key, "- số lượt dò:", probes)

assert table.keys[:4] == [0, 16, 32, 48]

print("Các test cơ bản đều đúng!")

import random

rng = random.Random(42)
table = LinearProbingHashTable(1024)
oracle = {}

# Đúng tỷ lệ: 40% thêm, 40% tìm, 20% xóa.
operations = ["put"] * 40000 + ["get"] * 40000 + ["remove"] * 20000
rng.shuffle(operations)

for operation in operations:
    # 512 khóa khác nhau để bảng không đầy.
    # Nhân 1024 để cố tình tạo đụng độ.
    key = rng.randrange(512) * 1024

    if operation == "put":
        value = rng.randrange(10000)
        table.put(key, value)
        oracle[key] = value

        assert table.get(key)[0] == oracle[key]

    elif operation == "get":
        assert table.get(key)[0] == oracle.get(key)

    else:
        existed = key in oracle
        removed, probes = table.remove(key)

        assert removed == existed
        oracle.pop(key, None)

    assert table.size == len(oracle)

# Kiểm tra lại toàn bộ khóa còn trong bảng.
for key, value in oracle.items():
    assert table.get(key)[0] == value

print("Fuzzing 100.000 thao tác: OK")