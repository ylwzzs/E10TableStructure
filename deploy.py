#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import fnmatch
from pathlib import Path

# 只在需要时导入oss2
try:
    import oss2
    OSS2_AVAILABLE = True
except ImportError:
    OSS2_AVAILABLE = False

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

def get_oss_files(bucket):
    """获取OSS上现有的文件列表"""
    oss_files = []
    try:
        for obj in oss2.ObjectIterator(bucket):
            oss_files.append(obj.key)
    except Exception as e:
        print(f"⚠️  获取OSS文件列表时出错: {e}")
        return []
    return oss_files

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

def sync_to_oss():
    """同步文件到阿里云OSS，确保与GitHub版本完全一致"""
    
    if not OSS2_AVAILABLE:
        print("错误: 缺少oss2模块")
        print("请运行: pip install oss2")
        sys.exit(1)
    
    # 从环境变量获取配置
    access_key_id = os.getenv('OSS_ACCESS_KEY_ID')
    access_key_secret = os.getenv('OSS_ACCESS_KEY_SECRET')
    endpoint = os.getenv('OSS_ENDPOINT')
    bucket_name = os.getenv('OSS_BUCKET')
    
    # 验证必要的环境变量
    if not all([access_key_id, access_key_secret, endpoint, bucket_name]):
        print("错误: 缺少必要的环境变量")
        print("请设置以下环境变量:")
        print("- OSS_ACCESS_KEY_ID")
        print("- OSS_ACCESS_KEY_SECRET")
        print("- OSS_ENDPOINT")
        print("- OSS_BUCKET")
        sys.exit(1)
    
    try:
        # 创建OSS客户端
        auth = oss2.Auth(access_key_id, access_key_secret)
        bucket = oss2.Bucket(auth, endpoint, bucket_name)
        
        print("🔄 开始同步文件到OSS...")
        
        # 获取本地文件列表
        local_files = get_local_files()
        local_files = [f for f in local_files if should_upload_file(f)]
        
        print(f"📁 本地文件数量: {len(local_files)}")
        
        # 获取OSS现有文件列表
        oss_files = get_oss_files(bucket)
        print(f"☁️  OSS现有文件数量: {len(oss_files)}")
        
        # 找出需要删除的文件（在OSS上但不在本地）
        files_to_delete = [f for f in oss_files if f not in local_files]
        
        # 找出需要上传的文件（在本地但不在OSS上，或需要更新）
        files_to_upload = []
        for file_path in local_files:
            if file_path not in oss_files:
                files_to_upload.append(file_path)
            else:
                # 检查文件是否需要更新（这里简化处理，实际可以比较修改时间或MD5）
                files_to_upload.append(file_path)
        
        # 执行删除操作
        if files_to_delete:
            print(f"\n🗑️  删除 {len(files_to_delete)} 个文件:")
            for file_path in files_to_delete:
                try:
                    bucket.delete_object(file_path)
                    print(f"   ✅ 删除: {file_path}")
                except Exception as e:
                    print(f"   ❌ 删除失败 {file_path}: {e}")
        else:
            print("\n✅ 没有需要删除的文件")
        
        # 执行上传操作
        if files_to_upload:
            print(f"\n📤 上传 {len(files_to_upload)} 个文件:")
            for file_path in files_to_upload:
                try:
                    if os.path.exists(file_path):
                        # 获取文件headers
                        headers = get_content_type_and_headers(file_path)
                        
                        # 上传文件
                        bucket.put_object_from_file(file_path, file_path, headers=headers)
                        print(f"   ✅ 上传: {file_path}")
                    else:
                        print(f"   ⚠️  文件不存在: {file_path}")
                except Exception as e:
                    print(f"   ❌ 上传失败 {file_path}: {e}")
        else:
            print("\n✅ 没有需要上传的文件")
        
        print(f"\n🎉 同步完成！")
        print(f"📊 统计信息:")
        print(f"   - 删除文件: {len(files_to_delete)}")
        print(f"   - 上传文件: {len(files_to_upload)}")
        print(f"   - 最终文件总数: {len(local_files)}")
        
        # 显示访问URL
        if endpoint and endpoint.startswith('https://'):
            domain = endpoint.replace('https://', '')
        elif endpoint:
            domain = endpoint
        else:
            domain = 'oss-cn-hangzhou.aliyuncs.com'  # 默认域名
            
        print(f'\n🌐 访问地址: https://{bucket_name}.{domain}')
        
    except Exception as e:
        print(f'❌ 同步失败: {e}')
        sys.exit(1)

def create_github_action():
    """创建GitHub Action工作流文件"""
    
    workflow_content = '''name: Deploy to Aliyun OSS

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Deploy to Aliyun OSS
        env:
          OSS_ACCESS_KEY_ID: ${{ secrets.OSS_ACCESS_KEY_ID }}
          OSS_ACCESS_KEY_SECRET: ${{ secrets.OSS_ACCESS_KEY_SECRET }}
          OSS_ENDPOINT: ${{ secrets.OSS_ENDPOINT }}
          OSS_BUCKET: ${{ secrets.OSS_BUCKET }}
        run: |
          python deploy.py
'''
    
    # 确保目录存在
    os.makedirs('.github/workflows', exist_ok=True)
    
    # 写入工作流文件
    with open('.github/workflows/deploy-aliyun.yml', 'w', encoding='utf-8') as f:
        f.write(workflow_content)
    
    print('✅ GitHub Action工作流文件已创建: .github/workflows/deploy-aliyun.yml')

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--create-action':
        create_github_action()
    else:
        sync_to_oss() 