import csv
import numpy as np
import matplotlib.pyplot as plt

# 1. Đọc dữ liệu từ file rq3_results.csv
data = []
with open("rq3_results.csv", mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append({
            "Algorithm": row["Algorithm"],
            "Load Factor": float(row["Load Factor"]),
            "Key Family": row["Key Family"],
            "Insert Probes (Avg)": float(row["Insert Probes (Avg)"]),
            "Miss Probes (Avg)": float(row["Miss Probes (Avg)"]),
            "Max Cluster": int(row["Max Cluster"]),
            "Avg Cluster": float(row["Avg Cluster"])
        })

algorithms = ["Linear Probing", "No-Perturb", "Perturbation Probing"]
key_families = ["K1", "K2", "K3", "K4"]
load_factors = [0.5, 0.66]
colors = ["#e74c3c", "#f39c12", "#2ecc71"]  # Đỏ, Cam, Xanh lá

def plot_metric(metric_name, ylabel, filename, use_log=True):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    fig.suptitle(f"So sánh {metric_name} trên 4 họ khóa (K1 - K4)", fontsize=15, fontweight="bold")

    x = np.arange(len(key_families))
    width = 0.25

    for idx, lf in enumerate(load_factors):
        ax = axes[idx]
        for i, algo in enumerate(algorithms):
            values = [
                 next(
                    (d[metric_name] for d in data 
                     if d["Algorithm"] == algo and d["Load Factor"] == lf and d["Key Family"] == kf),
                    0
                )
                for kf in key_families
            ]
            bars = ax.bar(x + (i - 1) * width, values, width, label=algo, color=colors[i], edgecolor="black")
            
            # Ghi số liệu trực tiếp lên đầu mỗi cột
            for bar in bars:
                h = bar.get_height()
                if h > 0:
                    label_text = f"{int(h)}" if h >= 10 else f"{h:.2f}"
                    ax.annotate(
                        label_text,
                        xy=(bar.get_x() + bar.get_width() / 2, h),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=8, rotation=0
                    )

        ax.set_title(f"Load Factor α = {lf}", fontsize=12, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels(key_families, fontsize=11)
        ax.set_xlabel("Họ khóa (Key Family)", fontsize=11)
        if idx == 0:
            ax.set_ylabel(ylabel, fontsize=11)
        if use_log:
            ax.set_yscale("log")
            ax.set_ylabel(f"{ylabel} (Thang đo Log)", fontsize=11)
        ax.grid(axis="y", linestyle="--", alpha=0.6)
        ax.legend(fontsize=10)

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"-> Đã xuất biểu đồ thành công: {filename}")

print("=" * 60)
print("ĐANG VẼ VÀ XUẤT BIỂU ĐỒ RQ3...")
print("=" * 60)

# Xuất 3 biểu đồ quan trọng nhất cho báo cáo RQ3
plot_metric("Insert Probes (Avg)", "Số lượt dò trung bình (Probes)", "rq3_insert_probes.png", use_log=True)
plot_metric("Miss Probes (Avg)", "Số lượt dò thất bại trung bình (Probes)", "rq3_miss_probes.png", use_log=True)
plot_metric("Max Cluster", "Kích thước cụm lớn nhất (Max Cluster)", "rq3_max_cluster.png", use_log=True)

print("Hoàn tất! Bạn hãy kiểm tra 3 file ảnh .png ở cột bên trái.")