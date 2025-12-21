import requests
import json
import sys
import io

# Đảm bảo hiển thị tiếng Việt chính xác khi in ra màn hình hoặc ghi file bằng lệnh >
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_nsmo_solar_data():
    url = "https://www.nsmo.vn/Dashboard/GetSoLieuCongSuatMtmn"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    try:
        # 1. Lấy dữ liệu từ API
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        full_json = response.json()

        # Truy cập vào $.result.data
        raw_regions = full_json.get('result', {}).get('data', [])

        # 2. Bóc tách dữ liệu theo cấu trúc lồng nhau (Nested)
        # Bước này lưu vào mảng {name, data: [{value, time}]}
        nested_data = []
        for region in raw_regions:
            name = region.get('name', 'N/A')
            inner_points = region.get('data', [])
            
            # Bóc tách lớp trong {value, time}
            processed_points = []
            for point in inner_points:
                processed_points.append({
                    "value": point.get('value'),
                    "time": point.get('time')
                })
            
            nested_data.append({
                "name": name,
                "data": processed_points
            })

        # 3. Chuyển đổi sang dạng phẳng (Flatten) để hiển thị [{name, value, time}]
        # Lưu ý: Tôi dùng 'value' thay vì 'data' ở key thứ 2 để phản ánh đúng giá trị công suất
        display_list = []
        for region in nested_data:
            region_name = region['name']
            for entry in region['data']:
                display_list.append({
                    "name": region_name,
                    "value": entry['value'],
                    "time": entry['time']
                })

        # 4. Hiển thị kết quả ra màn hình dưới dạng JSON list
        print(json.dumps(display_list, indent=4, ensure_ascii=False))

    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    get_nsmo_solar_data()