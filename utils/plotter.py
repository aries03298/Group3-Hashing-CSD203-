import csv
import matplotlib.pyplot as plt


def plot(filename, column):
    with open(filename, encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    for name, offset in [("Chaining", -0.2), ("Linear", 0.2)]:
        values = [
            float(row[column])
            for row in rows
            if row["algorithm"] == name
        ]

        positions = [i + offset for i in range(4)]
        plt.bar(positions, values, width=0.4, label=name)

    plt.xticks(range(4), ["K1", "K2", "K3", "K4"])
    plt.title(column)
    plt.ylabel(column)
    plt.legend()
    plt.tight_layout()
    plt.savefig(column + ".png")
    plt.close()


plot("rq2_count.csv", "hit_probes")
plot("rq2_count.csv", "miss_probes")
plot("rq2_time.csv", "hit_us")
plot("rq2_time.csv", "miss_us")
plot("rq2_time.csv", "build_ms")

print("Đã lưu 5 biểu đồ PNG")