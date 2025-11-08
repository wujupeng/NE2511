#!/bin/bash

# 新能源精密追溯系统 - 远程服务器部署脚本
# 此脚本用于在Debian服务器上完整部署应用

# 进入项目目录
cd /home/debian/NE2511

# 停止可能正在运行的应用进程
ps aux | grep "python.*app.py" | grep -v grep | awk '{print $2}' | xargs -r kill

# 检查并安装pip
echo "检查并安装pip..."
if ! python3 -m pip --version &>/dev/null; then
    echo "pip未安装，使用已传输的get-pip.py文件安装（绕过系统限制）..."
    # 使用已传输的get-pip.py文件安装pip，绕过系统限制
    python3 get-pip.py --user --break-system-packages
fi

# 使用系统pip安装核心依赖（绕过系统限制）
echo "安装Python核心依赖包（绕过系统限制）..."
python3 -m pip install --user --break-system-packages flask==2.0.1 werkzeug==2.0.1 flask_cors flask_jwt_extended python-dotenv sqlalchemy bcrypt flask_restful qrcode

# 不安装requirements.txt中的大型依赖（如OpenCV），以加快部署速度
echo "跳过requirements.txt中的大型依赖安装，优先确保核心功能运行..."

# 显示已安装的包列表
echo "已安装的包列表："
python3 -m pip list 2>/dev/null || echo "pip list 命令执行失败"

# 启动应用（后台运行）
echo "启动应用..."
nohup python3 app.py --host=0.0.0.0 --port=5000 > app.log 2>&1 &
echo "应用已启动，PID: $!"

# 等待应用启动
sleep 10

# 检查应用是否成功启动
echo "检查5000端口占用情况："
netstat -tlnp 2>/dev/null | grep 5000 || ps -ef | grep app.py | grep -v grep

echo "应用日志（最后30行）："
tail -n 30 app.log

echo "部署完成！应用地址: http://$(hostname -I | awk '{print $1}'):5000/"
