import argparse
import csv
import os
import random
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from data_generator import DataGenerator
from hash_tables.chaining import SeparateChainingHashTable
from hash_tables.linear_probing import LinearProbingHashTable
from hash_tables.double_hashing import DoubleHashingHashTable

SIZES = [2**14, 2**16, 2**18]        
ALPHAS = [0.1, 0.3, 0.5, 0.7, 0.9]   
QUERIES = 100                        

GENERATORS = {
    "K1": DataGenerator.generate_k1_random,
    "K2": DataGenerator.generate_k2_sequential,
    "K3": DataGenerator.generate_k3_timestamp,
    "K4": DataGenerator.generate_k4_power_of_two,
}

ALGORITHMS = [
    ("Chaining", SeparateChainingHashTable),
    ("Linear", LinearProbingHashTable),
    ("Double", DoubleHashingHashTable),
]

parser = argparse.ArgumentParser()
parser.add_argument("--family", default="K1", choices=GENERATORS)
args = parser.parse_args()

random.seed(42)
results = []

for M in SIZES:
    for alpha in ALPHAS:
        N = int(M * alpha)
        keys = GENERATORS[args.family](N)
        hits = random.sample(keys, min(QUERIES, N))


        shift = (max(keys) // M + 1) * M
        misses = [k + shift for k in hits]

        for name, table_class in ALGORITHMS:

            start = time.perf_counter_ns()
            table = table_class(M)
            for key in keys:
                table.put(key, key)
            build_ms = (time.perf_counter_ns() - start) / 1_000_000

            probes_avg = {}
            us = {}

            for kind, queries in [("hit", hits), ("miss", misses)]:

                total = 0
                for key in queries:
                    value, probes = table.get(key)
                    if kind == "hit":
                        assert value == key
                    else:
                        assert value is None
                    total += probes
                probes_avg[kind] = total / len(queries)
              
                samples = []
                for _ in range(3):
                    start = time.perf_counter_ns()
                    for key in queries:
                        table.get(key)
                    elapsed = time.perf_counter_ns() - start
                    samples.append(elapsed / len(queries) / 1000)
                samples.sort()
                us[kind] = samples[1]

            results.append([
                args.family, name, M, alpha, N,
                round(probes_avg["hit"], 3), round(probes_avg["miss"], 3),
                round(us["hit"], 3), round(us["miss"], 3),
                round(build_ms, 2),
            ])
            print(args.family, name, "M=%d" % M, "alpha=%.1f" % alpha,
                  "| hit: %.2f lượt dò" % probes_avg["hit"],
                  "| miss: %.2f lượt dò" % probes_avg["miss"],
                  flush=True)

filename = os.path.join(ROOT, "rq1_results.csv")
with open(filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "family", "algorithm", "M", "alpha", "N",
        "hit_probes", "miss_probes", "hit_us", "miss_us", "build_ms",
    ])
    writer.writerows(results)

print("Đã lưu:", filename)
