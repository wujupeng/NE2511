#!/bin/bash

# Docker构建脚本 - 带自动密码输入
echo "===== NE2511项目Docker构建脚本 ====="

# 设置密码（注意：这仅用于演示目的）
PASS="debian"

# 检查当前目录
cd "$(dirname "$0")"
echo "当前工作目录: $(pwd)"

# 检查Docker是否安装
echo "检查Docker环境..."
echo "$PASS" | sudo -S docker --version
if [ $? -ne 0 ]; then
    echo "错误: Docker未安装或不可用"
    exit 1
fi

# 创建默认的.env文件（如果不存在）
if [ ! -f .env ]; then
    echo "创建默认.env文件..."
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

# 使用sudo构建Docker镜像（带密码自动输入）
echo "开始构建Docker镜像..."
echo "$PASS" | sudo -S docker build -t ne2511:latest .

if [ $? -eq 0 ]; then
    echo "✅ Docker镜像构建成功: ne2511:latest"
    echo "\n列出已构建的镜像:"
    echo "$PASS" | sudo -S docker images ne2511
    echo "\n使用以下命令运行容器:"
    echo "echo \"$PASS\" | sudo -S docker run -d -p 5000:5000 --env-file .env ne2511:latest"
    
    # 自动运行容器示例
    echo "\n正在启动容器..."
    CONTAINER_ID=$(echo "$PASS" | sudo -S docker run -d -p 5000:5000 --env-file .env ne2511:latest)
    if [ $? -eq 0 ]; then
        echo "✅ 容器已启动，ID: $CONTAINER_ID"
        echo "\n容器运行状态:"
        echo "$PASS" | sudo -S docker ps -f "id=$CONTAINER_ID"
    else
        echo "❌ 容器启动失败"
    fi
else
    echo "❌ Docker镜像构建失败"
    exit 1
fi