"""
成本分析示例 - 比较不同价格摄像头的成本效益
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from camera_calculator import CameraCalculator, estimate_installation_complexity

def cost_analysis_demo():
    """成本分析演示"""
    print("=" * 60)
    print("摄像头成本分析示例")
    print("=" * 60)
    
    # 创建计算器实例
    calculator = CameraCalculator()
    
    # 示例参数
    sandbox_width = 15.0   # 沙盘宽度 15米
    sandbox_height = 12.0  # 沙盘高度 12米
    camera_height = 6.0    # 摄像头安装高度 6米
    horizontal_fov = 70.0  # 水平视场角 70度
    vertical_fov = 50.0    # 垂直视场角 50度
    
    print(f"测试场景:")
    print(f"  沙盘规格: {sandbox_width} × {sandbox_height} 米")
    print(f"  安装高度: {camera_height} 米")
    print(f"  视场角: {horizontal_fov}° × {vertical_fov}°")
    print()
    
    # 不同价位的摄像头规格
    camera_models = [
        {"name": "经济型", "price": 800, "description": "基础监控摄像头"},
        {"name": "标准型", "price": 1500, "description": "高清网络摄像头"},
        {"name": "高端型", "price": 3000, "description": "4K智能摄像头"},
        {"name": "专业型", "price": 5000, "description": "工业级监控设备"},
        {"name": "顶级型", "price": 8000, "description": "AI智能分析摄像头"}
    ]
    
    print("不同价位摄像头成本分析:")
    print("=" * 80)
    print(f"{'型号':<8} {'单价(元)':<10} {'数量':<6} {'设备成本':<12} {'人工成本':<12} {'总成本':<12} {'性价比':<8}")
    print("-" * 80)
    
    cost_analysis_results = []
    
    for model in camera_models:
        # 计算所需摄像头数量和成本
        result = calculator.calculate_camera_count(
            sandbox_width, sandbox_height, camera_height,
            horizontal_fov, vertical_fov, camera_price=model["price"]
        )
        
        # 计算安装复杂度
        complexity = estimate_installation_complexity(
            result['total_cameras'], 
            sandbox_width * sandbox_height
        )
        
        # 计算性价比 (覆盖率/万元)
        total_cost = result['total_cost'] + complexity['labor_cost']
        cost_efficiency = (result['coverage_ratio'] * 100) / (total_cost / 10000)
        
        cost_analysis_results.append({
            'model': model['name'],
            'price': model['price'],
            'cameras': result['total_cameras'],
            'equipment_cost': result['total_cost'],
            'labor_cost': complexity['labor_cost'],
            'total_cost': total_cost,
            'coverage_ratio': result['coverage_ratio'],
            'cost_efficiency': cost_efficiency,
            'complexity': complexity['complexity_level']
        })
        
        print(f"{model['name']:<8} ¥{model['price']:<9,} {result['total_cameras']:<6} "
              f"¥{result['total_cost']:<11,} ¥{complexity['labor_cost']:<11,.0f} "
              f"¥{total_cost:<11,.0f} {cost_efficiency:.2f}")
    
    print()
    
    # 找出最具性价比的方案
    best_efficiency = max(cost_analysis_results, key=lambda x: x['cost_efficiency'])
    lowest_cost = min(cost_analysis_results, key=lambda x: x['total_cost'])
    
    print("推荐方案分析:")
    print("-" * 50)
    print(f"最具性价比: {best_efficiency['model']} (性价比: {best_efficiency['cost_efficiency']:.2f})")
    print(f"  单价: ¥{best_efficiency['price']:,}")
    print(f"  数量: {best_efficiency['cameras']} 个")
    print(f"  总成本: ¥{best_efficiency['total_cost']:,.0f}")
    print(f"  安装复杂度: {best_efficiency['complexity']}")
    print()
    
    print(f"最低成本: {lowest_cost['model']} (总成本: ¥{lowest_cost['total_cost']:,.0f})")
    print(f"  单价: ¥{lowest_cost['price']:,}")
    print(f"  数量: {lowest_cost['cameras']} 个")
    print(f"  性价比: {lowest_cost['cost_efficiency']:.2f}")
    print(f"  安装复杂度: {lowest_cost['complexity']}")
    print()
    
    # 预算分析
    print("预算区间建议:")
    print("-" * 50)
    budget_ranges = [
        {"range": "经济预算 (≤3万)", "min": 0, "max": 30000},
        {"range": "标准预算 (3-6万)", "min": 30000, "max": 60000},
        {"range": "充足预算 (6-10万)", "min": 60000, "max": 100000},
        {"range": "高端预算 (>10万)", "min": 100000, "max": float('inf')}
    ]
    
    for budget_range in budget_ranges:
        suitable_models = [
            result for result in cost_analysis_results 
            if budget_range["min"] < result["total_cost"] <= budget_range["max"]
        ]
        
        if suitable_models:
            best_in_range = max(suitable_models, key=lambda x: x['cost_efficiency'])
            print(f"{budget_range['range']}: 推荐 {best_in_range['model']}")
            print(f"  总成本: ¥{best_in_range['total_cost']:,.0f}")
            print(f"  性价比: {best_in_range['cost_efficiency']:.2f}")
        else:
            print(f"{budget_range['range']}: 暂无合适方案")
    
    print()
    
    # 详细成本分解（以最佳性价比方案为例）
    print(f"详细成本分解 ({best_efficiency['model']}):")
    print("-" * 50)
    print(f"设备成本:")
    print(f"  摄像头: {best_efficiency['cameras']} × ¥{best_efficiency['price']:,} = ¥{best_efficiency['equipment_cost']:,}")
    print(f"  线缆布线: ¥{best_efficiency['equipment_cost'] * 0.15:,.0f} (约15%)")
    print(f"  网络设备: ¥{best_efficiency['equipment_cost'] * 0.10:,.0f} (约10%)")
    print(f"  存储设备: ¥{best_efficiency['equipment_cost'] * 0.20:,.0f} (约20%)")
    
    total_equipment = best_efficiency['equipment_cost'] * 1.45
    
    print(f"  设备小计: ¥{total_equipment:,.0f}")
    print()
    print(f"人工成本:")
    print(f"  安装调试: ¥{best_efficiency['labor_cost']:,.0f}")
    print(f"  项目管理: ¥{best_efficiency['labor_cost'] * 0.2:,.0f} (约20%)")
    print(f"  培训维护: ¥{best_efficiency['labor_cost'] * 0.1:,.0f} (约10%)")
    
    total_labor = best_efficiency['labor_cost'] * 1.3
    print(f"  人工小计: ¥{total_labor:,.0f}")
    print()
    print(f"项目总预算: ¥{total_equipment + total_labor:,.0f}")
    
    return cost_analysis_results

def compare_scenarios():
    """比较不同场景下的成本效益"""
    print("\n" + "=" * 60)
    print("不同场景成本对比")
    print("=" * 60)
    
    calculator = CameraCalculator()
    
    scenarios = [
        {"name": "小型沙盘", "width": 8, "height": 6, "camera_height": 4},
        {"name": "中型沙盘", "width": 15, "height": 12, "camera_height": 6},
        {"name": "大型沙盘", "width": 25, "height": 20, "camera_height": 8},
        {"name": "超大沙盘", "width": 40, "height": 30, "camera_height": 10}
    ]
    
    camera_price = 2000  # 标准价格
    
    print(f"{'场景':<12} {'尺寸(m)':<12} {'摄像头数':<8} {'设备成本':<12} {'人工成本':<12} {'单位成本':<12}")
    print("-" * 80)
    
    for scenario in scenarios:
        result = calculator.calculate_camera_count(
            scenario["width"], scenario["height"], scenario["camera_height"],
            60.0, 45.0, camera_price=camera_price
        )
        
        complexity = estimate_installation_complexity(
            result['total_cameras'], 
            scenario["width"] * scenario["height"]
        )
        
        area = scenario["width"] * scenario["height"]
        unit_cost = (result['total_cost'] + complexity['labor_cost']) / area
        
        print(f"{scenario['name']:<12} {scenario['width']}×{scenario['height']:<8} "
              f"{result['total_cameras']:<8} ¥{result['total_cost']:<11,} "
              f"¥{complexity['labor_cost']:<11,.0f} ¥{unit_cost:<11,.0f}/m²")

if __name__ == "__main__":
    # 运行成本分析
    results = cost_analysis_demo()
    
    # 运行场景对比
    compare_scenarios()
    
    print("\n" + "=" * 60)
    print("成本分析完成！")
    print("建议根据实际预算和质量要求选择合适的摄像头型号")
    print("=" * 60)