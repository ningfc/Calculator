#!/bin/bash

# 沙盘摄像头安装计算器启动脚本

echo "正在启动沙盘摄像头安装计算器..."
echo "请稍等，应用正在初始化..."

# 设置环境变量跳过Streamlit的email配置
export STREAMLIT_EMAIL=""
export STREAMLIT_THEME_BASE="light"
export STREAMLIT_DISABLE_USAGE_STATS=true

# 启动应用
/opt/miniconda3/bin/conda run -p /opt/miniconda3 --no-capture-output streamlit run main.py --server.port 8501 --browser.gatherUsageStats false

echo "应用已启动，请在浏览器中访问 http://localhost:8501"