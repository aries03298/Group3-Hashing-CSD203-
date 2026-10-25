import random

class DataGenerator:
    @staticmethod
    def generate_k1_random(n: int, max_val: int = 2**60 - 1) -> list[int]:
        """K1: Họ khóa ngẫu nhiên 60-bit"""
        return random.sample(range(1, max_val), n) if n < max_val else [random.randint(1, max_val) for _ in range(n)]

    @staticmethod
    def generate_k2_sequential(n: int, start: int = 1000) -> list[int]:
        """K2: Họ khóa có chuỗi tăng dần liên tiếp (Sequential)"""
        return list(range(start, start + n))

    @staticmethod
    def generate_k3_timestamp(n: int, step: int = 1000, start: int = 1700000000000) -> list[int]:
        """K3: Họ khóa Timestamp (bội số của 1000)"""
        return [start + i * step for i in range(n)]

    @staticmethod
    def generate_k4_power_of_two(n: int, step: int = 4096, start: int = 0) -> list[int]:
        """K4: Họ khóa có bước nhảy lũy thừa (4096 = 2^12)"""
        return [start + i * step for i in range(n)]