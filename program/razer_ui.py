"""
Razer风格拟物化UI组件
黑色为主，绿色为辅，立体真实的按键效果
"""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk
from theme import get_colors


class Razer3DButton(tk.Canvas):
    """
    Razer拟物化3D按钮
    - 多层阴影营造深度
    - 渐变模拟光泽
    - 内高光/外阴影
    - 按压下沉效果
    """
    def __init__(self, parent, text="Button", command=None, 
                 style="primary", width=140, height=45, state="normal", **kwargs):
        self.colors = get_colors()
        self.text = text
        self.command = command
        self.style = style
        self.btn_width = width
        self.btn_height = height
        self.state_var = state
        self.is_hovered = False
        self.is_pressed = False
        
        # 创建Canvas（仅留少量阴影空间）
        super().__init__(parent, width=width+2, height=height+4, 
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
        """绘制机械键盘风格按钮（精致、圆润、微妙）"""
        self.delete("all")
        
        base_x, base_y = 1, 1
        
        if self.state_var == "disabled":
            self._draw_disabled(base_x, base_y)
            return
        
        # 按下时轻微下沉
        if self.is_pressed:
            offset_y = 1
        else:
            offset_y = 0
        
        # 1. 底部阴影（非常细微，1px）
        if not self.is_pressed:
            self.create_rectangle(
                base_x, base_y + self.btn_height + 1,
                base_x + self.btn_width, base_y + self.btn_height + 2,
                fill='#0d0d0d',
                outline=""
            )
        
        # 2. 绘制按钮主体（带圆角效果的矩形）
        btn_y = base_y + offset_y
        
        if self.style == "primary":
            # Razer绿色按钮
            if self.is_pressed:
                # 按下：略暗
                fill_color = '#3ed62a'
            elif self.is_hovered:
                # 悬停：略亮并加绿边框
                fill_color = '#48e030'
            else:
                # 默认：标准Razer绿
                fill_color = '#44d62c'
            
            text_color = '#000000'
            border_color = self.colors['primary'] if self.is_hovered else '#38c023'
        else:
            # 灰色按钮
            if self.is_pressed:
                fill_color = '#252525'
            elif self.is_hovered:
                fill_color = '#333333'
            else:
                fill_color = '#2a2a2a'
            
            text_color = '#e0e0e0'
            border_color = '#202020'
        
        # 绘制外边框（1px）
        self.create_rectangle(
            base_x, btn_y,
            base_x + self.btn_width, btn_y + self.btn_height,
            fill=border_color,
            outline=""
        )
        
        # 3. 绘制按钮内部（机械键盘风格：微妙渐变）
        inner_margin = 1  # 细边框只需1px
        if self.style == "primary":
            # Razer绿色微妙渐变（机械键盘风格）
            if self.is_pressed:
                # 按下时略暗
                color_top = '#40d028'
                color_bottom = '#44d62c'
            elif self.is_hovered:
                # 悬停时略亮
                color_top = '#4ee636'
                color_bottom = '#44d62c'
            else:
                # 默认：轻微渐变（15%对比度）
                color_top = '#4ae633'  # 略亮绿（顶部）
                color_bottom = '#42d029'  # 略暗绿（底部）
            
            # 绘制渐变
            self._draw_gradient(
                base_x + inner_margin, btn_y + inner_margin,
                self.btn_width - inner_margin*2, self.btn_height - inner_margin*2,
                color_top, color_bottom
            )
            text_color = '#0d0d0d'  # 深灰文字（不是纯黑，避免太重）
        else:
            # 灰色微妙渐变（机械键盘风格）
            if self.is_pressed:
                # 按下时略暗
                color_top = '#262626'
                color_bottom = '#2a2a2a'
            elif self.is_hovered:
                # 悬停时略亮
                color_top = '#323232'
                color_bottom = '#2a2a2a'
            else:
                # 默认：轻微渐变（15%对比度）
                color_top = '#2e2e2e'  # 略亮灰（顶部）
                color_bottom = '#282828'  # 略暗灰（底部）
            
            self._draw_gradient(
                base_x + inner_margin, btn_y + inner_margin,
                self.btn_width - inner_margin*2, self.btn_height - inner_margin*2,
                color_top, color_bottom
            )
            text_color = '#d0d0d0'  # 浅灰文字
        
        # 4. 绘制顶部高光（机械键盘风格：微妙高光）
        if not self.is_pressed:
            highlight_height = self.btn_height // 3  # 减小高光区域
            # 使用微妙的高光（机械键盘效果）
            for i in range(highlight_height):
                ratio = 1 - i/highlight_height
                if self.style == "primary":
                    # 绿色按钮的微妙白色高光
                    brightness = int(255 * ratio * 0.15)  # 降低亮度
                    r = min(255, int(color_top[1:3], 16) + brightness)
                    g = min(255, int(color_top[3:5], 16) + brightness)
                    b = min(255, int(color_top[5:7], 16) + brightness)
                else:
                    # 灰色按钮的微妙白色高光
                    brightness = int(255 * ratio * 0.2)  # 降低亮度
                    base = int(color_top[1:3], 16)
                    r = g = b = min(255, base + brightness)
                
                highlight_color = f'#{r:02x}{g:02x}{b:02x}'
                y = btn_y + inner_margin + i
                self.create_line(
                    base_x + inner_margin + 6, y,
                    base_x + self.btn_width - inner_margin - 6, y,
                    fill=highlight_color,
                    width=1
                )
        
        # 5. 绘制底部阴影渐变（按下时凹陷效果）
        if self.is_pressed:
            shadow_height = 3
            # 使用实色渐变模拟内阴影
            shadow_colors_inner = ['#1a1a1a', '#222222', '#2a2a2a']  # 更轻的内阴影
            for i in range(shadow_height):
                y = btn_y + inner_margin + i
                self.create_line(
                    base_x + inner_margin + 6, y,
                    base_x + self.btn_width - inner_margin - 6, y,
                    fill=shadow_colors_inner[i],
                    width=1
                )
        
        # 6. 绘制文本（无阴影，干净清晰）
        text_y = base_y + self.btn_height//2 + offset_y
        text_x = base_x + self.btn_width//2
        
        # 直接绘制文本，不加阴影（避免残影）
        self.create_text(
            text_x, text_y,
            text=self.text,
            fill=text_color,
            font=("Microsoft YaHei UI", 10)  # 正常字重
        )
    
    def _draw_gradient(self, x, y, width, height, color_top, color_bottom):
        """绘制垂直渐变（确保完全撑满）"""
        # 解析颜色
        r1, g1, b1 = int(color_top[1:3], 16), int(color_top[3:5], 16), int(color_top[5:7], 16)
        r2, g2, b2 = int(color_bottom[1:3], 16), int(color_bottom[3:5], 16), int(color_bottom[5:7], 16)
        
        # 先填充整个区域为底色
        self.create_rectangle(
            x, y, x + width, y + height,
            fill=color_bottom,
            outline=""
        )
        
        # 绘制渐变条（从顶部到底部，完全撑满）
        steps = int(height)
        for i in range(steps):
            ratio = i / (steps - 1) if steps > 1 else 0
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            
            # 绘制完整宽度的矩形（确保左右两侧也有渐变）
            self.create_rectangle(
                x, y + i,
                x + width, y + i + 1,
                fill=color,
                outline=""
            )
    
    def _draw_disabled(self, base_x, base_y):
        """绘制禁用状态"""
        # 灰色边框
        self.create_rectangle(
            base_x, base_y,
            base_x + self.btn_width, base_y + self.btn_height,
            fill='#1a1a1a',
            outline=""
        )
        
        # 内部
        inner_margin = 2
        self.create_rectangle(
            base_x + inner_margin, base_y + inner_margin,
            base_x + self.btn_width - inner_margin, base_y + self.btn_height - inner_margin,
            fill='#2a2a2a',
            outline=""
        )
        
        # 文本
        self.create_text(
            base_x + self.btn_width//2, base_y + self.btn_height//2,
            text=self.text,
            fill=self.colors['text_disabled'],
            font=("Microsoft YaHei UI", 10)  # 正常字重
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
            self.is_pressed = False
            self._draw()
    
    def _on_press(self, event):
        """鼠标按下"""
        if self.state_var != "disabled":
            self.is_pressed = True
            self._draw()
    
    def _on_release(self, event):
        """鼠标释放"""
        if self.state_var != "disabled":
            self.is_pressed = False
            self._draw()
            if self.command and self.is_hovered:
                self.command()
    
    def config_state(self, state):
        """更新按钮状态"""
        self.state_var = state
        if state == "disabled":
            self.config(cursor="arrow")
        else:
            self.config(cursor="hand2")
        self._draw()


class Razer3DCard(tk.Frame):
    """
    Razer简约卡片（扁平化，细边框）
    - 1px细边框
    - 微妙阴影
    - 简洁现代
    - 适配深色/浅色模式
    """
    def __init__(self, parent, **kwargs):
        self.colors = get_colors()
        is_dark = self.colors.get('is_dark', True)
        
        # 创建外层容器
        super().__init__(parent, bg=self.colors['bg_main'], **kwargs)
        
        # 底部阴影（1px）
        shadow_color = '#0d0d0d' if is_dark else '#e0e0e0'
        self.shadow_outer = tk.Frame(self, bg=shadow_color)
        self.shadow_outer.pack(padx=(0, 1), pady=(0, 1), fill=tk.BOTH, expand=True)
        
        # 细边框（根据主题选择颜色）
        border_color = '#333333' if is_dark else '#d0d0d0'
        self.border_dark = tk.Frame(self.shadow_outer, bg=border_color)
        self.border_dark.pack(fill=tk.BOTH, expand=True)
        
        # 卡片主体
        self.card_body = tk.Frame(self.border_dark, bg=self.colors['bg_card'])
        self.card_body.pack(padx=1, pady=1, fill=tk.BOTH, expand=True)
        
        # 内容区域
        self.content_frame = tk.Frame(self.card_body, bg=self.colors['bg_card'])
        self.content_frame.pack(fill=tk.BOTH, expand=True)
    
    def get_content(self):
        """获取内容区域"""
        return self.content_frame


class Razer3DInput(tk.Frame):
    """
    Razer拟物化输入框
    - 内凹效果
    - 聚焦绿色发光
    """
    def __init__(self, parent, textvariable=None, width=20, **kwargs):
        self.colors = get_colors()
        self.is_focused = False
        
        super().__init__(parent, bg=self.colors['bg_main'])
        
        # 外边框（深色）
        self.outer_border = tk.Frame(self, bg='#0d0d0d')
        self.outer_border.pack(fill=tk.BOTH, expand=True)
        
        # 内边框（可变色，聚焦时变绿）
        self.inner_border = tk.Frame(self.outer_border, bg='#1a1a1a')
        self.inner_border.pack(padx=1, pady=1, fill=tk.BOTH, expand=True)
        
        # 输入框主体
        self.entry = tk.Entry(
            self.inner_border,
            textvariable=textvariable,
            width=width,
            bg=self.colors['bg_input'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['primary'],
            relief=tk.FLAT,
            borderwidth=0,
            font=("Microsoft YaHei UI", 10),
            **kwargs
        )
        self.entry.pack(padx=2, pady=2, fill=tk.BOTH, expand=True)
        
        # 绑定聚焦事件
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
    
    def _on_focus_in(self, event):
        """获得焦点 - 绿色发光"""
        self.is_focused = True
        self.outer_border.config(bg=self.colors['primary'])
        self.inner_border.config(bg=self.colors['primary_dark'])
    
    def _on_focus_out(self, event):
        """失去焦点"""
        self.is_focused = False
        self.outer_border.config(bg='#0d0d0d')
        self.inner_border.config(bg='#1a1a1a')


class Razer3DRadio(tk.Frame):
    """
    Razer拟物化单选框
    - 3D凸起效果（未选中）
    - 3D凹陷效果（选中）
    - 绿色发光
    """
    def __init__(self, parent, text, variable, value, **kwargs):
        self.colors = get_colors()
        self.text = text
        self.variable = variable
        self.value = value
        self.is_hovered = False
        
        super().__init__(parent, bg=self.colors['bg_main'], cursor="hand2", **kwargs)
        
        # 创建Canvas绘制3D效果
        self.canvas = tk.Canvas(
            self,
            width=100,
            height=32,
            bg=self.colors['bg_main'],
            highlightthickness=0
        )
        self.canvas.pack()
        
        # 绑定事件
        self.canvas.bind("<Button-1>", lambda e: variable.set(value))
        self.canvas.bind("<Enter>", self._on_enter)
        self.canvas.bind("<Leave>", self._on_leave)
        
        # 监听变量变化
        variable.trace_add("write", lambda *args: self._draw())
        
        # 初始绘制
        self._draw()
    
    def _draw(self):
        """绘制3D单选框（适配深色/浅色模式）"""
        self.canvas.delete("all")
        
        is_selected = (self.variable.get() == self.value)
        is_dark = self.colors.get('is_dark', True)
        
        # 计算文本宽度以调整Canvas大小
        temp_text = self.canvas.create_text(0, 0, text=self.text, font=("Microsoft YaHei UI", 9))
        bbox = self.canvas.bbox(temp_text)
        text_width = bbox[2] - bbox[0] if bbox else 60
        self.canvas.delete(temp_text)
        
        total_width = text_width + 24
        self.canvas.config(width=total_width)
        
        if is_selected:
            # 选中：略亮显示 + Razer绿色（不凹陷）
            if is_dark:
                # 深色模式
                border_color = self.colors['primary']
                bg_color = '#2c2c2c'  # 略亮的背景
                highlight_color = '#3a3a3a'
                text_color = self.colors['primary']
            else:
                # 浅色模式
                border_color = self.colors['primary_dark']
                bg_color = '#e8e8e8'  # 略亮的背景
                highlight_color = '#f5f5f5'
                text_color = self.colors['primary_dark']
            
            # 外边框（绿色）
            self.canvas.create_rectangle(0, 0, total_width, 32, fill=border_color, outline="")
            
            # 主体（略亮，保持凸起）
            self.canvas.create_rectangle(1, 1, total_width-1, 31, fill=bg_color, outline="")
            
            # 顶部高光（保持凸起效果）
            self.canvas.create_line(3, 2, total_width-3, 2, fill=highlight_color, width=1)
        else:
            # 未选中：凸起效果
            if is_dark:
                # 深色模式
                if self.is_hovered:
                    border_color = self.colors['primary_dark']
                    bg_color = '#2a2a2a'
                    highlight_color = '#444444'
                    text_color = self.colors['primary_light']
                else:
                    border_color = '#1a1a1a'
                    bg_color = '#2a2a2a'
                    highlight_color = '#3a3a3a'
                    text_color = self.colors['text_primary']
            else:
                # 浅色模式
                if self.is_hovered:
                    border_color = '#c0c0c0'
                    bg_color = '#e8e8e8'
                    highlight_color = '#f5f5f5'
                    text_color = self.colors['primary_dark']
                else:
                    border_color = '#d0d0d0'
                    bg_color = '#f0f0f0'
                    highlight_color = '#f8f8f8'
                    text_color = self.colors['text_primary']
            
            # 外边框
            self.canvas.create_rectangle(0, 0, total_width, 32, fill=border_color, outline="")
            
            # 主体
            self.canvas.create_rectangle(1, 1, total_width-1, 31, fill=bg_color, outline="")
            
            # 顶部高光
            self.canvas.create_line(3, 2, total_width-3, 2, fill=highlight_color, width=1)
        
        # 绘制文本
        self.canvas.create_text(
            total_width//2, 16,
            text=self.text,
            fill=text_color,
            font=("Microsoft YaHei UI", 9)
        )
    
    def _on_enter(self, event):
        self.is_hovered = True
        self._draw()
    
    def _on_leave(self, event):
        self.is_hovered = False
        self._draw()


class Razer3DCheckbox(tk.Frame):
    """
    Razer拟物化复选框
    - 3D开关效果
    """
    def __init__(self, parent, text, variable, **kwargs):
        self.colors = get_colors()
        self.text = text
        self.variable = variable
        self.is_hovered = False
        
        super().__init__(parent, bg=self.colors['bg_main'], cursor="hand2", **kwargs)
        
        # 创建Canvas
        self.canvas = tk.Canvas(
            self,
            width=100,
            height=32,
            bg=self.colors['bg_main'],
            highlightthickness=0
        )
        self.canvas.pack()
        
        # 绑定事件
        self.canvas.bind("<Button-1>", lambda e: variable.set(not variable.get()))
        self.canvas.bind("<Enter>", self._on_enter)
        self.canvas.bind("<Leave>", self._on_leave)
        
        # 监听变量变化
        variable.trace_add("write", lambda *args: self._draw())
        
        # 初始绘制
        self._draw()
    
    def _draw(self):
        """绘制3D复选框（适配深色/浅色模式）"""
        self.canvas.delete("all")
        
        is_checked = self.variable.get()
        is_dark = self.colors.get('is_dark', True)
        
        # 计算文本宽度
        temp_text = self.canvas.create_text(0, 0, text=self.text, font=("Microsoft YaHei UI", 9))
        bbox = self.canvas.bbox(temp_text)
        text_width = bbox[2] - bbox[0] if bbox else 60
        self.canvas.delete(temp_text)
        
        total_width = text_width + 24
        self.canvas.config(width=total_width)
        
        # 绘制方式同单选框（不凹陷）
        if is_checked:
            # 选中：略亮显示 + 绿色（不凹陷）
            if is_dark:
                border_color = self.colors['primary']
                bg_color = '#2c2c2c'
                highlight_color = '#3a3a3a'
                text_color = self.colors['primary']
            else:
                border_color = self.colors['primary_dark']
                bg_color = '#e8e8e8'
                highlight_color = '#f5f5f5'
                text_color = self.colors['primary_dark']
            
            # 外边框（绿色）
            self.canvas.create_rectangle(0, 0, total_width, 32, fill=border_color, outline="")
            
            # 主体（略亮，保持凸起）
            self.canvas.create_rectangle(1, 1, total_width-1, 31, fill=bg_color, outline="")
            
            # 顶部高光（保持凸起）
            self.canvas.create_line(3, 2, total_width-3, 2, fill=highlight_color, width=1)
        else:
            # 未选中：凸起
            if is_dark:
                if self.is_hovered:
                    border_color = self.colors['primary_dark']
                    bg_color = '#2a2a2a'
                    highlight_color = '#444444'
                    text_color = self.colors['primary_light']
                else:
                    border_color = '#1a1a1a'
                    bg_color = '#2a2a2a'
                    highlight_color = '#3a3a3a'
                    text_color = self.colors['text_primary']
            else:
                if self.is_hovered:
                    border_color = '#c0c0c0'
                    bg_color = '#e8e8e8'
                    highlight_color = '#f5f5f5'
                    text_color = self.colors['primary_dark']
                else:
                    border_color = '#d0d0d0'
                    bg_color = '#f0f0f0'
                    highlight_color = '#f8f8f8'
                    text_color = self.colors['text_primary']
            
            self.canvas.create_rectangle(0, 0, total_width, 32, fill=border_color, outline="")
            self.canvas.create_rectangle(1, 1, total_width-1, 31, fill=bg_color, outline="")
            self.canvas.create_line(3, 2, total_width-3, 2, fill=highlight_color, width=1)
        
        # 文本
        self.canvas.create_text(total_width//2, 16, text=self.text, fill=text_color, font=("Microsoft YaHei UI", 9))
    
    def _on_enter(self, event):
        self.is_hovered = True
        self._draw()
    
    def _on_leave(self, event):
        self.is_hovered = False
        self._draw()


# 测试代码
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Razer 拟物化UI测试")
    root.geometry("700x500")
    colors = get_colors()
    root.configure(bg=colors['bg_main'])
    
    # 标题
    title = tk.Label(
        root,
        text="Razer拟物化UI组件",
        font=("Microsoft YaHei UI", 24, "bold"),
        bg=colors['bg_main'],
        fg=colors['text_primary']
    )
    title.pack(pady=20)
    
    # 按钮测试
    btn_frame = tk.Frame(root, bg=colors['bg_main'])
    btn_frame.pack(pady=20)
    
    # 主按钮
    primary_btn = Razer3DButton(
        btn_frame,
        text="开始处理",
        command=lambda: print("Primary clicked"),
        style="primary",
        width=140,
        height=45
    )
    primary_btn.pack(side=tk.LEFT, padx=15)
    
    # 次按钮
    secondary_btn = Razer3DButton(
        btn_frame,
        text="取消",
        command=lambda: print("Secondary clicked"),
        style="secondary",
        width=140,
        height=45
    )
    secondary_btn.pack(side=tk.LEFT, padx=15)
    
    # 禁用按钮
    disabled_btn = Razer3DButton(
        btn_frame,
        text="禁用按钮",
        style="primary",
        width=140,
        height=45,
        state="disabled"
    )
    disabled_btn.pack(side=tk.LEFT, padx=15)
    
    # 卡片测试
    card = Razer3DCard(root)
    card.pack(padx=40, pady=20, fill=tk.BOTH, expand=True)
    
    content = card.get_content()
    
    tk.Label(
        content,
        text="这是一个Razer拟物化卡片",
        font=("Microsoft YaHei UI", 14, "bold"),
        bg=colors['bg_card'],
        fg=colors['text_primary']
    ).pack(pady=(20, 10), padx=20)
    
    # 单选框测试
    radio_frame = tk.Frame(content, bg=colors['bg_card'])
    radio_frame.pack(pady=10, padx=20)
    
    tk.Label(
        radio_frame,
        text="选择类型：",
        font=("Microsoft YaHei UI", 10),
        bg=colors['bg_card'],
        fg=colors['text_primary']
    ).pack(side=tk.LEFT, padx=(0, 10))
    
    radio_var = tk.StringVar(value="option1")
    
    Razer3DRadio(radio_frame, "选项一", radio_var, "option1").pack(side=tk.LEFT, padx=5)
    Razer3DRadio(radio_frame, "选项二", radio_var, "option2").pack(side=tk.LEFT, padx=5)
    Razer3DRadio(radio_frame, "选项三", radio_var, "option3").pack(side=tk.LEFT, padx=5)
    
    # 复选框测试
    check_frame = tk.Frame(content, bg=colors['bg_card'])
    check_frame.pack(pady=10, padx=20)
    
    tk.Label(
        check_frame,
        text="附加选项：",
        font=("Microsoft YaHei UI", 10),
        bg=colors['bg_card'],
        fg=colors['text_primary']
    ).pack(side=tk.LEFT, padx=(0, 10))
    
    check1_var = tk.BooleanVar(value=True)
    check2_var = tk.BooleanVar(value=False)
    
    Razer3DCheckbox(check_frame, "打包ZIP", check1_var).pack(side=tk.LEFT, padx=5)
    Razer3DCheckbox(check_frame, "生成日志", check2_var).pack(side=tk.LEFT, padx=5)
    
    # 输入框测试
    input_frame = tk.Frame(content, bg=colors['bg_card'])
    input_frame.pack(pady=10, padx=20, fill=tk.X)
    
    tk.Label(
        input_frame,
        text="输入框：",
        font=("Microsoft YaHei UI", 10),
        bg=colors['bg_card'],
        fg=colors['text_primary']
    ).pack(side=tk.LEFT, padx=(0, 10))
    
    input_var = tk.StringVar(value="测试文本")
    Razer3DInput(input_frame, textvariable=input_var, width=30).pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    root.mainloop()

