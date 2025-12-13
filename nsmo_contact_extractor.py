import requests
from bs4 import BeautifulSoup
from typing import Optional

# URL của trang web NSMO
URL = "https://www.nsmo.vn/"

# Các class phổ biến thường chứa địa chỉ liên hệ trong footer
# (Lưu ý: Cần kiểm tra thủ công cấu trúc HTML của trang NSMO để tìm ra class chính xác. 
# Ta sẽ thử các class chung nhất trước, hoặc thẻ footer.)
FOOTER_SELECTOR = "footer" 
ADDRESS_KEYWORDS = ["Địa chỉ", "address", "trụ sở", "Văn phòng"]

def extract_address_from_footer(url: str) -> Optional[str]:
    """
    Tải trang, tìm phần footer và trích xuất địa chỉ liên hệ.
    
    Args:
        url (str): Địa chỉ trang web cần lấy dữ liệu.
        
    Returns:
        Optional[str]: Chuỗi địa chỉ liên hệ hoặc None nếu không tìm thấy.
    """
    print(f"Đang tải dữ liệu từ: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # 1. Tải nội dung HTML
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 2. Tìm thẻ Footer chính
        # Thử tìm thẻ <footer> hoặc một thẻ có class liên quan
        footer = soup.find(FOOTER_SELECTOR)
        
        if not footer:
            print("LỖI: Không tìm thấy thẻ <footer> trên trang.")
            return None
        
        # 3. Tìm Địa chỉ bên trong Footer
        
        # Cách 1: Tìm kiếm các thẻ chứa từ khóa 'Địa chỉ'
        best_match = None
        
        for keyword in ADDRESS_KEYWORDS:
            # Tìm thẻ chứa từ khóa 'Địa chỉ' (ví dụ: <p>Địa chỉ: 123 ABC</p>)
            address_element = footer.find(lambda tag: tag.name in ['div', 'p', 'li', 'span'] and keyword in tag.get_text())
            
            if address_element:
                # Nếu tìm thấy, lấy toàn bộ văn bản của thẻ đó (và các thẻ con)
                best_match = address_element.get_text(strip=True, separator=' ')
                print(f"Đã tìm thấy địa chỉ dựa trên từ khóa '{keyword}'.")
                return best_match
        
        # Cách 2: Nếu không tìm thấy từ khóa, lấy toàn bộ văn bản của footer
        # (Đây là cách dự phòng, nhưng có thể chứa nhiều thông tin nhiễu)
        if best_match is None:
             print("WARNING: Không tìm thấy từ khóa 'Địa chỉ'. Trích xuất toàn bộ văn bản từ footer...")
             
             # Tìm một khối nội dung lớn trong footer (ví dụ: thẻ div đầu tiên trong footer)
             footer_content = footer.find('div')
             if footer_content:
                 return footer_content.get_text(strip=True, separator='\n')
             else:
                 # Nếu không có div, lấy toàn bộ footer
                 return footer.get_text(strip=True, separator='\n')
        
    except requests.exceptions.RequestException as e:
        print(f"LỖỖI KẾT NỐI hoặc TẢI TRANG: {e}")
        return None
    except Exception as e:
        print(f"LỖI KHÔNG XÁC ĐỊNH trong quá trình phân tích: {e}")
        return None

if __name__ == "__main__":
    address = extract_address_from_footer(URL)
    
    if address:
        print("\n=======================================================")
        print("ĐỊA CHỈ LIÊN HỆ TRÍCH XUẤT TỪ FOOTER:")
        print("=======================================================")
        print(address)
        print("=======================================================")
    else:
        print("\nKhông thể trích xuất địa chỉ liên hệ.")