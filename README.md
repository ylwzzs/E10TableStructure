# E10表结构管理系统

一个高效的表结构HTML文件管理和浏览系统，支持多维筛选、搜索和快速更新。

## 🚀 功能特性

- **多维筛选**: 支持按模块、数据库、表名、中文名词、描述等多维度筛选
- **级联筛选**: 筛选条件相互影响，实现精确筛选
- **实时搜索**: 支持模糊搜索和智能建议
- **快速更新**: 支持增量更新和批量处理
- **数据清理**: 自动检测和清理重复数据
- **整洁结构**: 清晰的目录组织，便于维护和部署

## 📁 项目结构

```
E10TableStructure/
├── index.html                    # 主索引页面（多维筛选界面）
├── all_tables.json              # 表结构数据文件
├── all_tables.json.backup       # 数据备份文件
├── css/                         # 样式文件目录
├── resources/                   # 表结构HTML文件目录
│   └── *.html                  # 10,122个表结构文件
├── update_tables.py             # 主要更新脚本
├── quick_update.py              # 快速更新脚本
├── clean_data.py                # 数据清理脚本
├── parse_html_tables.py         # HTML解析脚本
├── requirements.txt             # Python依赖
└── README.md                    # 项目说明
```

## 🛠️ 核心脚本

### 1. 主要更新脚本 (`update_tables.py`)
- 解析HTML文件，提取表结构信息
- 生成JSON数据文件
- 支持增量更新和强制更新
- 自动Git提交和推送

### 2. 快速更新脚本 (`quick_update.py`)
- 简化更新流程
- 支持多种更新模式
- 提供状态检查功能

### 3. 数据清理脚本 (`clean_data.py`)
- 检测和清理重复数据
- 验证数据完整性
- 生成清理报告

## 📊 数据统计

- **表结构文件**: 10,122个HTML文件
- **数据记录**: 10,122条表结构信息
- **支持筛选维度**: 5个（模块、数据库、表名、中文名词、描述）
- **文件大小**: 约64MB（JSON数据）

## 🚀 快速开始

### 1. 环境准备
```bash
pip install -r requirements.txt
```

### 2. 启动本地服务器
```bash
python3 -m http.server 8000
```

### 3. 访问系统
打开浏览器访问: http://localhost:8000

### 4. 更新数据
```bash
# 快速更新
python3 quick_update.py --update

# 强制更新所有文件
python3 quick_update.py --update --force

# 检查状态
python3 quick_update.py --status
```

## 🎯 使用指南

### 多维筛选
1. 选择模块/微服务，数据库下拉框会自动筛选
2. 选择数据库，表名搜索框会提供相关建议
3. 输入中文名词或表名进行模糊搜索
4. 所有筛选条件都会相互影响

### 数据更新
1. 将新的HTML文件放入 `resources/` 目录
2. 运行更新脚本：`python3 quick_update.py --update`
3. 系统会自动解析新文件并更新JSON数据

### 数据清理
```bash
python3 clean_data.py
```

## 📋 维护说明

### 新增文件
- 将表结构HTML文件放入 `resources/` 目录
- 运行更新脚本自动处理

### 备份策略
- 自动创建 `all_tables.json.backup` 备份
- 建议定期备份整个项目

### 部署建议
- 可部署到GitHub Pages、OSS等静态文件服务器
- 支持CDN加速
- 建议定期更新数据

## 🔧 技术栈

- **前端**: HTML5, CSS3, JavaScript, Bootstrap 5
- **后端**: Python 3
- **数据格式**: JSON
- **版本控制**: Git

## 📝 更新日志

### v2.0.0 (2024-07-18)
- ✅ 重新组织目录结构
- ✅ 清理多余文件和重复脚本
- ✅ 优化多维筛选功能
- ✅ 完善文档说明

### v1.0.0
- ✅ 基础表结构管理功能
- ✅ 多维筛选和搜索
- ✅ 自动更新和清理

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。

## 📞 联系方式

如有问题或建议，请提交 Issue 或 Pull Request。 