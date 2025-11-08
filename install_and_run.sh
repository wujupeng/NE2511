#!/bin/bash

# NE2511项目安装和运行脚本
echo "===== NE2511项目安装和运行脚本 ====="

# 检查当前目录
cd "$(dirname "$0")"
echo "当前工作目录: $(pwd)"

# 创建虚拟环境
echo "创建Python虚拟环境..."
python3 -m venv venv

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo "升级pip..."
pip install --upgrade pip

# 安装依赖
echo "安装项目依赖..."
pip install -r requirements.txt

# 创建.env文件（如果不存在）
if [ ! -f .env ]; then
    echo "创建.env文件..."
    cat > .env << EOF
# 数据库配置
DB_HOST=192.168.1.12
DB_USER=kis
DB_PASSWORD=Kis9090
DB_NAME=kis

# 应用配置
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
PORT=5000
DEBUG=False
EOF
    echo ".env文件已创建"
fi

# 运行应用
echo "启动应用服务器..."
echo "应用将在 http://localhost:5000 运行"
PORT=5000 python -m src.app