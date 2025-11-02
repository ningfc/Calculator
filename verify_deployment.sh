#!/bin/bash

# Docker部署验证脚本
# Docker deployment verification script

set -e

echo "🔍 Docker部署验证测试"
echo "===================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试结果统计
TESTS_PASSED=0
TESTS_FAILED=0

# 测试函数
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -n "测试: $test_name ... "
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ 通过${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}❌ 失败${NC}"
        ((TESTS_FAILED++))
        return 1
    fi
}

# 开始测试
echo "开始验证Docker部署..."
echo ""

# 1. 检查Docker服务
run_test "Docker服务运行状态" "docker info"

# 2. 检查Docker Compose
run_test "Docker Compose可用性" "docker-compose --version"

# 3. 检查容器运行状态
run_test "容器运行状态" "docker-compose ps | grep -q 'Up'"

# 4. 检查端口监听
run_test "端口8501监听状态" "netstat -tlnp 2>/dev/null | grep -q ':8501' || lsof -i :8501 > /dev/null 2>&1"

# 5. 检查应用健康状态
echo -n "测试: 应用健康检查 ... "
if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ 通过${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}❌ 失败${NC}"
    ((TESTS_FAILED++))
    echo "   提示: 应用可能还在启动中，请稍等片刻后重试"
fi

# 6. 检查主页面可访问性
echo -n "测试: 主页面访问 ... "
if curl -f http://localhost:8501 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ 通过${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}❌ 失败${NC}"
    ((TESTS_FAILED++))
fi

# 7. 检查输出目录
run_test "输出目录存在" "[ -d './output' ]"

# 8. 检查输出目录权限
run_test "输出目录可写" "[ -w './output' ]"

# 9. 检查容器镜像
run_test "镜像存在" "docker images | grep -q camera-calculator"

# 10. 检查容器日志（无错误）
echo -n "测试: 容器日志检查 ... "
if docker-compose logs camera-calculator 2>/dev/null | grep -q "ERROR\|FATAL\|Exception"; then
    echo -e "${RED}❌ 失败${NC}"
    echo "   发现错误日志，请检查:"
    docker-compose logs camera-calculator | grep -E "ERROR|FATAL|Exception" | tail -5
    ((TESTS_FAILED++))
else
    echo -e "${GREEN}✅ 通过${NC}"
    ((TESTS_PASSED++))
fi

# 显示测试结果
echo ""
echo "===================="
echo "📊 测试结果统计"
echo "===================="
echo -e "通过: ${GREEN}$TESTS_PASSED${NC}"
echo -e "失败: ${RED}$TESTS_FAILED${NC}"
echo -e "总计: $((TESTS_PASSED + TESTS_FAILED))"

if [ $TESTS_FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 所有测试通过！部署验证成功！${NC}"
    echo ""
    echo "📱 访问应用: http://localhost:8501"
    echo "📂 输出目录: $(pwd)/output"
    echo ""
    echo "🔧 管理命令:"
    echo "   查看状态: docker-compose ps"
    echo "   查看日志: docker-compose logs -f camera-calculator"
    echo "   停止服务: docker-compose down"
    echo "   重启服务: docker-compose restart"
    exit 0
else
    echo ""
    echo -e "${RED}❌ 部署验证失败！${NC}"
    echo ""
    echo "🔧 故障排除建议:"
    echo "1. 检查容器日志: docker-compose logs camera-calculator"
    echo "2. 检查端口占用: lsof -i :8501"
    echo "3. 重新启动服务: docker-compose down && docker-compose up -d"
    echo "4. 查看详细部署指南: DOCKER_DEPLOYMENT_GUIDE.md"
    exit 1
fi