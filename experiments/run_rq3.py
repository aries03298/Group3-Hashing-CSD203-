import csv
from hash_tables.linear_probing import Linear_Probing_Hash_Table
from hash_tables.no_perturb import No_Perturb_Hash_Table
from hash_tables.perturbation import Perturbation_Probing_Hash_Table
from utils.cluster_analyzer import analyze_clusters
capacity = 2048
keys = [i * capacity for i in range(1000)]
tables = {"Linear Probing": Linear_Probing_Hash_Table(capacity), "No-Perturb": No_Perturb_Hash_Table(capacity), "Perturbation Probing": Perturbation_Probing_Hash_Table(capacity)}
results = []
for name, table in tables.items():
    probes = 0
    for k in keys:
        if hasattr(table, "insert"):
            p = table.insert(k, k)
        elif hasattr(table, "put"):
            p = table.put(k, k)
        else:
            p = 1
        probes += p if isinstance(p, int) else 1
    clusters = analyze_clusters(table)
    results.append({"Algorithm": name, "Probes": probes, "Max Cluster": clusters["max_cluster_size"], "Avg Cluster": clusters["avg_cluster_size"]})
with open("rq3_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Algorithm", "Probes", "Max Cluster", "Avg Cluster"])
    writer.writeheader()
    writer.writerows(results)
