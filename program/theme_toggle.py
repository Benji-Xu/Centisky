"""
主题切换按钮组件
使用Emoji的太阳和月亮
"""
import tkinter as tk
from theme import get_colors


class ThemeToggleButton(tk.Label):
    """
    主题切换按钮 - Emoji日月图标
    """
    def __init__(self, parent, command=None, **kwargs):
        self.colors = get_colors()
        self.command = command
        self.is_dark = self.colors.get('is_dark', True)
        
        # 使用半圆图标
        # ◐ = 左半黑右半白（深色模式，点击变亮）
        # ◑ = 左半白右半黑（浅色模式，点击变暗）
        icon_text = "◐" if self.is_dark else "◑"
        
        # 获取父容器的背景色（自动适配）
        try:
            parent_bg = parent.cget('bg')
        except:
            parent_bg = self.colors['bg_main']
        
        super().__init__(
            parent,
            text=icon_text,
            font=("Microsoft YaHei UI", 20),  # 清晰字体
            bg=parent_bg,  # 使用父容器背景色，完美融合
            fg=self.colors['text_muted'],
            cursor="hand2",
            **kwargs
        )
        
        # 绑定事件
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
    
    def _on_enter(self, event):
        """鼠标进入"""
        self.config(fg=self.colors['primary'])
    
    def _on_leave(self, event):
        """鼠标离开"""
        self.config(fg=self.colors['text_muted'])
    
    def _on_click(self, event):
        """点击"""
        if self.command:
            self.command()


# 测试
if __name__ == "__main__":
    root = tk.Tk()
    root.title("主题切换按钮测试")
    root.geometry("300x200")
    colors = get_colors()
    root.configure(bg=colors['bg_main'])
    
    frame = tk.Frame(root, bg=colors['bg_main'])
    frame.pack(expand=True)
    
    label = tk.Label(frame, text="主题切换按钮：", font=("Microsoft YaHei UI", 12),
                     bg=colors['bg_main'], fg=colors['text_primary'])
    label.pack(side=tk.LEFT, padx=10)
    
    toggle_btn = ThemeToggleButton(frame, command=lambda: print("主题切换！"))
    toggle_btn.pack(side=tk.LEFT, padx=10)
    
    root.mainloop()

