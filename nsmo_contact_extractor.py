import requests
import argparse
from bs4 import BeautifulSoup
from typing import Optional

# URL mục tiêu
URL = "https://www.nsmo.vn/"

# XPath: //*[@id="Footer"]/div[1]/div[2]/div[4]
# Tương đương với việc tìm div thứ 4 trong div thứ 2 trong div thứ 1 bên trong #Footer
# Trong CSS Selector, chúng ta có thể dùng cú pháp: #Footer > div:nth-child(1) > div:nth-child(2) > div:nth-child(4)
CSS_SELECTOR = "#Footer > div:nth-child(1) > div:nth-child(2) > div:nth-child(4)"

def extract_address_by_xpath_equivalent(url: str, css_selector: str, verbose: bool) -> Optional[str]:
    """
    Tải trang, tìm thẻ theo CSS Selector (tương đương XPath), và trích xuất nội dung.
    
    Args:
        url (str): Địa chỉ trang web cần lấy dữ liệu.
        css_selector (str): CSS Selector tương đương với XPath mục tiêu.
        verbose (bool): Cờ bật chế độ chi tiết (debug).
        
    Returns:
        Optional[str]: Địa chỉ liên hệ được tìm thấy, hoặc None nếu không tìm thấy.
    """
    if verbose:
        print(f"--- BẮT ĐẦU TRÍCH XUẤT ĐỊA CHỈ TỪ FOOTER ---")
        print(f"  URL: {url}")
        print(f"  CSS Selector Tương đương XPath: {css_selector}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # 1. Tải nội dung HTML
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if verbose:
            print("  Bước 1: Tải và phân tích HTML thành công.")

        # 2. Tìm thẻ dựa trên CSS Selector
        target_element = soup.select_one(css_selector)
        
        if verbose:
            print(f"  Bước 2: Kết quả tìm kiếm thẻ: {'Tìm thấy' if target_element else 'Không tìm thấy'}")

        if not target_element:
            # Tìm kiếm dự phòng chỉ bằng ID "Footer" và lấy văn bản
            footer = soup.find(id="Footer")
            if footer:
                 if verbose:
                    print("  Bước 2. Dự phòng: Đã tìm thấy #Footer, đang trích xuất toàn bộ văn bản Footer.")
                 return footer.get_text(strip=True, separator='\n')
            
            print(f"LỖI: Không tìm thấy thẻ theo CSS Selector ('{css_selector}') và không tìm thấy thẻ #Footer.")
            return None

        # 3. Trích xuất văn bản từ thẻ mục tiêu
        # Dùng separator='\n' để giữ lại các dòng xuống nếu có
        address_text = target_element.get_text(strip=True, separator='\n')
        
        if verbose:
             print(f"  Bước 3: Trích xuất văn bản thành công.")
             
        return address_text

    except requests.exceptions.RequestException as e:
        print(f"LỖI KẾT NỐI hoặc TẢI TRANG: {e}")
        return None
    except Exception as e:
        print(f"LỖI KHÔNG XÁC ĐỊNH trong quá trình phân tích: {e}")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trích xuất địa chỉ liên hệ từ phần footer của trang web NSMO bằng CSS Selector.")
    parser.add_argument('--verbose', '-v', action='store_true', help='Hiển thị chi tiết quá trình tìm kiếm thẻ.')
    
    args = parser.parse_args()

    address = extract_address_by_xpath_equivalent(URL, CSS_SELECTOR, args.verbose)
        
    if address:
        print("\n=======================================================")
        print("KẾT QUẢ TRÍCH XUẤT ĐỊA CHỈ LIÊN HỆ")
        print("=======================================================")        
        print(address)
    else:
        print("Không thể trích xuất địa chỉ liên hệ.")
        
    print("=======================================================")