# Dàn ý bài nộp *(spec.md — nộp trước 23:59 ngày lab của lớp)*

> Copy dàn ý này vào `spec.md` của nhóm. Đây **không** phải form để điền đủ ô: mỗi mục chỉ cần đủ **bằng chứng** và **lập luận** ghi bên dưới. Viết ngắn, gạch đầu dòng là được. Hướng dẫn từng chặng: `02-guide.md`. Cách chấm: `04-rubric.md`.
>
> **Một quyết định = bốn ý:** đã cân nhắc phương án nào · chọn phương án nào · vì sao · loại các phương án kia vì sao. Bằng chứng = lập luận trỏ về một chỗ cụ thể: tool nào, dòng dữ liệu nào của track, điều gì trong mục "Sản phẩm thật hôm nay", chỗ nào trên prototype (ảnh đánh số). Không chạy agent.

```markdown
# Bài nộp LAB5 — [Track] · Nhóm [tên]
[Danh sách thành viên và việc mỗi người làm — copy bảng từ README]

## §1. Lát cắt & phạm vi
- Lát cắt (chép từ track).
- 3 việc tính năng KHÔNG làm, mỗi việc một câu vì sao.

## §2. Kịch bản rủi ro  (chặng 2)
- ≥8 kịch bản, mỗi lớp ①②③④ ít nhất một; mỗi kịch bản: tin người dùng · lớp · AI có thể sai thế nào · sản phẩm tốt nên làm gì · nhãn (nhẹ / sửa được / không chấp nhận được).
- Bằng chứng: cột "AI có thể sai thế nào" trỏ về một tool hoặc một dòng dữ liệu của track (hoặc chỗ dữ liệu không có).
- Quyết định: 2 kịch bản đắt nhất — vì sao đắt hơn các kịch bản còn lại; kịch bản nào suýt được chọn và vì sao không.

## §3. Khi AI sai  (chặng 3)
Với mỗi kịch bản đắt nhất:
- AI nói gì (nguyên văn) · người dùng thấy gì · làm gì tiếp · ai được báo, sau bao lâu.
- Quyết định: hỏi lại / trả lời kèm giới hạn / dừng và chuyển người — chọn cách nào, đã loại cách nào, vì sao.
- Loại lỗi (hệ thống / người dùng / ngữ cảnh) và vì sao cách nói, cách sửa đi theo loại đó.
- 2–3 nguyên tắc HAX/PAIR, mỗi cái trỏ vào một chỗ cụ thể (câu chữ hoặc chỗ trên màn hình).
- Lỗi nào sửa câu chữ không cứu được (nếu có), và thiết kế cứu nó thế nào.

## §4. Mức tự chủ (chặng 4)

AI được tự hướng dẫn, xin bằng chứng và chuyển hồ sơ theo các điều kiện dưới đây. Người có thẩm quyền xử lý khiếu nại của sàn quyết định hoàn tiền hoặc đóng khiếu nại. Bộ phận chuyên trách xử lý việc phạt shop.

## §4. Mức tự chủ (chặng 4)
AI được tự hướng dẫn, xin bằng chứng và chuyển hồ sơ theo các điều kiện dưới đây. Người có thẩm quyền xử lý khiếu nại của sàn quyết định hoàn tiền hoặc đóng khiếu nại. Bộ phận chuyên trách xử lý việc phạt shop.

### 4.1. Mức tự chủ của từng tool

| Tool | Mức đề xuất và điều kiện | Cái giá khi sai, khả năng sửa và chi phí chờ | Phương án đã cân nhắc |
|---|---|---|---|
| `yeu_cau_bang_chung` | **Tự làm.** Chỉ gửi khi đã xác định đúng đơn, đúng bên cần phản hồi và đúng bằng chứng còn thiếu. Nếu chưa rõ đơn nào hoặc hàng sai ở điểm nào, AI hỏi một câu làm rõ trước. | Tin đã gửi thì người nhận đã thấy. Hỏi nhầm bên hoặc hỏi lại bằng chứng đã có làm mất thời gian và có thể chậm phản hồi. Có thể đính chính bằng tin mới. | Duyệt tay từng tin giúp giảm lỗi nhưng làm chậm cả các ca thông thường. Nhóm đề xuất kiểm tra hồ sơ trước khi gửi và dùng mẫu trung lập nêu đúng mục còn thiếu. |
| `chuyen_truong_nhom` | **Tự làm.** Chuyển hồ sơ kèm lý do khi thiếu bản mô tả lúc đặt và chưa thể bổ sung, bằng chứng mâu thuẫn ở điểm quyết định, hoặc ca vượt thẩm quyền của AI. | Chuyển nhầm làm tăng hàng đợi và khiến hai bên chờ lâu hơn. Hồ sơ có thể được điều phối lại. | Duyệt trước khi chuyển giúp giảm chuyển nhầm nhưng thêm một lượt chờ. Nhóm đề xuất chuyển theo điều kiện cụ thể và hướng dẫn ngay với ca rõ ràng. |
| `soan_hoan_tien` | **Cần người duyệt.** Tool này thực hiện hoàn tiền. Nhân viên có thẩm quyền xem đơn, bản mô tả lúc đặt, bằng chứng hai bên, phản hồi của shop hoặc trạng thái hết hạn phản hồi, số tiền và lý do đề xuất. Quá hạn duyệt thì hồ sơ vẫn mở, người dùng thấy trạng thái chờ và trưởng nhóm được báo. | Hoàn sai làm người bán mất tiền và khó thu hồi. Chờ duyệt khiến người mua đủ điều kiện nhận tiền muộn hơn. AI chuẩn bị hồ sơ trước để giảm thời gian xử lý. | Hoàn tự động nhanh hơn nhưng có thể dựa trên bản mô tả sai phiên bản hoặc bằng chứng một phía. Giao toàn bộ việc chuẩn bị cho nhân viên làm tăng thời gian xử lý. Nhóm đề xuất cho AI soạn hồ sơ và yêu cầu phê duyệt trước khi chuyển tiền. |
| `tu_choi_khieu_nai` | **Cần người duyệt.** Nhân viên có thẩm quyền xem bản mô tả lúc đặt, lý do khiếu nại, bằng chứng hai bên, phần còn thiếu và lý do đề xuất đóng. Quá hạn duyệt thì hồ sơ vẫn mở, hai bên thấy trạng thái chờ và trưởng nhóm được báo. | Đóng sai khiến tiền về người bán và người mua phải yêu cầu xem xét lại. Việc đảo quyết định khó. Chờ duyệt kéo dài thời gian giải quyết cho cả hai bên. | Tự đóng khi hồ sơ thiếu bằng chứng có thể làm người mua chịu thiệt vì dữ liệu chưa đầy đủ. Nhóm đề xuất cho AI chỉ rõ mục còn thiếu và để người có thẩm quyền quyết định sau khi hai bên có cơ hội phản hồi. |
| `phat_shop` | **Cấm đối với AI trong luồng T4.** Khi có dấu hiệu hàng giả hoặc yêu cầu xử phạt, AI chuyển hồ sơ để điều phối đến bộ phận chuyên trách. | Phạt sai có thể làm giảm uy tín hoặc gián đoạn hoạt động của cả shop. Việc khôi phục khó. Chuyển chuyên trách tốn thời gian nhưng cho phép đánh giá bằng chứng và phạm vi ảnh hưởng. | Duyệt phạt ngay trong luồng xử lý một đơn dễ dẫn tới quyết định ảnh hưởng cả shop dựa trên hồ sơ của một giao dịch. Nhóm đề xuất chuyển sang quy trình chuyên trách. |

### 4.2. Tool khó xếp nhất — `soan_hoan_tien`

- **T4-02:** Người mua dọa bóc phốt trong khi tem hàng khớp với mô tả lúc đặt. Hoàn tự động có thể khiến shop mất tiền dù lời đe dọa không phải bằng chứng hàng giao sai.
- **T4-03:** Người mua nhận size M thay vì size L và shop đã xác nhận gửi nhầm. Nếu yêu cầu người duyệt ngay từ bước hướng dẫn, người mua phải chờ mới biết cách nộp yêu cầu.

**Đề xuất chốt:** AI hướng dẫn người mua gửi yêu cầu và chuẩn bị hồ sơ ngay. Nhân viên có thẩm quyền duyệt trước khi tiền được chuyển. Cách này giúp khách đi tiếp ngay ở T4-03 và chặn hoàn tiền sai ở T4-02.

**Lựa chọn ban đầu của từng thành viên:**

- **Lê Hoàng Quân — Cần người duyệt.** `soan_hoan_tien` thực hiện chuyển tiền cho người mua. Nếu AI hoàn tiền vì khách dọa bóc phốt trong khi tem hàng khớp với mô tả lúc đặt, shop có thể mất tiền và việc thu hồi sẽ khó. Tôi đề xuất để AI chuẩn bị hồ sơ, sau đó nhân viên có thẩm quyền duyệt trước khi chuyển tiền.
- **Kiều Đình Văn — Cần người duyệt.** Tôi lo AI dùng mô tả hiện tại của shop để quyết định hoàn tiền. Người duyệt cần đối chiếu bản mô tả lúc đặt hàng và bằng chứng của cả hai bên trước khi tiền được chuyển.
- **Nguyễn Tuấn Quang — Tự làm trong ca đủ căn cứ.** Ban đầu tôi muốn AI tự hoàn tiền khi đã xác định đúng đơn, có bằng chứng giao sai size và shop đã xác nhận gửi nhầm. Lý do là người mua phải chờ lâu hơn nếu ngay cả ca rõ ràng cũng cần duyệt tay.
- **Nguyễn Lâm Hoàng — Cấm AI thực hiện hoàn tiền.** Tôi đề xuất AI chỉ chuẩn bị hồ sơ vì tiền đã chuyển thì khó thu hồi. Nhân viên có thẩm quyền xem xét và trực tiếp thực hiện giao dịch hoàn tiền.
- **Quyết định cuối của nhóm — Cần người duyệt.** Ở T4-02, lời dọa bóc phốt không phải căn cứ hoàn tiền, nên nhân viên phải xem bằng chứng trước khi duyệt. Ở T4-03, shop đã xác nhận gửi sai size, nên AI có thể hướng dẫn khách gửi yêu cầu và chuẩn bị hồ sơ ngay. Khâu duyệt chỉ diễn ra trước khi chuyển tiền.

### 4.3. Thử mức tự chủ trên hai ca rủi ro nhất và một ca bình thường

| Kịch bản §2 | AI làm gì, người dùng thấy gì? | Cái sai có bị chặn? | Khi nào cần hỏi? Có phải chờ vô ích? |
|---|---|---|---|
| **T4-01 · Shop sửa mô tả sau khi bán** | AI đối chiếu bản mô tả lúc đặt của đúng đơn. Nếu thiếu bản đó và chưa thể bổ sung, AI hiển thị “Chưa có bản mô tả lúc đặt để đối chiếu” và chuyển hồ sơ kèm lý do. | **Có.** Trang hiện tại không đủ căn cứ để hoàn tiền hoặc đóng khiếu nại. Hai thao tác đều cần người duyệt. | Nếu chưa rõ đơn hoặc chi tiết bị sai, AI hỏi một câu trước. Khi đơn đã rõ và thiếu căn cứ quyết định, AI tự chuyển hồ sơ để người có thẩm quyền xem xét. |
| **T4-02 · Tem khớp mô tả, người mua dọa bóc phốt** | AI hiển thị nội dung đã đối chiếu và mục bằng chứng còn thiếu. Shop thấy nội dung khiếu nại liên quan và hạn phản hồi. Nếu hai bên vẫn tranh chấp, AI chuyển hồ sơ. | **Có.** Lời đe dọa không kích hoạt hoàn tiền. Tem khớp cũng chưa đủ để AI tự đóng hồ sơ khi còn bằng chứng cần xem. | AI chỉ yêu cầu đúng bên bổ sung đúng mục còn thiếu. Thời gian chờ dành cho phản hồi của hai bên và quyết định của người có thẩm quyền. |
| **T4-03 · Giao sai size, shop đã xác nhận** | Khi đã xác định đúng đơn, AI dùng xác nhận có sẵn trong hồ sơ, hướng dẫn người mua gửi yêu cầu ngay và chuẩn bị đề xuất hoàn. | **Có.** Hồ sơ có thể được soạn ngay. Tiền chỉ được chuyển sau khi người có thẩm quyền duyệt. | Người mua không phải nộp lại xác nhận của shop hoặc chờ mới được hướng dẫn. Khâu chờ duyệt bắt đầu ở quyết định chuyển tiền. |

### 4.4. Tách bước soạn đề xuất và thực hiện hoàn tiền

1. **Soạn đề xuất hoàn tiền — AI tự làm.** Bản nháp ghi mã đơn, bản mô tả lúc đặt, bằng chứng, phản hồi của hai bên, số tiền đề xuất và mục còn thiếu. Có thể sửa bản nháp.
2. **Thực hiện hoàn tiền — cần người duyệt.** Hệ thống chỉ thực hiện khi có phê duyệt cho đúng hồ sơ và số tiền. Nếu bằng chứng hoặc số tiền thay đổi sau khi duyệt, hồ sơ quay lại bước duyệt.

Ở T4-02, AI có thể chuẩn bị hồ sơ để nhân viên xem xét, trong khi quyết định chuyển tiền vẫn phụ thuộc vào bằng chứng và phê duyệt.

### 4.5. Lời hứa với người dùng

Khi AI đã chuẩn bị đề xuất, giao diện hiển thị:

> Đã chuẩn bị hồ sơ đề xuất hoàn tiền. Nhân viên sẽ xem xét bằng chứng và phản hồi của hai bên trước khi quyết định.

Trạng thái **Đã hoàn tiền** chỉ xuất hiện sau khi hệ thống xác nhận giao dịch hoàn tiền thành công.

## §5. Prototype  (chặng 5)
- Link hoặc file · công cụ · phần nào mock · có lời gọi AI thật không.
- 1–2 ảnh có đánh số; mỗi số: thể hiện gì · nguyên tắc HAX/PAIR nào · mức tự chủ nào.
- Quyết định: cách hiện độ chắc/bằng chứng và điều khiển mức tự chủ — đã nghĩ tới cách nào khác, vì sao chọn cách này.

## §6. Tốt là gì  (chặng 6 — nhẹ, bỏ được nếu thiếu giờ)
- 3 tiêu chí Pass/Fail chấm được; thiết kế của nhóm đạt tiêu chí nào trên 2 kịch bản đắt nhất; lỗi còn lại.

## §7. Demo
- Ca lạ nhận được ở demo: prototype đã làm gì, và nhóm có đổi ý gì sau ca đó không.
```
