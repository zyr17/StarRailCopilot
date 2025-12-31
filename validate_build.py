#!/usr/bin/env python3
"""
StarRailCopilot构建验证脚本
用于验证生成的便携版本是否包含所有必需文件
"""

import os
import sys
import json
from pathlib import Path

class BuildValidator:
    def __init__(self, build_dir):
        self.build_dir = Path(build_dir)
        self.results = {
            'passed': [],
            'failed': [],
            'warnings': [],
            'stats': {}
        }
    
    def validate(self):
        """执行完整验证"""
        print("🔍 开始验证StarRailCopilot构建...")
        print(f"📁 检查目录: {self.build_dir}")
        
        if not self.build_dir.exists():
            self.add_error(f"构建目录不存在: {self.build_dir}")
            return False
        
        # 执行各项验证
        self.check_critical_files()
        self.check_file_counts()
        self.check_directory_structure()
        self.check_python_environment()
        self.check_config_files()
        self.check_resources()
        
        # 生成报告
        self.generate_report()
        
        return len(self.results['failed']) == 0
    
    def check_critical_files(self):
        """检查关键文件"""
        print("\n📋 检查关键文件...")
        
        critical_files = [
            'resources/app.asar',  # Electron主包
            'toolkit/',           # Python环境目录
            'config/',            # 配置目录
            'deploy/',            # 部署目录
            'chrome_100_percent.pak',  # Chrome资源
            'd3dcompiler_47.dll', # DirectX组件
        ]
        
        for file_path in critical_files:
            full_path = self.build_dir / file_path
            if full_path.exists():
                self.add_pass(f"✅ 关键文件存在: {file_path}")
            else:
                self.add_error(f"❌ 关键文件缺失: {file_path}")
    
    def check_file_counts(self):
        """检查文件数量"""
        print("\n📊 统计文件数量...")
        
        try:
            # 统计总文件数
            all_files = list(self.build_dir.rglob('*'))
            file_count = len([f for f in all_files if f.is_file()])
            dir_count = len([f for f in all_files if f.is_dir()])
            
            # 统计不同类型文件
            py_files = list(self.build_dir.rglob('*.py'))
            dll_files = list(self.build_dir.rglob('*.dll'))
            pyd_files = list(self.build_dir.rglob('*.pyd'))
            json_files = list(self.build_dir.rglob('*.json'))
            yaml_files = list(self.build_dir.rglob('*.yaml'))
            yml_files = list(self.build_dir.rglob('*.yml'))
            
            self.results['stats'] = {
                'total_files': file_count,
                'total_dirs': dir_count,
                'python_files': len(py_files),
                'dll_files': len(dll_files),
                'pyd_files': len(pyd_files),
                'json_files': len(json_files),
                'yaml_files': len(yaml_files) + len(yml_files)
            }
            
            print(f"   总文件数: {file_count}")
            print(f"   总目录数: {dir_count}")
            print(f"   Python文件: {len(py_files)}")
            print(f"   DLL文件: {len(dll_files)}")
            print(f"   PYD文件: {len(pyd_files)}")
            print(f"   配置文件: {len(json_files) + len(yaml_files) + len(yml_files)}")
            
            # 验证文件数量是否合理
            if file_count < 1000:
                self.add_warning(f"文件数量较少 ({file_count}), 可能存在缺失")
            elif file_count < 5000:
                self.add_warning(f"文件数量偏少 ({file_count}), 建议检查是否完整")
            elif file_count < 10000:
                self.add_pass(f"文件数量基本合理 ({file_count})")
            else:
                self.add_pass(f"文件数量充足 ({file_count})")
                
            # Python文件数量检查
            if len(py_files) < 100:
                self.add_error(f"Python文件过少 ({len(py_files)}), 缺少Python环境")
            elif len(py_files) < 1000:
                self.add_warning(f"Python文件偏少 ({len(py_files)}), 可能不完整")
            else:
                self.add_pass(f"Python文件数量充足 ({len(py_files)})")
                
        except Exception as e:
            self.add_error(f"文件统计失败: {e}")
    
    def check_directory_structure(self):
        """检查目录结构"""
        print("\n📁 检查目录结构...")
        
        expected_dirs = [
            'toolkit',
            'config', 
            'deploy',
            'resources',
            'locales',
            'assets'
        ]
        
        for dir_name in expected_dirs:
            dir_path = self.build_dir / dir_name
            if dir_path.exists():
                file_count = len(list(dir_path.rglob('*')))
                self.add_pass(f"✅ 目录存在: {dir_name} ({file_count} 个文件)")
            else:
                self.add_error(f"❌ 目录缺失: {dir_name}")
    
    def check_python_environment(self):
        """检查Python环境"""
        print("\n🐍 检查Python环境...")
        
        # 检查Python DLL
        python_dlls = [
            'toolkit/DLLs/python37.dll',
            'toolkit/DLLs/python38.dll', 
            'toolkit/DLLs/python39.dll',
            'toolkit/DLLs/python310.dll'
        ]
        
        dll_found = False
        for dll in python_dlls:
            if (self.build_dir / dll).exists():
                self.add_pass(f"✅ Python DLL存在: {dll}")
                dll_found = True
                break
        
        if not dll_found:
            self.add_error("❌ Python DLL文件缺失，无法运行Python代码")
        
        # 检查Python标准库
        lib_path = self.build_dir / 'toolkit/Lib'
        if lib_path.exists():
            lib_files = len(list(lib_path.rglob('*.py')))
            if lib_files > 100:
                self.add_pass(f"✅ Python标准库完整 ({lib_files} 个文件)")
            else:
                self.add_warning(f"⚠️ Python标准库可能不完整 ({lib_files} 个文件)")
        else:
            self.add_error("❌ Python标准库目录缺失")
    
    def check_config_files(self):
        """检查配置文件"""
        print("\n⚙️ 检查配置文件...")
        
        config_files = [
            'config/deploy.yaml',
            'config/template.json',
            'deploy/installer.py',
            'deploy/set.py'
        ]
        
        for config_file in config_files:
            file_path = self.build_dir / config_file
            if file_path.exists():
                self.add_pass(f"✅ 配置文件存在: {config_file}")
            else:
                self.add_error(f"❌ 配置文件缺失: {config_file}")
    
    def check_resources(self):
        """检查资源文件"""
        print("\n🎨 检查资源文件...")
        
        # 检查app.asar
        asar_path = self.build_dir / 'resources/app.asar'
        if asar_path.exists():
            size_mb = asar_path.stat().st_size / (1024 * 1024)
            if size_mb > 1:
                self.add_pass(f"✅ app.asar文件存在 ({size_mb:.1f} MB)")
            else:
                self.add_warning(f"⚠️ app.asar文件过小 ({size_mb:.1f} MB)")
        else:
            self.add_error("❌ app.asar文件缺失")
        
        # 检查Chrome资源
        chrome_files = [
            'chrome_100_percent.pak',
            'chrome_200_percent.pak',
            'locales/en-US.pak'
        ]
        
        for chrome_file in chrome_files:
            if (self.build_dir / chrome_file).exists():
                self.add_pass(f"✅ Chrome资源存在: {chrome_file}")
            else:
                self.add_error(f"❌ Chrome资源缺失: {chrome_file}")
    
    def add_pass(self, message):
        """添加通过检查"""
        self.results['passed'].append(message)
        print(f"   {message}")
    
    def add_error(self, message):
        """添加错误"""
        self.results['failed'].append(message)
        print(f"   {message}")
    
    def add_warning(self, message):
        """添加警告"""
        self.results['warnings'].append(message)
        print(f"   {message}")
    
    def generate_report(self):
        """生成验证报告"""
        print("\n" + "="*60)
        print("📋 验证报告")
        print("="*60)
        
        print(f"\n✅ 通过检查: {len(self.results['passed'])}")
        print(f"❌ 错误: {len(self.results['failed'])}")
        print(f"⚠️ 警告: {len(self.results['warnings'])}")
        
        if self.results['stats']:
            print(f"\n📊 文件统计:")
            for key, value in self.results['stats'].items():
                print(f"   {key}: {value}")
        
        if self.results['failed']:
            print(f"\n❌ 错误详情:")
            for error in self.results['failed']:
                print(f"   • {error}")
        
        if self.results['warnings']:
            print(f"\n⚠️ 警告详情:")
            for warning in self.results['warnings']:
                print(f"   • {warning}")
        
        # 最终判定
        if len(self.results['failed']) == 0:
            print(f"\n🎉 验证通过! 构建版本质量良好。")
            return True
        else:
            print(f"\n💥 验证失败! 存在 {len(self.results['failed'])} 个严重问题。")
            return False

def main():
    if len(sys.argv) != 2:
        print("用法: python validate_build.py <构建目录>")
        sys.exit(1)
    
    build_dir = sys.argv[1]
    validator = BuildValidator(build_dir)
    success = validator.validate()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
