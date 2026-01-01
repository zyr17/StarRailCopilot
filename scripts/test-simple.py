#!/usr/bin/env python3
"""
Simple test script for debugging
"""

import os
import sys
from pathlib import Path

def main():
    try:
        print("=== 详细测试脚本开始 ===")
        
        # 检查当前工作目录
        print(f"当前工作目录: {Path.cwd()}")
        
        # 检查webapp目录
        webapp_dir = Path("webapp")
        print(f"webapp目录存在: {webapp_dir.exists()}")
        if webapp_dir.exists():
            print(f"webapp目录内容:")
            for item in webapp_dir.iterdir():
                print(f"  - {item.name} ({'directory' if item.is_dir() else 'file'})")
        
        # 检查dist目录
        dist_dir = Path("webapp") / "dist"
        print(f"dist目录存在: {dist_dir.exists()}")
        if dist_dir.exists():
            print(f"dist目录内容:")
            for item in dist_dir.iterdir():
                print(f"  - {item.name} ({'directory' if item.is_dir() else 'file'})")
        
        # 检查目标目录
        base_dir = Path("webapp") / "dist" / "win-unpacked"
        print(f"目标目录: {base_dir}")
        print(f"目标目录存在: {base_dir.exists()}")
        
        if not base_dir.exists():
            print("错误: 构建目录不存在")
            return 1
        
        # 统计现有文件
        file_count = sum(1 for _ in base_dir.rglob('*') if _.is_file())
        print(f"构建目录中现有文件数: {file_count}")
        
        # 创建简单的测试文件
        test_file = base_dir / "test.txt"
        test_file.write_text("测试文件创建成功\n", encoding='utf-8')
        print(f"创建测试文件: {test_file}")
        
        # 重新统计
        file_count = sum(1 for _ in base_dir.rglob('*') if _.is_file())
        print(f"创建测试文件后总数: {file_count}")
        
        print("=== 详细测试完成 ===")
        return 0
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())