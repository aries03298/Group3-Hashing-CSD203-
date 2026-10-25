import argparse
import csv
import random
import time

from data_generator import DataGenerator
from hash_tables.chaining import SeparateChainingHashTable
from hash_tables.linear_probing import LinearProbingHashTable


def max_cluster(table):
    # Tính cả cụm nối từ cuối mảng về đầu mảng.
    if table.size == table.capacity:
        return table.capacity

    start = 0
    while table.states[start] == 1:
        start += 1

    longest = 0
    current = 0

    for step in range(1, table.capacity + 1):
        i = (start + step) & table.mask

        if table.states[i] == 1:
            current += 1
            longest = max(longest, current)
        else:
            current = 0

    return longest


parser = argparse.ArgumentParser()
parser.add_argument("--count", action="store_true")
args = parser.parse_args()

random.seed(42)

M = 2**18
N = int(M * 0.66)
results = []

generators = [
    ("K1", DataGenerator.generate_k1_random),
    ("K2", DataGenerator.generate_k2_sequential),
    ("K3", DataGenerator.generate_k3_timestamp),
    ("K4", DataGenerator.generate_k4_power_of_two),
]

for family, generate in generators:
    keys = generate(N)
    hits = random.sample(keys, min(100, N))

    # Khóa vắng có cùng vị trí băm đầu với khóa có mặt.
    shift = (max(keys) // M + 1) * M
    misses = [key + shift for key in hits]

    algorithms = [
        ("Chaining", SeparateChainingHashTable),
        ("Linear", LinearProbingHashTable),
    ]

    for name, table_class in algorithms:
        print(family, name, "- đang nạp...", flush=True)

        # Thời gian tạo và nạp bảng.
        start = time.perf_counter_ns()
        table = table_class(M)

        for key in keys:
            table.put(key, key)

        build_ms = (time.perf_counter_ns() - start) / 1_000_000

        chain = ""
        cluster = ""

        if name == "Chaining":
            chain = max(len(bucket) for bucket in table.table)
        else:
            cluster = max_cluster(table)

        averages = []
        times = []
        output_check = 0

        for kind, queries in [("hit", hits), ("miss", misses)]:
            total_probes = 0

            # Kiểm tra kết quả và checksum ngoài khoảng đo.
            for key in queries:
                value, probes = table.get(key)

                if kind == "hit":
                    assert value == key
                    output_check += value
                else:
                    assert value is None
                    output_check += 1

                total_probes += probes

            if args.count:
                average = total_probes / len(queries)

                averages.append(average)
                times.append("")

                print(kind, ":", round(average, 2), "lượt dò")

            else:
                # Đo 3 lần, lấy giá trị ở giữa.
                samples = []

                for _ in range(3):
                    start = time.perf_counter_ns()

                    for key in queries:
                        table.get(key)

                    elapsed = time.perf_counter_ns() - start
                    samples.append(elapsed / len(queries) / 1000)

                samples.sort()
                microseconds = samples[1]

                averages.append("")
                times.append(microseconds)

                print(kind, ":", round(microseconds, 2), "us/get")

        output_check %= 2**64

        expected = (sum(hits) + len(misses)) % (2**64)
        assert output_check == expected

        print("Tạo và nạp bảng:", round(build_ms, 2), "ms")
        print("max_chain:", chain, "| max_cluster:", cluster)
        print("output_check:", output_check)

        results.append([
            family, name, M, N,
            averages[0], averages[1],
            times[0], times[1],
            build_ms, chain, cluster, output_check,
        ])

filename = "rq2_count.csv" if args.count else "rq2_time.csv"

with open(filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "family", "algorithm", "M", "N",
        "hit_probes", "miss_probes",
        "hit_us", "miss_us",
        "build_ms", "max_chain", "max_cluster", "output_check",
    ])

    writer.writerows(results)

print("Đã lưu:", filename)