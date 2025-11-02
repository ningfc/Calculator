"""
沙盘摄像头安装计算器
根据摄像头视场角和安装高度计算覆盖范围，并确定所需摄像头数量
"""

import math
import numpy as np
from typing import Tuple, List, Dict, Any


class CameraCalculator:
    """摄像头计算器类"""
    
    def __init__(self):
        self.camera_positions = []
        self.coverage_areas = []
    
    def calculate_coverage_area(self, height: float, horizontal_fov: float, vertical_fov: float) -> Dict[str, float]:
        """
        计算单个摄像头的覆盖范围
        
        Args:
            height: 摄像头安装高度（米）
            horizontal_fov: 水平视场角（度）
            vertical_fov: 垂直视场角（度）
            
        Returns:
            Dict: 包含覆盖面积和尺寸的字典
        """
        # 将角度转换为弧度
        h_fov_rad = math.radians(horizontal_fov)
        v_fov_rad = math.radians(vertical_fov)
        
        # 计算覆盖范围的长宽
        coverage_width = 2 * height * math.tan(h_fov_rad / 2)
        coverage_height = 2 * height * math.tan(v_fov_rad / 2)
        
        # 计算覆盖面积
        coverage_area = coverage_width * coverage_height
        
        return {
            'width': coverage_width,
            'height': coverage_height,
            'area': coverage_area,
            'camera_height': height,
            'horizontal_fov': horizontal_fov,
            'vertical_fov': vertical_fov
        }
    
    def calculate_camera_count(self, sandbox_width: float, sandbox_height: float, 
                             camera_height: float, horizontal_fov: float, 
                             vertical_fov: float, overlap_ratio: float = 0.2,
                             camera_price: float = 2000.0) -> Dict[str, Any]:
        """
        计算完全覆盖沙盘所需的摄像头数量
        
        Args:
            sandbox_width: 沙盘宽度（米）
            sandbox_height: 沙盘高度（米）
            camera_height: 摄像头安装高度（米）
            horizontal_fov: 水平视场角（度）
            vertical_fov: 垂直视场角（度）
            overlap_ratio: 重叠比例（默认20%）
            camera_price: 摄像头单价（元，默认2000元）
            
        Returns:
            Dict: 包含摄像头数量和布局信息的字典
        """
        # 计算单个摄像头的覆盖范围
        coverage = self.calculate_coverage_area(camera_height, horizontal_fov, vertical_fov)
        
        # 考虑重叠，计算有效覆盖范围
        effective_width = coverage['width'] * (1 - overlap_ratio)
        effective_height = coverage['height'] * (1 - overlap_ratio)
        
        # 计算所需摄像头数量
        cameras_x = math.ceil(sandbox_width / effective_width)
        cameras_y = math.ceil(sandbox_height / effective_height)
        total_cameras = cameras_x * cameras_y
        
        # 计算实际间距
        spacing_x = sandbox_width / cameras_x if cameras_x > 1 else sandbox_width / 2
        spacing_y = sandbox_height / cameras_y if cameras_y > 1 else sandbox_height / 2
        
        # 生成摄像头位置
        camera_positions = []
        for i in range(cameras_x):
            for j in range(cameras_y):
                x = spacing_x * (i + 0.5) if cameras_x > 1 else sandbox_width / 2
                y = spacing_y * (j + 0.5) if cameras_y > 1 else sandbox_height / 2
                camera_positions.append({'x': x, 'y': y, 'z': camera_height})
        
        # 计算覆盖率
        total_coverage_area = total_cameras * coverage['area']
        sandbox_area = sandbox_width * sandbox_height
        coverage_ratio = min(total_coverage_area / sandbox_area, 1.0) if sandbox_area > 0 else 0
        
        # 计算成本估算
        total_cost = total_cameras * camera_price
        
        self.camera_positions = camera_positions
        
        return {
            'total_cameras': total_cameras,
            'cameras_x': cameras_x,
            'cameras_y': cameras_y,
            'camera_positions': camera_positions,
            'spacing_x': spacing_x,
            'spacing_y': spacing_y,
            'coverage_per_camera': coverage,
            'effective_coverage': {
                'width': effective_width,
                'height': effective_height
            },
            'coverage_ratio': coverage_ratio,
            'overlap_ratio': overlap_ratio,
            'total_cost': total_cost,
            'camera_price': camera_price,
            'sandbox_dimensions': {
                'width': sandbox_width,
                'height': sandbox_height,
                'area': sandbox_area
            }
        }
    
    def calculate_optimal_height(self, sandbox_width: float, sandbox_height: float,
                               horizontal_fov: float, vertical_fov: float,
                               max_cameras: int = None, camera_price: float = 2000.0) -> Dict[str, Any]:
        """
        计算最优安装高度
        
        Args:
            sandbox_width: 沙盘宽度（米）
            sandbox_height: 沙盘高度（米）
            horizontal_fov: 水平视场角（度）
            vertical_fov: 垂直视场角（度）
            max_cameras: 最大摄像头数量限制
            camera_price: 摄像头单价（元，默认2000元）
            
        Returns:
            Dict: 最优高度和对应的配置信息
        """
        optimal_results = []
        
        # 测试不同高度（从1米到10米，步长0.5米）
        for height in np.arange(1.0, 10.1, 0.5):
            result = self.calculate_camera_count(
                sandbox_width, sandbox_height, height, 
                horizontal_fov, vertical_fov, camera_price=camera_price
            )
            
            # 如果设置了最大摄像头数量限制
            if max_cameras and result['total_cameras'] <= max_cameras:
                optimal_results.append({
                    'height': height,
                    'cameras': result['total_cameras'],
                    'coverage_ratio': result['coverage_ratio'],
                    'cost': result['total_cost'],
                    'result': result
                })
        
        # 如果没有找到满足条件的配置，返回摄像头数量最少的
        if not optimal_results:
            min_cameras = float('inf')
            best_height = 5.0  # 默认高度
            best_result = None
            
            for height in np.arange(1.0, 10.1, 0.5):
                result = self.calculate_camera_count(
                    sandbox_width, sandbox_height, height, 
                    horizontal_fov, vertical_fov, camera_price=camera_price
                )
                if result['total_cameras'] < min_cameras:
                    min_cameras = result['total_cameras']
                    best_height = height
                    best_result = result
            
            return {
                'optimal_height': best_height,
                'configuration': best_result,
                'alternatives': []
            }
        
        # 选择覆盖率最高的配置
        best_config = max(optimal_results, key=lambda x: x['coverage_ratio'])
        
        return {
            'optimal_height': best_config['height'],
            'configuration': best_config['result'],
            'alternatives': optimal_results[:5]  # 返回前5个备选方案
        }
    
    def get_coverage_visualization_data(self) -> List[Dict[str, Any]]:
        """
        获取可视化数据
        
        Returns:
            List: 摄像头覆盖范围的可视化数据
        """
        return [
            {
                'x': pos['x'],
                'y': pos['y'],
                'z': pos['z']
            }
            for pos in self.camera_positions
        ]


