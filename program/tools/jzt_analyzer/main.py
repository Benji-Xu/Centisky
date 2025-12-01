"""
京准通数据分析工具 - 快车投流周对比分析
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path
from datetime import datetime
import threading
import sys

# 添加父目录到路径以导入theme模块
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from theme import get_colors
from razer_ui import Razer3DCard
from unified_button import UnifiedButton
from theme_toggle import ThemeToggleButton

# 图片复制到剪贴板依赖（可选）
try:
    from PIL import Image
    import io
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

# 内嵌的 Windows 剪贴板操作（使用 PowerShell，无需外部依赖）
import subprocess
import tempfile
import base64

class WindowsClipboard:
    """使用 PowerShell 实现的 Windows 剪贴板操作"""
    
    @staticmethod
    def copy_image_to_clipboard(image_data):
        """将 BMP 图像数据复制到剪贴板"""
        try:
            # 创建临时文件存储 BMP 数据
            with tempfile.NamedTemporaryFile(suffix='.bmp', delete=False) as tmp_file:
                tmp_path = tmp_file.name
                tmp_file.write(image_data)
            
            try:
                # 转义路径中的反斜杠
                escaped_path = tmp_path.replace('\\', '\\\\')
                
                # 使用 PowerShell 将图像复制到剪贴板
                ps_script = f"""
                [System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null
                $image = [System.Drawing.Image]::FromFile('{escaped_path}')
                [System.Windows.Forms.Clipboard]::SetImage($image)
                $image.Dispose()
                """
                
                # 执行 PowerShell 脚本
                result = subprocess.run(
                    ['powershell', '-NoProfile', '-Command', ps_script],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode != 0:
                    raise Exception(f"PowerShell error: {result.stderr}")
                
                return True
            finally:
                # 清理临时文件
                import os
                try:
                    os.unlink(tmp_path)
                except:
                    pass
        
        except Exception as e:
            raise Exception(f"Clipboard operation failed: {e}")

# 导入核心模块
try:
    from . import core
    CORE_AVAILABLE = True
except:
    try:
        import core
        CORE_AVAILABLE = True
    except:
        CORE_AVAILABLE = False

# 导入可视化模块
try:
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 设置中文字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    MATPLOTLIB_AVAILABLE = True
except:
    MATPLOTLIB_AVAILABLE = False


class JZTAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Workit - 京准通数据分析工具")
        self.root.geometry("1100x750")
        self.root.resizable(True, True)
        
        # 不设置窗口图标（用户不需要）
        
        # Razer风格配色 - 自动跟随系统深色/浅色模式
        self.colors = get_colors()
        
        self.root.configure(bg=self.colors['bg_main'])
        self.center_window()
        
        # 数据文件
        self.current_file = None
        self.processing = False
        self.analysis_data = None
        self.weeks_info = []  # 可用的周列表
        
        # 周选择
        self.week1_var = tk.StringVar(value="")
        self.week2_var = tk.StringVar(value="")
        
        # 输出路径
        self.output_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        
        # 创建样式
        self.setup_styles()
        
        # 创建界面
        self.create_widgets()
    
    def center_window(self):
        """窗口居中"""
        self.root.update_idletasks()
        width = 1100
        height = 750
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        """设置样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure(
            "Modern.Horizontal.TProgressbar",
            troughcolor=self.colors['bg_main'],
            background=self.colors['primary'],
            borderwidth=0,
            thickness=12
        )
    
    def create_widgets(self):
        """创建UI组件 - 左右分栏布局"""
        
        # 顶部标题区域（统一布局）
        header_frame = tk.Frame(self.root, bg=self.colors['bg_main'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # 左侧返回按钮
        back_btn = tk.Label(
            header_frame,
            text="< 返回首页",
            font=("Microsoft YaHei UI", 10),
            bg=self.colors['bg_main'],
            fg=self.colors['text_muted'],
            cursor="hand2"
        )
        back_btn.place(relx=0.0, rely=0.61, x=40, anchor='w')
        back_btn.bind("<Button-1>", lambda e: self.back_to_launcher())
        back_btn.bind("<Enter>", lambda e: back_btn.config(fg=self.colors['text_primary']))
        back_btn.bind("<Leave>", lambda e: back_btn.config(fg=self.colors['text_muted']))
        
        # 右侧主题切换按钮
        theme_btn = ThemeToggleButton(header_frame, command=self.toggle_theme)
        theme_btn.place(relx=1.0, rely=0.58, x=-40, anchor='e')

        # 右上角帮助按钮（?）
        help_btn = tk.Label(
            header_frame,
            text="?",
            font=("Microsoft YaHei UI", 13, "bold"),
            bg=self.colors['bg_main'],
            fg=self.colors['text_muted'],
            cursor="hand2"
        )
        help_btn.place(relx=1.0, rely=0.61, x=-80, anchor='e')
        help_btn.bind("<Button-1>", lambda e: self.open_help())
        help_btn.bind("<Enter>", lambda e: help_btn.config(fg=self.colors['text_primary']))
        help_btn.bind("<Leave>", lambda e: help_btn.config(fg=self.colors['text_muted']))
        
        # 中间标题
        title_container = tk.Frame(header_frame, bg=self.colors['bg_main'])
        title_container.place(relx=0.5, rely=0.61, anchor='center')
        
        title_label = tk.Label(
            title_container,
            text="京准通快车数据分析",
            font=("Microsoft YaHei UI", 24, "bold"),
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary']
        )
        title_label.pack()
        
        # 主内容区域 - 左右分栏
        main_container = tk.Frame(self.root, bg=self.colors['bg_main'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=60, pady=35)
        
        # 左侧面板 - 上传和操作
        left_panel = tk.Frame(main_container, bg=self.colors['bg_main'], width=380)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 18))
        left_panel.pack_propagate(False)
        
        self.create_left_panel(left_panel)
        
        # 右侧面板 - 数据可视化
        right_panel = tk.Frame(main_container, bg=self.colors['bg_main'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_right_panel(right_panel)
    
    def create_left_panel(self, parent):
        """创建左侧面板"""
        
        # 文件上传卡片
        upload_card_container, upload_card = self.create_card(parent)
        upload_card_container.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        tk.Label(
            upload_card,
            text="数据文件",
            font=("Microsoft YaHei UI", 13, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(anchor=tk.W, pady=(0, 12))
        
        tk.Label(
            upload_card,
            text="上传京准通快车两周数据报表",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_muted']
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # 文件状态显示
        file_status_frame = tk.Frame(upload_card, bg=self.colors['bg_main'])
        file_status_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.file_label = tk.Label(
            file_status_frame,
            text="尚未选择文件",
            font=("Microsoft YaHei UI", 10),
            bg=self.colors['bg_main'],
            fg=self.colors['text_muted'],
            anchor=tk.W,
            padx=15,
            pady=12
        )
        self.file_label.pack(fill=tk.X)
        
        # 按钮区域
        button_frame = tk.Frame(upload_card, bg=self.colors['bg_card'])
        button_frame.pack(fill=tk.X)
        
        # 选择文件按钮（统一风格，缩小宽度）
        self.select_btn = UnifiedButton(
            button_frame,
            text="选择 Excel 文件",
            command=self.select_file,
            style="primary",
            width=135,
            height=38
        )
        self.select_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        # 分析按钮（统一风格）
        self.analyze_btn = UnifiedButton(
            button_frame,
            text="开始分析",
            command=self.start_analysis,
            style="primary",
            width=95,
            height=38,
            state="disabled"
        )
        self.analyze_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        # 清除按钮（统一风格）
        self.clear_btn = UnifiedButton(
            button_frame,
            text="清除",
            command=self.clear_file,
            style="secondary",
            width=75,
            height=38,
            state="disabled"
        )
        self.clear_btn.pack(side=tk.LEFT)
        
        # 周选择卡片
        week_select_card_container, week_select_card = self.create_card(parent)
        week_select_card_container.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            week_select_card,
            text="周期选择",
            font=("Microsoft YaHei UI", 13, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(anchor=tk.W, pady=(0, 12))
        
        # 本周选择
        tk.Label(
            week_select_card,
            text="本周：",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            anchor=tk.W
        ).pack(fill=tk.X, pady=(0, 5))
        
        self.week1_combo = ttk.Combobox(
            week_select_card,
            textvariable=self.week1_var,
            state='disabled',
            font=("Microsoft YaHei UI", 9),
            width=30
        )
        self.week1_combo.pack(fill=tk.X, pady=(0, 10))
        
        # 对比周选择
        tk.Label(
            week_select_card,
            text="对比周：",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            anchor=tk.W
        ).pack(fill=tk.X, pady=(0, 5))
        
        self.week2_combo = ttk.Combobox(
            week_select_card,
            textvariable=self.week2_var,
            state='disabled',
            font=("Microsoft YaHei UI", 9),
            width=30
        )
        self.week2_combo.pack(fill=tk.X)
        
        # 进度卡片
        progress_card_container, progress_card = self.create_card(parent)
        progress_card_container.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            progress_card,
            text="分析进度",
            font=("Microsoft YaHei UI", 13, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(anchor=tk.W, pady=(0, 10))
        
        self.progress_label = tk.Label(
            progress_card,
            text="等待开始...",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_muted'],
            anchor=tk.W
        )
        self.progress_label.pack(fill=tk.X, pady=(0, 8))
        
        self.progress_bar = ttk.Progressbar(
            progress_card,
            mode='determinate',
            maximum=100,
            style="Modern.Horizontal.TProgressbar",
            length=300
        )
        self.progress_bar.pack(fill=tk.X)
        self.progress_bar['value'] = 0
    
    def create_right_panel(self, parent):
        """创建右侧面板 - 数据可视化"""
        
        viz_card_container, viz_card = self.create_card(parent)
        viz_card_container.pack(fill=tk.BOTH, expand=True)

        # 标题行 + 复制按钮
        header_row = tk.Frame(viz_card, bg=self.colors['bg_card'])
        header_row.pack(fill=tk.X, pady=(0, 15))

        tk.Label(
            header_row,
            text="数据可视化",
            font=("Microsoft YaHei UI", 13, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT)

        self.copy_viz_btn = UnifiedButton(
            header_row,
            text="复制图片到剪贴板",
            command=self.copy_viz_to_clipboard,
            style="secondary",
            height=30,
            state="disabled"
        )
        self.copy_viz_btn.pack(side=tk.RIGHT)
        
        # 可视化容器
        self.viz_container = tk.Frame(viz_card, bg=self.colors['bg_card'])
        self.viz_container.pack(fill=tk.BOTH, expand=True)
        
        # 初始提示
        self.viz_placeholder = tk.Label(
            self.viz_container,
            text="上传数据文件后将显示可视化图表\n\n支持的指标：花费、点击数、展现数、交易额、投产比等",
            font=("Microsoft YaHei UI", 11),
            bg=self.colors['bg_card'],
            fg=self.colors['text_muted'],
            justify=tk.CENTER
        )
        self.viz_placeholder.pack(expand=True)
    
    def create_card(self, parent):
        """创建Razer 3D拟物化卡片"""
        card_3d = Razer3DCard(parent)
        content = card_3d.get_content()
        
        content_padded = tk.Frame(content, bg=self.colors['bg_card'])
        content_padded.pack(fill=tk.BOTH, expand=True, padx=20, pady=18)
        
        return card_3d, content_padded
    
    def select_file(self):
        """选择数据文件"""
        file_path = filedialog.askopenfilename(
            title="选择京准通快车数据文件",
            filetypes=[
                ("数据文件", "*.csv *.xlsx *.xls *.xlsm"),
                ("CSV 文件", "*.csv"),
                ("Excel 文件", "*.xlsx *.xls *.xlsm"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            self.current_file = file_path
            file_name = os.path.basename(file_path)
            self.file_label.config(
                text=f"✓ {file_name}",
                fg=self.colors['text_primary'],
                font=("Microsoft YaHei UI", 10, "bold")
            )
            
            # 识别周数据
            self.progress_label.config(text="正在识别周数据...")
            self.progress_bar['value'] = 50
            self.root.update()
            
            self.weeks_info = core.identify_weeks_in_data(file_path)
            
            if len(self.weeks_info) < 2:
                messagebox.showwarning("数据不足", "数据中少于2周，无法进行对比分析")
                self.current_file = None
                self.file_label.config(
                    text="尚未选择文件",
                    fg=self.colors['text_muted'],
                    font=("Microsoft YaHei UI", 10)
                )
                self.progress_label.config(text="等待开始...")
                self.progress_bar['value'] = 0
                return
            
            # 填充周选择下拉框（week_labels 按时间从早到晚）
            week_labels = [w['label'] for w in self.weeks_info]
            self.week1_combo['values'] = week_labels
            self.week2_combo['values'] = week_labels

            # 默认选择最近两周（最后两个元素）
            if len(week_labels) >= 1:
                self.week1_var.set(week_labels[-1])  # 最近一周
            if len(week_labels) >= 2:
                self.week2_var.set(week_labels[-2])  # 上一周
            
            # 启用下拉框
            self.week1_combo.config(state='readonly')
            self.week2_combo.config(state='readonly')
            
            self.progress_label.config(text=f"识别到 {len(self.weeks_info)} 周数据")
            self.progress_bar['value'] = 100
            
            self.analyze_btn.config_state("normal")
            self.clear_btn.config_state("normal")
    
    def clear_file(self):
        """清除文件"""
        self.current_file = None
        self.analysis_data = None
        self.weeks_info = []
        
        self.file_label.config(
            text="尚未选择文件",
            fg=self.colors['text_muted'],
            font=("Microsoft YaHei UI", 10)
        )
        
        # 清空并禁用周选择
        self.week1_var.set("")
        self.week2_var.set("")
        self.week1_combo['values'] = []
        self.week2_combo['values'] = []
        self.week1_combo.config(state='disabled')
        self.week2_combo.config(state='disabled')
        
        self.analyze_btn.config_state("disabled")
        self.clear_btn.config_state("disabled")
        self.progress_label.config(text="等待开始...")
        self.progress_bar['value'] = 0
        
        
        # 清除可视化
        self.clear_visualization()
    
    def clear_visualization(self):
        """清除可视化内容"""
        for widget in self.viz_container.winfo_children():
            widget.destroy()
        
        # 清空当前图像引用并禁用复制按钮
        self.current_figure = None
        if hasattr(self, 'copy_viz_btn'):
            self.copy_viz_btn.config_state("disabled")

        self.viz_placeholder = tk.Label(
            self.viz_container,
            text="上传数据文件后将显示可视化图表\n\n支持的指标：花费、点击数、展现数、交易额、投产比等",
            font=("Microsoft YaHei UI", 11),
            bg=self.colors['bg_card'],
            fg=self.colors['text_muted'],
            justify=tk.CENTER
        )
        self.viz_placeholder.pack(expand=True)
    
    def start_analysis(self):
        """开始分析"""
        if not self.current_file or self.processing:
            return
        
        if not CORE_AVAILABLE:
            messagebox.showerror("错误", "核心分析模块未加载！")
            return
        
        self.processing = True
        self.analyze_btn.config_state("disabled")
        self.clear_btn.config_state("disabled")
        self.select_btn.config_state("disabled")
        
        self.progress_label.config(text="正在分析中...")
        self.progress_bar['value'] = 0
        
        thread = threading.Thread(target=self._do_analysis, daemon=True)
        thread.start()
    
    def update_progress(self, value, text=None):
        """更新进度条"""
        self.progress_bar['value'] = value
        if text:
            self.progress_label.config(text=text)
        self.root.update()
    
    def _do_analysis(self):
        """执行分析（后台线程）"""
        try:
            self.update_progress(10, "正在读取数据...")
            
            # 获取选择的周编号
            week1_label = self.week1_var.get()
            week2_label = self.week2_var.get()
            
            # 从label中提取周编号
            week1_num = next((w['week_num'] for w in self.weeks_info if w['label'] == week1_label), 1)
            week2_num = next((w['week_num'] for w in self.weeks_info if w['label'] == week2_label), 2)
            
            # 调用核心分析模块
            result = core.analyze_kuaiche_data(
                file_path=self.current_file,
                week1_num=week1_num,
                week2_num=week2_num,
                progress_callback=self.update_progress,
                weeks_info=self.weeks_info
            )
            
            if result.get("success"):
                self.analysis_data = result
                
                self.root.after(0, lambda: self.progress_label.config(
                    text="✓ 分析完成！", 
                    fg=self.colors['success']
                ))
                self.root.after(0, lambda: self.progress_bar.__setitem__('value', 100))
                
                # 更新摘要
                self.root.after(0, lambda: self.update_summary(result))
                
                # 更新可视化
                self.root.after(0, lambda: self.update_visualization(result))
                
            else:
                error_msg = result.get("error", "未知错误")
                self.root.after(0, lambda: self.progress_label.config(
                    text="✗ 分析失败", 
                    fg=self.colors['danger']
                ))
                self.root.after(0, lambda: messagebox.showerror("分析失败", error_msg))
        
        except Exception as e:
            error_msg = str(e)
            import traceback
            error_trace = traceback.format_exc()
            print(error_trace)
            
            self.root.after(0, lambda: self.progress_label.config(
                text="✗ 发生异常", 
                fg=self.colors['danger']
            ))
            self.root.after(0, lambda: messagebox.showerror("异常", f"发生异常：{error_msg}"))
        
        finally:
            self.processing = False
            self.root.after(0, lambda: self.analyze_btn.config_state("normal"))
            self.root.after(0, lambda: self.clear_btn.config_state("normal"))
            self.root.after(0, lambda: self.select_btn.config_state("normal"))
    
    def update_summary(self, result):
        """更新数据摘要（已移除摘要文本区域，保留方法避免报错）"""
        pass
    
    def update_visualization(self, result):
        """更新数据可视化"""
        if not MATPLOTLIB_AVAILABLE:
            messagebox.showwarning("提示", "matplotlib 未安装，无法显示可视化图表")
            return
        
        # 清除现有内容
        for widget in self.viz_container.winfo_children():
            widget.destroy()
        
        # 创建图表
        fig = Figure(figsize=(7, 5.5), facecolor='white')
        fig.subplots_adjust(hspace=0.55, wspace=0.45, left=0.1, right=0.95, top=0.92, bottom=0.08)
        
        comparison = result.get('comparison', {})
        
        # 创建2x3的子图
        indicators = ['花费', '点击数', '展现数', '交易额', '投产比']
        positions = [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)]
        
        for i, (indicator, pos) in enumerate(zip(indicators[:5], positions)):
            ax = fig.add_subplot(2, 3, i + 1)
            
            week1_val = comparison.get(f'{indicator}_本周', 0)
            week2_val = comparison.get(f'{indicator}_上周', 0)
            change = comparison.get(f'{indicator}_变化', 0)
            
            # 柱状图
            bars = ax.bar(['上周', '本周'], [week2_val, week1_val], 
                          color=['#94a3b8', '#ff8c00'], width=0.55)
            
            # 调整x轴显示范围，让柱子间距适中
            ax.set_xlim(-0.7, 1.7)
            
            # 计算y轴上限，为标签留出空间
            max_val = max(week1_val, week2_val)
            ax.set_ylim(0, max_val * 1.15)  # 上方留出15%空间
            
            # 添加数值标签（字体与y轴刻度一致）
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:,.0f}' if indicator not in ['投产比'] else f'{height:.2f}',
                       ha='center', va='bottom', fontsize=8, family='sans-serif')
            
            # 标题和变化率
            color = '#10b981' if change >= 0 else '#ef4444'
            ax.set_title(f'{indicator}  ({change:+.1f}%)', fontsize=10.5, pad=8, color=color, weight='bold')
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            ax.set_axisbelow(True)
            
            # 设置刻度标签字体大小
            ax.tick_params(axis='both', labelsize=8)
            
        # 添加总览在第6个位置
        ax6 = fig.add_subplot(2, 3, 6)
        ax6.axis('off')
        
        # 判断趋势和颜色
        cost_change = comparison.get('花费_变化', 0)
        roi_change = comparison.get('投产比_变化', 0)
        
        # 标题
        ax6.text(0.5, 0.7, '整体表现：', ha='center', va='center',
                fontsize=11, transform=ax6.transAxes, weight='bold')
        
        # 投放趋势
        cost_text = '▲ 投放增长' if cost_change > 0 else '▼ 投放下降'
        cost_color = '#10b981' if cost_change > 0 else '#ef4444'
        ax6.text(0.5, 0.5, cost_text, ha='center', va='center',
                fontsize=10.5, transform=ax6.transAxes, color=cost_color)
        
        # ROI 趋势
        roi_text = '▲ ROI 提升' if roi_change > 0 else '▼ ROI 下降'
        roi_color = '#10b981' if roi_change > 0 else '#ef4444'
        ax6.text(0.5, 0.3, roi_text, ha='center', va='center',
                fontsize=10.5, transform=ax6.transAxes, color=roi_color)
        
        # 嵌入到 Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.viz_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 记录当前图像和画布，启用复制按钮
        self.current_figure = fig
        if hasattr(self, 'copy_viz_btn'):
            self.copy_viz_btn.config_state("normal")
    
    def toggle_theme(self):
        """切换主题（保留数据）"""
        from theme import get_theme
        current_theme = get_theme()
        new_dark_mode = not current_theme.is_dark
        
        # 保存数据
        saved_file = self.current_file
        saved_weeks = self.weeks_info.copy() if hasattr(self, 'weeks_info') else []
        
        self.root.destroy()
        import theme
        theme._global_theme = theme.RazerTheme(dark_mode=new_dark_mode)
        
        new_root = tk.Tk()
        app = JZTAnalyzerApp(new_root)
        
        # 恢复数据
        if saved_file:
            app.current_file = saved_file
            app.weeks_info = saved_weeks
            app.file_label.config(
                text=f"✓ {Path(saved_file).name}",
                fg=app.colors['text_primary'],
                font=("Microsoft YaHei UI", 10, "bold")
            )
            if saved_weeks:
                app.analyze_btn.config_state("normal")
                app.clear_btn.config_state("normal")
        
        new_root.mainloop()
    
    def back_to_launcher(self):
        """返回首页"""
        try:
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent.parent))
            from launcher import ToolLauncher
            
            self.root.destroy()
            
            new_root = tk.Tk()
            app = ToolLauncher(new_root)
            app.center_window()
            new_root.mainloop()
        except Exception as e:
            import traceback
            error_msg = f"返回首页失败：{e}\n\n{traceback.format_exc()}"
            print(error_msg)
            messagebox.showerror("返回失败", error_msg)

    def open_help(self):
        """显示使用说明（京准通数据分析）"""
        try:
            from tkinter import Canvas, Frame

            doc_path = Path(__file__).parent / "京准通数据分析使用说明.md"
            if not doc_path.exists():
                messagebox.showinfo("提示", f"未找到使用说明文件：\n{doc_path}")
                return

            raw = doc_path.read_text(encoding="utf-8", errors="ignore")

            help_win = tk.Toplevel(self.root)
            help_win.title("京准通数据分析工具 - 使用说明")
            help_win.configure(bg=self.colors['bg_main'])

            help_win.update_idletasks()
            w, h = 800, 600
            sw = help_win.winfo_screenwidth()
            sh = help_win.winfo_screenheight()
            x = (sw // 2) - (w // 2)
            y = (sh // 2) - (h // 2)
            help_win.geometry(f"{w}x{h}+{x}+{y}")
            help_win.transient(self.root)
            help_win.grab_set()

            canvas = Canvas(help_win, bg=self.colors['bg_main'], highlightthickness=0)
            scrollbar = tk.Scrollbar(help_win, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            inner = Frame(canvas, bg=self.colors['bg_main'])
            canvas.create_window((0, 0), window=inner, anchor='nw')

            def _on_configure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))

            inner.bind("<Configure>", _on_configure)

            def _on_mousewheel(event):
                if event.delta:
                    canvas.yview_scroll(int(-event.delta / 120), "units")

            canvas.bind_all("<MouseWheel>", _on_mousewheel)

            import re
            lines = raw.splitlines()
            for line in lines:
                stripped = line.rstrip()

                # 分隔线 ---
                if stripped.strip() == "---":
                    tk.Label(inner, text="", bg=self.colors['bg_main']).pack(pady=2)
                    continue

                if not stripped.strip():
                    tk.Label(inner, text="", bg=self.colors['bg_main']).pack()
                    continue

                m = re.match(r"^\s*(#{1,6})\s+(.*)$", stripped)
                if m:
                    level = len(m.group(1))
                    text = m.group(2)
                    text = text.replace("**", "").replace("`", "")
                    size = 16 if level <= 2 else 12
                    weight = "bold"
                    tk.Label(
                        inner,
                        text=text,
                        font=("Microsoft YaHei UI", size, weight),
                        bg=self.colors['bg_main'],
                        fg=self.colors['text_primary'],
                        anchor='w',
                        justify='left',
                        wraplength=760
                    ).pack(fill=tk.X, padx=12, pady=(6 if level <= 2 else 4, 2))
                    continue

                m = re.match(r"^\s*[-*+]\s+(.*)$", stripped)
                if m:
                    text = m.group(1).replace("**", "").replace("`", "")
                    text = "• " + text
                    tk.Label(
                        inner,
                        text=text,
                        font=("Microsoft YaHei UI", 10),
                        bg=self.colors['bg_main'],
                        fg=self.colors['text_primary'],
                        anchor='w',
                        justify='left',
                        wraplength=760
                    ).pack(fill=tk.X, padx=24, pady=1)
                    continue

                text = stripped.replace("**", "").replace("`", "")
                tk.Label(
                    inner,
                    text=text,
                    font=("Microsoft YaHei UI", 10),
                    bg=self.colors['bg_main'],
                    fg=self.colors['text_primary'],
                    anchor='w',
                    justify='left',
                    wraplength=760
                ).pack(fill=tk.X, padx=12, pady=1)

        except Exception as e:
            messagebox.showerror("错误", f"无法打开使用说明：{e}")

    def copy_viz_to_clipboard(self):
        """将当前可视化图片复制到系统剪贴板（Windows）"""
        if not PIL_AVAILABLE:
            messagebox.showwarning("提示", "复制失败：缺少 Pillow 依赖")
            return

        if not hasattr(self, 'current_figure') or self.current_figure is None:
            messagebox.showwarning("提示", "当前没有可复制的图表，请先完成分析")
            return

        try:
            import io as _io
            buf = _io.BytesIO()
            self.current_figure.savefig(buf, format='png', dpi=150)
            buf.seek(0)
            img = Image.open(buf)

            output = _io.BytesIO()
            img.convert("RGB").save(output, "BMP")
            data = output.getvalue()  # 保留完整的 BMP 文件
            output.close()

            # 使用内嵌的 Windows 剪贴板操作
            WindowsClipboard.copy_image_to_clipboard(data)

            messagebox.showinfo("成功", "已将可视化图片复制到剪贴板，可直接在 Word/微信 等处粘贴")
        except Exception as e:
            messagebox.showerror("错误", f"复制图片到剪贴板失败：{e}")


def main():
    """主函数"""
    try:
        root = tk.Tk()
        app = JZTAnalyzerApp(root)
        root.mainloop()
    except Exception as e:
        import traceback
        error_msg = f"启动失败：{e}\n\n{traceback.format_exc()}"
        print(error_msg)
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("京准通分析工具启动失败", error_msg)
        except:
            pass


if __name__ == "__main__":
    main()
