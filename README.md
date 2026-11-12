# K5-L3A-Day05-T4-DongBang

Prototype LAB5 — trợ lý khiếu nại hàng không đúng mô tả. Dữ liệu S01/S02 và các thao tác xử lý hồ sơ là giả lập.

## Chạy demo có AI thật — OpenRouter miễn phí

Cần Python 3.11 trở lên. Backend dùng FastAPI; HTML/CSS/JavaScript đảm nhiệm giao diện trong trình duyệt. Không cần Node.js.

Cài môi trường riêng trong thư mục repo (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

1. Copy `.env.example` thành `.env` tại thư mục gốc.
2. Điền khóa OpenRouter trong `.env` trên máy của bạn:

   ```dotenv
   OPENROUTER_API_KEY=your_private_key
   OPENROUTER_MODEL=openrouter/free
   PORT=3000
   ```

3. Chạy `.\.venv\Scripts\python.exe -m prototype.server` và mở [demo local](http://127.0.0.1:3000).
4. Chọn S01 hoặc S02, bấm **Gọi AI đối chiếu hồ sơ này**.
5. Khi thành công, xem nhận định, nguồn trích dẫn, bước đề xuất và model thực tế. Bấm **Tải bằng chứng JSON**; máy chủ cũng lưu tại `prototype/evidence/`.

`openrouter/free` tự chọn model miễn phí phù hợp. Có thể thay bằng ID cụ thể có đuôi `:free`. Máy chủ từ chối model trả phí, không tự chuyển sang model trả phí. Model miễn phí có thể hết quota, chậm hoặc không có endpoint phù hợp; khi đó giao diện báo lỗi và giữ bản mô phỏng.

API key chỉ được đọc ở máy chủ. `.env` và log bằng chứng được Git bỏ qua mặc định. Không dán khóa vào HTML, chat hay bài nộp. Chỉ hồ sơ dựng sẵn được gửi đến AI; ảnh và nội dung người dùng nhập không được gửi. Kết quả AI là phân tích, không gọi tool hoàn/đóng/phạt và không thay biên nhận hay quyết định nhân viên.

## Bằng chứng bonus +3

Log thật chứa ID phản hồi của OpenRouter, model thực tế, thời điểm, input giả, kết quả có căn cứ và `actions_executed: []`. Để nộp: chạy thành công một lần, chụp phần kết quả hoặc chọn đúng log đã kiểm tra để thêm vào bài. Không dùng kết quả unit test làm bằng chứng lời gọi thật. Việc tích hợp xong không tự đồng nghĩa đã đạt bonus: cần lời gọi thành công và bằng chứng.

Mở trực tiếp `prototype/index.html` vẫn chạy mô phỏng, nhưng nút AI thật cần máy chủ local. Dữ liệu/ảnh tải lên chỉ ở phiên trình duyệt; không có hệ thống hoàn tiền thật.

## Khi lời gọi AI thất bại

- `OUTPUT_TOKEN_LIMIT`: model đã dùng hết token cho suy luận/đầu ra. Bản hiện tại cấp 4.096 token và đặt reasoning ở mức low; model miễn phí vẫn có thể bị cắt. Có thể thử lại hoặc chọn model `:free` khác rồi khởi động lại máy chủ.
- `PROVIDER_429`: hết quota hoặc endpoint đang giới hạn lượt; đợi rồi thử lại.
- `INVALID_EVIDENCE` / `SOURCE_PRESENCE_MISMATCH`: model trả căn cứ hoặc trạng thái nguồn sai; kết quả bị chặn, không được dùng làm bằng chứng thành công.
- `PROVIDER_TIMEOUT` / `PROVIDER_CONNECTION`: kiểm tra mạng hoặc thử lại sau. Thời gian chờ provider là 75 giây.

Sau khi cập nhật code hoặc `.env`, dừng máy chủ bằng Ctrl+C rồi chạy lại. Log [bonus-evidence-s01.json](prototype/bonus-evidence-s01.json) là một lời gọi thật S01 đã kiểm tra, sử dụng model miễn phí và ghi chi phí 0; không phải phản hồi unit test. Kết quả từng lần gọi sau có thể khác vì `openrouter/free` chọn model động.

## Kiểm thử

Chạy `.\.venv\Scripts\python.exe -m unittest prototype.test_ai -v`. Bộ test Python dùng HTTPX MockTransport và ASGITransport để kiểm tra quyền, dữ liệu, xác minh trích dẫn, lỗi provider, giới hạn yêu cầu đồng thời và lưu log; không gọi model, không tốn quota, không chứng minh chất lượng model thực tế.

Tài liệu tích hợp: [OpenRouter Free Models Router](https://openrouter.ai/docs/guides/routing/routers/free-router), [Structured Outputs](https://openrouter.ai/docs/guides/features/structured-outputs).
