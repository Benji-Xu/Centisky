"""
工具启动器 - 主界面
Razer风格设计 - 专业高级黑绿色调
"""
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
from pathlib import Path
from theme import get_colors
from razer_ui import Razer3DCard
from theme_toggle import ThemeToggleButton
from update_checker import check_for_updates_async


class ToolLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Centisky")
        self.root.geometry("1100x700")
        self.root.resizable(True, True)
        
        # 不设置窗口图标（用户不需要）
        
        # Razer风格配色 - 自动跟随系统深色/浅色模式
        self.colors = get_colors()
        
        self.root.configure(bg=self.colors['bg_main'])
        self.center_window()
        self.create_widgets()
        
        # 异步检查更新（不阻塞主程序）
        check_for_updates_async()
        
    def center_window(self):
        """窗口居中"""
        self.root.update_idletasks()
        width = 1100
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """创建UI组件"""
        
        # 顶部导航栏
        header = tk.Frame(self.root, bg=self.colors['bg_card'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg=self.colors['bg_card'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=60, pady=0)
        
        # Logo/标题（左侧）
        title_container = tk.Frame(header_content, bg=self.colors['bg_card'])
        title_container.pack(side=tk.LEFT, pady=20)
        
        # 标题
        title_label = tk.Label(
            title_container,
            text="Centisky",
            font=("Microsoft YaHei UI", 18, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        )
        title_label.pack(side=tk.LEFT)
        
        # 主题切换按钮（右侧，自定义日月图标）
        theme_btn = ThemeToggleButton(header_content, command=self.toggle_theme)
        theme_btn.pack(side=tk.RIGHT, pady=28)
        
        # 底部分隔线
        tk.Frame(header, bg=self.colors['border_main'], height=1).pack(side=tk.BOTTOM, fill=tk.X)
        
        # Hero区域（大标题）
        hero_frame = tk.Frame(self.root, bg=self.colors['bg_main'], height=140)
        hero_frame.pack(fill=tk.X, pady=(20, 0))
        hero_frame.pack_propagate(False)
        
        hero_content = tk.Frame(hero_frame, bg=self.colors['bg_main'])
        hero_content.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(
            hero_content,
            text="工具集合",
            font=("Microsoft YaHei UI", 32, "bold"),
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary']
        ).pack()
        
        tk.Label(
            hero_content,
            text="选择你需要的工具开始使用",
            font=("Microsoft YaHei UI", 12),
            bg=self.colors['bg_main'],
            fg=self.colors['text_secondary']
        ).pack(pady=(8, 0))
        
        # 工具卡片区域
        cards_container = tk.Frame(self.root, bg=self.colors['bg_main'])
        cards_container.pack(fill=tk.BOTH, expand=True, padx=60, pady=(25, 30))
        
        # 卡片网格标题
        tk.Label(
            cards_container,
            text="可用工具",
            font=("Microsoft YaHei UI", 15, "bold"),
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary'],
            anchor=tk.W
        ).pack(fill=tk.X, pady=(0, 15))
        
        # 直接创建卡片网格（移除滚动条，4个工具不需要滚动）
        cards_grid = tk.Frame(cards_container, bg=self.colors['bg_main'])
        cards_grid.pack(fill=tk.BOTH, expand=True)
        
        # 工具卡片列表
        tools = [
            {
                'title': '图片处理工具',
                'description': '批量处理图片：格式转换、拼长图、切片等功能',
                'tags': ['图片', '批处理', '编辑'],
                'file': 'tools/image_processor/main.py',
                'status': 'active'
            },
            {
                'title': '视频处理工具',
                'description': '视频格式转换、压缩、调整尺寸、归类、分组打包、标题处理',
                'tags': ['视频', '格式转换', 'FFmpeg'],
                'file': 'tools/video_processor/main.py',
                'status': 'active'
            },
            {
                'title': '标签箱唛处理工具',
                'description': '自动生成标签和箱唛文件，支持3C和玩具类型',
                'tags': ['Excel', '自动化', '标签'],
                'file': 'tools/label_box/main.py',
                'status': 'active'
            },
            {
                'title': '开票信息处理',
                'description': '整理唯品会、小米有品等平台的开票Excel和发票文件，一键生成财务导入和对账所需表格',
                'tags': ['Excel', '开票', '唯品会', '小米有品'],
                'file': 'tools/invoice_processor/main.py',
                'status': 'active'
            },
            {
                'title': '京准通数据分析',
                'description': '快车投流周对比分析，可视化展示关键指标变化',
                'tags': ['数据分析', '京准通', '同比'],
                'file': 'tools/jzt_analyzer/main.py',
                'status': 'active'
            },
            {
                'title': '更多工具即将推出',
                'description': '我们正在开发更多实用工具，让工作流程更加高效便捷',
                'tags': ['开发中'],
                'file': None,
                'status': 'coming'
            },
        ]
        
        # 创建工具卡片（每行3个）- 使用grid布局确保宽度一致
        for idx, tool in enumerate(tools):
            row = idx // 3
            col = idx % 3
            self.create_tool_card_grid(cards_grid, tool, row, col)
        
        # 底部署名
        footer = tk.Frame(self.root, bg=self.colors['bg_main'], height=50)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        
        # Footer - 使用Text widget实现部分可点击，无多余间距
        footer_text = tk.Text(
            footer,
            height=1,
            width=37,  # "Developed by @Gabe-Xu with Cursor"长度
            bg=self.colors['bg_main'],
            fg=self.colors['text_muted'],
            relief=tk.FLAT,
            borderwidth=0,
            cursor="arrow",
            font=("Microsoft YaHei UI", 9),
            wrap=tk.NONE,
            highlightthickness=0
        )
        footer_text.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
        
        # 配置居中tag
        footer_text.tag_configure("center", justify='center')
        
        # 插入文本
        footer_text.insert("1.0", "Developed by @Benji-Xu with Windsurf", "center")
        footer_text.config(state=tk.DISABLED)
        
        # 让@Benji-Xu和Windsurf部分可点击
        footer_text.tag_add("github", "1.13", "1.22")
        footer_text.tag_config("github", foreground=self.colors['text_muted'])
        footer_text.tag_bind("github", "<Button-1>", lambda e: self.open_github())
        footer_text.tag_bind("github", "<Enter>", lambda e: [
            footer_text.tag_config("github", foreground=self.colors['primary'], underline=True),
            footer_text.config(cursor="hand2")
        ])
        footer_text.tag_bind("github", "<Leave>", lambda e: [
            footer_text.tag_config("github", foreground=self.colors['text_muted'], underline=False),
            footer_text.config(cursor="arrow")
        ])
        
        footer_text.tag_add("windsurf", "1.28", "1.36")
        footer_text.tag_config("windsurf", foreground=self.colors['text_muted'])
        footer_text.tag_bind("windsurf", "<Button-1>", lambda e: self.open_windsurf())
        footer_text.tag_bind("windsurf", "<Enter>", lambda e: [
            footer_text.tag_config("windsurf", foreground=self.colors['primary'], underline=True),
            footer_text.config(cursor="hand2")
        ])
        footer_text.tag_bind("windsurf", "<Leave>", lambda e: [
            footer_text.tag_config("windsurf", foreground=self.colors['text_muted'], underline=False),
            footer_text.config(cursor="arrow")
        ])
        
    def create_tooltip(self, widget, text):
        """创建tooltip提示框"""
        tooltip_window = None
        
        def show_tooltip(event):
            nonlocal tooltip_window
            if tooltip_window:
                return
            
            # 获取widget的位置
            x = widget.winfo_rootx() + 10
            y = widget.winfo_rooty() + widget.winfo_height() + 5
            
            # 创建tooltip窗口
            tooltip_window = tk.Toplevel(widget)
            tooltip_window.wm_overrideredirect(True)
            tooltip_window.wm_geometry(f"+{x}+{y}")
            
            # 设置tooltip内容
            label = tk.Label(
                tooltip_window,
                text=text,
                font=("Microsoft YaHei UI", 9),
                bg='#2d3748',
                fg='white',
                padx=12,
                pady=8,
                justify=tk.LEFT,
                wraplength=300
            )
            label.pack()
        
        def hide_tooltip(event):
            nonlocal tooltip_window
            if tooltip_window:
                tooltip_window.destroy()
                tooltip_window = None
        
        # 只绑定Enter和Leave事件，不干扰其他事件
        widget.bind("<Enter>", show_tooltip, add='+')
        widget.bind("<Leave>", hide_tooltip, add='+')
    
    def create_tool_card_grid(self, parent, tool, row, col):
        """创建工具卡片（使用grid布局）"""
        # 配置grid列权重，确保三列宽度相等
        parent.grid_columnconfigure(0, weight=1, uniform="card")
        parent.grid_columnconfigure(1, weight=1, uniform="card")
        parent.grid_columnconfigure(2, weight=1, uniform="card")
        
        # 配置grid行权重，确保所有行高度相等
        parent.grid_rowconfigure(0, weight=1, uniform="card_row")
        parent.grid_rowconfigure(1, weight=1, uniform="card_row")
        
        # 卡片容器（固定高度确保一致）
        card_wrapper = tk.Frame(parent, bg=self.colors['bg_main'], height=110)
        card_wrapper.grid(row=row, column=col, sticky="nsew", padx=7.5, pady=(0, 15))
        card_wrapper.grid_propagate(False)
        
        # 使用Razer 3D卡片（拟物化效果）
        card_3d = Razer3DCard(card_wrapper)
        card_3d.pack(fill=tk.BOTH, expand=True)
        card = card_3d.get_content()
        
        # 卡片内容
        card_content = tk.Frame(card, bg=self.colors['bg_card'])
        card_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 根据工具状态设置颜色
        if tool['status'] == 'coming':
            bg_color = self.colors['bg_hover']  # 灰色背景
            title_color = self.colors['text_disabled']  # 灰色标题
            desc_color = self.colors['text_muted']  # 更浅的灰色副标题
        else:
            bg_color = self.colors['bg_card']
            title_color = self.colors['text_primary']
            desc_color = self.colors['text_secondary']
        
        # 更新卡片背景色
        card.config(bg=bg_color)
        card_content.config(bg=bg_color)
        
        # 标题（一行）
        title_label = tk.Label(
            card_content,
            text=tool['title'],
            font=("Microsoft YaHei UI", 14, "bold"),  # 从12增大到14
            bg=bg_color,
            fg=title_color,
            anchor=tk.W
        )
        title_label.pack(fill=tk.X, pady=(0, 8))
        
        # 副标题（显示两行，超出截断）
        desc_text = tool['description']
        
        # 计算两行能显示的最大字符数
        # 内边距20px，wraplength设置为265px
        # 字号10, 中文约10px/字
        # 一行约26字符，两行约52字符，保守估计48字符（含标点和空格）
        max_chars = 48
        
        if len(desc_text) > max_chars:
            # 截断并添加省略号
            display_text = desc_text[:max_chars] + "..."
        else:
            display_text = desc_text
        
        desc_label = tk.Label(
            card_content,
            text=display_text,
            font=("Microsoft YaHei UI", 10),
            bg=bg_color,
            fg=desc_color,
            anchor=tk.W,
            justify=tk.LEFT,
            wraplength=265  # 配合内边距20px，确保不被截断
        )
        desc_label.pack(fill=tk.X)
        
        # 为可用工具添加点击事件和hover效果
        if tool['status'] == 'active':
            # 设置鼠标样式为手型
            card.config(cursor="hand2")
            card_content.config(cursor="hand2")
            
            # 点击事件
            def on_click(e):
                self.launch_tool(tool['file'])
            
            # Hover效果 - Razer风格：绿色边框（根据主题调整）
            def on_enter(e):
                # 根据主题选择合适的绿色
                is_dark = self.colors.get('is_dark', True)
                hover_green = self.colors['primary'] if is_dark else self.colors['primary_dark']
                
                # 卡片边框变绿
                card_3d.border_dark.config(bg=hover_green)
                # 标题变绿
                title_label.config(fg=hover_green)
            
            def on_leave(e):
                # 恢复颜色（根据主题）
                is_dark = self.colors.get('is_dark', True)
                card_3d.border_dark.config(bg='#333333' if is_dark else '#d0d0d0')
                # 恢复标题颜色
                title_label.config(fg=title_color)
            
            # 绑定事件到卡片（使用顶层容器）
            card_wrapper.config(cursor="hand2")
            card_wrapper.bind("<Button-1>", on_click)
            card_wrapper.bind("<Enter>", on_enter)
            card_wrapper.bind("<Leave>", on_leave)
            
            # 绑定到其他层级
            for widget in [card_3d, card, card_content, title_label, desc_label]:
                widget.config(cursor="hand2")
                widget.bind("<Button-1>", on_click)
                widget.bind("<Enter>", on_enter, add='+')
                widget.bind("<Leave>", on_leave, add='+')
    
    def launch_tool(self, tool_file):
        """启动工具"""
        if not tool_file:
            messagebox.showinfo("提示", "该工具尚未开发")
            return
        
        # 判断是哪个工具
        if 'label_box' in tool_file:
            # 启动标签箱唛工具
            try:
                # 导入工具模块
                sys.path.insert(0, str(Path(__file__).parent / "tools" / "label_box"))
                from tools.label_box.main import IntegratedApp
                
                # 销毁当前窗口
                self.root.destroy()
                
                # 创建新窗口运行工具
                new_root = tk.Tk()
                app = IntegratedApp(new_root)
                app.center_window()
                new_root.mainloop()
            except Exception as e:
                import traceback
                error_msg = f"启动工具失败：{e}\n\n{traceback.format_exc()}"
                print(error_msg)
                messagebox.showerror("启动失败", error_msg)
                # 失败后重新打开launcher
                self.root = tk.Tk()
                app = ToolLauncher(self.root)
                app.center_window()
                self.root.mainloop()
        elif 'image_processor' in tool_file:
            # 启动图片处理工具
            try:
                # 导入工具模块
                sys.path.insert(0, str(Path(__file__).parent / "tools" / "image_processor"))
                from tools.image_processor.main import ImageProcessorApp
                
                # 销毁当前窗口
                self.root.destroy()
                
                # 创建新窗口运行工具
                new_root = tk.Tk()
                app = ImageProcessorApp(new_root)
                new_root.mainloop()
            except Exception as e:
                import traceback
                error_msg = f"启动工具失败：{e}\n\n{traceback.format_exc()}"
                print(error_msg)
                messagebox.showerror("启动失败", error_msg)
                # 失败后重新打开launcher
                self.root = tk.Tk()
                app = ToolLauncher(self.root)
                app.center_window()
                self.root.mainloop()
        elif 'jzt_analyzer' in tool_file:
            # 启动京准通数据分析工具
            try:
                # 导入工具模块
                sys.path.insert(0, str(Path(__file__).parent / "tools" / "jzt_analyzer"))
                from tools.jzt_analyzer.main import JZTAnalyzerApp
                
                # 销毁当前窗口
                self.root.destroy()
                
                # 创建新窗口运行工具
                new_root = tk.Tk()
                app = JZTAnalyzerApp(new_root)
                new_root.mainloop()
            except Exception as e:
                import traceback
                error_msg = f"启动工具失败：{e}\n\n{traceback.format_exc()}"
                print(error_msg)
                messagebox.showerror("启动失败", error_msg)
                # 失败后重新打开launcher
                self.root = tk.Tk()
                app = ToolLauncher(self.root)
                app.center_window()
                self.root.mainloop()
        elif 'video_processor' in tool_file:
            # 启动视频处理工具
            try:
                # 导入工具模块
                sys.path.insert(0, str(Path(__file__).parent / "tools" / "video_processor"))
                from tools.video_processor.main import VideoProcessorApp
                
                # 销毁当前窗口
                self.root.destroy()
                
                # 创建新窗口运行工具
                new_root = tk.Tk()
                app = VideoProcessorApp(new_root)
                new_root.mainloop()
            except Exception as e:
                import traceback
                error_msg = f"启动工具失败：{e}\n\n{traceback.format_exc()}"
                print(error_msg)
                messagebox.showerror("启动失败", error_msg)
                # 失败后重新打开launcher
                self.root = tk.Tk()
                app = ToolLauncher(self.root)
                app.center_window()
                self.root.mainloop()
        elif 'invoice_processor' in tool_file:
            # 启动开票信息处理工具
            try:
                # 导入工具模块
                sys.path.insert(0, str(Path(__file__).parent / "tools" / "invoice_processor"))
                from tools.invoice_processor.main import InvoiceProcessorApp
                
                # 销毁当前窗口
                self.root.destroy()
                
                # 创建新窗口运行工具
                new_root = tk.Tk()
                app = InvoiceProcessorApp(new_root)
                new_root.mainloop()
            except Exception as e:
                import traceback
                error_msg = f"启动工具失败：{e}\n\n{traceback.format_exc()}"
                print(error_msg)
                messagebox.showerror("启动失败", error_msg)
                # 失败后重新打开launcher
                self.root = tk.Tk()
                app = ToolLauncher(self.root)
                app.center_window()
                self.root.mainloop()
        else:
            messagebox.showinfo("提示", "该工具尚未开发")
    
    def toggle_theme(self):
        """切换主题"""
        # 重新加载并切换主题
        from theme import get_theme
        current_theme = get_theme()
        new_dark_mode = not current_theme.is_dark
        
        # 重启应用以应用新主题
        self.root.destroy()
        new_root = tk.Tk()
        
        # 强制设置新主题
        import theme
        theme._global_theme = theme.RazerTheme(dark_mode=new_dark_mode)
        
        app = ToolLauncher(new_root)
        new_root.mainloop()
    
    def open_github(self):
        """打开GitHub主页"""
        import webbrowser
        webbrowser.open("https://github.com/Benji-Xu")
    
    def open_windsurf(self):
        """打开Windsurf官网"""
        import webbrowser
        webbrowser.open("https://windsurf.com")


def main():
    """主函数"""
    root = tk.Tk()
    app = ToolLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()

