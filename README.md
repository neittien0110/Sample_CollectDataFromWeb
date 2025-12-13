# THU THẬP DỮ LIỆU TỪ WEB

## Thu thập từ trang web tĩnh

Toàn bộ nội dung cần thu thập đã nằm sẵn trong 1 trang web với 1 URL duy nhất.\
Dấu hiệu đặc trưng là khi __View Source__ trang web thì có thể nhìn thấy nội dung cần tìm

Vậy để thu thập, chỉ cần 3 thao tác chính:

1. Tải về trang theo theo URL chỉ định
2. Xác định vị trí của nội dung cần tìm theo __XPath__, __JS Path__
3. Chỉ định bộ HTML Parser lấy chính xác nội dung theo vị trí đã tìm.

Ví dụ, chương trình sau sẽ lấy thông tin địa chỉ liên hệ, số điện thoai của công ty NSMO.

```shell
    python ./nsmo_contact_extractor.py
```

Chương trình được sinh từ lời Prompt Gemini:
> Hãy viết một chương trình python để đọc phần footer của trang web https://www.nsmo.vn/ và tìm ra địa chỉ liên hệ ở footer.
