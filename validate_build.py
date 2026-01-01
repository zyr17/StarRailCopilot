#!/usr/bin/env python3
"""
StarRailCopilot Build Validation Script
Used to verify that the generated portable version contains all required files
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
        """Perform complete validation"""
        print("[INFO] Starting StarRailCopilot build validation...")
        print(f"[INFO] Checking directory: {self.build_dir}")
        
        if not self.build_dir.exists():
            self.add_error(f"Build directory does not exist: {self.build_dir}")
            return False
        
        # Perform various validations
        self.check_critical_files()
        self.check_file_counts()
        self.check_directory_structure()
        self.check_python_environment()
        self.check_config_files()
        self.check_resources()
        
        # Generate report
        self.generate_report()
        
        return len(self.results['failed']) == 0
    
    def check_critical_files(self):
        """Check critical files"""
        print("\n[CHECK] Checking critical files...")
        
        critical_files = [
            'resources/app.asar',  # Electron main package
            'toolkit/',           # Python environment directory
            'config/',            # Configuration directory
            'deploy/',            # Deployment directory
            'chrome_100_percent.pak',  # Chrome resources
            'd3dcompiler_47.dll', # DirectX components
        ]
        
        for file_path in critical_files:
            full_path = self.build_dir / file_path
            if full_path.exists():
                self.add_pass(f"[OK] Critical file exists: {file_path}")
            else:
                self.add_error(f"[ERROR] Critical file missing: {file_path}")
    
    def check_file_counts(self):
        """Check file count"""
        print("\n[STATS] Counting files...")
        
        try:
            # Count total files
            all_files = list(self.build_dir.rglob('*'))
            file_count = len([f for f in all_files if f.is_file()])
            dir_count = len([f for f in all_files if f.is_dir()])
            
            # Count different file types
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
            
            print(f"   Total files: {file_count}")
            print(f"   Total directories: {dir_count}")
            print(f"   Python files: {len(py_files)}")
            print(f"   DLL files: {len(dll_files)}")
            print(f"   PYD files: {len(pyd_files)}")
            print(f"   Config files: {len(json_files) + len(yaml_files) + len(yml_files)}")
            
            # Verify file count is reasonable
            if file_count < 1000:
                self.add_warning(f"File count is low ({file_count}), may be missing files")
            elif file_count < 5000:
                self.add_warning(f"File count is somewhat low ({file_count}), check completeness")
            elif file_count < 10000:
                self.add_pass(f"File count is acceptable ({file_count})")
            else:
                self.add_pass(f"File count is sufficient ({file_count})")
                
            # Python file count check
            if len(py_files) < 100:
                self.add_error(f"Python files too few ({len(py_files)}), missing Python environment")
            elif len(py_files) < 1000:
                self.add_warning(f"Python files somewhat few ({len(py_files)}), may be incomplete")
            else:
                self.add_pass(f"Python file count sufficient ({len(py_files)})")
                
        except Exception as e:
            self.add_error(f"File counting failed: {e}")
    
    def check_directory_structure(self):
        """Check directory structure"""
        print("\n[DIR] Checking directory structure...")
        
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
                self.add_pass(f"[OK] Directory exists: {dir_name} ({file_count} files)")
            else:
                self.add_error(f"[ERROR] Directory missing: {dir_name}")
    
    def check_python_environment(self):
        """Check Python environment"""
        print("\n[PYTHON] Checking Python environment...")
        
        # Check Python DLL
        python_dlls = [
            'toolkit/DLLs/python37.dll',
            'toolkit/DLLs/python38.dll', 
            'toolkit/DLLs/python39.dll',
            'toolkit/DLLs/python310.dll'
        ]
        
        dll_found = False
        for dll in python_dlls:
            if (self.build_dir / dll).exists():
                self.add_pass(f"[OK] Python DLL exists: {dll}")
                dll_found = True
                break
        
        if not dll_found:
            self.add_error("[ERROR] Python DLL files missing, cannot run Python code")
        
        # Check Python standard library
        lib_path = self.build_dir / 'toolkit/Lib'
        if lib_path.exists():
            lib_files = len(list(lib_path.rglob('*.py')))
            if lib_files > 100:
                self.add_pass(f"[OK] Python standard library complete ({lib_files} files)")
            else:
                self.add_warning(f"[WARN] Python standard library may be incomplete ({lib_files} files)")
        else:
            self.add_error("[ERROR] Python standard library directory missing")
    
    def check_config_files(self):
        """Check configuration files"""
        print("\n[CONFIG] Checking config files...")
        
        config_files = [
            'config/deploy.yaml',
            'config/template.json',
            'deploy/installer.py',
            'deploy/set.py'
        ]
        
        for config_file in config_files:
            file_path = self.build_dir / config_file
            if file_path.exists():
                self.add_pass(f"[OK] Config file exists: {config_file}")
            else:
                self.add_error(f"[ERROR] Config file missing: {config_file}")
    
    def check_resources(self):
        """Check resource files"""
        print("\n[RESOURCES] Checking resource files...")
        
        # Check app.asar
        asar_path = self.build_dir / 'resources/app.asar'
        if asar_path.exists():
            size_mb = asar_path.stat().st_size / (1024 * 1024)
            if size_mb > 1:
                self.add_pass(f"[OK] app.asar file exists ({size_mb:.1f} MB)")
            else:
                self.add_warning(f"[WARN] app.asar file too small ({size_mb:.1f} MB)")
        else:
            self.add_error("[ERROR] app.asar file missing")
        
        # Check Chrome resources
        chrome_files = [
            'chrome_100_percent.pak',
            'chrome_200_percent.pak',
            'locales/en-US.pak'
        ]
        
        for chrome_file in chrome_files:
            if (self.build_dir / chrome_file).exists():
                self.add_pass(f"[OK] Chrome resource exists: {chrome_file}")
            else:
                self.add_error(f"[ERROR] Chrome resource missing: {chrome_file}")
    
    def add_pass(self, message):
        """Add pass check"""
        self.results['passed'].append(message)
        print(f"   {message}")
    
    def add_error(self, message):
        """Add error"""
        self.results['failed'].append(message)
        print(f"   {message}")
    
    def add_warning(self, message):
        """Add warning"""
        self.results['warnings'].append(message)
        print(f"   {message}")
    
    def generate_report(self):
        """Generate validation report"""
        print("\n" + "="*60)
        print("VALIDATION REPORT")
        print("="*60)
        
        print(f"\n[PASS] Passed checks: {len(self.results['passed'])}")
        print(f"[ERROR] Errors: {len(self.results['failed'])}")
        print(f"[WARN] Warnings: {len(self.results['warnings'])}")
        
        if self.results['stats']:
            print(f"\n[STATS] File statistics:")
            for key, value in self.results['stats'].items():
                print(f"   {key}: {value}")
        
        if self.results['failed']:
            print(f"\n[ERROR] Error details:")
            for error in self.results['failed']:
                print(f"   • {error}")
        
        if self.results['warnings']:
            print(f"\n[WARN] Warning details:")
            for warning in self.results['warnings']:
                print(f"   • {warning}")
        
        # Final determination
        if len(self.results['failed']) == 0:
            print(f"\n[SUCCESS] Validation passed! Build quality is good.")
            return True
        else:
            print(f"\n[FAIL] Validation failed! {len(self.results['failed'])} critical issues found.")
            return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_build.py <build_directory>")
        sys.exit(1)
    
    build_dir = sys.argv[1]
    validator = BuildValidator(build_dir)
    success = validator.validate()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
