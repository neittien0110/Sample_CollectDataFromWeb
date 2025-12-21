"""
Hãy viết một chương trình python để công suất điện mặt trời mái nhà 
nsmo.vn/Dashboard/GetSoLieuVanHanhNlttTrongTuan
Cấu trúc dữ liệu có dạng $.result.columns[ {name, data[{day, value] ]}].  
Bóc tách, đổi tên day thành time và hiển thị ra màn hình dạng phẳng [{name, value, time}]
"""
 
import requests
import json
import sys
import io

# 1. KHẮC PHỤC LỖI ENCODING KHI DÙNG LỆNH > 
# Ép luồng xuất chuẩn (stdout) phải dùng UTF-8 bất kể cài đặt hệ thống
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_nsmo_weekly_data():
    # URL API vận hành NLTT trong tuần
    url = "https://www.nsmo.vn/Dashboard/GetSoLieuVanHanhNlttTrongTuan"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    try:
        # 2. Gửi yêu cầu lấy dữ liệu
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        full_json = response.json()

        # 3. Truy cập vào $.result.columns
        # Cấu trúc: result -> columns (mảng các loại hình) -> data (mảng các ngày)
        columns = full_json.get('result', {}).get('columns', [])
        
        # 4. Mảng chứa kết quả phẳng [{name, value, time}]
        flattened_list = []

        for col in columns:
            category_name = col.get('name', 'N/A')
            inner_data = col.get('data', [])
            
            for entry in inner_data:
                # Bóc tách và đổi tên:
                # 'value' giữ nguyên
                # 'day' đổi tên thành 'time'
                flattened_list.append({
                    "name": category_name,
                    "value": entry.get('value'),
                    "time": entry.get('day')  # Đổi 'day' thành 'time'
                })

        # 5. Hiển thị ra màn hình dạng JSON phẳng
        # ensure_ascii=False: Giữ nguyên tiếng Việt có dấu
        # indent=4: Định dạng đẹp để dễ đọc/kiểm tra
        print(json.dumps(flattened_list, indent=4, ensure_ascii=False))

    except Exception as e:
        # Xuất lỗi ra luồng stderr để không làm bẩn file output nếu dùng lệnh >
        print(f"Lỗi: {e}", file=sys.stderr)

if __name__ == "__main__":
    get_nsmo_weekly_data()