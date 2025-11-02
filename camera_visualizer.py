"""
摄像头布局可视化模块
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import List, Dict, Any
import io
import base64


class CameraVisualizer:
    """摄像头布局可视化器"""
    
    def __init__(self):
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    
    def create_layout_plot(self, calculation_result: Dict[str, Any], 
                          show_coverage: bool = True, 
                          show_overlap: bool = True) -> str:
        """
        创建摄像头布局图
        
        Args:
            calculation_result: 计算结果
            show_coverage: 是否显示覆盖范围
            show_overlap: 是否显示重叠区域
            
        Returns:
            str: Base64编码的图片数据
        """
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        
        sandbox_width = calculation_result['sandbox_dimensions']['width']
        sandbox_height = calculation_result['sandbox_dimensions']['height']
        camera_positions = calculation_result['camera_positions']
        coverage = calculation_result['coverage_per_camera']
        
        # 绘制沙盘边界
        sandbox_rect = patches.Rectangle(
            (0, 0), sandbox_width, sandbox_height,
            linewidth=3, edgecolor='black', facecolor='lightgray', alpha=0.3
        )
        ax.add_patch(sandbox_rect)
        
        # 绘制摄像头覆盖范围
        if show_coverage:
            for i, pos in enumerate(camera_positions):
                # 计算覆盖范围的矩形
                coverage_x = pos['x'] - coverage['width'] / 2
                coverage_y = pos['y'] - coverage['height'] / 2
                
                # 绘制覆盖范围
                coverage_rect = patches.Rectangle(
                    (coverage_x, coverage_y), 
                    coverage['width'], coverage['height'],
                    linewidth=1, edgecolor='blue', facecolor='blue', 
                    alpha=0.2, linestyle='--'
                )
                ax.add_patch(coverage_rect)
                
                # 添加覆盖范围标签
                ax.text(pos['x'], pos['y'] - coverage['height']/3, 
                       f'覆盖范围\n{coverage["width"]:.1f}×{coverage["height"]:.1f}m',
                       ha='center', va='center', fontsize=8, 
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        # 绘制摄像头位置
        for i, pos in enumerate(camera_positions):
            # 摄像头图标
            camera_circle = patches.Circle(
                (pos['x'], pos['y']), 0.3, 
                facecolor='red', edgecolor='darkred', linewidth=2
            )
            ax.add_patch(camera_circle)
            
            # 摄像头编号
            ax.text(pos['x'], pos['y'], str(i+1), 
                   ha='center', va='center', fontweight='bold', 
                   color='white', fontsize=10)
            
            # 摄像头坐标标签
            ax.text(pos['x'], pos['y'] + 0.6, 
                   f'({pos["x"]:.1f}, {pos["y"]:.1f})',
                   ha='center', va='bottom', fontsize=8)
        
        # 设置坐标轴
        ax.set_xlim(-1, sandbox_width + 1)
        ax.set_ylim(-1, sandbox_height + 1)
        ax.set_xlabel('宽度 (米)', fontsize=12)
        ax.set_ylabel('高度 (米)', fontsize=12)
        ax.set_title(f'沙盘摄像头布局图\n沙盘尺寸: {sandbox_width}×{sandbox_height}m, '
                    f'摄像头数量: {len(camera_positions)}个', fontsize=14, fontweight='bold')
        
        # 添加网格
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
        
        # 添加图例
        legend_elements = [
            patches.Patch(color='lightgray', alpha=0.3, label='沙盘区域'),
            patches.Circle((0, 0), 0.1, facecolor='red', label='摄像头位置'),
        ]
        if show_coverage:
            legend_elements.append(
                patches.Patch(color='blue', alpha=0.2, label='覆盖范围')
            )
        
        ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
        
        # 添加统计信息
        stats_text = (
            f"安装高度: {coverage['camera_height']}m\n"
            f"视场角: {coverage['horizontal_fov']}°×{coverage['vertical_fov']}°\n"
            f"单摄像头覆盖: {coverage['width']:.1f}×{coverage['height']:.1f}m\n"
            f"覆盖率: {calculation_result['coverage_ratio']*100:.1f}%\n"
            f"总成本: ¥{calculation_result['total_cost']:,}"
        )
        
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
               verticalalignment='top', fontsize=10,
               bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.8))
        
        plt.tight_layout()
        
        # 转换为base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_base64
    
    def create_3d_visualization(self, calculation_result: Dict[str, Any]) -> str:
        """
        创建3D可视化图
        
        Args:
            calculation_result: 计算结果
            
        Returns:
            str: Base64编码的图片数据
        """
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        sandbox_width = calculation_result['sandbox_dimensions']['width']
        sandbox_height = calculation_result['sandbox_dimensions']['height']
        camera_positions = calculation_result['camera_positions']
        coverage = calculation_result['coverage_per_camera']
        camera_height = coverage['camera_height']
        
        # 绘制沙盘底面
        xx, yy = np.meshgrid([0, sandbox_width], [0, sandbox_height])
        zz = np.zeros_like(xx)
        ax.plot_surface(xx, yy, zz, alpha=0.3, color='lightgray')
        
        # 绘制摄像头位置和覆盖锥形
        for i, pos in enumerate(camera_positions):
            # 摄像头位置
            ax.scatter(pos['x'], pos['y'], pos['z'], 
                      color='red', s=100, alpha=1.0)
            
            # 摄像头到地面的连线
            ax.plot([pos['x'], pos['x']], [pos['y'], pos['y']], 
                   [pos['z'], 0], 'r--', alpha=0.5)
            
            # 覆盖范围的四个角点
            corners_x = [
                pos['x'] - coverage['width']/2,
                pos['x'] + coverage['width']/2,
                pos['x'] + coverage['width']/2,
                pos['x'] - coverage['width']/2,
                pos['x'] - coverage['width']/2
            ]
            corners_y = [
                pos['y'] - coverage['height']/2,
                pos['y'] - coverage['height']/2,
                pos['y'] + coverage['height']/2,
                pos['y'] + coverage['height']/2,
                pos['y'] - coverage['height']/2
            ]
            
            # 绘制覆盖范围边界
            ax.plot(corners_x, corners_y, [0]*5, 'b-', alpha=0.7)
            
            # 绘制从摄像头到覆盖区域角点的连线（视锥）
            for cx, cy in zip(corners_x[:-1], corners_y[:-1]):
                ax.plot([pos['x'], cx], [pos['y'], cy], [pos['z'], 0], 
                       'b-', alpha=0.3, linewidth=0.5)
            
            # 摄像头标签
            ax.text(pos['x'], pos['y'], pos['z'] + 0.3, f'摄像头{i+1}', 
                   fontsize=8, ha='center')
        
        # 设置坐标轴
        ax.set_xlabel('宽度 (米)')
        ax.set_ylabel('高度 (米)')
        ax.set_zlabel('高度 (米)')
        ax.set_title(f'摄像头3D布局图\n安装高度: {camera_height}m')
        
        # 设置视角
        ax.view_init(elev=20, azim=45)
        
        plt.tight_layout()
        
        # 转换为base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_base64
    
    def create_coverage_heatmap(self, calculation_result: Dict[str, Any], 
                               resolution: int = 100) -> str:
        """
        创建覆盖热力图
        
        Args:
            calculation_result: 计算结果
            resolution: 热力图分辨率
            
        Returns:
            str: Base64编码的图片数据
        """
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        
        sandbox_width = calculation_result['sandbox_dimensions']['width']
        sandbox_height = calculation_result['sandbox_dimensions']['height']
        camera_positions = calculation_result['camera_positions']
        coverage = calculation_result['coverage_per_camera']
        
        # 创建网格
        x = np.linspace(0, sandbox_width, resolution)
        y = np.linspace(0, sandbox_height, resolution)
        X, Y = np.meshgrid(x, y)
        
        # 计算每个点的覆盖情况
        coverage_count = np.zeros_like(X)
        
        for pos in camera_positions:
            # 计算每个摄像头的覆盖范围
            x_min = pos['x'] - coverage['width'] / 2
            x_max = pos['x'] + coverage['width'] / 2
            y_min = pos['y'] - coverage['height'] / 2
            y_max = pos['y'] + coverage['height'] / 2
            
            # 在覆盖范围内的点+1
            mask = (X >= x_min) & (X <= x_max) & (Y >= y_min) & (Y <= y_max)
            coverage_count += mask.astype(int)
        
        # 绘制热力图
        im = ax.imshow(coverage_count, extent=[0, sandbox_width, 0, sandbox_height], 
                      origin='lower', cmap='YlOrRd', alpha=0.8)
        
        # 添加颜色条
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('覆盖摄像头数量', fontsize=12)
        
        # 绘制摄像头位置
        for i, pos in enumerate(camera_positions):
            ax.scatter(pos['x'], pos['y'], color='blue', s=100, 
                      marker='s', edgecolor='white', linewidth=2)
            ax.text(pos['x'], pos['y'] + 0.3, f'{i+1}', 
                   ha='center', va='bottom', fontweight='bold', 
                   color='white', fontsize=10)
        
        # 设置坐标轴
        ax.set_xlabel('宽度 (米)', fontsize=12)
        ax.set_ylabel('高度 (米)', fontsize=12)
        ax.set_title('摄像头覆盖热力图', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # 转换为base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_base64
    
    def create_comparison_chart(self, height_analysis: List[Dict[str, Any]]) -> str:
        """
        创建不同高度对比图表
        
        Args:
            height_analysis: 不同高度的分析结果
            
        Returns:
            str: Base64编码的图片数据
        """
        if not height_analysis:
            return ""
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        heights = [result['height'] for result in height_analysis]
        camera_counts = [result['cameras'] for result in height_analysis]
        coverage_ratios = [result['coverage_ratio'] * 100 for result in height_analysis]
        costs = [result['cost'] for result in height_analysis]
        
        # 摄像头数量 vs 高度
        ax1.plot(heights, camera_counts, 'bo-', linewidth=2, markersize=6)
        ax1.set_xlabel('安装高度 (米)')
        ax1.set_ylabel('摄像头数量')
        ax1.set_title('摄像头数量 vs 安装高度')
        ax1.grid(True, alpha=0.3)
        
        # 覆盖率 vs 高度
        ax2.plot(heights, coverage_ratios, 'go-', linewidth=2, markersize=6)
        ax2.set_xlabel('安装高度 (米)')
        ax2.set_ylabel('覆盖率 (%)')
        ax2.set_title('覆盖率 vs 安装高度')
        ax2.grid(True, alpha=0.3)
        
        # 成本 vs 高度
        ax3.plot(heights, costs, 'ro-', linewidth=2, markersize=6)
        ax3.set_xlabel('安装高度 (米)')
        ax3.set_ylabel('总成本 (元)')
        ax3.set_title('总成本 vs 安装高度')
        ax3.grid(True, alpha=0.3)
        
        # 成本效益分析
        efficiency = [coverage_ratios[i] / (costs[i] / 1000) for i in range(len(costs))]
        ax4.plot(heights, efficiency, 'mo-', linewidth=2, markersize=6)
        ax4.set_xlabel('安装高度 (米)')
        ax4.set_ylabel('成本效益 (覆盖率/千元)')
        ax4.set_title('成本效益 vs 安装高度')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # 转换为base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_base64


def save_plot_as_file(img_base64: str, filename: str) -> str:
    """
    将base64图片保存为文件
    
    Args:
        img_base64: base64编码的图片
        filename: 保存的文件名
        
    Returns:
        str: 保存的文件路径
    """
    import os
    
    # 创建输出目录
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存文件
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'wb') as f:
        f.write(base64.b64decode(img_base64))
    
    return filepath