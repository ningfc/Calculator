# 中文字体显示问题解决方案

## 问题描述
在部署版本中，matplotlib生成的图表可能出现中文乱码（显示为方框），这是因为系统缺少合适的中文字体。

## 解决方案

### 🎯 自动检测和配置
项目已集成智能字体检测系统，会自动：
1. 检测当前操作系统类型
2. 查找可用的中文字体
3. 自动配置最佳字体选择
4. 如无中文字体则使用英文标签

### 📱 不同系统的字体支持

#### Windows 系统
自动检测字体（按优先级）：
- Microsoft YaHei UI
- Microsoft YaHei  
- SimHei
- SimSun
- KaiTi

#### macOS 系统
自动检测字体（按优先级）：
- Arial Unicode MS ✅
- PingFang SC
- Heiti SC
- Hiragino Sans GB

#### Linux 系统
自动检测字体（按优先级）：
- Noto Sans CJK SC
- Source Han Sans CN
- WenQuanYi Micro Hei
- WenQuanYi Zen Hei

### 🔧 手动安装中文字体

#### Ubuntu/Debian 系统
```bash
sudo apt-get update
sudo apt-get install fonts-noto-cjk fonts-wqy-zenhei fonts-wqy-microhei
sudo fc-cache -fv
```

#### CentOS/RHEL 系统
```bash
sudo yum install google-noto-cjk-fonts wqy-microhei-fonts
sudo fc-cache -fv
```

#### macOS 系统
通常已预装Arial Unicode MS，如需更多字体：
```bash
brew install font-noto-sans-cjk
```

#### Windows 系统
通常已预装微软雅黑等字体，如有问题可安装：
- 从Microsoft Store安装"中文语言包"
- 手动下载安装Noto Sans CJK字体

### 🐳 Docker 部署
项目提供的Dockerfile已包含中文字体：
```bash
# 构建镜像
docker build -t camera-calculator .

# 运行容器
docker run -p 8501:8501 camera-calculator

# 或使用docker-compose
docker-compose up
```

### 🧪 字体测试
运行字体测试脚本：
```bash
python test_font_fix.py
```

查看输出确认：
- ✅ 找到合适的中文字体：正常显示中文
- ⚠️ 未找到中文字体：使用英文标签

### 📋 发布前检查
运行完整检查：
```bash
./pre_release_check.sh
```

### 🔍 故障排除

#### 问题1：仍显示方框
**解决**：
1. 确认系统已安装中文字体
2. 重启Python应用
3. 清除matplotlib缓存：`rm -rf ~/.matplotlib`

#### 问题2：Docker中字体不正常
**解决**：
1. 使用项目提供的Dockerfile
2. 确保包含了字体安装步骤
3. 重新构建镜像

#### 问题3：性能问题
**解决**：
- 字体检测只在初始化时进行一次
- 生产环境建议固定字体配置
- 可通过环境变量预设字体

### 📚 相关文件
- `camera_visualizer.py`: 主要可视化模块
- `production_font_config.py`: 生产环境字体配置
- `test_font_fix.py`: 字体测试脚本
- `Dockerfile`: 包含字体的容器配置

### ✅ 测试确认
项目在以下环境测试通过：
- ✅ macOS (Arial Unicode MS)
- ✅ Ubuntu 20.04/22.04 (Docker)
- ✅ Windows 10/11 (Microsoft YaHei)
- ✅ CentOS 7/8 (Docker)

如有其他问题，请查看生成的测试图片或联系技术支持。