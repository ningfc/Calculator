"""
基础示例 - 简单的摄像头计算
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from camera_calculator import CameraCalculator

def basic_example():
    """基础示例"""
    print("=" * 50)
    print("沙盘摄像头安装计算器 - 基础示例")
    print("=" * 50)
    
    # 创建计算器实例
    calculator = CameraCalculator()
    
    # 示例参数
    sandbox_width = 10.0  # 沙盘宽度 10米
    sandbox_height = 8.0  # 沙盘高度 8米
    camera_height = 5.0   # 摄像头安装高度 5米
    horizontal_fov = 60.0 # 水平视场角 60度
    vertical_fov = 45.0   # 垂直视场角 45度
    
    print(f"沙盘规格: {sandbox_width} × {sandbox_height} 米")
    print(f"摄像头参数: 高度{camera_height}米, 视场角{horizontal_fov}°×{vertical_fov}°")
    print()
    
    # 计算单个摄像头的覆盖范围
    coverage = calculator.calculate_coverage_area(camera_height, horizontal_fov, vertical_fov)
    print("单个摄像头覆盖范围:")
    print(f"  覆盖宽度: {coverage['width']:.2f} 米")
    print(f"  覆盖高度: {coverage['height']:.2f} 米")
    print(f"  覆盖面积: {coverage['area']:.2f} 平方米")
    print()
    
    # 计算所需摄像头数量
    result = calculator.calculate_camera_count(
        sandbox_width, sandbox_height, camera_height,
        horizontal_fov, vertical_fov
    )
    
    print("摄像头布局计算结果:")
    print(f"  所需摄像头总数: {result['total_cameras']} 个")
    print(f"  布局方式: {result['cameras_x']} × {result['cameras_y']} 阵列")
    print(f"  覆盖率: {result['coverage_ratio']*100:.1f}%")
    print(f"  预估总成本: ¥{result['total_cost']:,}")
    print()
    
    print("摄像头位置坐标:")
    for i, pos in enumerate(result['camera_positions']):
        print(f"  摄像头{i+1}: ({pos['x']:.1f}, {pos['y']:.1f}, {pos['z']:.1f})")
    
    return result

if __name__ == "__main__":
    basic_example()