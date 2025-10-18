# PharmApp — Trình tải MP3 từ YouTube (Batch & Queue)

Bộ công cụ nhỏ gọn để **thu thập URL YouTube** (từ playlist hoặc channel) và **tải âm thanh MP3** bằng [yt-dlp]. Repo kèm theo các script **xử lý theo hàng đợi (queue) và chạy song song nhiều worker**; trên Windows có sẵn file `.bat/.ps1` để thao tác nhanh.

> **Chỉ dùng cho mục đích học tập/cá nhân.** Hãy tuân thủ Điều khoản dịch vụ của YouTube và luật bản quyền địa phương. Chỉ tải nội dung khi bạn có quyền.

---

## ✨ Tính năng

- **Thu thập URL**
  - Từ **playlist** → `1_get_url_yt_input_pl_v1.py`
  - Từ **channel** → `1_get_yt_urls_input_channel.py`
  - Có file .bat hỗ trợ chạy nhanh trên Windows.
- **Tải một luồng (single worker)** từ `url_yt.txt` → `2_down_mp3_url_yt_v2.py` (có hỏi đáp tương tác).
- **Tải hàng loạt theo hàng đợi (queue) và chạy song song**
  - Chuẩn bị & khử trùng lặp hàng đợi → `prepare_queue.ps1` / `prepare_queue.bat`
  - Lấy (pop) URL kế tiếp một cách an toàn → `url_queue_pop.py`
  - Mở nhiều worker → `launch_workers.bat` / `worker_queue.bat`.
- **Không cần tài khoản/API**; khi đã có danh sách URL, có thể chạy offline.
- **Python thuần**, phụ thuộc tối thiểu.

---

## 🗂️ Cấu trúc thư mục (tham khảo)

```
PharmApp-download-youtube-mp3/
├─ 0_how_use.md                  # Ghi chú nhanh (tiếng Việt)
├─ 1_get_url_yt_input_pl.bat     # Trợ lý Windows cho trình lấy URL playlist
├─ 1_get_url_yt_input_pl_v1.py   # Script lấy URL playlist (Python)
├─ 1_get_yt_urls_input_channel.bat
├─ 1_get_yt_urls_input_channel.py# Script lấy URL channel (Python)
├─ 1_get_yt_urls_option.bat      # Tùy chọn chạy nhanh
├─ 2_down_mp3_url_yt_v2.py       # Tải MP3 từ url_yt.txt (tương tác)
├─ launch_workers.bat            # Mở nhiều worker
├─ prepare_queue.bat             # Tạo hàng đợi từ url_yt.txt
├─ prepare_queue.ps1             # Bản PowerShell
├─ url_queue_pop.py              # Pop URL kế tiếp (an toàn khi chạy song song)
├─ url_yt.txt                    # Ví dụ danh sách URL
├─ url_yt.zip                    # Bản nén mẫu url_yt.txt
└─ url_yt_queue.txt              # Hàng đợi (được tạo ra)
```

> _Mẹo:_ Lưu `url_yt.txt` theo **UTF‑8**, mỗi dòng một URL.

---

## 📦 Yêu cầu

- **Python 3.9+**
- **yt-dlp** (trình tải video/audio)  
- **FFmpeg** (bắt buộc để trích âm thanh & mã hoá MP3)

```bash
# Windows (PowerShell)
pip install --upgrade yt-dlp

# macOS (Homebrew)
brew install yt-dlp ffmpeg

# Debian/Ubuntu
sudo apt-get update && sudo apt-get install -y yt-dlp ffmpeg
```

> Nếu tự cài `yt-dlp` dạng file thực thi, hãy đảm bảo nó nằm trong `PATH` và thường xuyên cập nhật.

---

## 🚀 Bắt đầu nhanh

### 1) Thu thập URL
**Playlist**
```bash
python 1_get_url_yt_input_pl_v1.py
# Làm theo hướng dẫn, dán URL playlist → ghi ra url_yt.txt
```

**Channel**
```bash
python 1_get_yt_urls_input_channel.py
# Làm theo hướng dẫn → ghi ra url_yt.txt
```

