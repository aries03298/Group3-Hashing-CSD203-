"""Run from project root: python -m experiments.run_rq2 --count"""
import argparse
import csv
import platform
import random
import statistics
import sys
import time
from pathlib import Path

from data_generator import DataGenerator
from hash_tables.chaining import SeparateChainingHashTable
from hash_tables.linear_probing import LinearProbingHashTable


def check(table, queries, present):
    total = 0
    probes = 0
    for key in queries:
        value, count = table.get(key)
        assert value == (key if present else None)
        assert table.get_value(key) == value
        probes += count
        total += 1 if value is None else value
    return probes / len(queries), total % 2**64


def measure(table, queries, repeats):
    get = table.get_value
    for key in queries[:100]:
        get(key)
    samples = []
    for _ in range(repeats):
        start = time.perf_counter_ns()
        for key in queries:
            get(key)
        samples.append((time.perf_counter_ns() - start) / len(queries) / 1000)
    return statistics.median(samples)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--capacity', type=int, default=2**18)
    parser.add_argument('--queries', type=int, default=512)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--repeats', type=int, default=3)
    parser.add_argument('--count', action='store_true')
    parser.add_argument('--output', default=None)
    args = parser.parse_args()
    m = args.capacity
    if m < 2 or m & (m - 1) or args.queries < 1 or args.repeats < 1:
        parser.error('Use power-of-two capacity >= 2 and positive queries/repeats')
    n = int(m * 0.66)
    mode = 'count' if args.count else 'time'
    output = Path(args.output or f'results/rq2_{mode}.csv')
    output.parent.mkdir(parents=True, exist_ok=True)
    generators = [
        ('K1', lambda n: DataGenerator.generate_k1_random(n, seed=args.seed)),
        ('K2', DataGenerator.generate_k2_sequential),
        ('K3', DataGenerator.generate_k3_timestamp),
        ('K4', DataGenerator.generate_k4_power_of_two),
    ]
    fields = ['family', 'algorithm', 'query_type', 'mode', 'capacity', 'n',
              'alpha', 'seed', 'query_count', 'repeats', 'build_ms',
              'avg_probes', 'us_per_op', 'max_chain', 'max_cluster',
              'output_check', 'python', 'platform']
    with output.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for family, generator in generators:
            rng = random.Random(args.seed)
            keys = generator(n)
            hits = rng.sample(keys, min(args.queries, n))
            # set is used only to prepare queries, not to implement a table.
            existing = set(keys)
            uniform = []
            while len(uniform) < len(hits):
                key = rng.randrange(2**60)
                if key not in existing:
                    uniform.append(key)
            shift = (max(keys) // m + 1) * m
            same_bucket = [key + shift for key in hits]
            assert all(key not in existing for key in same_bucket)
            assert all(hash(a) & (m-1) == hash(b) & (m-1)
                       for a, b in zip(hits, same_bucket))
            queries = [('hit', hits), ('miss_uniform', uniform),
                       ('miss_same_bucket', same_bucket)]
            for name, cls in [('sc', SeparateChainingHashTable),
                              ('lp', LinearProbingHashTable)]:
                print(f'{family} / {name}: loading {n} keys...', flush=True)
                start = time.perf_counter_ns()
                table = cls(m)
                for key in keys:
                    table.put(key, key)
                build_ms = (time.perf_counter_ns() - start) / 1e6
                chain = max(map(len, table.table)) if name == 'sc' else ''
                cluster = table.max_cluster() if name == 'lp' else ''
                for kind, query_keys in queries:
                    probes, checksum = check(table, query_keys, kind == 'hit')
                    expected = sum(query_keys) if kind == 'hit' else len(query_keys)
                    assert checksum == expected % 2**64
                    micros = '' if args.count else measure(table, query_keys, args.repeats)
                    writer.writerow(dict(zip(fields, [
                        family, name, kind, mode, m, n, n/m, args.seed,
                        len(query_keys), args.repeats, build_ms,
                        probes if args.count else '', micros, chain, cluster,
                        checksum, sys.version.split()[0], platform.platform()
                    ])))
                    f.flush()
                    print(f'  {kind}: probes={probes:.2f}, us/op={micros}', flush=True)
    print('Saved:', output)


if __name__ == '__main__':
    main()
