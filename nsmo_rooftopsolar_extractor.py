import requests
import json
import sys
from typing import List, Dict, Any, Optional
from dbstorage import DBInit, DBClose, get_source_id, DBWrite_CongSuatMTMN

# URL API
API_URL = "https://www.nsmo.vn/Dashboard/GetSoLieuCongSuatMtmn"

def extract_and_restructure_solar_data(url: str) -> Optional[List[Dict[str, Any]]]:
    """
    Tải dữ liệu công suất điện mặt trời từ API, sau đó tái cấu trúc theo yêu cầu.
    
    Returns:
        Optional[List[Dict[str, Any]]]: Danh sách dữ liệu đã được tái cấu trúc hoặc None.
    """
    print(f"Đang tải dữ liệu JSON từ: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json'
    }
    
    try:
        # 1. Tải dữ liệu JSON
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        # 2. Truy cập khóa $.result.data (Cấp 1)
        # Khóa ban đầu là $.result.data, nơi chứa danh sách các series dữ liệu
        result_data = data.get('result', {}).get('data')
        
        if not isinstance(result_data, list):
            print("LỖI: Không tìm thấy hoặc dữ liệu tại $.result.data không phải là một mảng.")
            return None
        
        final_restructured_data = []
        
        # 3. Lặp qua từng series (Cấp 1)
        for series in result_data:
            series_name = series.get('name')
            series_data_list = series.get('data')
            
            if series_name is None or not isinstance(series_data_list, list):
                print(f"CẢNH BÁO: Bỏ qua series dữ liệu không hợp lệ (Name: {series_name}).")
                continue

            # 4. Tái cấu trúc mảng con (Cấp 2)
            restructured_series_data = []
            
            # Khóa $.result.data[i].data là một mảng 2D (hoặc tương tự)
            # Ví dụ: [[value_1, time_1], [value_2, time_2], ...]
            for item in series_data_list:
                # Dữ liệu từ API thường là [value, time] hoặc [time, value]
                # Ta giả định dữ liệu có cấu trúc [value, time] hoặc tương tự
                if isinstance(item, list) and len(item) == 2:
                    restructured_series_data.append({
                        "value": item[1], # Thường là giá trị thực tế
                        "time": item[0]   # Thường là mốc thời gian/chỉ mục
                    })
                # Nếu dữ liệu là đối tượng {time: ..., value: ...}
                elif isinstance(item, dict) and 'time' in item and 'value' in item:
                    restructured_series_data.append({
                        "value": item['value'],
                        "time": item['time']
                    })
                # Nếu dữ liệu chỉ là một giá trị đơn, ta gán time là index
                elif isinstance(item, (int, float, str)):
                     restructured_series_data.append({
                        "value": item,
                        "time": f"Index_{series_data_list.index(item)}"
                    })
            
            # 5. Lưu cấu trúc Cấp 1
            final_restructured_data.append({
                "name": series_name,
                "data": restructured_series_data
            })
            
        print("  Tái cấu trúc dữ liệu thành công!")
        return final_restructured_data

    except requests.exceptions.RequestException as e:
        print(f"LỖI KẾT NỐI hoặc TẢI DỮ LIỆU: {e}")
        return None
    except json.JSONDecodeError:
        print("LỖI PHÂN TÍCH JSON: Dữ liệu nhận được không phải định dạng JSON hợp lệ.")
        return None
    except Exception as e:
        print(f"LỖI KHÔNG XÁC ĐỊNH: {e}")
        return None

if __name__ == "__main__":
    restructured_data = extract_and_restructure_solar_data(API_URL)
    
    if restructured_data:
        print("\n=======================================================")
        print("KẾT QUẢ TÁI CẤU TRÚC DỮ LIỆU CÔNG SUẤT ĐIỆN MẶT TRỜI")
        print("=======================================================")
        
        print(f"Đã trích xuất {len(restructured_data)} series dữ liệu.")
        
        # In ra cấu trúc của series đầu tiên để kiểm tra
        if restructured_data:
            first_series = restructured_data[0]
            print(f"\n--- Series đầu tiên: '{first_series['name']}' ---")
            print(f"Tổng số điểm dữ liệu: {len(first_series['data'])}")
            print("20 điểm dữ liệu đầu tiên:")
            
            # In 20 điểm dữ liệu đầu tiên theo cấu trúc {value, time}
            for i, item in enumerate(first_series['data'][:20]):
                print(f"  {i+1}: {{'value': {item['value']}, 'time': '{item['time']}'}}")

        print("...")
        print("=======================================================")
    else:
        print("\nKhông thể trích xuất hoặc tái cấu trúc dữ liệu.")
        sys.exit(1)

    # 1. Kết nối cơ sở dữ liệu
    db_conn = DBInit()
    if not db_conn:
        sys.exit(1);
        
    # 3. Xử lý và Ghi dữ liệu vào DB
    total_records = 0
    print("\nBắt đầu ghi dữ liệu vào SQL Server...")
    for series in restructured_data:
        source_name = series['name']
        restructured_series_data = series['data']
        
        # 3.1. Tìm Source ID (DataSource_Header.source_id)
        source_fk = get_source_id(source_name)
        if source_fk is None:
            continue
            
        # 3.2. Ghi từng bản ghi (measurement) vào bảng CongSuatMTMN
        records_processed = 0
        for record in restructured_series_data:
            value = record['value']
            time = record['time']
            
            # Gọi hàm ghi DB, bao gồm kiểm tra trùng lặp
            if DBWrite_CongSuatMTMN(source_fk, value, time):
                records_processed += 1
        
        total_records += records_processed
        print(f"  Series '{source_name}' (ID: {source_fk}): Đã xử lý {len(restructured_series_data)} bản ghi, ghi mới/bỏ qua {records_processed} bản.")

    print(f"\nTHÀNH CÔNG: Đã hoàn tất quá trình ghi dữ liệu. Tổng số bản ghi xử lý: {total_records}")

    # 4. Hiển thị toàn bộ data[].data[] ra màn hình console (Theo yêu cầu)
    print("\n--- TOÀN BỘ DỮ LIỆU ĐÃ TRÍCH XUẤT (CONSOLE OUTPUT) ---")
    for series in restructured_data:
        series_name = series['name']
        series_data = series['data']
        
        print(f"\n[SERIES: {series_name}] - Tổng số điểm dữ liệu: {len(series_data)}")
        
        # In tối đa 10 bản ghi đầu tiên
        display_count = min(len(series_data), 10) 
        
        if display_count > 0:
            for i in range(display_count):
                record = series_data[i]
                # Cố gắng in ra giá trị và thời gian
                print(f"    - Thời gian: {record.get('time', 'N/A')}, Giá trị: {record.get('value', 'N/A')}")
        
        if len(series_data) > display_count:
             print(f"  ... ({len(series_data) - display_count} bản ghi còn lại)")
    
    print("-----------------------------------------------------")
    
    # 5. Đóng kết nối     
    DBClose()
