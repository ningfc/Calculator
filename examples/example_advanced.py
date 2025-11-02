"""
高级示例 - 完整的摄像头计算和可视化
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from camera_calculator import CameraCalculator, estimate_installation_complexity, calculate_viewing_angle_from_lens
from camera_visualizer import CameraVisualizer, save_plot_as_file
import matplotlib.pyplot as plt

def advanced_example():
    """高级示例"""
    print("=" * 60)
    print("沙盘摄像头安装计算器 - 高级示例")
    print("=" * 60)
    
    # 创建实例
    calculator = CameraCalculator()
    visualizer = CameraVisualizer()
    
    # 示例参数 - 大型沙盘
    sandbox_width = 20.0   # 沙盘宽度 20米
    sandbox_height = 15.0  # 沙盘高度 15米
    
    # 通过镜头参数计算视场角
    focal_length = 8.0     # 焦距 8mm
    sensor_width = 6.4     # 传感器宽度 6.4mm
    sensor_height = 4.8    # 传感器高度 4.8mm
    
    horizontal_fov = calculate_viewing_angle_from_lens(focal_length, sensor_width)
    vertical_fov = calculate_viewing_angle_from_lens(focal_length, sensor_height)
    
    print(f"沙盘规格: {sandbox_width} × {sandbox_height} 米")
    print(f"镜头参数: 焦距{focal_length}mm, 传感器{sensor_width}×{sensor_height}mm")
    print(f"计算得到视场角: {horizontal_fov:.1f}° × {vertical_fov:.1f}°")
    print()
    
    # 分析不同安装高度的效果
    print("分析不同安装高度的效果:")
    print("-" * 40)
    
    heights_to_test = [3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    height_analysis = []
    
    for height in heights_to_test:
        result = calculator.calculate_camera_count(
            sandbox_width, sandbox_height, height,
            horizontal_fov, vertical_fov, overlap_ratio=0.15
        )
        
        complexity = estimate_installation_complexity(
            result['total_cameras'], 
            sandbox_width * sandbox_height
        )
        
        height_analysis.append({
            'height': height,
            'cameras': result['total_cameras'],
            'coverage_ratio': result['coverage_ratio'],
            'cost': result['total_cost'],
            'complexity': complexity['complexity_level']
        })
        
        print(f"高度{height}米: {result['total_cameras']}个摄像头, "
              f"覆盖率{result['coverage_ratio']*100:.1f}%, "
              f"成本¥{result['total_cost']:,}, "
              f"复杂度{complexity['complexity_level']}")
    
    print()
    
    # 寻找最优配置
    print("寻找最优配置:")
    print("-" * 40)
    
    optimal_result = calculator.calculate_optimal_height(
        sandbox_width, sandbox_height, horizontal_fov, vertical_fov,
        max_cameras=20  # 限制最多20个摄像头
    )
    
    if optimal_result['configuration']:
        opt_config = optimal_result['configuration']
        print(f"最优安装高度: {optimal_result['optimal_height']} 米")
        print(f"所需摄像头: {opt_config['total_cameras']} 个")
        print(f"覆盖率: {opt_config['coverage_ratio']*100:.1f}%")
        print(f"预估成本: ¥{opt_config['total_cost']:,}")
        print()
        
        # 安装复杂度分析
        complexity = estimate_installation_complexity(
            opt_config['total_cameras'], 
            sandbox_width * sandbox_height
        )
        
        print("安装复杂度分析:")
        print(f"  复杂度等级: {complexity['complexity_level']}")
        print(f"  预计安装时间: {complexity['installation_time']:.1f} 小时")
        print(f"  人工成本: ¥{complexity['labor_cost']:,.0f}")
        print(f"  总成本: ¥{opt_config['total_cost'] + complexity['labor_cost']:,.0f}")
        print()
        
        print("安装建议:")
        for i, recommendation in enumerate(complexity['recommendations'], 1):
            print(f"  {i}. {recommendation}")
        print()
        
        # 生成可视化图表
        print("生成可视化图表...")
        
        try:
            # 布局图
            layout_img = visualizer.create_layout_plot(opt_config, show_coverage=True)
            layout_file = save_plot_as_file(layout_img, "camera_layout.png")
            print(f"布局图已保存: {layout_file}")
            
            # 3D视图
            viz_3d_img = visualizer.create_3d_visualization(opt_config)
            viz_3d_file = save_plot_as_file(viz_3d_img, "camera_3d_view.png")
            print(f"3D视图已保存: {viz_3d_file}")
            
            # 覆盖热力图
            heatmap_img = visualizer.create_coverage_heatmap(opt_config)
            heatmap_file = save_plot_as_file(heatmap_img, "coverage_heatmap.png")
            print(f"覆盖热力图已保存: {heatmap_file}")
            
            # 对比分析图
            if optimal_result['alternatives']:
                comparison_img = visualizer.create_comparison_chart(optimal_result['alternatives'])
                comparison_file = save_plot_as_file(comparison_img, "height_comparison.png")
                print(f"高度对比图已保存: {comparison_file}")
            
        except Exception as e:
            print(f"生成可视化图表时出错: {e}")
        
        print()
        
        # 生成详细报告
        print("详细配置信息:")
        print("-" * 40)
        print(f"沙盘尺寸: {sandbox_width} × {sandbox_height} 米")
        print(f"摄像头布局: {opt_config['cameras_x']} × {opt_config['cameras_y']} 阵列")
        print(f"摄像头间距: {opt_config['spacing_x']:.1f} × {opt_config['spacing_y']:.1f} 米")
        print(f"单摄像头覆盖: {opt_config['coverage_per_camera']['width']:.1f} × {opt_config['coverage_per_camera']['height']:.1f} 米")
        print(f"重叠比例: {opt_config['overlap_ratio']*100:.0f}%")
        print()
        
        print("摄像头位置坐标:")
        for i, pos in enumerate(opt_config['camera_positions']):
            print(f"  摄像头{i+1:2d}: X={pos['x']:5.1f}m, Y={pos['y']:5.1f}m, Z={pos['z']:5.1f}m")
    
    else:
        print("未找到合适的配置")
    
    return optimal_result

def demo_lens_calculation():
    """演示镜头参数计算"""
    print("\n" + "=" * 60)
    print("镜头参数计算演示")
    print("=" * 60)
    
    # 常见镜头规格
    lens_specs = [
        {"name": "超广角", "focal": 2.8, "sensor_w": 6.4, "sensor_h": 4.8},
        {"name": "广角", "focal": 6.0, "sensor_w": 6.4, "sensor_h": 4.8},
        {"name": "标准", "focal": 8.0, "sensor_w": 6.4, "sensor_h": 4.8},
        {"name": "中焦", "focal": 12.0, "sensor_w": 6.4, "sensor_h": 4.8},
        {"name": "长焦", "focal": 16.0, "sensor_w": 6.4, "sensor_h": 4.8},
    ]
    
    print("常见镜头规格视场角对比:")
    print("-" * 50)
    print(f"{'镜头类型':<8} {'焦距(mm)':<8} {'水平视场角':<10} {'垂直视场角':<10}")
    print("-" * 50)
    
    for lens in lens_specs:
        h_fov = calculate_viewing_angle_from_lens(lens['focal'], lens['sensor_w'])
        v_fov = calculate_viewing_angle_from_lens(lens['focal'], lens['sensor_h'])
        print(f"{lens['name']:<8} {lens['focal']:<8} {h_fov:>8.1f}°    {v_fov:>8.1f}°")

if __name__ == "__main__":
    # 运行高级示例
    result = advanced_example()
    
    # 运行镜头计算演示
    demo_lens_calculation()
    
    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("生成的图片文件保存在 'output' 文件夹中")
    print("=" * 60)