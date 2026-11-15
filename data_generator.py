import random
class DataGenerator:
    # K1: số ngẫu nhiên 60 bit, không trùng nhau (dữ liệu bình thường, làm mốc so sánh)
    @staticmethod
    def generate_k1_random(n, max_val=2**60 - 1):
        return random.sample(range(1, max_val), n)
    # K2: số liên tiếp 1000, 1001, 1002... (mỗi khóa một ô liền kề)
    @staticmethod
    def generate_k2_sequential(n, start=1000):
        return [start + i for i in range(n)]
    # K3: timestamp mili giây, mỗi khóa cách nhau 1000 = 1 giây
    @staticmethod
    def generate_k3_timestamp(n, start=1700000000000, step=1000):
        return [start + i * step for i in range(n)]
    # K4: bước nhảy 4096 = 2^12 (khóa dồn vào rất ít ô, tệ nhất)
    @staticmethod
    def generate_k4_power_of_two(n, start=0, step=4096):
        return [start + i * step for i in range(n)]
k1_random = DataGenerator.generate_k1_random
k2_sequential = DataGenerator.generate_k2_sequential
k3_timestamp = DataGenerator.generate_k3_timestamp
k4_power_of_two = DataGenerator.generate_k4_power_of_two
