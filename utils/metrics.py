import time

def measure_execution_time_and_probes(hash_table, keys, is_lookup: bool = False):
    """Đo thời gian thực thi ns và tổng số lượt dò"""
    total_probes = 0
    start_time = time.perf_counter_ns()
    
    if is_lookup:
        for k in keys:
            _, probes = hash_table.get(k)
            total_probes += probes
    else:
        for k in keys:
            probes = hash_table.put(k, 1)
            total_probes += probes
            
    end_time = time.perf_counter_ns()
    elapsed_time_ns = end_time - start_time
    
    return elapsed_time_ns, total_probes