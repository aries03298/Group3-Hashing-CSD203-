import csv
import os
import sys
import time
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# Bản số liệu gốc đếm lượt dò của Linear Probing từ 0 (số ô phải bỏ qua),
# còn No-Perturb và Perturbation đếm từ 1 (gồm cả ô cuối). Mặc định giữ đúng như vậy
# để số liệu trùng bản cũ. Chạy với --consistent để cả 3 bảng cùng đếm từ 1.
CONSISTENT = "--consistent" in sys.argv
LINEAR_OFFSET = 0 if CONSISTENT else 1

RESULTS = os.path.join(ROOT, "results")
os.makedirs(RESULTS, exist_ok=True)

from hash_tables.linear_probing import LinearProbingHashTable
from hash_tables.no_perturb import No_Perturb_Hash_Table as NoPerturbHashTable
from hash_tables.perturbation import Perturbation_Probing_Hash_Table
from utils.cluster_analyzer import analyze_clusters

random.seed(2026)  # cố định K1 để chạy lại ra cùng kết quả

print("=" * 75)
print("KHỞI CHẠY THỰC NGHIỆM RQ3: 4 HỌ KHÓA (K1-K4) VỚI M = 2^18")
print("=" * 75)

# Cấu hình theo đúng đề tài: M = 2^18
CAPACITY = 2**18
LOAD_FACTORS = [0.50, 0.66]
KEY_FAMILIES = ["K1", "K2", "K3", "K4"]

def generate_keys(family, n_keys):
    if family == "K1":
        return random.sample(range(2**60), n_keys)
    elif family == "K2":
        base = 1000000
        return [base + i for i in range(n_keys)]
    elif family == "K3":
        t0 = 1700000000
        return [(t0 + i) * 1000 for i in range(n_keys)]
    elif family == "K4":
        base = 2000000
        return [base + i * 4096 for i in range(n_keys)]
    return []

results = []

for lf in LOAD_FACTORS:
    n_keys = int(CAPACITY * lf)
    print(f"\n--- ĐANG CHẠY VỚI LOAD FACTOR = {lf} (Số lượng khóa N = {n_keys}) ---")
    
    for family in KEY_FAMILIES:
        print(f"  + Tạo dữ liệu họ khóa {family}...")
        keys = generate_keys(family, n_keys)
        absent_keys = generate_keys("K1", 1000) # 1000 khóa ngẫu nhiên để test vắng mặt
        
        tables = {
            "Linear Probing": LinearProbingHashTable(CAPACITY),
            "No-Perturb": NoPerturbHashTable(CAPACITY),
            "Perturbation Probing": Perturbation_Probing_Hash_Table(CAPACITY)
        }
        
        for name, table in tables.items():
            off = LINEAR_OFFSET if name == "Linear Probing" else 0
            # 1. Đo Probes Nạp (Insert)
            insert_probes = 0
            for k in keys:
                if hasattr(table, "insert"):
                    p = table.insert(k, k)
                elif hasattr(table, "put"):
                    p = table.put(k, k)
                else:
                    p = 1
                insert_probes += (p if isinstance(p, int) else 1) - off
            
            # 2. Đo Probes Tra cứu vắng mặt (Miss)
            miss_probes = 0
            for k in absent_keys:
                if hasattr(table, "lookup"):
                    _, p = table.lookup(k)
                else:
                    _, p = table.get(k)
                miss_probes += p - off
                
            # Đồng bộ thuộc tính để phân tích cụm
            if not hasattr(table, "slots") and hasattr(table, "keys"):
                table.slots = table.keys
                
            clusters = analyze_clusters(table)
            
            results.append({
                "Algorithm": name,
                "Load Factor": lf,
                "Key Family": family,
                "Insert Probes (Avg)": round(insert_probes / n_keys, 2),
                "Miss Probes (Avg)": round(miss_probes / len(absent_keys), 2),
                "Max Cluster": clusters["max_cluster_size"],
                "Avg Cluster": round(clusters["avg_cluster_size"], 2)
            })
            print(f"    -> {name:20s} | Kích thước cụm Max: {clusters['max_cluster_size']}")

# Xuất kết quả
with open(os.path.join(RESULTS, "rq3_results.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "Algorithm", "Load Factor", "Key Family", 
        "Insert Probes (Avg)", "Miss Probes (Avg)", 
        "Max Cluster", "Avg Cluster"
    ])
    writer.writeheader()
    writer.writerows(results)

print("\nHoàn tất! Đã lưu toàn bộ dữ liệu 4 họ khóa vào rq3_results.csv")
