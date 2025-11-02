# 沙盘摄像头安装计算器

一个专业的沙盘摄像头安装计算和规划工具，支持基于摄像头视场角和安装高度自动计算覆盖范围，确定最优摄像头数量和布局方案。

## 功能特性

### 🎯 核心功能
- **智能计算**: 根据摄像头视场角和安装高度自动计算覆盖范围
- **最优布局**: 自动计算所需摄像头数量和最优布局方案
- **成本估算**: 提供设备成本和安装成本的详细预算
- **复杂度评估**: 评估安装复杂度并提供专业建议

### 📊 可视化展示
- **2D布局图**: 清晰展示摄像头位置和覆盖范围
- **3D立体视图**: 立体展示安装高度和覆盖锥形
- **覆盖热力图**: 直观显示覆盖密度分布
- **对比分析图**: 不同配置方案的对比分析

### 🔧 专业工具
- **镜头参数计算**: 支持通过焦距和传感器尺寸计算视场角
- **高度优化**: 自动寻找最优安装高度
- **重叠控制**: 可调节摄像头覆盖重叠比例
- **导出功能**: 支持配置报告和位置数据导出

## 技术架构

```
├── camera_calculator.py    # 核心计算模块
├── camera_visualizer.py    # 可视化模块
├── main.py                 # Web应用主程序
├── examples/               # 示例代码
│   ├── example_basic.py    # 基础示例
│   └── example_advanced.py # 高级示例
└── requirements.txt        # 依赖包列表
```

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd Calculator

# 安装依赖
pip install -r requirements.txt
```

### 2. 运行Web应用

```bash
# 启动Streamlit应用
streamlit run main.py
```

应用将在浏览器中自动打开，默认地址：http://localhost:8501

### 3. 运行示例代码

```bash
# 基础示例
python examples/example_basic.py

# 高级示例（包含可视化）
python examples/example_advanced.py
```

## 使用指南

### Web应用界面

1. **参数配置**
   - 在左侧边栏输入沙盘尺寸
   - 选择摄像头参数输入方式（直接输入视场角或通过镜头参数计算）
   - 设置安装高度和高级参数

2. **查看结果**
   - 查看关键指标：摄像头数量、覆盖率、成本等
   - 浏览详细配置信息和位置坐标
   - 查看安装复杂度评估和建议

3. **可视化分析**
   - 选择需要显示的图表类型
   - 分析摄像头布局和覆盖情况
   - 使用优化功能寻找最佳配置

4. **导出报告**
   - 生成完整的配置报告
   - 导出摄像头位置数据

### 代码API使用

```python
from camera_calculator import CameraCalculator
from camera_visualizer import CameraVisualizer

# 创建计算器实例
calculator = CameraCalculator()

# 计算摄像头布局
result = calculator.calculate_camera_count(
    sandbox_width=10.0,      # 沙盘宽度
    sandbox_height=8.0,      # 沙盘高度
    camera_height=5.0,       # 安装高度
    horizontal_fov=60.0,     # 水平视场角
    vertical_fov=45.0,       # 垂直视场角
    overlap_ratio=0.2        # 重叠比例
)

# 寻找最优配置
optimal = calculator.calculate_optimal_height(
    sandbox_width=10.0,
    sandbox_height=8.0,
    horizontal_fov=60.0,
    vertical_fov=45.0,
    max_cameras=20
)

# 生成可视化图表
visualizer = CameraVisualizer()
layout_img = visualizer.create_layout_plot(result)
```

## 计算原理

### 覆盖范围计算

基于摄像头视场角和安装高度计算地面覆盖范围：

```
覆盖宽度 = 2 × 安装高度 × tan(水平视场角/2)
覆盖高度 = 2 × 安装高度 × tan(垂直视场角/2)
```

### 摄像头数量计算

考虑重叠比例的有效覆盖面积：

```
有效覆盖宽度 = 覆盖宽度 × (1 - 重叠比例)
有效覆盖高度 = 覆盖高度 × (1 - 重叠比例)

水平摄像头数 = ceil(沙盘宽度 / 有效覆盖宽度)
垂直摄像头数 = ceil(沙盘高度 / 有效覆盖高度)
```

### 视场角计算

通过镜头焦距和传感器尺寸计算视场角：

```
视场角 = 2 × arctan(传感器尺寸 / (2 × 焦距))
```

## 配置参数说明

| 参数 | 描述 | 单位 | 典型值 |
|------|------|------|--------|
| 沙盘宽度 | 沙盘的水平宽度 | 米 | 5-50 |
| 沙盘高度 | 沙盘的垂直高度 | 米 | 3-30 |
| 安装高度 | 摄像头离地面高度 | 米 | 3-10 |
| 水平视场角 | 摄像头水平视野角度 | 度 | 30-120 |
| 垂直视场角 | 摄像头垂直视野角度 | 度 | 20-90 |
| 重叠比例 | 相邻摄像头覆盖重叠率 | % | 10-30 |

## 常见摄像头规格

| 类型 | 焦距(mm) | 水平视场角 | 垂直视场角 | 适用场景 |
|------|----------|------------|------------|----------|
| 超广角 | 2.8 | 83.0° | 65.4° | 小型沙盘，近距离全覆盖 |
| 广角 | 6.0 | 46.8° | 35.8° | 中型沙盘，平衡覆盖 |
| 标准 | 8.0 | 36.3° | 27.7° | 大型沙盘，标准安装 |
| 中焦 | 12.0 | 24.8° | 18.9° | 超大沙盘，远距离监控 |
| 长焦 | 16.0 | 18.8° | 14.4° | 特定区域，精确监控 |

## 输出文件

运行后会在以下位置生成文件：

- `output/camera_layout.png` - 摄像头布局图
- `output/camera_3d_view.png` - 3D立体视图
- `output/coverage_heatmap.png` - 覆盖热力图
- `output/height_comparison.png` - 高度对比分析图

## 依赖包

- `streamlit` - Web应用框架
- `matplotlib` - 图表绘制
- `numpy` - 数值计算
- `pandas` - 数据处理

## 应用场景

- **数字沙盘监控**: 规划沙盘监控摄像头布局
- **展览展示**: 展馆沙盘的监控系统设计
- **教学培训**: 沙盘演练的视频记录系统
- **军事应用**: 军事沙盘的监控规划
- **城市规划**: 城市模型的监控覆盖

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进项目。

## 联系方式

如有问题或建议，请通过Issue联系。