import time

def measure(hash_table, keys, is_lookup=False):
    tong_luot_do = 0
    bat_dau = time.perf_counter_ns()
    
    if is_lookup:
        for k in keys:
            luot_do = hash_table.get(k)[1]
            tong_luot_do += luot_do
    
    else:
        for k in keys:
            luot_do = hash_table.put(k, 1)
            tong_luot_do += luot_do
            
    ket_thuc = time.perf_counter_ns()
    thoi_gian = ket_thuc - bat_dau
    return thoi_gian, tong_luot_do
