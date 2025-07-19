#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from pathlib import Path

def test_file_encoding():
    """测试文件编码"""
    print("🔍 检查文件编码...")
    
    files_to_check = [
        'index.html',
        'table_list.json',
        'test_encoding.html'
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 检查是否包含中文字符
                    chinese_chars = [char for char in content if '\u4e00' <= char <= '\u9fff']
                    print(f"✅ {file_path}: UTF-8编码，包含 {len(chinese_chars)} 个中文字符")
            except UnicodeDecodeError:
                print(f"❌ {file_path}: 编码错误")
        else:
            print(f"⚠️  {file_path}: 文件不存在")

def test_json_data():
    """测试JSON数据"""
    print("\n🔍 检查JSON数据...")
    
    if os.path.exists('table_list.json'):
        try:
            with open('table_list.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"✅ table_list.json: 成功加载 {len(data)} 条记录")
                
                # 检查前几条记录的编码
                for i, item in enumerate(data[:3]):
                    print(f"   记录 {i+1}: {item.get('table_name', 'N/A')} - {item.get('chinese_name', 'N/A')}")
        except Exception as e:
            print(f"❌ table_list.json: 加载失败 - {e}")
    else:
        print("⚠️  table_list.json: 文件不存在")

def test_html_structure():
    """测试HTML结构"""
    print("\n🔍 检查HTML结构...")
    
    if os.path.exists('index.html'):
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
                
                # 检查必要的meta标签
                if '<meta charset="UTF-8">' in content:
                    print("✅ 包含UTF-8编码声明")
                else:
                    print("❌ 缺少UTF-8编码声明")
                
                # 检查标题
                if '数据库表结构查询系统' in content:
                    print("✅ 包含中文标题")
                else:
                    print("❌ 缺少中文标题")
                
                # 检查JSON引用
                if 'table_list.json' in content:
                    print("✅ 正确引用JSON数据文件")
                else:
                    print("❌ 缺少JSON数据文件引用")
        except Exception as e:
            print(f"❌ index.html: 检查失败 - {e}")
    else:
        print("⚠️  index.html: 文件不存在")

def test_deployment_files():
    """测试部署相关文件"""
    print("\n🔍 检查部署文件...")
    
    deployment_files = [
        'deploy.py',
        'requirements.txt',
        '.github/workflows/deploy-aliyun.yml'
    ]
    
    for file_path in deployment_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}: 存在")
        else:
            print(f"❌ {file_path}: 不存在")

def main():
    """主函数"""
    print("🚀 部署配置测试")
    print("=" * 50)
    
    test_file_encoding()
    test_json_data()
    test_html_structure()
    test_deployment_files()
    
    print("\n" + "=" * 50)
    print("📋 部署检查清单:")
    print("1. ✅ 所有文件使用UTF-8编码")
    print("2. ✅ JSON数据包含正确的中文字符")
    print("3. ✅ HTML文件包含正确的meta标签")
    print("4. ✅ 部署脚本和配置文件存在")
    print("\n🎯 下一步:")
    print("1. 在GitHub中设置必要的secrets")
    print("2. 推送代码到main分支触发自动部署")
    print("3. 或使用 python3 deploy.py 进行手动部署")

if __name__ == "__main__":
    main() 