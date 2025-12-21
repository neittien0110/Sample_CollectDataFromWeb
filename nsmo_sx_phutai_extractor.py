"""
Prompt: Hãy viết một chương trình python để công suất điện mặt trời mái nhà https://www.nsmo.vn/Dashboard/GetBcsxChartDataPhuTai
Lưu phần phần key $.result vào một mảng có cấu trúc dạng {name, data}.  Sau đó bóc tách sâu hơn với các key $.result.data[i].data thì lưu vào mảng con bên trong với cấu trúc {value, hour} và đổi tên ý nghĩa hour thành time .
Hiển thị ra màn hình dạng cấu trúc phẳng [{name, data, time}]
Encoding dữ liệu để hiển thị tương thich UTF-8 tiếng Việt và kể cả xuất ra file
"""

import requests
import json
import sys

# ÉP LUỒNG XUẤT (STDOUT) DÙNG UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def get_nsmo_phutai_to_stdout():
    url = "https://www.nsmo.vn/Dashboard/GetBcsxChartDataPhuTai"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=20)
        data_json = response.json()
        result_list = data_json.get('result', [])
        
        final_list = []
        for item in result_list:
            region_name = item.get('name', 'N/A')
            for entry in item.get('data', []):
                final_list.append({
                    "name": region_name,
                    "data": entry.get('value'),
                    "time": entry.get('hour')
                })

        # Quan trọng: ensure_ascii=False
        print(json.dumps(final_list, indent=4, ensure_ascii=False))

    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    get_nsmo_phutai_to_stdout()