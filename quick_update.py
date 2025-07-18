#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速更新脚本
功能：手动触发表结构更新，支持多种触发方式
"""

import os
import sys
import json
import subprocess
import logging
from pathlib import Path
from datetime import datetime
import argparse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('quick_update.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class QuickUpdater:
    def __init__(self, update_script="update_tables.py"):
        self.update_script = Path(update_script)
        self.project_dir = Path.cwd()
        
    def run_update(self, force=False, push_git=True, commit_message=None):
        """执行更新"""
        logger.info("开始快速更新...")
        print("🔄 开始快速更新...")
        
        try:
            # 构建命令参数
            cmd = ['python3', str(self.update_script)]
            
            if force:
                cmd.append('--force')
                logger.info("强制更新模式")
                print("⚡ 强制更新模式")
            
            if not push_git:
                cmd.append('--no-git')
                logger.info("跳过Git推送")
                print("🚫 跳过Git推送")
            
            if commit_message:
                cmd.extend(['--commit-message', commit_message])
                logger.info(f"自定义提交信息: {commit_message}")
                print(f"📝 自定义提交信息: {commit_message}")
            
            # 执行更新
            logger.info(f"执行命令: {' '.join(cmd)}")
            print("🚀 执行更新脚本...")
            
            # 使用实时输出，这样可以看到进度条
            result = subprocess.run(cmd, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                logger.info("✅ 更新成功完成")
                print("✅ 表结构更新成功完成！")
                return True
            else:
                logger.error(f"❌ 更新失败: {result.stderr}")
                print(f"❌ 更新失败: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 执行更新时出错: {e}")
            print(f"❌ 执行更新时出错: {e}")
            return False
    
    def check_status(self):
        """检查当前状态"""
        logger.info("检查项目状态...")
        
        # 检查HTML文件数量
        html_files = list(self.project_dir.glob("*.html"))
        print(f"📁 HTML文件数量: {len(html_files)}")
        
        # 检查JSON文件
        json_file = self.project_dir / "all_tables.json"
        if json_file.exists():
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"📊 JSON中的表数量: {len(data)}")
            except Exception as e:
                print(f"❌ 读取JSON文件失败: {e}")
        else:
            print("⚠️  JSON文件不存在")
        
        # 检查Git状态
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, encoding='utf-8')
            if result.stdout.strip():
                print("🔄 Git有未提交的更改")
                print(result.stdout)
            else:
                print("✅ Git工作区干净")
        except Exception as e:
            print(f"⚠️  检查Git状态失败: {e}")
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
🔄 快速表结构更新工具

使用方法:
  python3 quick_update.py [选项]

选项:
  --update, -u          执行更新
  --force, -f           强制更新所有文件
  --no-git, -n          不推送到Git
  --status, -s          检查当前状态
  --commit-msg MSG      自定义Git提交信息
  --help, -h            显示此帮助信息

示例:
  python3 quick_update.py --update                    # 正常更新
  python3 quick_update.py --update --force           # 强制更新
  python3 quick_update.py --update --no-git          # 只更新JSON，不推送Git
  python3 quick_update.py --status                   # 检查状态
  python3 quick_update.py --update --commit-msg "更新用户表"  # 自定义提交信息

快捷键:
  python3 quick_update.py -u                         # 快速更新
  python3 quick_update.py -u -f                      # 强制更新
  python3 quick_update.py -s                         # 查看状态
        """
        print(help_text)

def main():
    parser = argparse.ArgumentParser(description='快速表结构更新工具')
    parser.add_argument('--update', '-u', action='store_true', help='执行更新')
    parser.add_argument('--force', '-f', action='store_true', help='强制更新所有文件')
    parser.add_argument('--no-git', '-n', action='store_true', help='不推送到Git')
    parser.add_argument('--status', '-s', action='store_true', help='检查当前状态')
    parser.add_argument('--commit-msg', help='自定义Git提交信息')
    
    args = parser.parse_args()
    
    updater = QuickUpdater()
    
    # 如果没有参数，显示帮助
    if len(sys.argv) == 1:
        updater.show_help()
        return
    
    # 检查状态
    if args.status:
        updater.check_status()
        return
    
    # 显示帮助（通过argparse自动处理）
    
    # 执行更新
    if args.update:
        commit_message = args.commit_msg or f"快速更新表结构 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        success = updater.run_update(
            force=args.force,
            push_git=not args.no_git,
            commit_message=commit_message
        )
        
        if success:
            print("\n🎉 更新完成！您可以:")
            print("  1. 查看更新后的JSON文件")
            print("  2. 检查Git提交历史")
            print("  3. 访问网页查看效果")
        else:
            print("\n❌ 更新失败，请检查日志文件")
    else:
        updater.show_help()

if __name__ == "__main__":
    main() 