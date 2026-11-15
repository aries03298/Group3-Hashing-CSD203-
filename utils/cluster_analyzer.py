def analyze_clusters(hash_table, wrap=False):
    slots = hash_table.slots
    tomb = getattr(hash_table, "tombstone_obj", None)
    def occupied(item):
        if item is None or item is tomb:
            return False
        return not (isinstance(item, str) and item == "TOMBSTONE")
    flags = [occupied(x) for x in slots]
    clusters = []
    current = 0
    for f in flags:
        if f:
            current += 1
        elif current > 0:
            clusters.append(current)
            current = 0
    if current > 0:
        # Cụm cuối nối vòng với cụm đầu nếu ô 0 cũng có khóa.
        if wrap and flags[0] and len(clusters) > 0 and current != len(flags):
            clusters[0] += current
        else:
            clusters.append(current)
    max_cluster = max(clusters) if clusters else 0
    avg_cluster = sum(clusters) / len(clusters) if clusters else 0.0
    return {"clusters": clusters, "total_clusters": len(clusters),
            "max_cluster_size": max_cluster, "avg_cluster_size": avg_cluster}
