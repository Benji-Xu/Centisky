"""
集成工具启动器 - 单一界面，工具UI直接集成到右侧面板
Razer风格设计 - 专业高级黑绿色调
"""
import tkinter as tk
from tkinter import messagebox
import sys
from pathlib import Path
from theme import get_colors
from theme_toggle import ThemeToggleButton


class MockTkRoot(tk.Frame):
    """模拟Tk窗口的对象，继承自Frame以支持作为容器使用"""
    def __init__(self, parent_frame):
        # 初始化为Frame
        super().__init__(parent_frame)
        self.pack(fill=tk.BOTH, expand=True)
        
        self._geometry = None
        self._title = None
        self._parent_frame = parent_frame
        self._resizable_width = True
        self._resizable_height = True
    
    def title(self, text=None):
        """模拟title方法"""
        if text is not None:
            self._title = text
        return self._title
    
    def geometry(self, geom=None):
        """模拟geometry方法"""
        if geom is not None:
            self._geometry = geom
        return self._geometry
    
    def resizable(self, width=None, height=None):
        """模拟resizable方法"""
        if width is not None:
            self._resizable_width = width
        if height is not None:
            self._resizable_height = height
        return (self._resizable_width, self._resizable_height)
    
    def update_idletasks(self):
        """模拟update_idletasks方法"""
        try:
            super().update_idletasks()
        except:
            pass
    
    def winfo_screenwidth(self):
        """模拟winfo_screenwidth方法"""
        try:
            return super().winfo_screenwidth()
        except:
            return 1920
    
    def winfo_screenheight(self):
        """模拟winfo_screenheight方法"""
        try:
            return super().winfo_screenheight()
        except:
            return 1080
    
    def winfo_children(self):
        """模拟winfo_children方法"""
        return super().winfo_children()
    
    def pack_propagate(self, flag):
        """模拟pack_propagate方法"""
        super().pack_propagate(flag)
    
    def destroy(self):
        """模拟destroy方法 - 不真正销毁"""
        pass
    
    def bind(self, sequence, func, add=None):
        """模拟bind方法"""
        try:
            return super().bind(sequence, func, add=add)
        except:
            pass
    
    def after(self, ms, func=None, *args):
        """模拟after方法"""
        try:
            return super().after(ms, func, *args)
        except:
            pass
    
    def after_cancel(self, id):
        """模拟after_cancel方法"""
        try:
            return super().after_cancel(id)
        except:
            pass
    
    def mainloop(self):
        """模拟mainloop方法 - 不执行"""
        pass
    
    def quit(self):
        """模拟quit方法 - 不执行"""
        pass
    
    def withdraw(self):
        """模拟withdraw方法"""
        pass
    
    def deiconify(self):
        """模拟deiconify方法"""
        pass
    
    def winfo_exists(self):
        """模拟winfo_exists方法"""
        try:
            return super().winfo_exists()
        except:
            return True


class ToolFrameAdapter:
    """工具Frame适配器 - 将工具UI适配到Frame中"""
    def __init__(self, frame, tool_info):
        self.frame = frame
        self.tool_info = tool_info
        self.tool_instance = None
        self.load_tool()
    
    def load_tool(self):
        """加载工具到Frame中"""
        try:
            # 导入工具模块
            module_name = self.tool_info['module']
            class_name = self.tool_info['class']
            
            # 动态导入模块
            module = __import__(module_name, fromlist=[class_name])
            tool_class = getattr(module, class_name)
            
            # 创建模拟的Tk窗口对象
            mock_root = MockTkRoot(self.frame)
            
            # 创建工具实例，传入模拟的Tk窗口
            self.tool_instance = tool_class(mock_root)
            
        except Exception as e:
            import traceback
            print(f"加载工具失败：{e}")
            print(traceback.format_exc())
            raise


class IntegratedToolLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Centisky")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)
        
        # 移除最大化按钮（Windows）
        try:
            self.root.attributes('-toolwindow', False)
            # 禁用最大化
            self.root.maxsize(1200, 700)
            self.root.minsize(1200, 700)
        except:
            pass
        
        # Razer风格配色
        self.colors = get_colors()
        self.root.configure(bg=self.colors['bg_main'])
        
        # 当前选中的工具
        self.current_tool = None
        self.current_tool_frame = None
        self.tool_adapters = {}  # 缓存工具适配器
        self.last_tool_name = None  # 记录上次选中的工具
        
        # 初始化工具列表
        self.tools = [
            {
                'name': '图片处理工具',
                'icon': '🖼️',
                'description': '批量处理图片：格式转换、拼长图、切片等',
                'file': 'tools/image_processor/main.py',
                'class': 'ImageProcessorApp',
                'module': 'tools.image_processor.main',
                'status': 'active'
            },
            {
                'name': '视频处理工具',
                'icon': '🎬',
                'description': '视频格式转换、压缩、调整尺寸等',
                'file': 'tools/video_processor/main.py',
                'class': 'VideoProcessorApp',
                'module': 'tools.video_processor.main',
                'status': 'active'
            },
            {
                'name': '标签箱唛工具',
                'icon': '📦',
                'description': '自动生成标签和箱唛文件',
                'file': 'tools/label_box/main.py',
                'status': 'active'
            },
            {
                'name': '发票整理工具',
                'icon': '📄',
                'description': '整理开票文件，生成财务导入表格',
                'file': 'tools/invoice_processor/main.py',
                'class': 'InvoiceProcessorApp',
                'module': 'tools.invoice_processor.main',
                'status': 'active'
            },
            {
                'name': '京准通数据分析',
                'icon': '📊',
                'description': '快车投流周对比分析，可视化展示',
                'file': 'tools/jzt_analyzer/main.py',
                'class': 'JZTAnalyzerApp',
                'module': 'tools.jzt_analyzer.main',
                'status': 'active'
            },
        ]
        
        self.center_window()
        self.create_widgets()
        
    def center_window(self):
        """窗口居中"""
        self.root.update_idletasks()
        width = 1200
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """创建UI组件"""
        
        # 顶部导航栏
        header = tk.Frame(self.root, bg=self.colors['bg_card'], height=1)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # 底部分隔线
        tk.Frame(header, bg=self.colors['border_main'], height=1).pack(side=tk.BOTTOM, fill=tk.X)
        
        # 主容器（左侧边栏 + 右侧内容）
        main_container = tk.Frame(self.root, bg=self.colors['bg_main'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # 先创建右侧内容区域（初始化content_area）
        self.create_content_area(main_container)
        
        # 再创建左侧边栏
        self.create_sidebar(main_container)
        
    def create_sidebar(self, parent):
        """创建左侧边栏"""
        sidebar = tk.Frame(parent, bg=self.colors['bg_card'], width=180)
        sidebar.pack(side=tk.LEFT, fill=tk.BOTH, padx=0, pady=0)
        sidebar.pack_propagate(False)
        
        # 顶部标题
        title_frame = tk.Frame(sidebar, bg=self.colors['bg_card'])
        title_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        tk.Label(
            title_frame,
            text="工具合集",
            font=("Microsoft YaHei UI", 12, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(anchor=tk.W)
        
        # 工具列表容器（上方，可扩展）
        tools_container = tk.Frame(sidebar, bg=self.colors['bg_card'])
        tools_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # 创建工具按钮
        self.tool_buttons = {}
        for idx, tool in enumerate(self.tools):
            self.create_tool_button(tools_container, tool, idx)
        
        # 底部主题切换按钮（左中位置）
        bottom_frame = tk.Frame(sidebar, bg=self.colors['bg_card'])
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=0, pady=(10, 10))
        
        theme_btn = ThemeToggleButton(bottom_frame, command=self.toggle_theme)
        theme_btn.pack(anchor=tk.W, padx=15)
        
        # 默认选中第一个工具
        if self.tools:
            self.select_tool(self.tools[0])
    
    def create_tool_button(self, parent, tool, idx):
        """创建工具按钮"""
        # 按钮背景（撑满宽度，iOS风格圆角）
        btn = tk.Frame(
            parent,
            bg=self.colors['bg_hover'],
            relief=tk.FLAT,
            cursor="hand2",
            height=45,
            highlightthickness=0
        )
        btn.pack(fill=tk.X, padx=0, pady=0)
        btn.pack_propagate(False)
        
        # 按钮内容
        btn_content = tk.Frame(btn, bg=self.colors['bg_hover'], highlightthickness=0)
        btn_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)
        
        # 工具名称
        name_label = tk.Label(
            btn_content,
            text=tool['name'],
            font=("Microsoft YaHei UI", 10),
            bg=self.colors['bg_hover'],
            fg=self.colors['text_primary'],
            anchor=tk.W
        )
        name_label.pack(fill=tk.X)
        
        # 点击事件
        def on_click(e):
            self.select_tool(tool)
        
        # Hover效果
        def on_enter(e):
            btn.config(bg=self.colors['primary'])
            btn_content.config(bg=self.colors['primary'])
            name_label.config(bg=self.colors['primary'], fg='white')
        
        def on_leave(e):
            if self.current_tool != tool:
                btn.config(bg=self.colors['bg_hover'])
                btn_content.config(bg=self.colors['bg_hover'])
                name_label.config(bg=self.colors['bg_hover'], fg=self.colors['text_primary'])
        
        # 绑定事件
        for widget in [btn, btn_content, name_label]:
            widget.bind("<Button-1>", on_click)
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.config(cursor="hand2")
        
        # 保存按钮引用
        self.tool_buttons[tool['name']] = {
            'frame': btn,
            'content': btn_content,
            'name_label': name_label,
            'tool': tool
        }
    
    def create_content_area(self, parent):
        """创建右侧内容区域"""
        self.content_area = tk.Frame(parent, bg=self.colors['bg_main'])
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=0, pady=0)
    
    def select_tool(self, tool):
        """选中工具"""
        self.current_tool = tool
        self.last_tool_name = tool['name']  # 保存当前工具名称
        
        # 更新按钮样式
        for tool_name, btn_info in self.tool_buttons.items():
            if btn_info['tool'] == tool:
                # 选中状态
                btn_info['frame'].config(bg=self.colors['primary'])
                btn_info['content'].config(bg=self.colors['primary'])
                btn_info['name_label'].config(bg=self.colors['primary'], fg='white')
            else:
                # 未选中状态
                btn_info['frame'].config(bg=self.colors['bg_hover'])
                btn_info['content'].config(bg=self.colors['bg_hover'])
                btn_info['name_label'].config(bg=self.colors['bg_hover'], fg=self.colors['text_primary'])
        
        # 显示工具界面
        self.show_tool(tool)
    
    def show_tool(self, tool):
        """显示工具界面"""
        # 清空内容区域
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # 创建工具容器（直接显示工具，不添加标题）
        tool_container = tk.Frame(self.content_area, bg=self.colors['bg_main'])
        tool_container.pack(fill=tk.BOTH, expand=True)
        
        # 加载工具到容器中
        try:
            # 每次都创建新的工具适配器，避免窗口路径问题
            adapter = ToolFrameAdapter(tool_container, tool)
            self.tool_adapters[tool['name']] = adapter
            
        except Exception as e:
            import traceback
            error_msg = f"加载工具失败：{e}\n\n{traceback.format_exc()}"
            print(error_msg)
            
            error_label = tk.Label(
                tool_container,
                text=f"加载失败：{str(e)}",
                font=("Microsoft YaHei UI", 12),
                bg=self.colors['bg_main'],
                fg='#ff6b6b'
            )
            error_label.pack(pady=20)
    
    def toggle_theme(self):
        """切换主题"""
        from theme import get_theme
        current_theme = get_theme()
        new_dark_mode = not current_theme.is_dark
        
        # 保存当前工具名称
        last_tool = self.last_tool_name
        
        # 重启应用以应用新主题
        self.root.destroy()
        new_root = tk.Tk()
        
        # 强制设置新主题
        import theme
        theme._global_theme = theme.RazerTheme(dark_mode=new_dark_mode)
        
        app = IntegratedToolLauncher(new_root)
        
        # 恢复上次选中的工具
        if last_tool:
            for tool in app.tools:
                if tool['name'] == last_tool:
                    app.select_tool(tool)
                    break
        
        new_root.mainloop()


def main():
    """主函数"""
    root = tk.Tk()
    app = IntegratedToolLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
