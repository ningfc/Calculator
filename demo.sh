#!/bin/bash

# 沙盘摄像头安装计算器 - 完整功能演示

echo "🎬 沙盘摄像头安装计算器 - 功能演示"
echo "================================================"

echo ""
echo "📊 1. 基础功能演示"
echo "----------------------------------------"
/opt/miniconda3/bin/conda run -p /opt/miniconda3 --no-capture-output python examples/example_basic.py

echo ""
echo "💰 2. 成本分析演示"
echo "----------------------------------------"
/opt/miniconda3/bin/conda run -p /opt/miniconda3 --no-capture-output python examples/cost_analysis_demo.py

echo ""
echo "🌐 3. 启动Web应用"
echo "----------------------------------------"
echo "正在启动Web应用..."
echo "请在浏览器中访问: http://localhost:8504"
echo "按 Ctrl+C 停止应用"
echo ""

# 启动Web应用
/opt/miniconda3/bin/conda run -p /opt/miniconda3 --no-capture-output streamlit run main.py --server.port 8504