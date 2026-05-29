# 🐍 Snake-Deep-Q-Learning

Mô hình AI chơi game Snake sử dụng Deep Q-Learning.

---

## Yêu cầu cài đặt

Trước khi chạy project, hãy cài đặt các thành phần sau:

1. Tải và cài đặt Python: https://www.python.org/
2. Mở Command Prompt (CMD)
3. Di chuyển đến thư mục chứa repository:

   ```bash
   cd duong_dan_den_repository
   ```
4. Cài đặt các thư viện cần thiết:

   ```bash
   python -m pip install -r requirement.txt
   ```

---

## Bắt đầu huấn luyện AI

Chạy lệnh sau trong Command Prompt:

```bash
python train.py
```

Lưu ý:

* Mô hình sẽ tự động được lưu sau mỗi 10 ván chơi.
* Sau khi huấn luyện xong, bạn có thể đóng chương trình.

Model đã huấn luyện sẽ được lưu tại:

```bash
model.pth
```

---

## Chơi với model đã huấn luyện

Chạy:

```bash
python play.py
```

---

## Tùy chỉnh cài đặt

Bạn có thể thay đổi một số tham số trong file:

```bash
settings.py
```

### Các tùy chọn:

* `BLOCK_SIZE` *(mặc định = 30)*
  Kích thước của mỗi ô trong game.
  Đảm bảo rằng:

  ```python
  600 / BLOCK_SIZE
  ```

  cho ra một số chẵn.

* `SPEED` *(mặc định = 60)*
  Điều chỉnh tốc độ cập nhật của trò chơi.

* `Color`
  Thay đổi màu sắc của game.

---

## 📁 Cấu trúc file chính

| File            | Chức năng                     |
| -------------   | ----------------------------- |
| `train.py`      | Huấn luyện AI                 |
| `play.py`       | Chơi bằng model đã huấn luyện |
| `settings.py`   | Tùy chỉnh tham số game        |
| `model.pth`     | File model đã lưu             |
| `plotting.py`   | Tạo biểu đồ                   |
| `snake_game.py` | Trò chơi rắn săn mồi          |

---
