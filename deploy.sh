#!/bin/bash

# 沙盘摄像头计算器 - Docker快速部署脚本
# Quick deployment script for Camera Calculator

set -e

echo "🚀 沙盘摄像头计算器 - Docker快速部署"
echo "=================================="

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    echo "   macOS: brew install --cask docker"
    echo "   Linux: curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

echo "✅ Docker环境检查通过"

# 检查端口占用
if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  端口8501已被占用，请停止占用该端口的进程或修改配置"
    echo "   查看占用进程: lsof -i :8501"
    read -p "是否继续部署？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 创建输出目录
echo "📁 创建输出目录..."
mkdir -p output
chmod 755 output

# 选择部署模式
echo ""
echo "请选择部署模式："
echo "1) 生产模式 (端口8501)"
echo "2) 开发模式 (端口8502，支持热重载)"
echo "3) 同时启动两个模式"
read -p "请输入选择 (1-3): " -n 1 -r mode
echo

case $mode in
    1)
        echo "🔨 启动生产模式..."
        docker-compose up -d camera-calculator
        ACCESS_URL="http://localhost:8501"
        ;;
    2)
        echo "🔨 启动开发模式..."
        docker-compose up -d camera-calculator-dev
        ACCESS_URL="http://localhost:8502"
        ;;
    3)
        echo "🔨 启动所有服务..."
        docker-compose up -d
        ACCESS_URL="生产版本: http://localhost:8501, 开发版本: http://localhost:8502"
        ;;
    *)
        echo "❌ 无效选择，退出"
        exit 1
        ;;
esac

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "📊 检查服务状态..."
docker-compose ps

# 检查健康状态
echo "🩺 检查应用健康状态..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
        echo "✅ 应用启动成功！"
        break
    elif [ $attempt -eq $max_attempts ]; then
        echo "❌ 应用启动超时，请检查日志"
        echo "   查看日志: docker-compose logs camera-calculator"
        exit 1
    else
        echo "   尝试 $attempt/$max_attempts - 等待应用启动..."
        sleep 2
        ((attempt++))
    fi
done

# 显示访问信息
echo ""
echo "🎉 部署完成！"
echo "=================================="
echo "📱 访问地址: $ACCESS_URL"
echo "📂 输出目录: $(pwd)/output"
echo ""
echo "🔧 常用命令:"
echo "   查看状态: docker-compose ps"
echo "   查看日志: docker-compose logs camera-calculator"
echo "   停止服务: docker-compose down"
echo "   重启服务: docker-compose restart"
echo ""
echo "📖 详细文档: DOCKER_DEPLOYMENT_GUIDE.md"

# 可选：自动打开浏览器
if [[ "$OSTYPE" == "darwin"* ]]; then
    read -p "是否自动打开浏览器？(y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [ "$mode" = "1" ] || [ "$mode" = "3" ]; then
            open http://localhost:8501
        fi
        if [ "$mode" = "2" ] || [ "$mode" = "3" ]; then
            open http://localhost:8502
        fi
    fi
fi

echo "🚀 享受使用沙盘摄像头计算器！"