def calculate_viewing_angle_from_lens(focal_length: float, sensor_size: float) -> float:
    """
    根据镜头焦距和传感器尺寸计算视场角
    
    Args:
        focal_length: 焦距（mm）
        sensor_size: 传感器尺寸（mm）
        
    Returns:
        float: 视场角（度）
    """
    angle_rad = 2 * math.atan(sensor_size / (2 * focal_length))
    return math.degrees(angle_rad)


def estimate_installation_complexity(camera_count: int, area: float) -> Dict[str, Any]:
    """
    估算安装复杂度和时间
    
    Args:
        camera_count: 摄像头数量
        area: 安装区域面积（平方米）
        
    Returns:
        Dict: 安装复杂度评估
    """
    # 基础安装时间（小时/摄像头）
    base_time_per_camera = 2
    
    # 复杂度因子
    if camera_count <= 4:
        complexity_factor = 1.0
        complexity_level = "简单"
    elif camera_count <= 10:
        complexity_factor = 1.2
        complexity_level = "中等"
    elif camera_count <= 20:
        complexity_factor = 1.5
        complexity_level = "复杂"
    else:
        complexity_factor = 2.0
        complexity_level = "非常复杂"
    
    # 计算估算时间
    installation_time = camera_count * base_time_per_camera * complexity_factor
    
    # 估算人工成本（假设200元/小时）
    labor_cost = installation_time * 200
    
    return {
        'complexity_level': complexity_level,
        'installation_time': installation_time,
        'labor_cost': labor_cost,
        'complexity_factor': complexity_factor,
        'recommendations': _get_installation_recommendations(complexity_level, camera_count)
    }


def _get_installation_recommendations(complexity_level: str, camera_count: int) -> List[str]:
    """获取安装建议"""
    recommendations = []
    
    if complexity_level == "简单":
        recommendations.extend([
            "可以由1-2名技术人员完成安装",
            "建议提前规划线缆走向",
            "确保电源供应充足"
        ])
    elif complexity_level == "中等":
        recommendations.extend([
            "建议由2-3名技术人员协作安装",
            "需要详细的安装方案和时间规划",
            "考虑使用PoE供电减少布线复杂度",
            "预留10%的时间缓冲"
        ])
    elif complexity_level == "复杂":
        recommendations.extend([
            "需要专业安装团队（3-4人）",
            "建议分阶段安装和测试",
            "必须有详细的施工图纸",
            "考虑使用专业的线缆管理系统",
            "预留20%的时间缓冲"
        ])
    else:  # 非常复杂
        recommendations.extend([
            "需要专业的大型项目安装团队",
            "必须有项目管理和质量控制",
            "建议采用模块化安装方式",
            "需要专业的网络和存储设备",
            "预留30%的时间缓冲",
            "考虑分期实施"
        ])
    
    return recommendations