"""
Prompt: 
Hãy viết một chương trình python để công suất điện mặt trời mái nhà nsmo.vn/Dashboard/GetSoLieuVanHanhNlttTrongTuan
Cấu trúc dữ liệu có dạng $.result.columns[ {name, data[{day, value] ]}].  Bóc tách, đổi tên day thành time và hiển thị ra màn hình dạng phẳng [{name, value, time}]
Encoding dữ liệu để hiển thị tương thich UTF-8 tiếng Việt
"""

import requests
import json
import sys
import io

# Cấu hình hệ thống để xử lý UTF-8 đồng nhất trên Windows/Linux
# Đảm bảo lệnh 'print' không bị lỗi font khi dùng lệnh > hoặc |

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_nsmo_data():
    # URL API lấy công suất theo loại hình
    url = "https://www.nsmo.vn/Dashboard/GetBcsxChartDataCongSuatTheoLoaiHinh"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    try:
        # 1. Gửi yêu cầu lấy dữ liệu
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        full_json = response.json()

        # 2. Lấy phần mảng gốc từ $.result
        # Cấu trúc API này: result là mảng các loại hình (Thủy điện, Nhiệt điện...)
        result_array = full_json.get('result', [])

        # 3. Mảng đích để lưu cấu trúc phẳng [{name, data, time}]
        flat_results = []

        for category in result_array:
            # Lấy tên loại hình
            name = category.get('name', 'N/A')
            
            # Lấy mảng dữ liệu con ($.result[i].data)
            inner_data = category.get('data', [])
            
            for entry in inner_data:
                # Tạo đối tượng phẳng theo yêu cầu:
                # - name: Tên loại hình
                # - data: Giá trị công suất (lấy từ key 'value')
                # - time: Thời gian (lấy từ key 'hour' và đổi tên)
                flat_item = {
                    "name": name,
                    "data": entry.get('value'),
                    "time": entry.get('hour')
                }
                flat_results.append(flat_item)

        # 4. Hiển thị kết quả ra màn hình
        # ensure_ascii=False: Giữ nguyên ký tự tiếng Việt có dấu
        # indent=4: Định dạng JSON đẹp, dễ đọc
        print(json.dumps(flat_results, indent=4, ensure_ascii=False))

    except requests.exceptions.RequestException as e:
        print(f"Lỗi kết nối: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Lỗi xử lý dữ liệu: {e}", file=sys.stderr)

if __name__ == "__main__":
    get_nsmo_data()