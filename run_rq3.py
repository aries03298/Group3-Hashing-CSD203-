import csv
from data_generator import DataGenerator
from utils.metrics import measure_execution_time_and_probes
from hash_tables.linear_probing import Linear_Probing_Hash_Table
from hash_tables.no_perturb import No_Perturb_Hash_Table
from hash_tables.perturbation import Perturbation_Probing_Hash_Table
from utils.cluster_analyzer import analyze_clusters
capacity = 2**18
results = []
for alpha in [0.50, 0.66]:
    n = int(capacity * alpha)
    datasets = {"K1": DataGenerator.generate_k1_random(n), "K2": DataGenerator.generate_k2_sequential(n), "K3": DataGenerator.generate_k3_timestamp(n), "K4": DataGenerator.generate_k4_power_of_two(n)}
    for name, keys in datasets.items():
        lp = Linear_Probing_Hash_Table(capacity=capacity)
        if not hasattr(lp, 'put'): lp.put = lp.insert
        tables = {"Linear Probing": lp, "No-Perturb": No_Perturb_Hash_Table(capacity=capacity), "Perturbation Probing": Perturbation_Probing_Hash_Table(capacity=capacity)}
        for algo, ht in tables.items():
            t_ns, probes = measure_execution_time_and_probes(ht, keys)
            c = analyze_clusters(ht)
            results.append({"Dataset": name, "Load Factor": alpha, "Algorithm": algo, "Keys": n, "Probes": probes, "Time_ns": t_ns, "Max Cluster": c["max_cluster_size"], "Avg Cluster": c["avg_cluster_size"]})
with open("rq3_results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)
print("Done")