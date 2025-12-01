"""
Razer风格UI组件
提供具有渐变、阴影和立体效果的自定义组件
"""
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk, ImageFilter
from theme import get_colors


class RazerButton(tk.Canvas):
    """
    Razer风格按钮 - 具有渐变和立体效果
    """
    def __init__(self, parent, text="Button", command=None, 
                 style="primary", width=120, height=40, **kwargs):
        """
        创建Razer风格按钮
        :param style: "primary" 或 "secondary"
        """
        self.colors = get_colors()
        self.text = text
        self.command = command
        self.style = style
        self.btn_width = width
        self.btn_height = height
        self.is_hovered = False
        self.is_pressed = False
        
        # 创建Canvas
        super().__init__(parent, width=width, height=height, 
                        bg=self.colors['bg_main'], 
                        highlightthickness=0, **kwargs)
        
        # 绑定事件
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        
        # 绘制按钮
        self._draw()
        
        # 设置鼠标样式
        self.config(cursor="hand2")
    
    def _draw(self):
        """绘制按钮"""
        self.delete("all")
        
        # 根据状态和样式选择颜色
        if self.style == "primary":
            if self.is_pressed:
                bg_color = self.colors['btn_primary_active']
                glow = False
            elif self.is_hovered:
                bg_color = self.colors['btn_primary_hover']
                glow = True
            else:
                bg_color = self.colors['btn_primary_bg']
                glow = False
            text_color = self.colors['btn_primary_text']
        else:  # secondary
            if self.is_pressed:
                bg_color = self.colors['btn_secondary_active']
            elif self.is_hovered:
                bg_color = self.colors['btn_secondary_hover']
            else:
                bg_color = self.colors['btn_secondary_bg']
            text_color = self.colors['btn_secondary_text']
            glow = False
        
        # 绘制外发光（仅主按钮悬停时）
        if glow:
            self.create_rectangle(
                -2, -2, self.btn_width+2, self.btn_height+2,
                fill=self.colors['glow_green'],
                outline=""
            )
        
        # 绘制阴影
        shadow_offset = 2 if not self.is_pressed else 1
        self.create_rectangle(
            shadow_offset, shadow_offset, 
            self.btn_width+shadow_offset, self.btn_height+shadow_offset,
            fill=self.colors['shadow_md'],
            outline=""
        )
        
        # 绘制按钮主体
        y_offset = 1 if self.is_pressed else 0
        self.create_rectangle(
            y_offset, y_offset, 
            self.btn_width+y_offset, self.btn_height+y_offset,
            fill=bg_color,
            outline=self.colors['border_light'] if self.style == "secondary" else ""
        )
        
        # 绘制顶部高光（模拟立体效果）
        if not self.is_pressed:
            self.create_line(
                y_offset+2, y_offset+2, 
                self.btn_width+y_offset-2, y_offset+2,
                fill=self.colors['highlight'],
                width=2
            )
        
        # 绘制文本
        self.create_text(
            self.btn_width//2 + y_offset, self.btn_height//2 + y_offset,
            text=self.text,
            fill=text_color,
            font=("Microsoft YaHei UI", 10, "bold")
        )
    
    def _on_enter(self, event):
        """鼠标进入"""
        self.is_hovered = True
        self._draw()
    
    def _on_leave(self, event):
        """鼠标离开"""
        self.is_hovered = False
        self.is_pressed = False
        self._draw()
    
    def _on_press(self, event):
        """鼠标按下"""
        self.is_pressed = True
        self._draw()
    
    def _on_release(self, event):
        """鼠标释放"""
        self.is_pressed = False
        self._draw()
        if self.command and self.is_hovered:
            self.command()
    
    def config_text(self, text):
        """更新按钮文本"""
        self.text = text
        self._draw()


class RazerCard(tk.Frame):
    """
    Razer风格卡片 - 具有阴影和边框
    """
    def __init__(self, parent, elevated=False, **kwargs):
        """
        创建Razer风格卡片
        :param elevated: 是否为抬高样式（更明显的阴影）
        """
        self.colors = get_colors()
        self.elevated = elevated
        
        # 创建外层容器（用于阴影）
        super().__init__(parent, bg=self.colors['bg_main'], **kwargs)
        
        # 创建阴影层
        self.shadow_frame = tk.Frame(
            self,
            bg=self.colors['shadow_md'] if elevated else self.colors['shadow_sm'],
        )
        self.shadow_frame.pack(padx=(2, 0), pady=(2, 0), fill=tk.BOTH, expand=True)
        
        # 创建卡片主体
        self.card_frame = tk.Frame(
            self.shadow_frame,
            bg=self.colors['bg_elevated'] if elevated else self.colors['bg_card'],
        )
        self.card_frame.pack(padx=(0, 2), pady=(0, 2), fill=tk.BOTH, expand=True)
        
        # 创建边框
        self.border_frame = tk.Frame(
            self.card_frame,
            bg=self.colors['border_main'],
        )
        self.border_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建内容区域
        self.content_frame = tk.Frame(
            self.border_frame,
            bg=self.colors['bg_elevated'] if elevated else self.colors['bg_card'],
        )
        self.content_frame.pack(padx=1, pady=1, fill=tk.BOTH, expand=True)
    
    def get_content_frame(self):
        """获取内容框架"""
        return self.content_frame


