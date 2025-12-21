"""
Prompt: 
Hãy viết một chương trình python để đọc payloa từ https://www.nsmo.vn/Dashboard/GetBcsxChartDataPhanBoTheoChuSoHuuGetBcsxChart
Hiển thị dữ liệu $.result trong payload trên
"""

import requests
import json
import sys
import io

# Cấu hình ép luồng xuất (stdout) dùng UTF-8 để bảo vệ tiếng Việt
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_nsmo_ownership_data():
    # URL API phân bổ theo chủ sở hữu
    url = "https://www.nsmo.vn/Dashboard/GetBcsxChartDataPhanBoTheoChuSoHuu"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    try:
        # 1. Gửi yêu cầu lấy dữ liệu
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        # 2. Phân tích cú pháp JSON
        full_json = response.json()

        # 3. Trích xuất phần dữ liệu $.result
        result_data = full_json.get('result', [])

        if not result_data:
            print("⚠️ Không tìm thấy dữ liệu trong phần 'result'.")
            return

        # 4. Hiển thị toàn bộ dữ liệu $.result ra màn hình
        # indent=4: thụt đầu dòng cho dễ đọc
        # ensure_ascii=False: hiển thị tiếng Việt có dấu thay vì mã Unicode (\u...)
        print(json.dumps(result_data, indent=4, ensure_ascii=False))

    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi kết nối API: {e}", file=sys.stderr)
    except Exception as e:
        print(f"❌ Đã xảy ra lỗi: {e}", file=sys.stderr)

if __name__ == "__main__":
    get_nsmo_ownership_data()