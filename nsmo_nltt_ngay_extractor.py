"""
Prompt: 
Hãy viết một chương trình python để công suất điện mặt trời mái nhà nsmo.vn/Dashboard/GetSoLieuVanHanhNlttNgay
Hiển thị dữ liệu $.result.data trong payload trên
"""

import requests
import json
import sys
import io

# Cấu hình ép luồng xuất (stdout) dùng chuẩn UTF-8
# Giúp hiển thị tiếng Việt và dùng lệnh > xem.txt không bị lỗi font
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_nsmo_daily_data():
    # URL API vận hành NLTT theo ngày
    url = "https://www.nsmo.vn/Dashboard/GetSoLieuVanHanhNlttNgay"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    try:
        # 1. Gửi yêu cầu lấy dữ liệu
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        # Chuyển đổi phản hồi sang dạng JSON
        full_json = response.json()

        # 2. Trích xuất dữ liệu từ khóa $.result.data
        # Cấu trúc: result (dict) -> data (thường là mảng các điểm dữ liệu)
        result_data = full_json.get('result', {}).get('data', [])

        if not result_data:
            print("⚠️ Không tìm thấy dữ liệu trong $.result.data")
            return

        # 3. Hiển thị dữ liệu ra màn hình
        # ensure_ascii=False: Để giữ nguyên ký tự tiếng Việt
        # indent=4: Định dạng thụt đầu dòng cho dễ đọc
        print(json.dumps(result_data, indent=4, ensure_ascii=False))

    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi kết nối API: {e}", file=sys.stderr)
    except Exception as e:
        print(f"❌ Đã xảy ra lỗi: {e}", file=sys.stderr)

if __name__ == "__main__":
    get_nsmo_daily_data()