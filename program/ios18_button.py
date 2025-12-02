"""
iOS 18风格按钮 - 扁平化圆角矩形
"""
import tkinter as tk
from theme import get_colors


class iOS18Button(tk.Frame):
    """
    iOS 18风格按钮
    - 扁平化设计
    - 圆角矩形（12px）
    - 统一内边距
    - iOS蓝色主题
    """
    def __init__(self, parent, text="Button", command=None,
                 style="primary", width=120, height=40, state="normal", **kwargs):
        super().__init__(parent, **kwargs)
        
        self.colors = get_colors()
        self.text = text
        self.command = command
        self.style = style
        self.btn_width = width
        self.btn_height = height
        self.state_var = state
        self.is_hovered = False
        
        # 设置Frame大小
        self.config(width=width, height=height, bg=self.colors['bg_main'], highlightthickness=0)
        self.pack_propagate(False)
        
        # 创建Canvas用于绘制圆角矩形
        self.canvas = tk.Canvas(
            self,
            width=width,
            height=height,
            bg=self.colors['bg_main'],
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 创建文本标签
        self.label = tk.Label(
            self,
            text=text,
            font=("Microsoft YaHei UI", 10),
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary'],
            highlightthickness=0
        )
        self.label.place(relx=0.5, rely=0.5, anchor='center')
        
        # 绑定事件
        if state != "disabled":
            self.canvas.bind("<Enter>", self._on_enter)
            self.canvas.bind("<Leave>", self._on_leave)
            self.canvas.bind("<Button-1>", self._on_press)
            self.canvas.bind("<ButtonRelease-1>", self._on_release)
            self.label.bind("<Enter>", self._on_enter)
            self.label.bind("<Leave>", self._on_leave)
            self.label.bind("<Button-1>", self._on_press)
            self.label.bind("<ButtonRelease-1>", self._on_release)
            self.canvas.config(cursor="hand2")
            self.label.config(cursor="hand2")
        
        self._draw()
    
    def _draw(self):
        """绘制按钮"""
        self.canvas.delete("all")
        
        if self.state_var == "disabled":
            self._draw_disabled()
        elif self.style == "primary":
            self._draw_primary()
        else:
            self._draw_secondary()
    
    def _draw_primary(self):
        """绘制主按钮（iOS蓝色）"""
        is_dark = self.colors.get('is_dark', True)
        
        if self.is_hovered:
            if is_dark:
                bg_color = '#0051CC'  # 深蓝
            else:
                bg_color = '#0051CC'  # 深蓝
        else:
            if is_dark:
                bg_color = '#007AFF'  # iOS蓝
            else:
                bg_color = '#007AFF'  # iOS蓝
        
        # 绘制圆角矩形
        self._draw_rounded_rect(bg_color)
        
        # 更新标签颜色
        self.label.config(fg='white')
    
    def _draw_secondary(self):
        """绘制次按钮（灰色）"""
        is_dark = self.colors.get('is_dark', True)
        
        if self.is_hovered:
            if is_dark:
                bg_color = '#3a3a3a'
            else:
                bg_color = '#e8e8e8'
        else:
            if is_dark:
                bg_color = '#333333'
            else:
                bg_color = '#f0f0f0'
        
        # 绘制圆角矩形
        self._draw_rounded_rect(bg_color)
        
        # 更新标签颜色
        if is_dark:
            self.label.config(fg=self.colors['text_primary'])
        else:
            self.label.config(fg=self.colors['text_primary'])
    
    def _draw_disabled(self):
        """绘制禁用状态"""
        is_dark = self.colors.get('is_dark', True)
        
        if is_dark:
            bg_color = '#2a2a2a'
        else:
            bg_color = '#e8e8e8'
        
        self._draw_rounded_rect(bg_color)
        self.label.config(fg=self.colors['text_disabled'])
    
    def _draw_rounded_rect(self, color):
        """绘制圆角矩形"""
        radius = 12
        
        # 绘制圆角矩形（使用多个弧线和线段）
        self.canvas.create_arc(
            0, 0, radius*2, radius*2,
            start=90, extent=90, fill=color, outline=color
        )
        self.canvas.create_arc(
            self.btn_width - radius*2, 0, self.btn_width, radius*2,
            start=0, extent=90, fill=color, outline=color
        )
        self.canvas.create_arc(
            self.btn_width - radius*2, self.btn_height - radius*2, self.btn_width, self.btn_height,
            start=270, extent=90, fill=color, outline=color
        )
        self.canvas.create_arc(
            0, self.btn_height - radius*2, radius*2, self.btn_height,
            start=180, extent=90, fill=color, outline=color
        )
        
        # 绘制矩形中间部分
        self.canvas.create_rectangle(
            radius, 0, self.btn_width - radius, self.btn_height,
            fill=color, outline=color
        )
        self.canvas.create_rectangle(
            0, radius, self.btn_width, self.btn_height - radius,
            fill=color, outline=color
        )
    
    def _on_enter(self, event):
        """鼠标进入"""
        if self.state_var != "disabled":
            self.is_hovered = True
            self._draw()
    
    def _on_leave(self, event):
        """鼠标离开"""
        if self.state_var != "disabled":
            self.is_hovered = False
            self._draw()
    
    def _on_press(self, event):
        """按钮按下"""
        if self.state_var != "disabled" and self.command:
            self.command()
    
    def _on_release(self, event):
        """按钮释放"""
        pass
    
    def config_state(self, state):
        """配置按钮状态"""
        self.state_var = state
        self._draw()
