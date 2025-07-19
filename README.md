# 📊 数据库表结构查询系统

这是一个现代化的数据库表结构查询系统，用于快速查找和浏览系统的数据库表结构文档。

## 🌟 功能特性

- **📈 全面搜索**: 支持按表名、中文名称搜索
- **🔍 智能分类**: 自动分类AI、用户、流程、人事、CRM、系统相关表
- **⚡ 快速响应**: 前端搜索，无需后端服务
- **📱 响应式设计**: 支持桌面和移动设备
- **🎨 现代UI**: 美观的用户界面和流畅的交互

## 📁 文件结构

```
E10TableStructure/
├── index.html              # 主页面
├── table_list.json         # 表结构数据索引
├── server.py               # 自定义HTTP服务器（解决编码问题）
├── deploy.py               # 阿里云OSS同步部署脚本
├── requirements.txt        # Python依赖
├── test_deploy.py          # 部署测试脚本
├── test_sync.py            # 同步功能测试脚本
├── resources/              # 表结构文档目录
│   ├── *.html              # 各个表的详细结构文档
│   ├── css/                # 样式文件
│   └── js/                 # 脚本文件
└── .github/workflows/      # GitHub Actions部署配置
    └── deploy-aliyun.yml   # 阿里云OSS自动部署配置
```

## 🚀 使用方法

### 在线访问
- **阿里云OSS部署**: 通过GitHub Actions自动部署到阿里云OSS
- **本地测试**: 使用自定义HTTP服务器确保编码正确

### 本地运行
1. 克隆仓库到本地
2. 启动自定义HTTP服务器：
   ```bash
   python3 server.py
   ```
3. 访问 `http://localhost:8080`

### 部署到阿里云OSS
详细部署说明请参考 [DEPLOYMENT.md](DEPLOYMENT.md)

## 🔧 技术栈

- **前端**: 纯 HTML/CSS/JavaScript
- **部署**: 阿里云OSS + GitHub Actions
- **数据**: JSON 格式的表结构索引
- **编码**: UTF-8 确保中文正常显示
- **同步**: 完全同步策略，确保OSS与GitHub版本一致

## 📊 数据统计

- 总表数量: **10,350+** 个数据库表
- 涵盖模块: AI、用户管理、流程、人事、CRM、系统配置等
- 文档格式: 详细的表结构信息，包含字段类型、约束等

## 🔍 搜索功能

### 支持的搜索方式
- **表名搜索**: 直接输入表名如 `user_info`
- **中文搜索**: 输入中文描述如 `用户信息`
- **模糊搜索**: 支持部分匹配

### 分类筛选
- **AI相关**: 以 `ai_` 开头的表
- **用户相关**: 包含 user、account、employee 的表
- **流程相关**: 包含 flow、workflow、approval 的表
- **人事相关**: 以 `hr_` 开头或包含 attend 的表
- **CRM相关**: 以 `crm_` 开头的表
- **系统相关**: 包含 system、config、setting 的表

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个系统！

## 📝 许可证

本项目采用 MIT 许可证。 