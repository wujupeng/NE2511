# NE2511 新能源精密追溯系统

## 项目概述
NE2511是一个基于Flask的新能源精密追溯系统，旨在实现产品全生命周期管理、区块链存储、二维码追溯等核心功能。系统通过SSH隧道连接远程MySQL数据库，确保数据安全传输和存储。

## 系统架构

### 技术栈
- **后端框架**：Flask
- **数据库**：MySQL（通过SSH隧道连接）
- **前端技术**：HTML/CSS/JavaScript
- **部署方式**：Docker容器化部署

### 核心功能模块
- 产品生命周期管理
- 区块链数据存储
- 二维码追溯系统
- 用户认证与权限管理
- 数据可视化与报表

## 安装与配置

### 环境要求
- Python 3.8+
- MySQL 5.7+
- Docker（可选，用于容器化部署）
- SSH客户端（用于数据库连接）

### 本地开发环境设置

1. **克隆项目仓库**
```bash
git clone https://github.com/wujupeng/NE2511.git
cd NE2511
```

2. **创建虚拟环境**
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**

创建并编辑 `.env` 文件：
```env
# 数据库连接配置（通过SSH隧道）
DB_HOST=localhost
DB_PORT=33060
DB_USER=kiss
DB_PASSWORD=kiss
DB_NAME=kiss

# 应用配置
SECRET_KEY=your_secret_key_here
DEBUG=True
```

5. **设置SSH隧道**

在使用应用前，需要建立SSH隧道连接到远程MySQL服务器：
```bash
ssh -L 33060:localhost:3306 debian@192.168.1.12
```

6. **初始化数据库**（如需）
```bash
python init_admin.py
```

7. **启动应用**
```bash
python app.py
```

应用将在 http://localhost:5000 启动。

## Docker部署

### 构建Docker镜像
```bash
./build_docker.sh
```

### 运行Docker容器
```bash
docker run -d -p 5000:5000 --env-file .env ne2511-app
```

## 项目结构

```
NE2511/
├── app.py              # 应用入口文件
├── requirements.txt    # Python依赖列表
├── Dockerfile          # Docker构建文件
├── build_docker.sh     # Docker构建脚本
├── deploy_remote.sh    # 远程部署脚本
├── install_and_run.sh  # 安装运行脚本
└── src/                # 源代码目录
    ├── api/            # API接口定义
    ├── app.py          # 应用核心配置
    ├── config/         # 配置文件
    ├── models/         # 数据库模型
    ├── services/       # 业务逻辑层
    ├── static/         # 静态资源
    ├── templates/      # HTML模板
    └── utils/          # 工具函数
```

## 关键功能文件说明

- **app.py**: 应用程序主入口，设置路由和中间件
- **src/models/**: 定义数据库表结构和关系
- **src/api/**: RESTful API接口定义
- **src/services/**: 核心业务逻辑实现
- **check_database_tables.py**: 数据库表检查工具
- **create_kiss_user.py**: 创建kiss用户的工具脚本
- **health_check.py**: 系统健康检查脚本

## 安全注意事项

1. 生产环境中请修改默认的数据库密码和SECRET_KEY
2. 确保SSH隧道配置安全，定期更新密钥
3. 部署时关闭DEBUG模式
4. 定期备份数据库

## 故障排除

1. **数据库连接问题**：确保SSH隧道正常运行，检查.env文件中的配置是否正确
2. **权限错误**：运行 `create_kiss_user.py` 确保用户权限正确
3. **表结构问题**：使用 `fix_database.py` 修复数据库表结构

## 许可证

© 2024 NE2511新能源精密追溯系统

## 联系信息

如有问题，请联系项目维护者。