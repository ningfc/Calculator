"""
发布版本字体配置 - 确保中文显示正常
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import os
import warnings


def configure_fonts_for_production():
    """
    为生产环境配置字体，确保中文正常显示
    """
    system = platform.system()
    
    # 详细的字体候选列表
    font_candidates = {
        "Windows": [
            'Microsoft YaHei UI',
            'Microsoft YaHei',
            'SimHei',
            'SimSun',
            'KaiTi',
            'FangSong',
            'NSimSun',
            'DengXian'
        ],
        "Darwin": [  # macOS
            'Arial Unicode MS',
            'PingFang SC',
            'Heiti SC',
            'Heiti TC',
            'STHeiti',
            'Hiragino Sans GB',
            'Apple LiGothic',
            'Apple LiSung'
        ],
        "Linux": [
            'Noto Sans CJK SC',
            'Noto Sans CJK TC',
            'Source Han Sans CN',
            'Source Han Sans TW',
            'WenQuanYi Micro Hei',
            'WenQuanYi Zen Hei',
            'WenQuanYi Bitmap Song',
            'AR PL UMing CN',
            'AR PL UKai CN'
        ]
    }
    
    # 获取当前系统的字体候选
    candidates = font_candidates.get(system, font_candidates["Linux"])
    
    # 获取所有可用字体
    available_fonts = set(f.name for f in fm.fontManager.ttflist)
    
    # 查找可用的中文字体
    selected_font = None
    for font in candidates:
        if font in available_fonts:
            selected_font = font
            break
    
    # 如果主要候选都没找到，尝试模糊匹配
    if selected_font is None:
        chinese_keywords = [
            'chinese', 'cjk', 'han', 'hei', 'song', 'kai', 'fangsong',
            'yahei', 'simsun', 'simhei', 'pingfang', 'heiti', 'noto',
            'source', 'wenquanyi', 'ar pl', 'hiragino', 'apple'
        ]
        
        for font_name in available_fonts:
            font_lower = font_name.lower()
            if any(keyword in font_lower for keyword in chinese_keywords):
                # 优先选择包含"sans"或"ui"的字体（通常显示效果更好）
                if 'sans' in font_lower or 'ui' in font_lower:
                    selected_font = font_name
                    break
                elif selected_font is None:
                    selected_font = font_name
    
    # 设置matplotlib参数
    if selected_font:
        plt.rcParams.update({
            'font.sans-serif': [selected_font, 'Arial', 'DejaVu Sans', 'sans-serif'],
            'font.family': 'sans-serif',
            'axes.unicode_minus': False,
            'font.size': 10
        })
        
        # 验证字体设置
        try:
            # 创建一个临时图形来测试字体
            fig, ax = plt.subplots(figsize=(2, 1))
            ax.text(0.5, 0.5, '测试中文字体', fontsize=12, ha='center', va='center')
            plt.close(fig)
            
            print(f"✅ 字体配置成功: {selected_font}")
            return selected_font
            
        except Exception as e:
            warnings.warn(f"字体 {selected_font} 配置失败: {e}")
            selected_font = None
    
    # 如果所有尝试都失败，使用备用方案
    if selected_font is None:
        plt.rcParams.update({
            'font.sans-serif': ['Arial', 'DejaVu Sans', 'Liberation Sans', 'sans-serif'],
            'font.family': 'sans-serif',
            'axes.unicode_minus': False,
            'font.size': 10
        })
        
        print("⚠️  未找到合适的中文字体，将使用英文标签")
        return None
    
    return selected_font


def get_fallback_labels():
    """
    获取英文标签映射，用于没有中文字体的情况
    """
    return {
        # 基本标签
        '沙盘摄像头布局图': 'Camera Layout Plan',
        '沙盘尺寸': 'Sandbox Size',
        '摄像头数量': 'Camera Count',
        '安装高度': 'Installation Height',
        '视场角': 'Field of View',
        '覆盖范围': 'Coverage Area',
        '覆盖率': 'Coverage Rate',
        '总成本': 'Total Cost',
        '单摄像头覆盖': 'Single Camera Coverage',
        
        # 坐标轴标签
        '宽度': 'Width',
        '高度': 'Height',
        '米': 'm',
        
        # 图例标签
        '沙盘区域': 'Sandbox Area',
        '摄像头位置': 'Camera Position',
        '摄像头': 'Camera',
        
        # 3D标签
        '摄像头3D布局图': '3D Camera Layout',
        
        # 热力图标签
        '摄像头覆盖热力图': 'Camera Coverage Heatmap',
        '覆盖摄像头数量': 'Coverage Camera Count',
        
        # 对比图标签
        '成本效益': 'Cost Efficiency',
        
        # 统计标签
        '设备成本': 'Equipment Cost',
        '人工成本': 'Labor Cost',
        '性价比': 'Cost-Performance Ratio'
    }


def create_production_config():
    """
    创建生产环境的配置文件
    """
    config_content = '''# 生产环境matplotlib配置
# 解决中文显示问题

import matplotlib.pyplot as plt
import warnings

# 抑制字体警告
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')

# 基础配置
plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'savefig.facecolor': 'white',
    'savefig.bbox': 'tight',
    'savefig.dpi': 150,
    'figure.autolayout': True
})

print("matplotlib配置已加载")
'''
    
    config_file = '/Users/fangchaoning/Code/SandTable/Calculator/production_config.py'
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    return config_file


if __name__ == "__main__":
    print("🔧 配置生产环境字体...")
    font = configure_fonts_for_production()
    
    if font:
        print(f"✅ 中文字体配置完成: {font}")
    else:
        print("⚠️  将使用英文标签模式")
    
    # 创建配置文件
    config_file = create_production_config()
    print(f"📄 配置文件已创建: {config_file}")
    
    # 显示系统字体信息
    print(f"\n💻 系统: {platform.system()}")
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    chinese_fonts = [f for f in available_fonts if any(
        keyword in f.lower() for keyword in ['chinese', 'cjk', 'han', 'hei', 'song']
    )]
    print(f"📊 中文相关字体数量: {len(chinese_fonts)}")