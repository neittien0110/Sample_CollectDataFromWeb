# Hướng Dẫn Kết Nối SQL Server Trong Python

Dưới đây là hướng dẫn chi tiết về nguyên lý, cách cài đặt và sử dụng kết nối cơ sở dữ liệu SQL Server trong Python, sử dụng thư viện `pyodbc` và tuân thủ các yêu cầu về cấu trúc hàm của chương trình chính.

---

## I. Nguyên Lý Kết Nối Cơ Sở Dữ Liệu (DB Connection Principle)

Nguyên tắc chung để ứng dụng Python tương tác với SQL Server là thông qua một giao diện chuẩn gọi là **ODBC**.

1. **ODBC (Open Database Connectivity):** Là một API (Application Programming Interface) chuẩn, cho phép ứng dụng truy cập dữ liệu trong nhiều hệ quản trị cơ sở dữ liệu khác nhau (SQL Server, MySQL,...) bằng cùng một bộ lệnh.
2. **ODBC Driver:** Là phần mềm do nhà cung cấp (Microsoft) phát triển, cài đặt trên máy tính của bạn. Nó có nhiệm vụ dịch các yêu cầu truy vấn chuẩn (SQL) từ ứng dụng thành các giao thức và lệnh cụ thể mà SQL Server có thể xử lý.
3. **Thư viện Python (`pyodbc`):** Là thư viện Python được sử dụng để gọi các hàm của ODBC Driver, đóng vai trò là cầu nối giữa mã Python và Driver.

## Nội dung file sqlserver.json

Cấu hình kết nối với SQLServer

```json
{
    "ConnectionString": "DRIVER=SQL Server;SERVER=TEN_SERVER_CUA_BAN;DATABASE=TEN_DB_CUA_BAN;UID=USER_CUA_BAN;PWD=PASSWORD_CUA_BAN;"
}
```

## Sử dụng

Chỉ có 4 hàm 

- __DBInit__: Khởi tạo kết nối cơ sở dữ liệu
- __get_source_id__: Xác định dữ liệu thuộc đối tượng cung cấp nào
- __DBWrite_CongSuatMTMN__: Ghi dữ liệu vào bảng Công suất MTMN
- __DBClose__: Đóng kết nối cơ sở dữ liệu
