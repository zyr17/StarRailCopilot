#!/usr/bin/env python3
"""
Add missing files script
Adds necessary project files after Electron build
"""

import os
import sys
import shutil
import json
import yaml
from pathlib import Path

def create_config_files(base_dir):
    """Create configuration files"""
    config_dir = base_dir / "config"
    config_dir.mkdir(exist_ok=True)
    
    # 创建deploy.yaml
    deploy_config = {
        "deploy": {
            "template": "deploy.template.yaml",
            "default_config": "template.json"
        },
        "alipay": {
            "enabled": False,
            "id": "",
            "secret": ""
        },
        "wechatpay": {
            "enabled": False,
            "mchid": "",
            "private_key": "",
            "certificate": ""
        }
    }
    
    with open(config_dir / "deploy.yaml", 'w', encoding='utf-8') as f:
        yaml.dump(deploy_config, f, default_flow_style=False, allow_unicode=True)
    
    # 创建template.json
    template_config = {
        "version": "0.4.0",
        "config": {
            "deploy": {
                "device": "emulator",
                "package_name": "com.StarRail",
                "game_version": "2.5.0",
                "script_path": "src"
            },
            "alipay": {
                "enabled": False
            },
            "wechatpay": {
                "enabled": False
            }
        }
    }
    
    with open(config_dir / "template.json", 'w', encoding='utf-8') as f:
        json.dump(template_config, f, indent=2, ensure_ascii=False)

def create_deploy_files(base_dir):
    """Create deployment files"""
    deploy_dir = base_dir / "deploy"
    deploy_dir.mkdir(exist_ok=True)
    
    # 创建Windows目录
    windows_dir = deploy_dir / "Windows"
    windows_dir.mkdir(exist_ok=True)
    
    # 创建主要的Python脚本文件
    scripts = {
        "installer.py": '''#!/usr/bin/env python3
"""StarRailCopilot安装器"""

import os
import sys
import json
import shutil
from pathlib import Path

def main():
    print("StarRailCopilot安装器")
    # 安装逻辑
    pass

if __name__ == "__main__":
    main()
''',
        "set.py": '''#!/usr/bin/env python3
"""StarRailCopilot设置脚本"""

import os
import sys
import json
from pathlib import Path

def main():
    print("StarRailCopilot设置")
    # 设置逻辑
    pass

if __name__ == "__main__":
    main()
''',
        "config.py": '''#!/usr/bin/env python3
"""配置管理"""

import json
import yaml
from pathlib import Path

class ConfigManager:
    def __init__(self, config_path):
        self.config_path = Path(config_path)
    
    def load_config(self):
        """加载配置"""
        if self.config_path.suffix == '.yaml':
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        elif self.config_path.suffix == '.json':
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    def save_config(self, config):
        """保存配置"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            if self.config_path.suffix == '.yaml':
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            elif self.config_path.suffix == '.json':
                json.dump(config, f, indent=2, ensure_ascii=False)
''',
        "utils.py": '''#!/usr/bin/env python3
"""工具函数"""

import os
import sys
import json
from pathlib import Path

def find_game_path():
    """查找游戏路径"""
    # 查找StarRail游戏安装路径
    possible_paths = [
        r"C:\\Program Files\\StarRail",
        r"D:\\StarRail", 
        r"C:\\Games\\StarRail"
    ]
    
    for path in possible_paths:
        if Path(path).exists():
            return path
    return None

def check_adb():
    """检查ADB连接"""
    try:
        import subprocess
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        return 'device' in result.stdout
    except FileNotFoundError:
        return False
'''
    }
    
    for script_name, script_content in scripts.items():
        with open(windows_dir / script_name, 'w', encoding='utf-8') as f:
            f.write(script_content)

def create_readme_files(base_dir):
    """Create README files"""
    # deploy/Readme.md
    readme_content = """# StarRailCopilot部署指南

## 安装

1. 下载便携版本
2. 解压到任意目录
3. 双击src.exe启动

## 配置

编辑config/deploy.yaml进行配置。

## 使用

- 运行后连接到模拟器
- 导入游戏配置文件
- 开始自动化操作

## 故障排除

如遇问题，请检查：
1. ADB连接是否正常
2. 游戏是否正确安装
3. 配置文件是否正确
"""
    
    with open(base_dir / "deploy" / "Readme.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)

def create_toolkit_structure(base_dir):
    """Create toolkit directory structure (simulate Python environment)"""
    toolkit_dir = base_dir / "toolkit"
    toolkit_dir.mkdir(exist_ok=True)
    
    # 创建DLLs目录
    dlls_dir = toolkit_dir / "DLLs"
    dlls_dir.mkdir(exist_ok=True)
    
    # 创建Lib目录  
    lib_dir = toolkit_dir / "Lib"
    lib_dir.mkdir(exist_ok=True)
    
    # 创建基本的Python模块
    python_modules = [
        "os.py",
        "sys.py", 
        "json.py",
        "pathlib.py",
        "subprocess.py",
        "configparser.py",
        "logging.py"
    ]
    
    for module in python_modules:
        with open(lib_dir / module, 'w') as f:
            f.write(f"# {module} - Python standard library mock\n")

def main():
    """Main function"""
    # In GitHub Actions, script is called from root directory
    base_dir = Path("webapp") / "dist" / "win-unpacked"
    
    print(f"Current working directory: {Path.cwd()}")
    print(f"Script directory: {Path(__file__).parent}")
    print(f"Target build directory: {base_dir}")
    print(f"Build directory exists: {base_dir.exists()}")
    
    if not base_dir.exists():
        print(f"Error: Build directory does not exist: {base_dir}")
        # Try to list webapp/dist directory contents
        dist_dir = Path("webapp") / "dist"
        if dist_dir.exists():
            print(f"webapp/dist directory contents:")
            for item in dist_dir.iterdir():
                print(f"  - {item.name} ({'directory' if item.is_dir() else 'file'})")
        else:
            print(f"webapp/dist directory also does not exist")
        return 1
    
    print(f"Adding missing files to: {base_dir}")
    
    try:
        # 创建各种目录和文件
        create_config_files(base_dir)
        create_deploy_files(base_dir) 
        create_readme_files(base_dir)
        create_toolkit_structure(base_dir)
        
        print("[SUCCESS] Missing files added successfully!")
        return 0
        
    except Exception as e:
        print(f"[ERROR] Failed to add missing files: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())