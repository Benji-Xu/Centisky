"""
Razer风格主题管理模块
支持深色/浅色模式，跟随系统主题
"""
import os
import sys


def detect_system_dark_mode():
    """检测系统是否使用深色模式"""
    if sys.platform == "win32":
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            # 0 = 深色模式, 1 = 浅色模式
            return value == 0
        except Exception:
            # 默认使用深色模式
            return True
    else:
        # 其他系统默认深色模式
        return True


class RazerTheme:
    """Razer风格主题配色方案"""
    
    # Razer绿色系
    RAZER_GREEN = '#44d62c'           # Razer标准绿
    RAZER_GREEN_HOVER = '#5ae639'     # 绿色悬停
    RAZER_GREEN_LIGHT = '#88ff77'     # 绿色淡色
    RAZER_GREEN_DARK = '#2fb81b'      # 绿色深色
    RAZER_GREEN_PALE = '#e8ffe5'      # 绿色极淡（浅色模式背景）
    
    # iOS 18风格蓝色系
    IOS_BLUE = '#007AFF'              # iOS标准蓝
    IOS_BLUE_LIGHT = '#5AC8FA'        # iOS浅蓝
    IOS_BLUE_PALE = '#E8F4FF'         # iOS极淡蓝（浅色模式背景）
    
    def __init__(self, dark_mode=None):
        """
        初始化主题
        :param dark_mode: True=深色模式, False=浅色模式, None=自动检测
        """
        if dark_mode is None:
            dark_mode = detect_system_dark_mode()
        
        self.is_dark = dark_mode
        
        if dark_mode:
            self.colors = self._dark_theme()
        else:
            self.colors = self._light_theme()
    
    def _dark_theme(self):
        """深色模式配色 - iOS 18风格：黑灰为主，蓝为辅"""
        return {
            # 主题标识
            'is_dark': True,
            # 主色调 - iOS蓝（辅助色，用于强调）
            'primary': self.IOS_BLUE,               # iOS蓝
            'primary_hover': self.IOS_BLUE_LIGHT,  # 蓝色悬停
            'primary_light': self.IOS_BLUE_LIGHT,  # 蓝色淡色
            'primary_dark': '#0051CC',              # 蓝色深色
            'primary_glow': '#007AFF80',            # 蓝色发光（半透明）
            
            # 辅助色
            'secondary': '#888888',                 # 中灰色
            'success': '#44d62c',                   # 成功绿
            'danger': '#ff3860',                    # 危险红
            'warning': '#ffaa00',                   # 警告橙
            'info': '#00c9ff',                      # 信息蓝
            
            # 背景色（黑灰为主）
            'bg_darkest': '#000000',                # 最深黑
            'bg_dark': '#0d0d0d',                   # 纯黑背景
            'bg_main': '#1a1a1a',                   # 主背景（深灰黑）
            'bg_elevated': '#222222',               # 抬高背景
            'bg_card': '#2a2a2a',                   # 卡片背景（中灰黑）
            'bg_card_hover': '#333333',             # 卡片悬停
            'bg_hover': '#252525',                  # 悬停背景
            'bg_input': '#1e1e1e',                  # 输入框背景
            
            # 渐变色（用于立体效果）
            'gradient_start': '#2a2a2a',            # 渐变起点
            'gradient_end': '#1a1a1a',              # 渐变终点
            'gradient_top': '#333333',              # 顶部高光
            'gradient_bottom': '#0d0d0d',           # 底部阴影
            
            # 文本色
            'text_primary': '#ffffff',              # 主文本（纯白）
            'text_secondary': '#b0b0b0',            # 次要文本（灰白）
            'text_tertiary': '#808080',             # 三级文本
            'text_disabled': '#4d4d4d',             # 禁用文本（深灰）
            'text_muted': '#666666',                # 淡化文本（中灰）
            'text_hint': '#555555',                 # 提示文本
            
            # 边框和分隔线
            'border_dark': '#1a1a1a',               # 深色边框
            'border_main': '#333333',               # 主边框
            'border_light': '#444444',              # 浅边框
            'border_focus': self.RAZER_GREEN,       # 聚焦边框（Razer绿）
            'divider': '#2a2a2a',                   # 分隔线
            
            # 按钮色（立体渐变效果）
            'btn_primary_bg': self.RAZER_GREEN,     # 主按钮背景（Razer绿）
            'btn_primary_bg_start': '#4de635',      # 主按钮渐变起点
            'btn_primary_bg_end': '#3bc625',        # 主按钮渐变终点
            'btn_primary_hover': self.RAZER_GREEN_HOVER, # 主按钮悬停
            'btn_primary_active': self.RAZER_GREEN_DARK, # 主按钮按下
            'btn_primary_text': '#000000',          # 主按钮文本（黑色）
            'btn_primary_shadow': '#00000080',      # 主按钮阴影
            
            'btn_secondary_bg': '#2a2a2a',          # 次按钮背景
            'btn_secondary_bg_start': '#333333',    # 次按钮渐变起点
            'btn_secondary_bg_end': '#222222',      # 次按钮渐变终点
            'btn_secondary_hover': '#383838',       # 次按钮悬停
            'btn_secondary_active': '#1a1a1a',      # 次按钮按下
            'btn_secondary_text': '#ffffff',        # 次按钮文本
            'btn_secondary_border': '#444444',      # 次按钮边框
            
            # 阴影和光效
            'shadow': '#000000',                    # 默认阴影色
            'shadow_sm': '#00000040',               # 小阴影
            'shadow_md': '#00000060',               # 中阴影
            'shadow_lg': '#00000080',               # 大阴影
            'glow_green': '#44d62c40',              # 绿色光晕
            'glow_green_strong': '#44d62c80',       # 强绿色光晕
            'highlight': '#ffffff20',               # 高光
        }
    
    def _light_theme(self):
        """浅色模式配色 - iOS 18风格：白色为主，蓝为辅"""
        return {
            # 主题标识
            'is_dark': False,
            # 主色调 - iOS蓝（辅助色，用于强调）
            'primary': self.IOS_BLUE,               # iOS蓝
            'primary_hover': '#0051CC',             # 蓝色深色
            'primary_light': self.IOS_BLUE_LIGHT,  # 蓝色淡色
            'primary_dark': '#0051CC',              # 蓝色深色
            'primary_glow': '#007AFF40',            # 蓝色发光（半透明）
            
            # 辅助色
            'secondary': '#666666',                 # 深灰色
            'success': '#2fb81b',                   # 成功绿（深色）
            'danger': '#e02b56',                    # 危险红（深色）
            'warning': '#ff9500',                   # 警告橙（深色）
            'info': '#0099cc',                      # 信息蓝（深色）
            
            # 背景色（白色为主）
            'bg_darkest': '#e0e0e0',                # 最深背景
            'bg_dark': '#f0f0f0',                   # 深背景（浅灰）
            'bg_main': '#f8f8f8',                   # 主背景
            'bg_elevated': '#ffffff',               # 抬高背景
            'bg_card': '#ffffff',                   # 卡片背景
            'bg_card_hover': '#f0f0f0',             # 卡片悬停
            'bg_hover': '#f0f0f0',                  # 悬停背景
            'bg_input': '#ffffff',                  # 输入框背景
            
            # 渐变色（用于立体效果）
            'gradient_start': '#ffffff',            # 渐变起点
            'gradient_end': '#f8f8f8',              # 渐变终点
            'gradient_top': '#ffffff',              # 顶部高光
            'gradient_bottom': '#e0e0e0',           # 底部阴影
            
            # 文本色
            'text_primary': '#1a1a1a',              # 主文本（接近黑）
            'text_secondary': '#4a4a4a',            # 次要文本（深灰）
            'text_tertiary': '#666666',             # 三级文本
            'text_disabled': '#aaaaaa',             # 禁用文本（中灰）
            'text_muted': '#888888',                # 淡化文本（浅灰）
            'text_hint': '#999999',                 # 提示文本
            
            # 边框和分隔线
            'border_dark': '#c0c0c0',               # 深色边框
            'border_main': '#d0d0d0',               # 主边框
            'border_light': '#e0e0e0',              # 浅边框
            'border_focus': self.RAZER_GREEN,       # 聚焦边框（Razer绿）
            'divider': '#e0e0e0',                   # 分隔线
            
            # 按钮色（立体渐变效果）
            'btn_primary_bg': self.RAZER_GREEN,     # 主按钮背景（Razer绿）
            'btn_primary_bg_start': '#5ae639',      # 主按钮渐变起点
            'btn_primary_bg_end': '#3bc625',        # 主按钮渐变终点
            'btn_primary_hover': self.RAZER_GREEN_DARK, # 主按钮悬停
            'btn_primary_active': '#2aa015',        # 主按钮按下
            'btn_primary_text': '#ffffff',          # 主按钮文本（白色）
            'btn_primary_shadow': '#00000020',      # 主按钮阴影
            
            'btn_secondary_bg': '#ffffff',          # 次按钮背景
            'btn_secondary_bg_start': '#ffffff',    # 次按钮渐变起点
            'btn_secondary_bg_end': '#f8f8f8',      # 次按钮渐变终点
            'btn_secondary_hover': '#f0f0f0',       # 次按钮悬停
            'btn_secondary_active': '#e8e8e8',      # 次按钮按下
            'btn_secondary_text': '#1a1a1a',        # 次按钮文本
            'btn_secondary_border': '#d0d0d0',      # 次按钮边框
            
            # 阴影和光效
            'shadow': '#d0d0d0',                    # 默认阴影色
            'shadow_sm': '#00000010',               # 小阴影
            'shadow_md': '#00000020',               # 中阴影
            'shadow_lg': '#00000030',               # 大阴影
            'glow_green': '#44d62c30',              # 绿色光晕
            'glow_green_strong': '#44d62c60',       # 强绿色光晕
            'highlight': '#ffffff80',               # 高光
        }
    
    def get_colors(self):
        """获取当前主题的配色方案"""
        return self.colors
    
    def is_dark_mode(self):
        """返回当前是否为深色模式"""
        return self.is_dark


# 全局主题实例（默认自动检测）
_global_theme = None


def get_theme(dark_mode=None):
    """
    获取全局主题实例
    :param dark_mode: True=深色模式, False=浅色模式, None=自动检测
    """
    global _global_theme
    if _global_theme is None or dark_mode is not None:
        _global_theme = RazerTheme(dark_mode)
    return _global_theme


def get_colors(dark_mode=None):
    """
    快捷获取配色方案
    :param dark_mode: True=深色模式, False=浅色模式, None=自动检测
    """
    return get_theme(dark_mode).get_colors()


# 测试代码
if __name__ == "__main__":
    print("=== 系统主题检测 ===")
    is_dark = detect_system_dark_mode()
    print(f"系统深色模式: {is_dark}")
    
    print("\n=== 深色主题配色 ===")
    theme_dark = RazerTheme(dark_mode=True)
    for key, value in theme_dark.get_colors().items():
        print(f"{key:20s}: {value}")
    
    print("\n=== 浅色主题配色 ===")
    theme_light = RazerTheme(dark_mode=False)
    for key, value in theme_light.get_colors().items():
        print(f"{key:20s}: {value}")

