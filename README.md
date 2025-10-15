#HỆ THỐNG BÃI GIỮ XE THÔNG MINH sử dụng Computer Vision và Machine Learning (có thể thay bằng yolov8)

Hệ thống đếm chỗ đỗ xe tự động sử dụng Computer Vision và Machine Learning.

## 🚀 Tính năng

- Phát hiện chỗ đỗ xe trống và đã có xe
- Hiển thị video với khung màu xanh (trống) và đỏ (có xe)
- **Đếm số lượng chỗ trống/tổng số chỗ**
- **Track số lượng xe hiện có trong bãi xe**
- **Tính toán tỷ lệ sử dụng bãi xe (Occupancy Rate)**
- **Export thống kê ra file JSON**
- Sử dụng AI để phân tích hình ảnh
- Ghi lại video đầu ra kèm overlay kết quả (output.mp4)

## 📊 Thống kê được hiển thị

- **Tổng số chỗ đỗ xe** (Total Spots)
- **Số chỗ trống** (Available Spots) - màu xanh 🟢
- **Số chỗ đã có xe** (Occupied Spots) - màu đỏ 🔴  
- **Tỷ lệ sử dụng** (Occupancy Rate) - phần trăm
- **Trạng thái bãi xe**: Good (<80%), Moderate (80-95%), Full (>95%)

## 📋 Yêu cầu hệ thống

- Python 3.7+
- Windows/Linux/macOS
- Webcam hoặc video file

## 🛠️ Cài đặt

### 1. Clone repository
```bash
git clone <repository-url>
cd IntelliPark-System
```

### 2. Cài đặt dependencies
```bash
pip install opencv-python scikit-learn pandas Pillow scikit-image matplotlib
pip install "numpy<2"  # Để tương thích với OpenCV
```

Đảm bảo các file sau có trong thư mục:
- `data/parking_1920_1080_loop.mp4` - Video mẫu
- `model/model.p` - Model AI đã train
- `mask_1920_1080.png` - Mask xác định vùng chỗ đỗ xe

## 🎯 Cách sử dụng

### Chạy với video mẫu
```bash
python main.py
```

- Cửa sổ xem trực tiếp sẽ hiển thị.
- Video đầu ra sẽ được lưu tại `./output.mp4`.

### Điều khiển
- **`q`** - Thoát chương trình
- **`e`** - Export thống kê hiện tại ra file JSON
- **`s`** - Hiển thị summary thống kê trong console

### Giao diện hiển thị
Chương trình sẽ hiển thị video với các khung màu:
- 🟢 **Xanh**: Chỗ đỗ xe trống
- 🔴 **Đỏ**: Chỗ đỗ xe đã có xe

**Thông tin thống kê hiển thị ở góc trên bên trái:**
- Tổng số chỗ đỗ xe
- Số chỗ trống / Số chỗ có xe
- Tỷ lệ sử dụng bãi xe (%)

## 📈 Export thống kê

Khi nhấn phím `e`, hệ thống sẽ tạo file JSON chứa:
- Thời gian ghi nhận
- Số liệu thống kê tổng quan
- Chi tiết từng chỗ đỗ xe (trống/có xe)
- Tọa độ các chỗ đỗ xe

File được lưu với tên: `parking_stats_YYYYMMDD_HHMMSS.json`

## 🧩 Tuỳ chỉnh đầu vào/đầu ra

- Thay đổi video input trong `main.py`:
```python
video_path = './data/your_video.mp4'
```

- Thay đổi mask trong `main.py`:
```python
mask = './your_mask.png'
```

- Thay đổi nơi lưu video đầu ra trong `main.py`:
```python
output_path = './your_output.mp4'
```

## 📁 Cấu trúc dự án

```
IntelliPark-System/
├── main.py              # File chính chạy hệ thống (ghi output.mp4)
├── util.py              # Các hàm tiện ích và model AI
├── requirements.txt     # Danh sách dependencies
├── README.md           # Hướng dẫn sử dụng
├── QUICK_START.md      # Hướng dẫn nhanh
├── REPORT.md           # Báo cáo phân tích dự án
├── setup.py            # Kiểm tra môi trường & dữ liệu
├── data/               # Thư mục chứa video mẫu
│   ├── parking_1920_1080_loop.mp4
│   └── parking_crop_loop.mp4
├── model/              # Thư mục chứa model AI
│   └── model.p
├── clf-data/           # Dữ liệu training
│   ├── empty/          # Ảnh chỗ trống
│   └── not_empty/      # Ảnh chỗ có xe
└── mask_1920_1080.png  # Mask xác định vùng chỗ đỗ xe
```

## 🔧 Cấu hình

### Thay đổi video input
Sửa đường dẫn trong `main.py`:
```python
video_path = './data/your_video.mp4'  # Thay đổi tên file video
```

### Thay đổi mask
Sửa đường dẫn trong `main.py`:
```python
mask = './your_mask.png'  # Thay đổi file mask
```

### Thay đổi đầu ra video
Sửa biến `output_path` trong `main.py`:
```python
output_path = './your_output.mp4'
```

## 🐛 Xử lý lỗi thường gặp

### Lỗi "No module named 'skimage'"
```bash
pip install scikit-image
```

### Lỗi NumPy version
```bash
pip install "numpy<2"
```

### Lỗi "Video file not found"
- Kiểm tra đường dẫn file video trong `main.py`
- Đảm bảo file video tồn tại trong thư mục `data/`

### Lỗi "Model file not found"
- Kiểm tra file `model/model.p` có tồn tại không
- Tải lại model từ link Google Drive ở trên

## 📊 Kết quả

Hệ thống sẽ hiển thị:
- Video với các khung màu xanh/đỏ
- **Thống kê chi tiết**: Số chỗ trống, số chỗ có xe, tỷ lệ sử dụng
- **Trạng thái bãi xe**: Good/Moderate/Full
- Video đầu ra được lưu tại `output.mp4`
- **File thống kê JSON** khi nhấn phím `e`

## 🔮 Tính năng tương lai

- **Real-time API** để tích hợp với hệ thống khác
- **Database** lưu trữ lịch sử đếm xe
- **Alert system** thông báo khi bãi xe đầy
- **Web dashboard** giao diện web theo dõi
- **Mobile app** để xem thống kê từ xa



