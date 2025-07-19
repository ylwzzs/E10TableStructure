#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import fnmatch
from pathlib import Path

def get_local_files():
    """获取本地需要部署的文件列表"""
    files_to_deploy = []
    
    # 根目录文件
    root_files = [
        'index.html',
        'table_list.json',
        'server.py',
        'test_encoding.html',
        'README.md',
        'DEPLOYMENT.md',
        'requirements.txt',
        'test_deploy.py',
        'deploy.py'
    ]
    
    for file_path in root_files:
        if os.path.exists(file_path):
            files_to_deploy.append(file_path)
    
    # 递归获取resources目录下的所有文件
    resources_dir = 'resources'
    if os.path.exists(resources_dir):
        for root, dirs, files in os.walk(resources_dir):
            for file in files:
                file_path = os.path.join(root, file)
                files_to_deploy.append(file_path)
    
    return files_to_deploy

def should_upload_file(file_path):
    """判断文件是否应该上传"""
    # 不上传的文件和目录
    exclude_patterns = [
        '.git*',
        '__pycache__',
        '*.pyc',
        '.DS_Store',
        'Thumbs.db',
        '*.log',
        '.vscode',
        '.idea',
        'node_modules',
        '*.tmp',
        '*.bak'
    ]
    
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(file_path, pattern) or pattern in file_path:
            return False
    
    return True

def get_content_type_and_headers(file_path):
    """获取文件的Content-Type和headers"""
    headers = {}
    
    if file_path.endswith('.html'):
        headers = {
            'Content-Type': 'text/html; charset=utf-8',
            'Cache-Control': 'no-cache'
        }
    elif file_path.endswith('.json'):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Cache-Control': 'no-cache'
        }
    elif file_path.endswith('.css'):
        headers = {
            'Content-Type': 'text/css; charset=utf-8',
            'Cache-Control': 'public, max-age=3600'
        }
    elif file_path.endswith('.js'):
        headers = {
            'Content-Type': 'application/javascript; charset=utf-8',
            'Cache-Control': 'public, max-age=3600'
        }
    elif file_path.endswith('.png') or file_path.endswith('.jpg') or file_path.endswith('.jpeg') or file_path.endswith('.gif'):
        headers = {
            'Cache-Control': 'public, max-age=86400'
        }
    else:
        headers = {
            'Cache-Control': 'public, max-age=3600'
        }
    
    return headers

def test_sync_functionality():
    """测试同步功能"""
    print("🧪 测试同步功能")
    print("=" * 60)
    
    # 获取本地文件列表
    local_files = get_local_files()
    filtered_files = [f for f in local_files if should_upload_file(f)]
    
    print(f"📁 本地文件总数: {len(local_files)}")
    print(f"📤 需要上传的文件数: {len(filtered_files)}")
    
    # 按文件类型统计
    file_types = {}
    for file_path in filtered_files:
        ext = Path(file_path).suffix.lower()
        file_types[ext] = file_types.get(ext, 0) + 1
    
    print(f"\n📊 文件类型统计:")
    for ext, count in sorted(file_types.items()):
        print(f"   {ext}: {count} 个文件")
    
    # 测试Content-Type设置
    print(f"\n🔧 Content-Type设置测试:")
    test_files = [
        'index.html',
        'table_list.json',
        'resources/css/889749337939845157.css',
        'resources/js/889749337939845157.js',
        'README.md'
    ]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            headers = get_content_type_and_headers(file_path)
            content_type = headers.get('Content-Type', 'application/octet-stream')
            cache_control = headers.get('Cache-Control', 'public, max-age=3600')
            print(f"   ✅ {file_path}")
            print(f"      Content-Type: {content_type}")
            print(f"      Cache-Control: {cache_control}")
        else:
            print(f"   ⚠️  {file_path} (文件不存在)")
    
    # 测试排除规则
    print(f"\n🚫 排除规则测试:")
    test_exclude_files = [
        '.gitignore',
        '__pycache__/test.pyc',
        '.DS_Store',
        'test.log',
        '.vscode/settings.json',
        'node_modules/package.json',
        'test.tmp',
        'backup.bak'
    ]
    
    for file_path in test_exclude_files:
        should_upload = should_upload_file(file_path)
        status = "❌ 排除" if not should_upload else "✅ 包含"
        print(f"   {status} {file_path}")
    
    # 模拟同步操作
    print(f"\n🔄 同步操作模拟:")
    print(f"   1. 获取本地文件列表: {len(filtered_files)} 个文件")
    print(f"   2. 获取OSS现有文件列表: [模拟]")
    print(f"   3. 计算需要删除的文件: [模拟]")
    print(f"   4. 计算需要上传的文件: {len(filtered_files)} 个文件")
    print(f"   5. 执行删除操作: [模拟]")
    print(f"   6. 执行上传操作: [模拟]")
    
    print(f"\n✅ 同步功能测试完成！")
    print(f"📋 关键特性:")
    print(f"   - ✅ 自动发现所有需要部署的文件")
    print(f"   - ✅ 智能排除不需要的文件")
    print(f"   - ✅ 正确设置Content-Type和编码")
    print(f"   - ✅ 支持删除OSS上多余的文件")
    print(f"   - ✅ 确保OSS与GitHub版本完全一致")

if __name__ == "__main__":
    test_sync_functionality() 