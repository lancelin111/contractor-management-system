#!/bin/bash

echo "==================================="
echo "  外包人员管理系统启动脚本"
echo "==================================="

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

# 检查MySQL是否运行
if ! command -v mysql &> /dev/null; then
    echo "警告: 未找到MySQL命令，请确保MySQL已安装并运行"
fi

# 启动后端
echo ""
echo "正在启动后端服务..."
cd backend

if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo "启动Flask服务器（端口5000）..."
python app.py &
BACKEND_PID=$!
cd ..

# 等待后端启动
sleep 3

# 启动前端
echo ""
echo "正在启动前端服务..."
cd frontend
python3 -m http.server 8080 &
FRONTEND_PID=$!
cd ..

echo ""
echo "==================================="
echo "  系统启动成功！"
echo "==================================="
echo ""
echo "后端服务: http://localhost:5000"
echo "前端页面: http://localhost:8080"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo ""

# 等待用户中断
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
