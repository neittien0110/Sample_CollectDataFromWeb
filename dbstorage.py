import requests
import json
import pyodbc
import os
import sys
from typing import List, Dict, Any, Optional

# --- CẤU HÌNH VÀ HẰNG SỐ ---
CONFIG_FILE = "sqlserver.json"

# Biến kết nối toàn cục
conn: Optional[pyodbc.Connection] = None

# --- CHỨC NĂNG KẾT NỐI CƠ SỞ DỮ LIỆU ---

def DBInit() -> Optional[pyodbc.Connection]:
    """
    Khởi tạo kết nối đến SQL Server bằng cách đọc ConnectionString từ file cấu hình.
    """
    global conn
    
    if conn:
        print("Kết nối đã được khởi tạo trước đó.")
        return conn

    if not os.path.exists(CONFIG_FILE):
        print(f"LỖI: Không tìm thấy file cấu hình '{CONFIG_FILE}'.")
        return None

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            conn_str = config.get("ConnectionString")
            if not conn_str:
                print("LỖI: File cấu hình không chứa khóa 'ConnectionString'.")
                return None

        # Thiết lập kết nối
        conn = pyodbc.connect(conn_str)
        print("THÀNH CÔNG: Đã kết nối đến SQL Server.")
        return conn

    except FileNotFoundError:
        print(f"LỖI: Không tìm thấy file '{CONFIG_FILE}'.")
    except json.JSONDecodeError:
        print(f"LỖI: File '{CONFIG_FILE}' không phải là JSON hợp lệ.")
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"LỖI KẾT NỐI DB: {sqlstate}")
        print("Vui lòng kiểm tra lại ConnectionString và Driver.")
    except Exception as e:
        print(f"LỖI KHÔNG XÁC ĐỊNH: {e}")
        
    return None

def DBClose():
    """Đóng kết nối cơ sở dữ liệu nếu nó đang mở."""
    global conn
    if conn:
        conn.close()
        conn = None
        print("\nĐã đóng kết nối SQL Server.")

def get_source_id(source_name: str) -> Optional[int]:
    """
    Tìm Source ID từ bảng DataSource_Header dựa trên source_name.
    Nếu không tìm thấy, sẽ tạo mới và trả về ID.
    """
    if not conn:
        print("LỖI: Kết nối DB chưa được thiết lập.")
        return None

    cursor = conn.cursor()
    try:
        # 1. Tìm Source_ID hiện có
        cursor.execute("SELECT source_id FROM DataSource_Header WHERE source_name = ?", source_name)
        row = cursor.fetchone()
        
        if row:
            source_id = row[0]
            # print(f"  > Tìm thấy Source ID: {source_id} cho '{source_name}'.")
            return source_id
        
        # 2. Nếu không có, tạo mới
        # *Lưu ý: Giả định source_id là IDENTITY và cột 'source_name' là NVARCHAR*
        cursor.execute("INSERT INTO DataSource_Header (source_name) VALUES (?)", source_name)
        cursor.execute("SELECT SCOPE_IDENTITY()") # Lấy ID vừa được tạo
        new_id = cursor.fetchone()[0]
        conn.commit()
        # print(f"  > Đã tạo mới Source ID: {new_id} cho '{source_name}'.")
        return int(new_id)

    except pyodbc.Error as ex:
        print(f"LỖI DB khi tìm/tạo Source ID cho '{source_name}': {ex}")
        conn.rollback()
        return None
    finally:
        cursor.close()

def DBWrite_CongSuatMTMN(source_fk: int, value: float, time: str) -> bool:
    """
    Ghi dữ liệu công suất vào bảng CongSuatMTMN.
    Kiểm tra trùng lặp trước khi INSERT.
    """
    if not conn: return False

    cursor = conn.cursor()
    try:
        # 1. Kiểm tra trùng lặp
        cursor.execute("""
            SELECT 1 FROM CongSuatMTMN 
            WHERE source_fk = ? AND measurement_time = ? AND measurement_value = ?
        """, source_fk, time, value)
        
        if cursor.fetchone():
            # print(f"  Đã tồn tại: (Source:{source_fk}, Time:{time}, Value:{value}). Bỏ qua.")
            return True # Đánh dấu là thành công (vì không cần làm gì)

        # 2. Nếu không trùng lặp, thực hiện INSERT
        # *Lưu ý: Giả định các cột 'measurement_time' là NVARCHAR và 'measurement_value' là FLOAT/DECIMAL*
        cursor.execute("""
            INSERT INTO CongSuatMTMN (source_fk, measurement_time, measurement_value) 
            VALUES (?, ?, ?)
        """, source_fk, time, value)
        
        conn.commit()
        # print(f"  SUCCESS: Đã ghi bản ghi mới: (Source:{source_fk}, Time:{time}, Value:{value})")
        return True

    except pyodbc.Error as ex:
        print(f"LỖI DB khi ghi dữ liệu: (Source:{source_fk}, Time:{time}, Value:{value}): {ex}")
        conn.rollback()
        return False
    finally:
        cursor.close()

