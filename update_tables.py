#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
表结构更新脚本
功能：
1. 增量更新HTML文件
2. 转换为UTF-8编码
3. 更新JSON文件
4. 自动推送到GitHub
"""

import os
import json
import hashlib
import subprocess
import shutil
from datetime import datetime
from pathlib import Path
import chardet
from bs4 import BeautifulSoup
import argparse
import logging
from tqdm import tqdm
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('update_tables.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TableStructureUpdater:
    def __init__(self, source_dir=".", json_file="all_tables.json", backup_dir="backup"):
        self.source_dir = Path(source_dir)
        self.json_file = Path(json_file)
        self.backup_dir = Path(backup_dir)
        self.hash_file = Path("file_hashes.json")
        self.tables_data = []
        
        # 创建备份目录
        self.backup_dir.mkdir(exist_ok=True)
        
    def detect_encoding(self, file_path):
        """检测文件编码"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                return result['encoding']
        except Exception as e:
            logger.error(f"检测编码失败 {file_path}: {e}")
            return 'utf-8'
    
    def convert_to_utf8(self, file_path):
        """将文件转换为UTF-8编码"""
        try:
            encoding = self.detect_encoding(file_path)
            if encoding and encoding.lower() != 'utf-8':
                logger.info(f"转换编码 {file_path}: {encoding} -> UTF-8")
                
                # 读取原文件
                with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                    content = f.read()
                
                # 备份原文件
                backup_path = self.backup_dir / f"{file_path.name}.{encoding}"
                shutil.copy2(file_path, backup_path)
                logger.info(f"备份原文件到: {backup_path}")
                
                # 写入UTF-8文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return True
            return False
        except Exception as e:
            logger.error(f"转换编码失败 {file_path}: {e}")
            return False
    
    def parse_html_file(self, file_path):
        """解析HTML文件，提取表结构信息"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # 提取表名（从文件名或页面内容）
            table_name = file_path.stem
            if '(' in table_name and ')' in table_name:
                # 处理类似 "table_name(描述)_id.html" 的格式
                table_name = table_name.split('(')[0]
            
            # 提取中文描述
            table_comment = ""
            description = ""
            
            # 尝试从页面标题或内容中提取描述
            title_tag = soup.find('title')
            if title_tag:
                title_text = title_tag.get_text().strip()
                if '(' in title_text and ')' in title_text:
                    table_comment = title_text.split('(')[1].split(')')[0]
                    description = title_text
            
            # 尝试从页面内容中提取更多信息
            body_text = soup.get_text()
            
            # 提取模块信息（如果存在）
            module = ""
            if "模块" in body_text or "微服务" in body_text:
                # 简单的模块提取逻辑，可以根据实际HTML结构调整
                lines = body_text.split('\n')
                for line in lines:
                    if "模块" in line or "微服务" in line:
                        module = line.strip()
                        break
            
            # 提取数据库信息（如果存在）
            db_name = ""
            if "数据库" in body_text:
                lines = body_text.split('\n')
                for line in lines:
                    if "数据库" in line:
                        db_name = line.strip()
                        break
            
            return {
                "table_name": table_name,
                "table_comment": table_comment,
                "module": module,
                "db_name": db_name,
                "description": description,
                "file": file_path.name,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"解析HTML文件失败 {file_path}: {e}")
            return None
    
    def calculate_file_hash(self, file_path):
        """计算文件MD5哈希值"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            logger.error(f"计算文件哈希失败 {file_path}: {e}")
            return None
    
    def load_file_hashes(self):
        """加载文件哈希记录"""
        if self.hash_file.exists():
            try:
                with open(self.hash_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"加载哈希记录失败: {e}")
        return {}
    
    def save_file_hashes(self, hashes):
        """保存文件哈希记录"""
        try:
            with open(self.hash_file, 'w', encoding='utf-8') as f:
                json.dump(hashes, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存哈希记录失败: {e}")
    
    def get_html_files(self):
        """获取所有HTML文件"""
        return list(self.source_dir.glob("*.html"))
    
    def update_tables_data(self, force_update=False):
        """更新表结构数据"""
        html_files = self.get_html_files()
        file_hashes = self.load_file_hashes()
        updated_files = []
        converted_files = []
        skipped_files = []
        
        print(f"📁 开始处理 {len(html_files)} 个HTML文件...")
        logger.info(f"开始处理 {len(html_files)} 个HTML文件")
        
        # 检查是否支持tqdm进度条
        try:
            # 尝试使用tqdm进度条
            with tqdm(total=len(html_files), desc="处理文件", unit="个", 
                     bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]") as pbar:
                
                for i, html_file in enumerate(html_files):
                    # 更新进度条描述
                    pbar.set_description(f"处理 {html_file.name[:30]}...")
                    
                    current_hash = self.calculate_file_hash(html_file)
                    if current_hash is None:
                        pbar.update(1)
                        continue
                    
                    # 检查是否需要更新
                    needs_update = force_update or html_file.name not in file_hashes or file_hashes[html_file.name] != current_hash
                    
                    if needs_update:
                        logger.info(f"处理文件: {html_file.name}")
                        
                        # 检查编码，如果是UTF-8且不需要强制更新，则跳过
                        if not force_update:
                            encoding = self.detect_encoding(html_file)
                            if encoding and encoding.lower() == 'utf-8':
                                # 只更新哈希记录，不处理文件
                                file_hashes[html_file.name] = current_hash
                                skipped_files.append(html_file.name)
                                pbar.update(1)
                                continue
                        
                        # 转换编码
                        if self.convert_to_utf8(html_file):
                            converted_files.append(html_file.name)
                        
                        # 解析HTML
                        table_data = self.parse_html_file(html_file)
                        if table_data:
                            # 更新或添加表数据
                            self.update_table_in_data(table_data)
                            updated_files.append(html_file.name)
                        
                        # 更新哈希记录
                        file_hashes[html_file.name] = current_hash
                    else:
                        # 文件没有变化，跳过处理
                        skipped_files.append(html_file.name)
                    
                    pbar.update(1)
                    
        except Exception as e:
            # 如果tqdm失败，使用简单的进度显示
            print(f"⚠️  进度条显示失败，使用简单进度显示: {e}")
            logger.warning(f"进度条显示失败，使用简单进度显示: {e}")
            
            for i, html_file in enumerate(html_files):
                # 每处理100个文件显示一次进度
                if i % 100 == 0 or i == len(html_files) - 1:
                    progress = (i + 1) / len(html_files) * 100
                    print(f"📊 进度: {i+1}/{len(html_files)} ({progress:.1f}%) - 处理: {html_file.name[:50]}...")
                
                current_hash = self.calculate_file_hash(html_file)
                if current_hash is None:
                    continue
                
                # 检查是否需要更新
                needs_update = force_update or html_file.name not in file_hashes or file_hashes[html_file.name] != current_hash
                
                if needs_update:
                    logger.info(f"处理文件: {html_file.name}")
                    
                    # 检查编码，如果是UTF-8且不需要强制更新，则跳过
                    if not force_update:
                        encoding = self.detect_encoding(html_file)
                        if encoding and encoding.lower() == 'utf-8':
                            # 只更新哈希记录，不处理文件
                            file_hashes[html_file.name] = current_hash
                            skipped_files.append(html_file.name)
                            continue
                    
                    # 转换编码
                    if self.convert_to_utf8(html_file):
                        converted_files.append(html_file.name)
                    
                    # 解析HTML
                    table_data = self.parse_html_file(html_file)
                    if table_data:
                        # 更新或添加表数据
                        self.update_table_in_data(table_data)
                        updated_files.append(html_file.name)
                    
                    # 更新哈希记录
                    file_hashes[html_file.name] = current_hash
                else:
                    # 文件没有变化，跳过处理
                    skipped_files.append(html_file.name)
        
        # 保存哈希记录
        self.save_file_hashes(file_hashes)
        
        print(f"✅ 更新完成: {len(updated_files)} 个文件更新, {len(converted_files)} 个文件转换编码, {len(skipped_files)} 个文件跳过")
        logger.info(f"更新完成: {len(updated_files)} 个文件更新, {len(converted_files)} 个文件转换编码, {len(skipped_files)} 个文件跳过")
        return updated_files, converted_files
    
    def clean_duplicate_data(self):
        """清理重复的表数据"""
        if not self.tables_data:
            return
        
        print("🧹 清理重复数据...")
        original_count = len(self.tables_data)
        
        # 使用字典去重，以table_name为键
        unique_tables = {}
        duplicates = []
        
        for table in self.tables_data:
            table_name = table.get('table_name', '')
            if table_name in unique_tables:
                # 发现重复，保留最新的
                existing = unique_tables[table_name]
                existing_updated = existing.get('last_updated', '')
                current_updated = table.get('last_updated', '')
                
                if current_updated > existing_updated:
                    # 当前记录更新，替换旧的
                    duplicates.append(existing)
                    unique_tables[table_name] = table
                else:
                    # 保留现有的，当前记录是重复的
                    duplicates.append(table)
            else:
                unique_tables[table_name] = table
        
        # 更新数据列表
        self.tables_data = list(unique_tables.values())
        
        cleaned_count = len(self.tables_data)
        duplicate_count = len(duplicates)
        
        print(f"✅ 清理完成: 原始 {original_count} 个表 -> 清理后 {cleaned_count} 个表，删除 {duplicate_count} 个重复")
        logger.info(f"清理重复数据: 原始 {original_count} 个表 -> 清理后 {cleaned_count} 个表，删除 {duplicate_count} 个重复")
        
        if duplicates:
            logger.info(f"删除的重复表: {[d.get('table_name', '') for d in duplicates[:10]]}...")
    
    def update_table_in_data(self, new_table_data):
        """更新或添加表数据到现有数据中"""
        # 查找是否已存在该表
        existing_index = None
        for i, table in enumerate(self.tables_data):
            if table.get('table_name') == new_table_data['table_name']:
                existing_index = i
                break
        
        if existing_index is not None:
            # 更新现有记录
            self.tables_data[existing_index].update(new_table_data)
            logger.info(f"更新表: {new_table_data['table_name']}")
        else:
            # 添加新记录
            self.tables_data.append(new_table_data)
            logger.info(f"添加新表: {new_table_data['table_name']}")
    
    def load_existing_data(self):
        """加载现有的JSON数据"""
        if self.json_file.exists():
            try:
                print("📖 加载现有JSON数据...")
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    self.tables_data = json.load(f)
                print(f"📊 已加载 {len(self.tables_data)} 个表的数据")
                logger.info(f"加载现有数据: {len(self.tables_data)} 个表")
                
                # 清理重复数据
                self.clean_duplicate_data()
                
            except Exception as e:
                logger.error(f"加载现有数据失败: {e}")
                self.tables_data = []
        else:
            self.tables_data = []
    
    def save_json_data(self):
        """保存JSON数据"""
        try:
            print("💾 保存JSON数据...")
            # 按表名排序
            self.tables_data.sort(key=lambda x: x.get('table_name', ''))
            
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(self.tables_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 保存完成: {len(self.tables_data)} 个表")
            logger.info(f"保存JSON数据: {len(self.tables_data)} 个表")
            return True
        except Exception as e:
            logger.error(f"保存JSON数据失败: {e}")
            return False
    
    def git_operations(self, commit_message=None):
        """执行Git操作"""
        try:
            print("🔍 检查Git状态...")
            # 检查是否有变更
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, encoding='utf-8')
            
            if not result.stdout.strip():
                print("✅ 没有文件变更，跳过Git操作")
                logger.info("没有文件变更，跳过Git操作")
                return True
            
            print("📝 执行Git操作...")
            # 添加所有文件
            subprocess.run(['git', 'add', '.'], check=True)
            print("✅ Git add 完成")
            logger.info("Git add 完成")
            
            # 提交
            if not commit_message:
                commit_message = f"自动更新表结构 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            print(f"✅ Git commit 完成: {commit_message}")
            logger.info(f"Git commit 完成: {commit_message}")
            
            # 推送到远程仓库
            print("🚀 推送到远程仓库...")
            subprocess.run(['git', 'push'], check=True)
            print("✅ Git push 完成")
            logger.info("Git push 完成")
            
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Git操作失败: {e}")
            return False
        except Exception as e:
            logger.error(f"Git操作异常: {e}")
            return False
    
    def run_update(self, force_update=False, auto_git=True, commit_message=None):
        """运行完整的更新流程"""
        print("🔄 开始表结构更新流程...")
        logger.info("开始表结构更新流程")
        
        # 1. 加载现有数据
        self.load_existing_data()
        
        # 2. 更新表数据
        updated_files, converted_files = self.update_tables_data(force_update)
        
        if not updated_files and not converted_files:
            print("✅ 没有文件需要更新")
            logger.info("没有文件需要更新")
            return True
        
        # 3. 保存JSON数据
        if not self.save_json_data():
            return False
        
        # 4. Git操作
        if auto_git:
            if not self.git_operations(commit_message):
                return False
        
        print("🎉 表结构更新流程完成")
        logger.info("表结构更新流程完成")
        return True

def main():
    parser = argparse.ArgumentParser(description='表结构更新脚本')
    parser.add_argument('--source-dir', default='.', help='HTML文件源目录')
    parser.add_argument('--json-file', default='all_tables.json', help='输出JSON文件名')
    parser.add_argument('--backup-dir', default='backup', help='备份目录')
    parser.add_argument('--force', action='store_true', help='强制更新所有文件')
    parser.add_argument('--no-git', action='store_true', help='不执行Git操作')
    parser.add_argument('--commit-message', help='Git提交信息')
    
    args = parser.parse_args()
    
    updater = TableStructureUpdater(
        source_dir=args.source_dir,
        json_file=args.json_file,
        backup_dir=args.backup_dir
    )
    
    success = updater.run_update(
        force_update=args.force,
        auto_git=not args.no_git,
        commit_message=args.commit_message
    )
    
    if success:
        logger.info("更新成功完成")
        exit(0)
    else:
        logger.error("更新失败")
        exit(1)

if __name__ == "__main__":
    main() 