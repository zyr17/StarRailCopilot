#!/usr/bin/env python3
"""
Simple test script for debugging
"""

import os
import sys
from pathlib import Path

def main():
    try:
        print("=== 简单测试脚本开始 ===")
        
        # 基本路径检查
        base_dir = Path("webapp") / "dist" / "win-unpacked"
        print(f"目标目录: {base_dir}")
        print(f"目录存在: {base_dir.exists()}")
        
        if not base_dir.exists():
            print("错误: 构建目录不存在")
            return 1
        
        # 创建简单的测试文件
        test_file = base_dir / "test.txt"
        test_file.write_text("测试文件创建成功\n", encoding='utf-8')
        print(f"创建测试文件: {test_file}")
        
        # 统计文件数量
        file_count = sum(1 for _ in base_dir.rglob('*') if _.is_file())
        print(f"当前文件总数: {file_count}")
        
        print("=== 简单测试完成 ===")
        return 0
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())