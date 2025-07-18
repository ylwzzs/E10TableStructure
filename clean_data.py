#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据清理脚本
功能：清理JSON文件中的重复表数据
"""

import json
import logging
from pathlib import Path
from datetime import datetime
import argparse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('clean_data.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DataCleaner:
    def __init__(self, json_file="all_tables.json"):
        self.json_file = Path(json_file)
        self.tables_data = []
        
    def load_data(self):
        """加载JSON数据"""
        if not self.json_file.exists():
            print(f"❌ JSON文件不存在: {self.json_file}")
            return False
            
        try:
            print(f"📖 加载JSON数据: {self.json_file}")
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.tables_data = json.load(f)
            
            print(f"📊 加载了 {len(self.tables_data)} 个表的数据")
            return True
            
        except Exception as e:
            print(f"❌ 加载数据失败: {e}")
            logger.error(f"加载数据失败: {e}")
            return False
    
    def analyze_duplicates(self):
        """分析重复数据"""
        if not self.tables_data:
            print("❌ 没有数据可分析")
            return
        
        print("🔍 分析重复数据...")
        
        # 统计表名出现次数
        table_name_counts = {}
        for table in self.tables_data:
            table_name = table.get('table_name', '')
            if table_name:
                table_name_counts[table_name] = table_name_counts.get(table_name, 0) + 1
        
        # 找出重复的表名
        duplicates = {name: count for name, count in table_name_counts.items() if count > 1}
        
        if duplicates:
            print(f"⚠️  发现 {len(duplicates)} 个重复的表名:")
            for table_name, count in sorted(duplicates.items()):
                print(f"   - {table_name}: {count} 次")
        else:
            print("✅ 没有发现重复的表名")
        
        return duplicates
    
    def clean_duplicates(self, strategy='latest'):
        """清理重复数据"""
        if not self.tables_data:
            print("❌ 没有数据可清理")
            return False
        
        print("🧹 开始清理重复数据...")
        original_count = len(self.tables_data)
        
        # 使用字典去重
        unique_tables = {}
        duplicates = []
        
        for table in self.tables_data:
            table_name = table.get('table_name', '')
            if not table_name:
                # 跳过没有表名的记录
                duplicates.append(table)
                continue
                
            if table_name in unique_tables:
                # 发现重复，根据策略选择保留哪个
                existing = unique_tables[table_name]
                
                if strategy == 'latest':
                    # 保留最新的
                    existing_updated = existing.get('last_updated', '')
                    current_updated = table.get('last_updated', '')
                    
                    if current_updated > existing_updated:
                        # 当前记录更新，替换旧的
                        duplicates.append(existing)
                        unique_tables[table_name] = table
                    else:
                        # 保留现有的，当前记录是重复的
                        duplicates.append(table)
                elif strategy == 'first':
                    # 保留第一个
                    duplicates.append(table)
                elif strategy == 'merge':
                    # 合并数据（保留所有非空字段）
                    merged = existing.copy()
                    for key, value in table.items():
                        if value and (key not in merged or not merged[key]):
                            merged[key] = value
                    unique_tables[table_name] = merged
                    duplicates.append(table)
            else:
                unique_tables[table_name] = table
        
        # 更新数据列表
        self.tables_data = list(unique_tables.values())
        
        cleaned_count = len(self.tables_data)
        duplicate_count = len(duplicates)
        
        print(f"✅ 清理完成:")
        print(f"   - 原始数据: {original_count} 个表")
        print(f"   - 清理后: {cleaned_count} 个表")
        print(f"   - 删除重复: {duplicate_count} 个")
        print(f"   - 减少: {original_count - cleaned_count} 个")
        
        logger.info(f"清理重复数据: 原始 {original_count} -> 清理后 {cleaned_count}, 删除 {duplicate_count} 个重复")
        
        if duplicates:
            print(f"🗑️  删除的重复表 (前10个):")
            for i, dup in enumerate(duplicates[:10]):
                print(f"   {i+1}. {dup.get('table_name', 'Unknown')} - {dup.get('file', 'Unknown file')}")
            if len(duplicates) > 10:
                print(f"   ... 还有 {len(duplicates) - 10} 个重复表")
        
        return True
    
    def save_data(self):
        """保存清理后的数据"""
        try:
            print("💾 保存清理后的数据...")
            
            # 按表名排序
            self.tables_data.sort(key=lambda x: x.get('table_name', ''))
            
            # 备份原文件
            backup_file = self.json_file.with_suffix('.json.backup')
            if self.json_file.exists():
                import shutil
                shutil.copy2(self.json_file, backup_file)
                print(f"📦 已备份原文件到: {backup_file}")
            
            # 保存新数据
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(self.tables_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 数据已保存: {len(self.tables_data)} 个表")
            logger.info(f"保存清理后的数据: {len(self.tables_data)} 个表")
            return True
            
        except Exception as e:
            print(f"❌ 保存数据失败: {e}")
            logger.error(f"保存数据失败: {e}")
            return False
    
    def validate_data(self):
        """验证数据完整性"""
        if not self.tables_data:
            print("❌ 没有数据可验证")
            return False
        
        print("🔍 验证数据完整性...")
        
        # 检查必需字段
        missing_fields = {}
        empty_table_names = 0
        
        for i, table in enumerate(self.tables_data):
            table_name = table.get('table_name', '')
            if not table_name:
                empty_table_names += 1
                continue
            
            # 检查必需字段
            required_fields = ['table_name', 'file']
            for field in required_fields:
                if field not in table or not table[field]:
                    if field not in missing_fields:
                        missing_fields[field] = []
                    missing_fields[field].append(table_name)
        
        print(f"📊 数据验证结果:")
        print(f"   - 总表数: {len(self.tables_data)}")
        print(f"   - 空表名: {empty_table_names}")
        
        if missing_fields:
            print(f"   - 缺失字段:")
            for field, tables in missing_fields.items():
                print(f"     * {field}: {len(tables)} 个表缺失")
        else:
            print(f"   - 所有必需字段完整")
        
        return len(missing_fields) == 0 and empty_table_names == 0

def main():
    parser = argparse.ArgumentParser(description='数据清理脚本')
    parser.add_argument('--json-file', default='all_tables.json', help='JSON文件路径')
    parser.add_argument('--analyze', action='store_true', help='只分析重复数据，不清理')
    parser.add_argument('--clean', action='store_true', help='清理重复数据')
    parser.add_argument('--strategy', choices=['latest', 'first', 'merge'], default='latest', 
                       help='清理策略: latest(保留最新), first(保留第一个), merge(合并数据)')
    parser.add_argument('--validate', action='store_true', help='验证数据完整性')
    parser.add_argument('--backup', action='store_true', help='创建备份')
    
    args = parser.parse_args()
    
    cleaner = DataCleaner(args.json_file)
    
    # 加载数据
    if not cleaner.load_data():
        exit(1)
    
    # 分析重复数据
    duplicates = cleaner.analyze_duplicates()
    
    # 验证数据
    if args.validate:
        cleaner.validate_data()
    
    # 清理数据
    if args.clean or (not args.analyze and duplicates):
        if duplicates:
            print(f"\n🔄 发现重复数据，开始清理...")
            if cleaner.clean_duplicates(args.strategy):
                cleaner.save_data()
                print("🎉 数据清理完成！")
            else:
                print("❌ 数据清理失败")
                exit(1)
        else:
            print("✅ 没有重复数据需要清理")
    
    # 最终验证
    if args.clean or (not args.analyze and duplicates):
        print("\n🔍 最终验证...")
        cleaner.validate_data()

if __name__ == "__main__":
    main() 