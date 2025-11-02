"""
沙盘摄像头安装计算器 - 单页面Web应用
"""

import streamlit as st
import pandas as pd
from camera_calculator import CameraCalculator, estimate_installation_complexity, calculate_viewing_angle_from_lens
from camera_visualizer import CameraVisualizer
import numpy as np


def main():
    """主应用函数"""
    st.set_page_config(
        page_title="沙盘摄像头安装计算器",
        page_icon="📹",
        layout="wide"
    )
    
    st.title("📹 沙盘摄像头安装计算器")
    st.markdown("---")
    
    # 创建计算器和可视化器实例
    calculator = CameraCalculator()
    visualizer = CameraVisualizer()
    
    # 侧边栏 - 输入参数
    with st.sidebar:
        st.header("📋 配置参数")
        
        # 沙盘参数
        st.subheader("🗺️ 沙盘规格")
        sandbox_width = st.number_input("沙盘宽度 (米)", min_value=1.0, max_value=100.0, value=10.0, step=0.5)
        sandbox_height = st.number_input("沙盘高度 (米)", min_value=1.0, max_value=100.0, value=8.0, step=0.5)
        
        # 摄像头参数
        st.subheader("📹 摄像头规格")
        
        # 参数输入方式选择
        input_method = st.radio(
            "参数输入方式",
            ["直接输入视场角", "通过镜头参数计算"]
        )
        
        if input_method == "直接输入视场角":
            horizontal_fov = st.number_input("水平视场角 (度)", min_value=10.0, max_value=180.0, value=60.0, step=1.0)
            vertical_fov = st.number_input("垂直视场角 (度)", min_value=10.0, max_value=180.0, value=45.0, step=1.0)
        else:
            st.write("**镜头参数**")
            focal_length = st.number_input("焦距 (mm)", min_value=1.0, max_value=100.0, value=8.0, step=0.1)
            sensor_width = st.number_input("传感器宽度 (mm)", min_value=1.0, max_value=50.0, value=6.4, step=0.1)
            sensor_height = st.number_input("传感器高度 (mm)", min_value=1.0, max_value=50.0, value=4.8, step=0.1)
            
            # 计算视场角
            horizontal_fov = calculate_viewing_angle_from_lens(focal_length, sensor_width)
            vertical_fov = calculate_viewing_angle_from_lens(focal_length, sensor_height)
            
            st.info(f"计算得到的视场角:\n- 水平: {horizontal_fov:.1f}°\n- 垂直: {vertical_fov:.1f}°")
        
        camera_height = st.number_input("安装高度 (米)", min_value=1.0, max_value=20.0, value=5.0, step=0.5)
        
        # 高级设置
        st.subheader("⚙️ 高级设置")
        overlap_ratio = st.slider("重叠比例", min_value=0.0, max_value=0.5, value=0.2, step=0.05)
        max_cameras = st.number_input("最大摄像头数量限制 (0=无限制)", min_value=0, max_value=100, value=0)
        
        # 计算按钮
        calculate_btn = st.button("🔄 重新计算", type="primary")
    
    # 主内容区域
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📊 计算结果")
        
        # 执行计算
        try:
            result = calculator.calculate_camera_count(
                sandbox_width, sandbox_height, camera_height,
                horizontal_fov, vertical_fov, overlap_ratio
            )
            
            # 显示关键指标
            metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
            
            with metrics_col1:
                st.metric("摄像头总数", f"{result['total_cameras']}个")
            
            with metrics_col2:
                st.metric("覆盖率", f"{result['coverage_ratio']*100:.1f}%")
            
            with metrics_col3:
                st.metric("总成本", f"¥{result['total_cost']:,}")
            
            with metrics_col4:
                coverage_area = result['coverage_per_camera']['area']
                st.metric("单摄像头覆盖", f"{coverage_area:.1f}m²")
            
            # 详细信息表格
            st.subheader("📋 详细配置信息")
            
            config_data = {
                "参数": [
                    "沙盘尺寸", "摄像头布局", "安装高度", "视场角",
                    "单摄像头覆盖", "有效覆盖", "摄像头间距", "重叠比例"
                ],
                "数值": [
                    f"{sandbox_width} × {sandbox_height} 米",
                    f"{result['cameras_x']} × {result['cameras_y']} 阵列",
                    f"{camera_height} 米",
                    f"{horizontal_fov:.1f}° × {vertical_fov:.1f}°",
                    f"{result['coverage_per_camera']['width']:.1f} × {result['coverage_per_camera']['height']:.1f} 米",
                    f"{result['effective_coverage']['width']:.1f} × {result['effective_coverage']['height']:.1f} 米",
                    f"{result['spacing_x']:.1f} × {result['spacing_y']:.1f} 米",
                    f"{overlap_ratio*100:.0f}%"
                ]
            }
            
            config_df = pd.DataFrame(config_data)
            st.table(config_df)
            
            # 摄像头位置信息
            st.subheader("📍 摄像头位置坐标")
            
            position_data = {
                "摄像头编号": [f"摄像头{i+1}" for i in range(len(result['camera_positions']))],
                "X坐标 (米)": [f"{pos['x']:.1f}" for pos in result['camera_positions']],
                "Y坐标 (米)": [f"{pos['y']:.1f}" for pos in result['camera_positions']],
                "Z坐标 (米)": [f"{pos['z']:.1f}" for pos in result['camera_positions']]
            }
            
            position_df = pd.DataFrame(position_data)
            st.dataframe(position_df, use_container_width=True)
            
        except Exception as e:
            st.error(f"计算出错: {str(e)}")
            return
    
    with col2:
        st.header("⚠️ 安装复杂度评估")
        
        # 安装复杂度分析
        complexity = estimate_installation_complexity(
            result['total_cameras'], 
            sandbox_width * sandbox_height
        )
        
        # 复杂度指标
        st.metric("复杂度等级", complexity['complexity_level'])
        st.metric("预计安装时间", f"{complexity['installation_time']:.1f}小时")
        st.metric("人工成本估算", f"¥{complexity['labor_cost']:,.0f}")
        
        # 安装建议
        st.subheader("💡 安装建议")
        for recommendation in complexity['recommendations']:
            st.write(f"• {recommendation}")
    
    # 可视化部分
    st.header("📈 可视化图表")
    
    # 可视化选项
    viz_col1, viz_col2, viz_col3 = st.columns(3)
    
    with viz_col1:
        show_layout = st.checkbox("显示布局图", value=True)
    
    with viz_col2:
        show_3d = st.checkbox("显示3D视图", value=False)
    
    with viz_col3:
        show_heatmap = st.checkbox("显示覆盖热力图", value=False)
    
    # 生成和显示图表
    if show_layout:
        st.subheader("🗺️ 摄像头布局图")
        try:
            layout_img = visualizer.create_layout_plot(result)
            st.image(f"data:image/png;base64,{layout_img}", caption="摄像头布局图")
        except Exception as e:
            st.error(f"生成布局图失败: {str(e)}")
    
    if show_3d:
        st.subheader("🎯 3D布局视图")
        try:
            viz_3d_img = visualizer.create_3d_visualization(result)
            st.image(f"data:image/png;base64,{viz_3d_img}", caption="3D布局视图")
        except Exception as e:
            st.error(f"生成3D视图失败: {str(e)}")
    
    if show_heatmap:
        st.subheader("🔥 覆盖热力图")
        try:
            heatmap_img = visualizer.create_coverage_heatmap(result)
            st.image(f"data:image/png;base64,{heatmap_img}", caption="覆盖热力图")
        except Exception as e:
            st.error(f"生成热力图失败: {str(e)}")
    
    # 优化建议部分
    st.header("🎯 优化建议")
    
    if st.button("🔍 分析最优安装高度"):
        with st.spinner("正在计算最优配置..."):
            max_cams = max_cameras if max_cameras > 0 else None
            optimal_result = calculator.calculate_optimal_height(
                sandbox_width, sandbox_height, horizontal_fov, vertical_fov, max_cams
            )
            
            st.subheader("🏆 最优配置")
            
            opt_col1, opt_col2 = st.columns(2)
            
            with opt_col1:
                st.metric("最优安装高度", f"{optimal_result['optimal_height']} 米")
                opt_config = optimal_result['configuration']
                st.metric("所需摄像头", f"{opt_config['total_cameras']} 个")
                st.metric("预计成本", f"¥{opt_config['total_cost']:,}")
            
            with opt_col2:
                if optimal_result['alternatives']:
                    st.subheader("📊 备选方案对比")
                    comparison_img = visualizer.create_comparison_chart(optimal_result['alternatives'])
                    if comparison_img:
                        st.image(f"data:image/png;base64,{comparison_img}", caption="不同高度对比分析")
    
    # 导出功能
    st.header("💾 导出报告")
    
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        if st.button("📄 生成配置报告"):
            # 生成配置报告
            report_content = generate_config_report(result, complexity)
            st.download_button(
                label="下载配置报告",
                data=report_content,
                file_name=f"摄像头配置报告_{sandbox_width}x{sandbox_height}m.txt",
                mime="text/plain"
            )
    
    with export_col2:
        if st.button("📊 导出位置数据"):
            # 导出CSV数据
            csv_data = position_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="下载位置数据CSV",
                data=csv_data,
                file_name=f"摄像头位置数据_{sandbox_width}x{sandbox_height}m.csv",
                mime="text/csv"
            )


