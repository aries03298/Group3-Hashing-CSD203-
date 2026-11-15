# 📚 Đề tài 2: Bảng băm cho khóa có quy luật & Dò nhiễu loạn trong Python Dict

* **Học phần:** CSD203 (Data Structures and Algorithms with Python)
* **Lớp:** AI21B — FA26

---

## 🚀 Tổng quan dự án
Dự án này thực hiện khảo sát thực nghiệm các phương pháp giải quyết đụng độ trong Bảng băm (Hash Tables) và tìm hiểu sâu cơ chế **Dò nhiễu loạn (Perturbation Probing)** được sử dụng trong mã nguồn lõi CPython (`dictobject.c`).

Đối với các số nguyên có kích thước nhỏ và vừa trong Python, mã băm thỏa mãn tính chất `hash(k) == k`. Khi gặp các tập khóa có quy luật (như chuỗi tăng dần, timestamp, bước nhảy lũy thừa của 2), các cơ chế dò truyền thống dễ bị suy biến hiệu năng do hiện tượng kết chùm nguyên phát (Primary Clustering). Dự án này tiến hành cài đặt thủ công và so sánh hiệu năng giữa:
1. **Separate Chaining** (Nối kết ngoài)
2. **Linear Probing** (Dò tuyến tính có sử dụng cơ chế `Tombstone`)
3. **Double Hashing** (Băm kép)
4. **No-Perturb** (Dò kiểu CPython nhưng bỏ perturb: `i = 5i + 1`)
5. **Perturbation Probing** (Dò nhiễu loạn chuẩn của CPython Dict)

---

## 📂 Cấu trúc thư mục dự án

```text
Group3-Hashing-CSD203/
├── README.md
├── requirements.txt           # Thư viện phụ thuộc
├── main.py                    # File điểm vào
├── data_generator.py          # Sinh 4 họ khóa (K1, K2, K3, K4)
├── hash_tables/               # Các cài đặt bảng băm
│   ├── base.py                #   Lớp cơ sở (giao diện chung)
│   ├── chaining.py            #   Separate Chaining
│   ├── linear_probing.py      #   Linear Probing (có Tombstone)
│   ├── double_hashing.py      #   Double Hashing
│   ├── no_perturb.py          #   Dò i = 5i + 1 (không perturb)
│   └── perturbation.py        #   Dò nhiễu loạn kiểu CPython
├── experiments/               # Kịch bản thực nghiệm
│   ├── run_rq1.py             #   RQ1: hệ số tải α và kích thước M
│   ├── run_rq2.py             #   RQ2: 4 họ khóa K1–K4
│   └── run_rq3.py             #   RQ3: đánh giá dò nhiễu loạn
├── utils/                     # Công cụ hỗ trợ
│   ├── metrics.py             #   Đo thời gian & đếm lượt dò
│   ├── cluster_analyzer.py    #   Phân tích kích thước cụm
│   ├── plot_rq1.py            #   Vẽ biểu đồ RQ1
│   └── plotter.py             #   Vẽ biểu đồ RQ2
├── tests/
│   └── test_linear_probing.py # Kiểm thử Linear Probing
├── results/                   # Số liệu đầu ra (.csv)
└── figures/                   # Biểu đồ đầu ra (.png)
```

---

## ▶️ Cách chạy

Chạy tại thư mục gốc của dự án:

```bash
pip install -r requirements.txt

python tests/test_linear_probing.py          # kiểm thử

python experiments/run_rq1.py --family K1    # RQ1 (K1, K2, K3 hoặc K4)
python experiments/run_rq2.py --count        # RQ2: đếm lượt dò
python experiments/run_rq2.py                # RQ2: đo thời gian
python experiments/run_rq3.py                # RQ3 (thêm --consistent để mọi bảng đếm lượt dò từ 1)

python utils/plot_rq1.py                     # vẽ biểu đồ RQ1 -> figures/
python utils/plotter.py                      # vẽ biểu đồ RQ2 -> figures/
```

Số liệu được ghi vào `results/`, biểu đồ vào `figures/`.
