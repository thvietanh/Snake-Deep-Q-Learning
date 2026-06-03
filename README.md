# 🐍 Snake-Deep-Q-Learning

Mô hình AI chơi game Rắn săn mồi sử dụng Deep Q-Learning.

---

# Download the pre-trained model here: [Download](https://github.com/thvietanh/Snake-Deep-Q-Learning/releases/tag/v1.0.1)

## Custom installation and training your own model

Trước khi chạy chương trình, hãy cài đặt các tài nguyên sau:

1. Tải và cài đặt Python: https://www.python.org/downloads/
2. Mở Command Prompt (CMD)
3. Di chuyển đến thư mục chứa repository đã tải về:

```bash
cd duong_dan_den_repository
   ```
4. Cài đặt các thư viện cần thiết:

```bash
py -m pip install -r requirement.txt
```
* Trong trường hợp gặp xung đột và lỗi, bạn có thể tạo một môi trường ảo (virtual environment):
```bash
py -m venv venv
```
* Khởi động môi trường ảo:

*Windows (CMD)*
```bash
venv\Scripts\activate.bat
```
or *Windows (Powershell)*
```bash
venv/Scripts/Activate.ps1
```
* Tắt môi trường ảo:
```bash
deactivate
```

---

## Bắt đầu huấn luyện AI

Chạy lệnh sau trong Command Prompt:

```bash
py train.py
```

Lưu ý:

* Mô hình sẽ tự động được lưu sau mỗi 10 ván chơi.
* Sau khi huấn luyện xong, bạn có thể đóng chương trình.

Mô hình đã huấn luyện sẽ được lưu tại:

```bash
model.pth
```

---

## Chơi với model đã huấn luyện

* Method 1: 
Chạy:
```bash
py app.py
```

* Method 2: If you want a clean executable file for distribution, run:
```bash
build.bat
```
(or if you are using CMD):
```bash
cmd /c build.bat
```
Your trained game will be in ```dist/Snake Game.exe```
---

## Tùy chỉnh cài đặt

Bạn có thể thay đổi một số tham số trong file:```settings.py```

### Các tùy chọn:

* `BLOCK_SIZE` *(mặc định = 40)*
  Kích thước của mỗi ô trong game.
  Đảm bảo rằng:

  ```python
  800 / BLOCK_SIZE
  ```

  cho ra một số chẵn.

* `SPEED` *(mặc định = 30)*
  Điều chỉnh tốc độ cập nhật của trò chơi.

* `Color`
  Thay đổi màu sắc của game.

---

## Cấu trúc file chính

| File            | Chức năng                     |
| -------------   | ----------------------------- |
| `train.py`      | Huấn luyện AI                 |
| `app.py`        | Chơi bằng model đã huấn luyện |
| `settings.py`   | Tùy chỉnh tham số game        |
| `model.pth`     | File model đã lưu             |
| `plotting.py`   | Tạo biểu đồ                   |
| `snake_game.py` | Trò chơi rắn săn mồi          |

---
