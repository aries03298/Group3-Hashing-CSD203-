import random

# K1: số ngẫu nhiên 60-bit, không trùng nhau (dữ liệu bình thường, làm mốc so sánh)
def k1_random(n, max_val = 2**60 - 1):
    return random.sample(range(1, max_val), n)

# K2: số liên tiếp 1000, 1001, 1002... (mỗi khóa một ô liền kề)
def k2_sequential(n, start=1000):
    return list(range(start, start + n))

# K3: timestamp mili giây, mỗi khóa cách nhau 1000 = 1 giây
def k3_timestamp(n, start=1700000000000, step=1000):
    danh_sach = []
    for i in range(n):
        khoa = start + i * step
        danh_sach.append(khoa)
    return danh_sach

# K4: bước nhảy 4096 = 2^12 (khóa dồn vào rất ít ô, tệ nhất)
def k4_power_of_two(n, start=0, step=4096):
    danh_sach = []
    for i in range(n):
        khoa = start + i * step
        danh_sach.append(khoa)
    return danh_sach

#Chay thu
#print(k1_random(3))
#print(k2_sequential(5))
#print(k3_timestamp(3))
#print(k4_power_of_two(4))