def generate_config_report(result: dict, complexity: dict) -> str:
    """生成配置报告"""
    report = f"""
沙盘摄像头安装配置报告
========================

项目概况
--------
沙盘尺寸: {result['sandbox_dimensions']['width']} × {result['sandbox_dimensions']['height']} 米
沙盘面积: {result['sandbox_dimensions']['area']} 平方米

摄像头配置
----------
摄像头总数: {result['total_cameras']} 个
布局方式: {result['cameras_x']} × {result['cameras_y']} 阵列
安装高度: {result['coverage_per_camera']['camera_height']} 米
视场角: {result['coverage_per_camera']['horizontal_fov']}° × {result['coverage_per_camera']['vertical_fov']}°

覆盖范围
--------
单摄像头覆盖: {result['coverage_per_camera']['width']:.1f} × {result['coverage_per_camera']['height']:.1f} 米
单摄像头面积: {result['coverage_per_camera']['area']:.1f} 平方米
总覆盖率: {result['coverage_ratio']*100:.1f}%
重叠比例: {result['overlap_ratio']*100:.0f}%

成本估算
--------
设备成本: ¥{result['total_cost']:,}
人工成本: ¥{complexity['labor_cost']:,.0f}
总成本: ¥{result['total_cost'] + complexity['labor_cost']:,.0f}

安装信息
--------
复杂度等级: {complexity['complexity_level']}
预计安装时间: {complexity['installation_time']:.1f} 小时

摄像头位置坐标
--------------
"""
    
    for i, pos in enumerate(result['camera_positions']):
        report += f"摄像头{i+1}: ({pos['x']:.1f}, {pos['y']:.1f}, {pos['z']:.1f})\n"
    
    report += f"""
安装建议
--------
"""
    
    for recommendation in complexity['recommendations']:
        report += f"• {recommendation}\n"
    
    return report


if __name__ == "__main__":
    main()