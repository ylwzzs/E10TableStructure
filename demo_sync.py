#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
阿里云OSS同步功能演示

这个脚本演示了如何确保OSS上的文件与GitHub版本完全一致。
主要功能包括：
1. 自动发现需要部署的文件
2. 智能排除不需要的文件
3. 计算文件差异
4. 执行删除和上传操作
"""

import os
import fnmatch
from pathlib import Path

def demo_sync_process():
    """演示同步过程"""
    
    print("🔄 阿里云OSS同步功能演示")
    print("=" * 60)
    
    # 模拟本地文件列表
    local_files = [
        'index.html',
        'table_list.json',
        'server.py',
        'README.md',
        'resources/table1.html',
        'resources/table2.html',
        'resources/css/style.css',
        'resources/js/script.js'
    ]
    
    # 模拟OSS现有文件列表（包含一些旧文件）
    oss_files = [
        'index.html',
        'table_list.json',
        'old_file.html',  # 需要删除的旧文件
        'deprecated.js',  # 需要删除的旧文件
        'resources/table1.html',
        'resources/table2.html',
        'resources/css/style.css'
    ]
    
    print("📁 本地文件列表:")
    for file in local_files:
        print(f"   ✅ {file}")
    
    print(f"\n☁️  OSS现有文件列表:")
    for file in oss_files:
        print(f"   📄 {file}")
    
    # 计算需要删除的文件
    files_to_delete = [f for f in oss_files if f not in local_files]
    
    # 计算需要上传的文件
    files_to_upload = [f for f in local_files if f not in oss_files or True]  # 简化处理
    
    print(f"\n🗑️  需要删除的文件 ({len(files_to_delete)} 个):")
    for file in files_to_delete:
        print(f"   ❌ {file}")
    
    print(f"\n📤 需要上传的文件 ({len(files_to_upload)} 个):")
    for file in files_to_upload:
        print(f"   ✅ {file}")
    
    # 模拟同步操作
    print(f"\n🔄 执行同步操作:")
    print("   1. 删除多余文件...")
    for file in files_to_delete:
        print(f"      🗑️  删除: {file}")
    
    print("   2. 上传/更新文件...")
    for file in files_to_upload:
        print(f"      📤 上传: {file}")
    
    print(f"\n🎉 同步完成！")
    print(f"📊 最终结果:")
    print(f"   - 删除文件: {len(files_to_delete)} 个")
    print(f"   - 上传文件: {len(files_to_upload)} 个")
    print(f"   - 最终文件总数: {len(local_files)} 个")
    
    print(f"\n✨ 同步优势:")
    print(f"   - 🔄 确保OSS与GitHub版本完全一致")
    print(f"   - 🗑️  自动清理已删除的文件")
    print(f"   - 📤 自动上传新增的文件")
    print(f"   - 🔧 自动更新修改的文件")
    print(f"   - 🚫 智能排除不需要的文件")

def demo_content_type_setting():
    """演示Content-Type设置"""
    
    print(f"\n🔧 Content-Type设置演示")
    print("=" * 40)
    
    test_files = [
        ('index.html', 'text/html; charset=utf-8'),
        ('table_list.json', 'application/json; charset=utf-8'),
        ('style.css', 'text/css; charset=utf-8'),
        ('script.js', 'application/javascript; charset=utf-8'),
        ('image.png', 'image/png'),
        ('README.md', 'text/markdown; charset=utf-8')
    ]
    
    for file_path, expected_type in test_files:
        print(f"   📄 {file_path}")
        print(f"      Content-Type: {expected_type}")
        if 'charset=utf-8' in expected_type:
            print(f"      ✅ 确保中文字符正确显示")

if __name__ == "__main__":
    demo_sync_process()
    demo_content_type_setting()
    
    print(f"\n" + "=" * 60)
    print("💡 使用说明:")
    print("   1. 运行 python3 deploy.py 进行实际部署")
    print("   2. 运行 python3 test_sync.py 测试同步功能")
    print("   3. 推送代码到GitHub会自动触发部署") 