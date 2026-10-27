import csv
import os

import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, "rq1_results.csv"), encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

SIZES = sorted({int(r["M"]) for r in rows})
ALGORITHMS = ["Chaining", "Linear", "Double"]
MARKERS = {"Chaining": "o", "Linear": "s", "Double": "^"}


def draw(hit_col, miss_col, hit_label, miss_label, filename):
    fig, axes = plt.subplots(2, len(SIZES), figsize=(12, 7), sharey="row")

    for col, M in enumerate(SIZES):
        for row, (column, label) in enumerate(
            [(hit_col, hit_label), (miss_col, miss_label)]
        ):
            ax = axes[row][col]

            for name in ALGORITHMS:
                points = sorted(
                    (float(r["alpha"]), float(r[column]))
                    for r in rows
                    if r["algorithm"] == name and int(r["M"]) == M
                )
                ax.plot(
                    [p[0] for p in points],
                    [p[1] for p in points],
                    marker=MARKERS[name],
                    label=name,
                )

            if row == 1:
                ax.set_yscale("log")
                ax.set_xlabel("Hệ số tải α")
            if col == 0:
                ax.set_ylabel(label)

            ax.set_title("M = 2^%d" % (M.bit_length() - 1))
            ax.grid(True, alpha=0.3)

    axes[0][0].legend()
    fig.tight_layout()
    fig.savefig(os.path.join(ROOT, filename), dpi=150)
    plt.close(fig)


draw("hit_probes", "miss_probes",
     "Lượt dò TB (tìm thấy)", "Lượt dò TB (không thấy, log)",
     "rq1_probes.png")

draw("hit_us", "miss_us",
     "Thời gian mỗi get, µs (tìm thấy)", "Thời gian mỗi get, µs (không thấy, log)",
     "rq1_time.png")

print("Đã lưu: rq1_probes.png, rq1_time.png")
