"""
统一按钮样式 - 参考单选框的拟物化风格
简洁、轻量、凸起/凹陷效果
"""
import tkinter as tk
from theme import get_colors


class UnifiedButton(tk.Canvas):
    """
    统一风格按钮（参考单选框样式）
    - 1px细边框
    - 凸起效果
    - 按下凹陷
    - 悬停绿边框
    """
    def __init__(self, parent, text="Button", command=None,
                 style="primary", width=120, height=36, state="normal",
                 auto_width=False, **kwargs):
        self.colors = get_colors()
        self.text = text
        self.command = command
        self.style = style
        self.btn_width = width
        self.btn_height = height
        self.state_var = state
        self.is_hovered = False
        self.is_pressed = False
        
        # 如果开启 auto_width，根据文本内容动态计算宽度
        if auto_width:
            try:
                import tkinter.font as tkfont
                font = tkfont.Font(family="Microsoft YaHei UI", size=10)
                text_width = font.measure(self.text)
                # 文字宽度 + 左右内边距（大致与现有按钮风格保持一致）
                padding = 32
                self.btn_width = max(text_width + padding, 60)
            except Exception:
                # 回退到传入的宽度
                self.btn_width = width
        
        # 创建Canvas
        super().__init__(parent,
                        width=self.btn_width,
                        height=self.btn_height,
                        bg=self.colors['bg_main'],
                        highlightthickness=0, **kwargs)
        
        # 绑定事件
        if state != "disabled":
            self.bind("<Enter>", self._on_enter)
            self.bind("<Leave>", self._on_leave)
            self.bind("<Button-1>", self._on_press)
            self.bind("<ButtonRelease-1>", self._on_release)
            self.config(cursor="hand2")
        
        # 绘制按钮
        self._draw()
    
    def _draw(self):
        """绘制按钮（参考单选框风格）"""
        self.delete("all")
        
        if self.state_var == "disabled":
            self._draw_disabled()
            return
        
        if self.style == "primary":
            if self.is_pressed:
                # 按下：凹陷效果（深色内凹）
                self._draw_pressed_primary()
            else:
                # 默认/悬停：凸起效果
                self._draw_normal_primary()
        else:
            if self.is_pressed:
                # 按下：凹陷
                self._draw_pressed_secondary()
            else:
                # 默认/悬停：凸起
                self._draw_normal_secondary()
    
    def _draw_normal_primary(self):
        """绘制正常/悬停状态的主按钮（凸起）"""
        is_dark = self.colors.get('is_dark', True)
        
        if is_dark:
            # 深色模式
            border_color = '#1a1a1a'
            if self.is_hovered:
                bg_color = '#2c2c2c'
                text_color = self.colors['primary']
                highlight_color = '#3a3a3a'
            else:
                bg_color = '#2a2a2a'
                text_color = self.colors['text_primary']
                highlight_color = '#3a3a3a'
        else:
            # 浅色模式
            border_color = '#d0d0d0'
            if self.is_hovered:
                bg_color = '#e8e8e8'
                text_color = self.colors['primary_dark']
                highlight_color = '#f5f5f5'
            else:
                bg_color = '#f0f0f0'
                text_color = self.colors['text_primary']
                highlight_color = '#f8f8f8'
        
        # 外边框
        self.create_rectangle(0, 0, self.btn_width, self.btn_height, fill=border_color, outline="")
        
        # 主体
        self.create_rectangle(1, 1, self.btn_width-1, self.btn_height-1, fill=bg_color, outline="")
        
        # 顶部高光
        self.create_line(3, 2, self.btn_width-3, 2, fill=highlight_color, width=1)
        
        # 文本
        self.create_text(
            self.btn_width//2, self.btn_height//2,
            text=self.text,
            fill=text_color,
            font=("Microsoft YaHei UI", 10)
        )
    
    def _draw_pressed_primary(self):
        """绘制按下状态的主按钮（略暗，不凹陷）"""
        is_dark = self.colors.get('is_dark', True)
        
        if is_dark:
            # 深色模式：略暗
            border_color = '#1a1a1a'
            bg_color = '#252525'  # 比默认略暗
            highlight_color = '#333333'
            text_color = self.colors['primary']
        else:
            # 浅色模式：略暗
            border_color = '#d0d0d0'
            bg_color = '#e0e0e0'  # 比默认略暗
            highlight_color = '#eeeeee'
            text_color = self.colors['primary_dark']
        
        # 外边框
        self.create_rectangle(0, 0, self.btn_width, self.btn_height, fill=border_color, outline="")
        
        # 主体（略暗，但保持凸起）
        self.create_rectangle(1, 1, self.btn_width-1, self.btn_height-1, fill=bg_color, outline="")
        
        # 顶部高光（保留凸起效果）
        self.create_line(3, 2, self.btn_width-3, 2, fill=highlight_color, width=1)
        
        # 文本（绿色）
        self.create_text(
            self.btn_width//2, self.btn_height//2,
            text=self.text,
            fill=text_color,
            font=("Microsoft YaHei UI", 10)
        )
    
    def _draw_normal_secondary(self):
        """绘制正常/悬停状态的次按钮（凸起）"""
        is_dark = self.colors.get('is_dark', True)
        
        if is_dark:
            # 深色模式
            border_color = '#1a1a1a'
            if self.is_hovered:
                bg_color = '#2c2c2c'
                text_color = self.colors['primary']
                highlight_color = '#3a3a3a'
            else:
                bg_color = '#2a2a2a'
                text_color = self.colors['text_primary']
                highlight_color = '#3a3a3a'
        else:
            # 浅色模式
            border_color = '#d0d0d0'
            if self.is_hovered:
                bg_color = '#e8e8e8'
                text_color = self.colors['primary_dark']
                highlight_color = '#f5f5f5'
            else:
                bg_color = '#f0f0f0'
                text_color = self.colors['text_primary']
                highlight_color = '#f8f8f8'
        
        # 外边框
        self.create_rectangle(0, 0, self.btn_width, self.btn_height, fill=border_color, outline="")
        
        # 主体
        self.create_rectangle(1, 1, self.btn_width-1, self.btn_height-1, fill=bg_color, outline="")
        
        # 顶部高光
        self.create_line(3, 2, self.btn_width-3, 2, fill=highlight_color, width=1)
        
        # 文本
        self.create_text(
            self.btn_width//2, self.btn_height//2,
            text=self.text,
            fill=text_color,
            font=("Microsoft YaHei UI", 10)
        )
    
    def _draw_pressed_secondary(self):
        """绘制按下状态的次按钮（略暗，不凹陷）"""
        is_dark = self.colors.get('is_dark', True)
        
        if is_dark:
            # 深色模式：略暗
            border_color = '#1a1a1a'
            bg_color = '#252525'  # 比默认略暗
            highlight_color = '#333333'
            text_color = self.colors['primary']
        else:
            # 浅色模式：略暗
            border_color = '#d0d0d0'
            bg_color = '#e0e0e0'  # 比默认略暗
            highlight_color = '#eeeeee'
            text_color = self.colors['primary_dark']
        
        # 外边框
        self.create_rectangle(0, 0, self.btn_width, self.btn_height, fill=border_color, outline="")
        
        # 主体（略暗，保持凸起）
        self.create_rectangle(1, 1, self.btn_width-1, self.btn_height-1, fill=bg_color, outline="")
        
        # 顶部高光（保留凸起效果）
        self.create_line(3, 2, self.btn_width-3, 2, fill=highlight_color, width=1)
        
        # 文本（绿色）
        self.create_text(
            self.btn_width//2, self.btn_height//2,
            text=self.text,
            fill=text_color,
            font=("Microsoft YaHei UI", 10)
        )
    
    def _draw_disabled(self):
        """绘制禁用状态"""
        is_dark = self.colors.get('is_dark', True)
        
        if is_dark:
            # 深色模式
            border_color = '#1a1a1a'
            bg_color = '#222222'
        else:
            # 浅色模式
            border_color = '#d0d0d0'
            bg_color = '#e8e8e8'
        
        # 边框
        self.create_rectangle(0, 0, self.btn_width, self.btn_height, fill=border_color, outline="")
        
        # 内部
        self.create_rectangle(1, 1, self.btn_width-1, self.btn_height-1, fill=bg_color, outline="")
        
        # 文本
        self.create_text(
            self.btn_width//2, self.btn_height//2,
            text=self.text,
            fill=self.colors['text_disabled'],
            font=("Microsoft YaHei UI", 10)
        )
    
    def _on_enter(self, event):
        if self.state_var != "disabled":
            self.is_hovered = True
            self._draw()
    
    def _on_leave(self, event):
        if self.state_var != "disabled":
            self.is_hovered = False
            self.is_pressed = False
            self._draw()
    
    def _on_press(self, event):
        if self.state_var != "disabled":
            self.is_pressed = True
            self._draw()
    
    def _on_release(self, event):
        if self.state_var != "disabled":
            self.is_pressed = False
            self._draw()
            if self.command and self.is_hovered:
                self.command()
    
    def config_state(self, state):
        """更新按钮状态"""
        old_state = self.state_var
        self.state_var = state
        
        if state == "disabled":
            # 禁用状态：解绑事件
            self.unbind("<Enter>")
            self.unbind("<Leave>")
            self.unbind("<Button-1>")
            self.unbind("<ButtonRelease-1>")
            self.config(cursor="arrow")
        else:
            # 正常状态：绑定事件（如果之前是禁用状态）
            if old_state == "disabled":
                self.bind("<Enter>", self._on_enter)
                self.bind("<Leave>", self._on_leave)
                self.bind("<Button-1>", self._on_press)
                self.bind("<ButtonRelease-1>", self._on_release)
            self.config(cursor="hand2")
        
        self._draw()


# 测试
if __name__ == "__main__":
    root = tk.Tk()
    root.title("统一按钮样式测试")
    root.geometry("600x300")
    colors = get_colors()
    root.configure(bg=colors['bg_main'])
    
    title = tk.Label(root, text="统一按钮样式（参考单选框）", 
                     font=("Microsoft YaHei UI", 18, "bold"),
                     bg=colors['bg_main'], fg=colors['text_primary'])
    title.pack(pady=20)
    
    frame = tk.Frame(root, bg=colors['bg_main'])
    frame.pack(pady=20)
    
    btn1 = UnifiedButton(frame, text="选择 Excel 文件", style="primary", width=150, height=40)
    btn1.pack(side=tk.LEFT, padx=10)
    
    btn2 = UnifiedButton(frame, text="开始处理", style="primary", width=120, height=40)
    btn2.pack(side=tk.LEFT, padx=10)
    
    btn3 = UnifiedButton(frame, text="清除", style="secondary", width=90, height=40)
    btn3.pack(side=tk.LEFT, padx=10)
    
    btn4 = UnifiedButton(frame, text="禁用", style="primary", width=100, height=40, state="disabled")
    btn4.pack(side=tk.LEFT, padx=10)
    
    root.mainloop()