class RazerInput(tk.Frame):
    """
    Razer风格输入框 - 带边框和聚焦效果
    """
    def __init__(self, parent, placeholder="", **kwargs):
        """创建Razer风格输入框"""
        self.colors = get_colors()
        self.placeholder = placeholder
        
        # 创建外层容器
        super().__init__(parent, bg=self.colors['bg_main'])
        
        # 创建边框容器
        self.border_frame = tk.Frame(
            self,
            bg=self.colors['border_main'],
        )
        self.border_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建输入框
        self.entry = tk.Entry(
            self.border_frame,
            bg=self.colors['bg_input'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['primary'],
            relief=tk.FLAT,
            borderwidth=0,
            font=("Microsoft YaHei UI", 10),
            **kwargs
        )
        self.entry.pack(padx=1, pady=1, fill=tk.BOTH, expand=True)
        
        # 绑定聚焦事件
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        
        # 显示占位符
        if placeholder:
            self._show_placeholder()
    
    def _show_placeholder(self):
        """显示占位符"""
        self.entry.insert(0, self.placeholder)
        self.entry.config(fg=self.colors['text_hint'])
    
    def _on_focus_in(self, event):
        """获得焦点"""
        self.border_frame.config(bg=self.colors['border_focus'])
        # 清除占位符
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=self.colors['text_primary'])
    
    def _on_focus_out(self, event):
        """失去焦点"""
        self.border_frame.config(bg=self.colors['border_main'])
        # 恢复占位符
        if not self.entry.get():
            self._show_placeholder()
    
    def get(self):
        """获取输入内容"""
        value = self.entry.get()
        return "" if value == self.placeholder else value
    
    def set(self, value):
        """设置输入内容"""
        self.entry.delete(0, tk.END)
        if value:
            self.entry.insert(0, value)
            self.entry.config(fg=self.colors['text_primary'])
        else:
            self._show_placeholder()


class RazerTitle(tk.Label):
    """
    Razer风格标题 - 带绿色装饰条
    """
    def __init__(self, parent, text="", size="large", **kwargs):
        """
        创建Razer风格标题
        :param size: "large", "medium", "small"
        """
        self.colors = get_colors()
        
        # 根据大小选择字体
        font_sizes = {
            "large": 24,
            "medium": 18,
            "small": 14
        }
        font_size = font_sizes.get(size, 18)
        
        super().__init__(
            parent,
            text=text,
            font=("Microsoft YaHei UI", font_size, "bold"),
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary'],
            **kwargs
        )


def create_separator(parent, orientation="horizontal"):
    """
    创建分隔线
    :param orientation: "horizontal" 或 "vertical"
    """
    colors = get_colors()
    
    if orientation == "horizontal":
        frame = tk.Frame(parent, bg=colors['divider'], height=1)
    else:
        frame = tk.Frame(parent, bg=colors['divider'], width=1)
    
    return frame


# 测试代码
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Razer UI Components Test")
    root.geometry("600x400")
    colors = get_colors()
    root.configure(bg=colors['bg_main'])
    
    # 标题
    title = RazerTitle(root, text="Razer风格组件测试", size="large")
    title.pack(pady=20)
    
    # 按钮容器
    btn_frame = tk.Frame(root, bg=colors['bg_main'])
    btn_frame.pack(pady=20)
    
    # 主按钮
    primary_btn = RazerButton(
        btn_frame, 
        text="主要按钮", 
        command=lambda: print("Primary clicked"),
        style="primary",
        width=140,
        height=45
    )
    primary_btn.pack(side=tk.LEFT, padx=10)
    
    # 次按钮
    secondary_btn = RazerButton(
        btn_frame,
        text="次要按钮",
        command=lambda: print("Secondary clicked"),
        style="secondary",
        width=140,
        height=45
    )
    secondary_btn.pack(side=tk.LEFT, padx=10)
    
    # 卡片
    card = RazerCard(root, elevated=True)
    card.pack(padx=40, pady=20, fill=tk.BOTH, expand=True)
    
    content = card.get_content_frame()
    content.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
    
    tk.Label(
        content,
        text="这是一个Razer风格的卡片",
        font=("Microsoft YaHei UI", 12),
        bg=colors['bg_elevated'],
        fg=colors['text_primary']
    ).pack(pady=10)
    
    # 输入框
    input_widget = RazerInput(content, placeholder="输入内容...")
    input_widget.pack(fill=tk.X, padx=20, pady=10)
    
    root.mainloop()