### 2) Tải MP3 (một luồng)
```bash
python 2_down_mp3_url_yt_v2.py
# Script sẽ hỏi:
#  - Ngôn ngữ (nếu có)
#  - Đường dẫn đầy đủ tới url_yt.txt
#  - Thư mục đầu ra
#  - Có tải phụ đề/video kèm không (nếu hỗ trợ)
#  - Cách xử lý file tồn tại (ghi đè / bỏ qua)
```

### 3) Tải song song theo hàng đợi (Windows)
Với danh sách rất dài, hãy dùng quy trình queue:

```powershell
# Tạo hàng đợi từ url_yt.txt (có thể khử trùng lặp/ngẫu nhiên hoá)
.\prepare_queue.ps1

# HOẶC (cmd)
prepare_queue.bat

# Mở nhiều worker (mỗi worker sẽ pop URL kế tiếp từ hàng đợi)
launch_workers.bat
# Hoặc dùng worker_queue.bat, script này sẽ gọi url_queue_pop.py
```

Mỗi worker sẽ lặp: gọi `url_queue_pop.py` để lấy URL kế tiếp trong `url_yt_queue.txt`, sau đó chạy `2_down_mp3_url_yt_v2.py` cho URL đó. Cách này tránh va chạm và mở rộng song song an toàn.

---

## ⚙️ Ghi chú & mẹo

- **FFmpeg là bắt buộc** để trích xuất MP3. Cài đặt và kiểm tra `ffmpeg -version`.
- **Mẫu tên file (template)**: yt‑dlp sử dụng chuỗi template trong script. Nếu muốn dạng _Tiêu đề [VideoID] - YYYY-MM-DD.mp3_, hãy tìm chuỗi output trong `2_down_mp3_url_yt_v2.py` và chỉnh, ví dụ:  
  `-o "%(title)s [%(id)s] - %(upload_date>%Y-%m-%d)s.%(ext)s"`
- **Tiếp tục/nhảy qua**: Với danh sách lớn, ưu tiên **Skip if exists** để chạy nhiều lần mà không hỏng quy trình.
- **Đường dẫn Windows**: Tránh ký tự cấm `<>:"|?*`. Khi nhập bằng Python string, cần escape `\` hoặc bọc bằng dấu ngoặc kép.

---

## ❗ Pháp lý

Dự án dùng cho **mục đích cá nhân/học tập hợp pháp**. Bạn tự chịu trách nhiệm tuân thủ **Điều khoản của YouTube** và luật bản quyền. **Không** tải/công bố lại nội dung khi chưa có quyền.

---

## 🛠️ Khắc phục sự cố

- **`ffmpeg not found`** → Cài FFmpeg và thêm vào PATH (`ffmpeg -version`).
- **`HTTP 403/410`** → Cập nhật yt‑dlp: `python -m pip install -U yt-dlp`.
- **Tên file bị lỗi dấu** → Đảm bảo môi trường UTF‑8; có thể bổ sung bước làm sạch tiêu đề.
- **WinError 123 (đường dẫn)** → Kiểm tra ký tự cấm và dấu gạch chéo ngược.
- **Tải chậm/đứt** → Hạn chế số worker đồng thời; có thể bật log để theo dõi retry.

---

## 🗺️ Lộ trình (đề xuất)

- Thêm `requirements.txt` & `pyproject.toml`.
- Chuẩn hoá CLI bằng `argparse` (thay prompt tương tác).
- Tuỳ chọn **nhúng metadata ID3** & ảnh bìa qua FFmpeg/yt-dlp.
- Thêm **Dockerfile** để chạy tái lập trên mọi nền tảng.
- Thêm **LICENSE** (MIT/Apache-2.0) để rõ quyền sử dụng.

---

## 🤝 Đóng góp

Rất hoan nghênh PR! Với thay đổi lớn (tham số CLI, template output, định dạng queue…), vui lòng mở issue trước để thảo luận.

---

## 📄 Giấy phép

Repo **chưa có file license**. Nên thêm **MIT** hoặc **Apache‑2.0** để cộng đồng dễ sử dụng và đóng góp.

---

## 🙏 Ghi công

- Dựa trên **yt-dlp** và **FFmpeg**.
- Thuộc hệ sinh thái công cụ **PharmApp**.
