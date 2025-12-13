import requests
import json
from typing import List, Dict, Any, Optional

# URL API của tỷ giá Techcombank
API_URL = "https://techcombank.com/content/techcombank/web/vn/vi/cong-cu-tien-ich/ty-gia/_jcr_content.exchange-rates.integration.json"
# Khóa mục tiêu (sử dụng ký hiệu dot notation)
TARGET_KEY_PATH = "exchangeRate.data"

def get_exchange_rates_from_json_api(url: str, key_path: str) -> Optional[List[Dict[str, Any]]]:
    """
    Tải file JSON từ URL, phân tích và trích xuất dữ liệu theo đường dẫn khóa.
    
    Args:
        url (str): Địa chỉ API JSON.
        key_path (str): Đường dẫn khóa để truy cập dữ liệu (ví dụ: "exchangeRate.data").
        
    Returns:
        Optional[List[Dict[str, Any]]]: Danh sách tỷ giá hoặc None nếu trích xuất thất bại.
    """
    print(f"Đang tải dữ liệu JSON từ: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json'
    }
    
    try:
        # 1. Tải dữ liệu JSON
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() # Báo lỗi nếu mã trạng thái không phải 200
        
        # 2. Phân tích dữ liệu JSON
        data = response.json()
        
        # 3. Trích xuất dữ liệu theo đường dẫn khóa
        keys = key_path.split('.')
        current_data = data
        
        print(f"  Đang tìm kiếm khóa: {key_path}")
        
        for key in keys:
            if isinstance(current_data, dict) and key in current_data:
                current_data = current_data[key]
            else:
                print(f"LỖI: Không tìm thấy khóa '{key}' trong đường dẫn '{key_path}'.")
                return None
        
        # 4. Kiểm tra cấu trúc cuối cùng
        if isinstance(current_data, list):
            print("  Trích xuất thành công dữ liệu tỷ giá!")
            return current_data
        else:
            print(f"LỖI: Dữ liệu cuối cùng không phải là một mảng (list). Kiểu dữ liệu là {type(current_data)}")
            return None

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
    exchange_rates_data = get_exchange_rates_from_json_api(API_URL, TARGET_KEY_PATH)
    
    if exchange_rates_data:
        print("\n=======================================================")
        print(f"KẾT QUẢ TRÍCH XUẤT TỪ '{TARGET_KEY_PATH}'")
        print("=======================================================")
        
        # In ra 5 bản ghi đầu tiên để kiểm tra cấu trúc
        print(f"Đã tìm thấy {len(exchange_rates_data)} bản ghi. 5 bản ghi đầu tiên:")
        
        # Sử dụng pandas để in ra cấu trúc bảng dễ đọc hơn (tùy chọn)
        try:
            import pandas as pd
            df = pd.DataFrame(exchange_rates_data)
            print(df.head().to_string(index=False))
        except ImportError:
            # Nếu pandas không được cài đặt, in ra JSON thô
            for i, rate in enumerate(exchange_rates_data[:5]):
                print(f"  {i+1}: {rate}")

        print("...")
        print("=======================================================")
        
        # Dữ liệu đầy đủ được lưu trong biến exchange_rates_data (dưới dạng List[Dict[...]])
    else:
        print("\nKhông thể trích xuất dữ liệu tỷ giá từ API.")