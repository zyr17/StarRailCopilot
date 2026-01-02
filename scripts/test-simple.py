#!/usr/bin/env python3
"""
Simple test script for debugging
"""

import os
import sys
from pathlib import Path

def main():
    try:
        print("=== Detailed test script started ===")
        
        # Check current working directory
        print(f"Current working directory: {Path.cwd()}")
        
        # Check webapp directory
        webapp_dir = Path("webapp")
        print(f"Webapp directory exists: {webapp_dir.exists()}")
        if webapp_dir.exists():
            print(f"Webapp directory contents:")
            for item in webapp_dir.iterdir():
                print(f"  - {item.name} ({'directory' if item.is_dir() else 'file'})")
        
        # Check dist directory
        dist_dir = Path("webapp") / "dist"
        print(f"Dist directory exists: {dist_dir.exists()}")
        if dist_dir.exists():
            print(f"Dist directory contents:")
            for item in dist_dir.iterdir():
                print(f"  - {item.name} ({'directory' if item.is_dir() else 'file'})")
        
        # Check target directory
        base_dir = Path("webapp") / "dist" / "win-unpacked"
        print(f"Target directory: {base_dir}")
        print(f"Target directory exists: {base_dir.exists()}")
        
        if not base_dir.exists():
            print("ERROR: Build directory does not exist")
            return 1
        
        # Count existing files
        file_count = sum(1 for _ in base_dir.rglob('*') if _.is_file())
        print(f"Current file count in build directory: {file_count}")
        
        # Create simple test file
        test_file = base_dir / "test.txt"
        test_file.write_text("Test file created successfully\n", encoding='utf-8')
        print(f"Created test file: {test_file}")
        
        # Recount files
        file_count = sum(1 for _ in base_dir.rglob('*') if _.is_file())
        print(f"Total files after test: {file_count}")
        
        print("=== Detailed test completed ===")
        return 0
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())