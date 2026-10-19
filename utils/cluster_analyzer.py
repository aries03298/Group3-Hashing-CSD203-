def analyze_clusters(hash_table):
    slots = hash_table.slots
    clusters = []
    current_cluster_size = 0
    for item in slots:
        if item is not None and item != "TOMBSTONE":
            current_cluster_size += 1
        else:
            if current_cluster_size > 0:
                clusters.append(current_cluster_size)
                current_cluster_size = 0
    if current_cluster_size > 0:
        clusters.append(current_cluster_size)
    max_cluster = max(clusters) if clusters else 0
    avg_cluster = sum(clusters) / len(clusters) if clusters else 0.0
    return {"clusters": clusters, "total_clusters": len(clusters), "max_cluster_size": max_cluster, "avg_cluster_size": avg_cluster}