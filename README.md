# 📚 Đề tài 2: Bảng băm cho khóa có quy luật & Dò nhiễu loạn trong Python Dict

* **Học phần:** CSD203 (Data Structures and Algorithms with Python)
* **Lớp:** AI21B — FA26

---

## 🚀 Tổng quan dự án
Dự án này thực hiện khảo sát thực nghiệm các phương pháp giải quyết đụng độ trong Bảng băm (Hash Tables) và tìm hiểu sâu cơ chế **Dò nhiễu loạn (Perturbation Probing)** được sử dụng trong mã nguồn lõi CPython (`dictobject.c`). 

Đối với các số nguyên có kích thước nhỏ và vừa trong Python, mã băm thỏa mãn tính chất `hash(k) == k`. Khi gặp các tập khóa có quy luật (như chuỗi tăng dần, timestamp, bước nhảy lũy thừa của 2), các cơ chế dò truyền thống dễ bị suy biến hiệu năng do hiện tượng kết chùm nguyên phát (Primary Clustering). Dự án này tiến hành cài đặt thủ công và so sánh hiệu năng giữa:
1. **Separate Chaining** (Nối kết ngoài)
2. **Linear Probing** (Dò tuyến tính có sử dụng cơ chế `Tombstone`)
3. **Perturbation Probing** (Dò nhiễu loạn chuẩn của CPython Dict)

---

## 📂 Cấu trúc thư mục dự án

```text
Group3-Hashing-CSD203/
├── data_generator.py          # Module sinh 4 họ khóa (K1, K2, K3, K4)
├── hash_tables/               # Thư mục chứa các cài đặt Bảng băm
│   ├── __init__.py
│   ├── base.py                # Lớp cơ sở (Interface chung)
│   ├── chaining.py            # Cài đặt Separate Chaining
│   ├── linear_probing.py      # Cài đặt Linear Probing (có Tombstone)
│   └── perturbation.py        # Cài đặt Dò nhiễu loạn CPython Dict
├── experiments/               # Các kịch bản chạy thực nghiệm
│   ├── __init__.py
│   ├── run_rq1.py             # Thí nghiệm RQ1: Khảo sát hệ số tải α và kích thước M
│   ├── run_rq2.py             # Thí nghiệm RQ2: Khảo sát 4 họ khóa K1 - K4
│   └── run_rq3.py             # Thí nghiệm RQ3: Đánh giá cơ chế Dò nhiễu loạn
├── utils/                     # Các công cụ hỗ trợ tính toán và vẽ đồ thị
│   ├── metrics.py             # Đo thời gian execution time & đếm số lượt dò (probes)
│   └── plotter.py             # Trực quan hóa dữ liệu bằng Matplotlib / Seaborn
├── main.py                    # File điểm vào (Entry point) điều khiển chương trình
├── requirements.txt           # Danh sách thư viện phụ thuộc (matplotlib, pandas, numpy...)
└── README.md                  # Tài liệu hướng dẫn dự án
