"""
Duolingo风格按钮组件
- 圆角矩形
- 底部厚阴影
- 按下时阴影消失
- Razer绿配色
"""
import tkinter as tk
from theme import get_colors


class DuolingoButton(tk.Canvas):
    """
    Duolingo风格按钮 - 圆角+厚底阴影
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
        
        # 圆角半径
        self.radius = 8
        # 厚阴影高度
        self.shadow_height = 4
        
        # 创建Canvas（留出阴影空间）
        super().__init__(parent, 
                        width=width, 
                        height=height + self.shadow_height, 
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
        """绘制Duolingo风格按钮"""
        self.delete("all")
        
        if self.state_var == "disabled":
            self._draw_disabled()
            return
        
        # 按下时阴影消失，按钮下移
        if self.is_pressed:
            offset_y = self.shadow_height
            show_shadow = False
        else:
            offset_y = 0
            show_shadow = True
        
        # 确定颜色
        if self.style == "primary":
            if self.is_pressed:
                top_color = '#3ed62a'
                bottom_color = '#40d028'
                border_color = '#2eb820'
            elif self.is_hovered:
                top_color = '#50e838'
                bottom_color = '#44d62c'
                border_color = '#38c023'
            else:
                top_color = '#4ae633'
                bottom_color = '#42d029'
                border_color = '#38c023'
            
            shadow_color = '#2a5020'  # 深绿阴影
            text_color = '#0d0d0d'
        else:
            if self.is_pressed:
                top_color = '#282828'
                bottom_color = '#2a2a2a'
                border_color = '#202020'
            elif self.is_hovered:
                top_color = '#353535'
                bottom_color = '#2c2c2c'
                border_color = '#252525'
            else:
                top_color = '#2f2f2f'
                bottom_color = '#282828'
                border_color = '#202020'
            
            shadow_color = '#0d0d0d'  # 深黑阴影
            text_color = '#d0d0d0'
        
        # 1. 绘制底部厚阴影（Duolingo特色）
        if show_shadow:
            self._draw_rounded_rect(
                0, self.shadow_height,
                self.btn_width, self.btn_height + self.shadow_height,
                self.radius,
                shadow_color
            )
        
        # 2. 绘制按钮边框
        self._draw_rounded_rect(
            0, offset_y,
            self.btn_width, self.btn_height + offset_y,
            self.radius,
            border_color
        )
        
        # 3. 绘制按钮主体（渐变）
        margin = 2
        self._draw_rounded_gradient(
            margin, offset_y + margin,
            self.btn_width - margin, self.btn_height + offset_y - margin,
            self.radius - 1,
            top_color, bottom_color
        )
        
        # 4. 顶部高光（轻微）
        if not self.is_pressed:
            highlight_h = self.btn_height // 4
            for i in range(highlight_h):
                ratio = 1 - i / highlight_h
                brightness = int(50 * ratio)
                r = min(255, int(top_color[1:3], 16) + brightness)
                g = min(255, int(top_color[3:5], 16) + brightness)
                b = min(255, int(top_color[5:7], 16) + brightness)
                hl_color = f'#{r:02x}{g:02x}{b:02x}'
                
                y = offset_y + margin + 3 + i
                self.create_line(
                    margin + 8, y,
                    self.btn_width - margin - 8, y,
                    fill=hl_color,
                    width=1
                )
        
        # 5. 绘制文本
        text_y = self.btn_height//2 + offset_y
        text_x = self.btn_width//2
        
        self.create_text(
            text_x, text_y,
            text=self.text,
            fill=text_color,
            font=("Microsoft YaHei UI", 10)
        )
    
    def _draw_rounded_rect(self, x1, y1, x2, y2, radius, color):
        """绘制圆角矩形"""
        # 四个角的圆弧
        self.create_arc(x1, y1, x1+radius*2, y1+radius*2, start=90, extent=90, fill=color, outline="")
        self.create_arc(x2-radius*2, y1, x2, y1+radius*2, start=0, extent=90, fill=color, outline="")
        self.create_arc(x1, y2-radius*2, x1+radius*2, y2, start=180, extent=90, fill=color, outline="")
        self.create_arc(x2-radius*2, y2-radius*2, x2, y2, start=270, extent=90, fill=color, outline="")
        
        # 四条边
        self.create_rectangle(x1+radius, y1, x2-radius, y2, fill=color, outline="")
        self.create_rectangle(x1, y1+radius, x2, y2-radius, fill=color, outline="")
    
    def _draw_rounded_gradient(self, x1, y1, x2, y2, radius, color_top, color_bottom):
        """绘制圆角渐变矩形"""
        # 先绘制圆角矩形作为底色
        self._draw_rounded_rect(x1, y1, x2, y2, radius, color_bottom)
        
        # 绘制渐变
        height = y2 - y1
        r1, g1, b1 = int(color_top[1:3], 16), int(color_top[3:5], 16), int(color_top[5:7], 16)
        r2, g2, b2 = int(color_bottom[1:3], 16), int(color_bottom[3:5], 16), int(color_bottom[5:7], 16)
        
        for i in range(int(height)):
            ratio = i / (height - 1) if height > 1 else 0
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            
            y = y1 + i
            # 根据位置调整线条长度（模拟圆角）
            if i < radius:
                # 顶部圆角区域
                offset = radius - int((radius**2 - (radius-i)**2)**0.5)
                self.create_line(x1 + offset, y, x2 - offset, y, fill=color, width=1)
            elif i > height - radius:
                # 底部圆角区域
                offset = radius - int((radius**2 - (i - (height-radius))**2)**0.5)
                self.create_line(x1 + offset, y, x2 - offset, y, fill=color, width=1)
            else:
                # 中间直线区域
                self.create_line(x1, y, x2, y, fill=color, width=1)
    
    def _draw_disabled(self):
        """绘制禁用状态"""
        # 灰色圆角按钮
        self._draw_rounded_rect(
            0, 0,
            self.btn_width, self.btn_height,
            self.radius,
            '#1a1a1a'
        )
        
        self._draw_rounded_rect(
            2, 2,
            self.btn_width - 2, self.btn_height - 2,
            self.radius - 1,
            '#252525'
        )
        
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
        self.state_var = state
        if state == "disabled":
            self.config(cursor="arrow")
        else:
            self.config(cursor="hand2")
        self._draw()


# 测试
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Duolingo风格按钮测试")
    root.geometry("500x300")
    colors = get_colors()
    root.configure(bg=colors['bg_main'])
    
    title = tk.Label(root, text="Duolingo风格按钮", font=("Microsoft YaHei UI", 20, "bold"),
                     bg=colors['bg_main'], fg=colors['text_primary'])
    title.pack(pady=20)
    
    frame = tk.Frame(root, bg=colors['bg_main'])
    frame.pack(pady=20)
    
    btn1 = DuolingoButton(frame, text="选择 Excel 文件", style="primary", width=160, height=48)
    btn1.pack(side=tk.LEFT, padx=10)
    
    btn2 = DuolingoButton(frame, text="开始分析", style="primary", width=120, height=48)
    btn2.pack(side=tk.LEFT, padx=10)
    
    btn3 = DuolingoButton(frame, text="清除", style="secondary", width=90, height=48)
    btn3.pack(side=tk.LEFT, padx=10)
    
    root.mainloop()

