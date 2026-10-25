import random
import unittest
from hash_tables.linear_probing import LinearProbingHashTable


class TestLinearProbing(unittest.TestCase):
    def test_delete_and_update(self):
        t = LinearProbingHashTable(8)
        for key in [0, 8, 16]:
            t.put(key, key)
        self.assertTrue(t.remove(8)[0])
        self.assertEqual(t.get(16)[0], 16)
        t.put(16, 99)
        self.assertEqual(t.get(16)[0], 99)
        self.assertEqual(t.size, 2)
        self.assertEqual(t.keys.count(16), 1)
        t.put(24, 100)
        self.assertEqual(t.keys[1], 24)
        self.assertEqual(t.size, 3)

    def test_remove_missing(self):
        t = LinearProbingHashTable(8)
        t.put(0, 1)
        before = (t.keys.copy(), t.values.copy(), t.states.copy(), t.size)
        self.assertFalse(t.remove(8)[0])
        self.assertEqual(before, (t.keys, t.values, t.states, t.size))

    def test_wraparound(self):
        t = LinearProbingHashTable(8)
        for key in [7, 15, 23]:
            t.put(key, key)
        self.assertEqual([t.keys[7], t.keys[0], t.keys[1]], [7, 15, 23])
        self.assertEqual(t.get(23), (23, 3))
        self.assertEqual(t.max_cluster(), 3)

    def test_trace(self):
        t = LinearProbingHashTable(16)
        for probes, key in enumerate([0, 16, 32, 48], 1):
            self.assertEqual(t.put(key, key), probes)
            self.assertEqual(t.get(key), (key, probes))
        self.assertEqual(t.keys[:4], [0, 16, 32, 48])

    def test_full(self):
        t = LinearProbingHashTable(2)
        t.put(0, 10)
        t.put(1, 20)
        self.assertEqual(t.get(2), (None, 2))
        self.assertIsNone(t.get_value(2))
        with self.assertRaises(OverflowError):
            t.put(2, 30)
        t.remove(0)
        t.put(2, 30)
        self.assertEqual(t.get(2)[0], 30)
        self.assertEqual(t.size, 2)
        self.assertEqual(t.max_cluster(), 2)

    def test_empty_and_capacity(self):
        t = LinearProbingHashTable(8)
        self.assertEqual(t.get(0), (None, 1))
        self.assertEqual(t.max_cluster(), 0)
        self.assertEqual(t.put(0, 0), 1)
        with self.assertRaises(ValueError):
            LinearProbingHashTable(7)

    def test_fuzzing(self):
        rng = random.Random(42)
        t = LinearProbingHashTable(1024)
        oracle = {}
        operations = ['put'] * 40000 + ['get'] * 40000 + ['remove'] * 20000
        rng.shuffle(operations)
        actual_check = expected_check = 0
        for operation in operations:
            # 512 possible keys prevent overflow; mixed buckets cause collisions.
            x = rng.randrange(512)
            key = x * 1024 if x % 2 else x
            if operation == 'put':
                value = rng.randrange(1000000)
                t.put(key, value)
                oracle[key] = value
                self.assertEqual(t.get(key)[0], oracle[key])
            elif operation == 'get':
                value = t.get(key)[0]
                expected = oracle.get(key)
                self.assertEqual(value, expected)
                actual_check += 1 if value is None else value
                expected_check += 1 if expected is None else expected
            else:
                self.assertEqual(t.remove(key)[0], key in oracle)
                oracle.pop(key, None)
                self.assertIsNone(t.get(key)[0])
            self.assertEqual(t.get_value(key), oracle.get(key))
            self.assertEqual(t.size, len(oracle))
        self.assertEqual(actual_check % 2**64, expected_check % 2**64)
        for key, value in oracle.items():
            self.assertEqual(t.get(key)[0], value)
        print('Fuzzing: 100000 operations passed; checksum =', actual_check % 2**64)


if __name__ == '__main__':
    unittest.main()
