#!/usr/bin/env python3
"""
Setup script for IntelliPark-System
Tự động cài đặt dependencies và kiểm tra môi trường
"""

import subprocess
import sys
import os

def run_command(command):
    """Chạy lệnh và trả về kết quả"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_python_version():
    """Kiểm tra phiên bản Python"""
    if sys.version_info < (3, 7):
        print("❌ Cần Python 3.7 trở lên!")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} - OK")
    return True

def check_files():
    """Kiểm tra các file cần thiết"""
    print("🔍 Kiểm tra các file cần thiết...")
    
    required_files = [
        "data/parking_1920_1080_loop.mp4",
        "model/model.p", 
        "mask_1920_1080.png"
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - KHÔNG TÌM THẤY")
            missing_files.append(file_path)
    
    if missing_files:
        print("\n⚠️  Một số file bị thiếu!")
        print("📥 Tải dữ liệu từ: https://drive.google.com/drive/folders/1CjEFWihRqTLNUnYRwHXxGAVwSXF2k8QC?usp=sharing")
        return False
    
    print("✅ Tất cả file cần thiết đã có!")
    return True

def main():
    """Hàm chính"""
    print("🚀 Parking Space Counter - Setup")
    print("=" * 40)
    
    # Kiểm tra Python version
    if not check_python_version():
        sys.exit(1)
    
    # Kiểm tra files
    if not check_files():
        print("\n💡 Sau khi tải dữ liệu, chạy lại: python setup.py")
        sys.exit(1)
    
    print("\n🎉 Setup hoàn tất!")
    print("🚀 Chạy dự án: python main.py")
    print("📖 Xem hướng dẫn: README.md")

if __name__ == "__main__":
    main()