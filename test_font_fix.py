"""
测试中文字体显示修复
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from camera_calculator import CameraCalculator
from camera_visualizer import CameraVisualizer, save_plot_as_file

def test_font_fix():
    """测试字体修复效果"""
    print("🔧 测试中文字体显示修复")
    print("=" * 50)
    
    # 创建计算器和可视化器
    calculator = CameraCalculator()
    visualizer = CameraVisualizer()
    
    print(f"当前系统检测到的字体: {visualizer.font_name}")
    
    # 测试计算
    result = calculator.calculate_camera_count(
        sandbox_width=12.0,
        sandbox_height=10.0,
        camera_height=5.0,
        horizontal_fov=60.0,
        vertical_fov=45.0,
        camera_price=2500.0
    )
    
    print(f"计算结果: {result['total_cameras']}个摄像头")
    
    # 测试各种图表生成
    try:
        print("\n📊 生成测试图表...")
        
        # 布局图
        print("1. 生成布局图...")
        layout_img = visualizer.create_layout_plot(result)
        layout_file = save_plot_as_file(layout_img, "test_layout_font_fix.png")
        print(f"   ✅ 布局图已保存: {layout_file}")
        
        # 3D视图
        print("2. 生成3D视图...")
        viz_3d_img = visualizer.create_3d_visualization(result)
        viz_3d_file = save_plot_as_file(viz_3d_img, "test_3d_font_fix.png")
        print(f"   ✅ 3D视图已保存: {viz_3d_file}")
        
        # 热力图
        print("3. 生成覆盖热力图...")
        heatmap_img = visualizer.create_coverage_heatmap(result)
        heatmap_file = save_plot_as_file(heatmap_img, "test_heatmap_font_fix.png")
        print(f"   ✅ 覆盖热力图已保存: {heatmap_file}")
        
        # 对比图
        print("4. 生成高度对比图...")
        height_analysis = []
        for height in [3.0, 4.0, 5.0, 6.0, 7.0]:
            test_result = calculator.calculate_camera_count(
                12.0, 10.0, height, 60.0, 45.0, camera_price=2500.0
            )
            height_analysis.append({
                'height': height,
                'cameras': test_result['total_cameras'],
                'coverage_ratio': test_result['coverage_ratio'],
                'cost': test_result['total_cost']
            })
        
        comparison_img = visualizer.create_comparison_chart(height_analysis)
        comparison_file = save_plot_as_file(comparison_img, "test_comparison_font_fix.png")
        print(f"   ✅ 对比图已保存: {comparison_file}")
        
        print("\n🎉 所有测试图表生成成功！")
        print("请检查output文件夹中的图片，确认中文显示是否正常。")
        
        # 显示可用字体信息
        print(f"\n📝 字体信息:")
        print(f"   选择的字体: {visualizer.font_name}")
        if visualizer.font_name:
            print("   ✅ 找到合适的中文字体")
        else:
            print("   ⚠️  未找到中文字体，使用英文标签")
        
    except Exception as e:
        print(f"❌ 生成图表时出错: {e}")
        import traceback
        traceback.print_exc()

def show_available_fonts():
    """显示系统可用字体"""
    import matplotlib.font_manager as fm
    import platform
    
    print(f"\n💻 系统信息: {platform.system()}")
    print("🔤 系统可用字体 (包含中文相关关键词):")
    print("-" * 60)
    
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    chinese_fonts = []
    
    keywords = ['chinese', 'cjk', 'han', 'hei', 'song', 'kai', 'fangsong', 
                'yahei', 'simsun', 'simhei', 'arial unicode', 'pingfang', 'heiti']
    
    for font_name in available_fonts:
        if any(keyword in font_name.lower() for keyword in keywords):
            chinese_fonts.append(font_name)
    
    # 去重并排序
    chinese_fonts = sorted(list(set(chinese_fonts)))
    
    if chinese_fonts:
        for i, font in enumerate(chinese_fonts[:10], 1):  # 只显示前10个
            print(f"{i:2d}. {font}")
        if len(chinese_fonts) > 10:
            print(f"    ... 还有 {len(chinese_fonts) - 10} 个字体")
    else:
        print("❌ 未找到相关中文字体")
    
    print(f"\n📊 总计找到 {len(chinese_fonts)} 个可能的中文字体")

if __name__ == "__main__":
    # 显示字体信息
    show_available_fonts()
    
    # 运行测试
    test_font_fix()
    
    print("\n" + "=" * 50)
    print("字体修复测试完成！")
    print("如果图片中仍有乱码，请安装相应的中文字体包。")
    print("=" * 50)