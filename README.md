# 外包人员管理系统

一个功能完整的外包人员管理系统，支持人员信息查询、展示和管理。

## 功能特性

- 🔍 **智能搜索**：支持按关键字、部门、状态等多维度搜索
- 👤 **人员管理**：完整的人员信息管理，包括基本信息、工作经历、项目经历等
- 📊 **数据可视化**：直观展示人员信息和统计数据
- 📱 **响应式设计**：支持PC端和移动端访问
- 🎨 **现代化UI**：清新简洁的用户界面

## 系统架构

### 技术栈

**后端：**
- Python 3.x
- Flask 3.0.0 - Web框架
- PyMySQL 1.1.0 - MySQL数据库驱动
- Flask-CORS 4.0.0 - 跨域支持

**前端：**
- HTML5
- CSS3
- Vanilla JavaScript (原生JS)

**数据库：**
- MySQL 8.0+

## 数据库设计

系统包含7个核心数据表：

1. **contractors** - 外包人员基本信息表
2. **work_experience** - 工作经历表
3. **project_experience** - 项目经历表
4. **skills** - 技能标签表
5. **training_records** - 培训记录表
6. **performance_reviews** - 绩效评估表
7. **contracts** - 合同信息表

详细的数据库结构请参考：`database/schema.sql`

## 快速开始

### 环境要求

- Python 3.8+
- MySQL 8.0+
- 现代浏览器（Chrome、Firefox、Safari等）

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/lancelin111/contractor-management-system.git
cd contractor-management-system
```

#### 2. 配置数据库

确保MySQL服务正在运行，然后创建数据库并导入数据：

```bash
# 创建数据库表结构
mysql -u root -p test < database/schema.sql

# 导入示例数据
mysql -u root -p test < database/sample_data.sql
```

#### 3. 配置后端

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置数据库密码
# 方式1：设置环境变量
export DB_PASSWORD="your_password"

# 方式2：或直接修改 app.py 中的 DB_CONFIG
```

#### 4. 启动后端服务

```bash
# 在 backend 目录下
source venv/bin/activate
python app.py
```

后端服务将在 `http://localhost:5000` 启动

#### 5. 启动前端服务

打开新的终端窗口：

```bash
cd frontend
python3 -m http.server 8080
```

前端服务将在 `http://localhost:8080` 启动

#### 6. 访问系统

打开浏览器访问：`http://localhost:8080`

## API 接口文档

### 1. 获取人员列表

```
GET /api/contractors
```

**查询参数：**
- `keyword` - 搜索关键字（可选）
- `department` - 部门筛选（可选）
- `status` - 状态筛选（可选）
- `page` - 页码，默认1
- `page_size` - 每页数量，默认10

**响应示例：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "list": [...],
    "total": 100,
    "page": 1,
    "page_size": 10
  }
}
```

### 2. 获取人员详情

```
GET /api/contractors/{id}
```

### 3. 获取部门列表

```
GET /api/departments
```

### 4. 获取统计信息

```
GET /api/stats
```

### 5. 健康检查

```
GET /api/health
```

## 项目结构

```
contractor-management-system/
├── backend/                 # 后端代码
│   ├── app.py              # Flask应用主文件
│   ├── config.py           # 配置文件
│   ├── requirements.txt    # Python依赖
│   ├── .env.example        # 环境变量示例
│   └── venv/               # 虚拟环境
├── frontend/               # 前端代码
│   ├── index.html          # 主页面
│   ├── style.css           # 样式文件
│   └── app.js              # JavaScript逻辑
├── database/               # 数据库文件
│   ├── schema.sql          # 数据库结构
│   └── sample_data.sql     # 示例数据
└── README.md               # 项目文档
```

## 功能截图

系统主要包含以下页面和功能：

1. **人员列表页**：展示所有外包人员的卡片列表，支持搜索和筛选
2. **人员详情页**：展示人员的完整信息

## 部署建议

### 生产环境部署

1. **后端部署**：
   - 使用 Gunicorn 或 uWSGI 作为WSGI服务器
   - 配置 Nginx 作为反向代理
   - 使用环境变量管理敏感信息

2. **前端部署**：
   - 可以部署到任何静态文件服务器
   - 建议使用CDN加速静态资源

### 安全建议

- 修改默认数据库密码
- 启用HTTPS
- 添加用户认证和权限管理
- 实施API访问频率限制
- 定期更新依赖包

## 更新日志

### v1.0.0 (2025-10-31)

- 初始版本发布
- 实现基本的人员管理功能
- 支持搜索和筛选
- 完整的人员信息展示
- 响应式设计

## 许可证

本项目采用 MIT 许可证。

---

⭐ 如果这个项目对你有帮助，请给个Star支持一下！
