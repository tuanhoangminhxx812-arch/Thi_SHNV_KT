# 📝 Ứng Dụng Ôn Tập Trắc Nghiệm - Sát Hạch Nghiệp Vụ Tài Chính Kế Toán 2025

Ứng dụng học tập trắc nghiệm được xây dựng bằng **Streamlit + Python**, hỗ trợ ôn tập sát hạch nghiệp vụ Tài chính Kế toán cho cán bộ nhân viên.

---

## 🎯 Tính năng chính

| Tính năng | Mô tả |
|-----------|-------|
| **2 đối tượng thi** | Kế toán trưởng, Trưởng-Phó phòng & Chuyên viên |
| **9 chủ đề** | KTT-130, CV-120, Tổng hợp, Thuế, QC chi tiêu nội bộ, Quản trị rủi ro, ERP, Kế toán, Chế độ kế toán TT99 |
| **Trắc nghiệm từng câu** | Hiển thị 1 câu/trang, phản hồi đúng/sai ngay lập tức |
| **Xáo trộn ngẫu nhiên** | Thứ tự câu hỏi random mỗi lần làm bài |
| **Chấm điểm** | Tính %, ngưỡng đạt ≥ 70% |
| **Xem lại bài làm** | Bảng chi tiết đúng/sai sau khi hoàn thành |
| **Giao diện đẹp** | Font Times New Roman, sidebar gradient, progress bar |

---

## 📁 Cấu trúc thư mục

```
Thi_SHNV_KT/
├── app.py                          # Ứng dụng Streamlit chính
├── requirements.txt                # Danh sách thư viện cần cài
├── README.md                       # File hướng dẫn (file này)
├── Đề thi...kế toán trường...xls   # Bộ đề KTT / Trưởng-Phó phòng
└── Đề thi...chuyên viên.xls        # Bộ đề Chuyên viên
```

---

## 🚀 Hướng dẫn cài đặt và chạy

### 1. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 2. Chạy ứng dụng

```bash
streamlit run app.py
```

### 3. Mở trình duyệt

Truy cập địa chỉ: **http://localhost:8501**

---

## 🖥️ Hướng dẫn sử dụng

1. **Chọn đối tượng thi**: Dropdown ở sidebar trái → chọn "Kế toán trưởng, Trưởng-Phó phòng" hoặc "Chuyên viên"
2. **Chọn chủ đề**: Bấm vào 1 trong 9 chủ đề ở sidebar
3. **Làm bài**: Chọn đáp án A/B/C/D → Bấm "Trả lời"
4. **Xem phản hồi**: 
   - ✅ Đúng → Thông báo xanh
   - ❌ Sai → Thông báo đỏ + hiển thị đáp án đúng
5. **Bấm "Câu tiếp theo"** để sang câu kế
6. **Hoàn thành**: Xem bảng điểm + chi tiết bài làm
7. **Làm lại**: Bấm "Làm lại" ở sidebar hoặc cuối bài

---

## 📊 Tiêu chí đánh giá

| Kết quả | Điều kiện |
|---------|-----------|
| 🟢 **ĐẠT** | Trả lời đúng ≥ 70% tổng số câu |
| 🔴 **CHƯA ĐẠT** | Trả lời đúng < 70% tổng số câu |

---

## 🛠️ Yêu cầu hệ thống

- Python 3.8+
- Các thư viện: `streamlit`, `pandas`, `xlrd`
- Trình duyệt web (Chrome, Edge, Firefox...)

---

## 📌 Ghi chú

- Dữ liệu câu hỏi được đọc trực tiếp từ 2 file Excel `.xls` đi kèm
- Câu hỏi được xáo trộn ngẫu nhiên mỗi lần làm bài để tăng hiệu quả ôn tập
- Thứ tự đáp án giữ nguyên như file gốc
- Font chữ: Times New Roman, cỡ 12pt
