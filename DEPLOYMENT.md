# 阿里云OSS部署指南

## 🎯 部署目标

确保部署到阿里云OSS后，网页能够正确显示中文字符，避免乱码问题。

## 📋 部署前准备

### 1. 阿里云OSS配置

1. **创建OSS Bucket**
   - 登录阿里云控制台
   - 创建OSS Bucket
   - 设置Bucket为公共读权限
   - 记录Bucket名称和Endpoint

2. **配置静态网站托管**
   - 在Bucket管理页面启用静态网站托管
   - 设置默认首页为 `index.html`
   - 设置默认404页面（可选）

3. **配置跨域设置（CORS）**
   ```json
   {
     "allowedOrigins": ["*"],
     "allowedMethods": ["GET", "HEAD"],
     "allowedHeaders": ["*"],
     "maxAgeSeconds": 3600
   }
   ```

### 2. GitHub Secrets配置

在GitHub仓库的Settings > Secrets and variables > Actions中添加以下secrets：

- `ALIYUN_ACCESS_KEY_ID`: 阿里云AccessKey ID
- `ALIYUN_ACCESS_KEY_SECRET`: 阿里云AccessKey Secret
- `ALIYUN_OSS_ENDPOINT`: OSS Endpoint（如：oss-cn-hangzhou.aliyuncs.com）
- `ALIYUN_OSS_BUCKET`: OSS Bucket名称

## 🚀 自动部署

### 方式一：GitHub Actions（推荐）

**注意**：项目已清理重复的部署配置，现在只使用 `deploy-aliyun.yml` 进行阿里云OSS部署。

1. **推送代码到main分支**
   ```bash
   git add .
   git commit -m "Update deployment configuration"
   git push origin main
   ```

2. **GitHub Actions会自动触发部署**
   - 查看Actions页面确认部署状态
   - 部署完成后会显示访问地址

### 清理说明

已删除以下重复的配置文件：
- ❌ `deploy.yml` - 旧的GitHub Pages部署配置
- ❌ `deploy-oss.yml` - 旧的ossutil部署配置
- ✅ `deploy-aliyun.yml` - 新的Python脚本部署配置（推荐使用）

### 方式二：手动部署

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **设置环境变量**
   ```bash
   export ALIYUN_ACCESS_KEY_ID="your_access_key_id"
   export ALIYUN_ACCESS_KEY_SECRET="your_access_key_secret"
   export ALIYUN_OSS_ENDPOINT="oss-cn-hangzhou.aliyuncs.com"
   export ALIYUN_OSS_BUCKET="your_bucket_name"
   ```

3. **执行部署**
   ```bash
   python3 deploy.py
   ```

## 🔧 编码问题解决方案

### 1. 文件编码设置

部署脚本会自动为不同文件类型设置正确的Content-Type：

- **HTML文件**: `text/html; charset=utf-8`
- **JSON文件**: `application/json; charset=utf-8`
- **CSS文件**: `text/css; charset=utf-8`
- **JS文件**: `application/javascript; charset=utf-8`

## 🔄 文件同步机制

### 1. 完全同步策略

部署脚本采用**完全同步**策略，确保OSS上的文件与GitHub版本完全一致：

1. **获取本地文件列表**：扫描所有需要部署的文件
2. **获取OSS文件列表**：获取OSS上现有的所有文件
3. **计算差异**：
   - 需要删除的文件：在OSS上但不在本地
   - 需要上传的文件：在本地但不在OSS上，或需要更新
4. **执行同步**：先删除多余文件，再上传/更新文件

### 2. 智能文件过滤

自动排除以下不需要部署的文件：
- `.git*` - Git相关文件
- `__pycache__` - Python缓存
- `*.pyc` - Python编译文件
- `.DS_Store` - macOS系统文件
- `*.log` - 日志文件
- `.vscode`, `.idea` - IDE配置
- `node_modules` - Node.js依赖
- `*.tmp`, `*.bak` - 临时文件

### 3. 缓存控制

- **HTML/JSON文件**: `Cache-Control: no-cache`（确保内容及时更新）
- **CSS/JS文件**: `Cache-Control: public, max-age=3600`（适当缓存）
- **图片文件**: `Cache-Control: public, max-age=86400`（长期缓存）

### 4. 浏览器兼容性

确保HTML文件包含正确的meta标签：
```html
<meta charset="UTF-8">
```

## 🌐 访问地址

部署完成后，可以通过以下地址访问：

- **OSS直接访问**: `https://{bucket-name}.{endpoint}`
- **自定义域名**: 如果配置了自定义域名，使用自定义域名访问

## 🧪 测试验证

### 1. 编码测试页面

访问 `https://{your-domain}/test_encoding.html` 验证：
- ✅ 中文字符正常显示
- ✅ 特殊符号（emoji）正常显示
- ✅ JSON数据正确加载

### 2. 主页面测试

访问主页面验证：
- ✅ 页面标题和描述正常显示
- ✅ 筛选功能正常工作
- ✅ 表格数据正确显示
- ✅ 中文搜索功能正常

## 🔍 故障排除

### 1. 乱码问题

如果仍然出现乱码：

1. **检查OSS文件元数据**
   ```bash
   # 使用阿里云CLI检查文件元数据
   aliyun oss head {bucket-name}/{file-name}
   ```

2. **确认Content-Type设置**
   - HTML文件应该显示：`Content-Type: text/html; charset=utf-8`
   - JSON文件应该显示：`Content-Type: application/json; charset=utf-8`

3. **清除浏览器缓存**
   - 强制刷新页面（Ctrl+F5）
   - 清除浏览器缓存

### 2. 部署失败

1. **检查GitHub Secrets**
   - 确认所有必要的secrets都已设置
   - 检查AccessKey权限是否正确

2. **检查OSS权限**
   - 确认AccessKey有OSS读写权限
   - 确认Bucket为公共读权限

3. **查看GitHub Actions日志**
   - 在Actions页面查看详细错误信息

## 📞 技术支持

如果遇到问题，请检查：
1. GitHub Actions日志
2. 浏览器开发者工具的网络请求
3. OSS文件元数据设置 