"""
视频处理工具
支持视频格式转换、压缩、提取封面等功能
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import os
from datetime import datetime
import threading
import subprocess
import json
import shutil
from zipfile import ZipFile, ZIP_DEFLATED
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import sys

# 添加父目录到路径以导入theme模块
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from theme import get_colors
from razer_ui import Razer3DCard, Razer3DRadio, Razer3DCheckbox
from unified_button import UnifiedButton
from theme_toggle import ThemeToggleButton


class VideoProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Centisky - 视频处理工具")
        self.root.geometry("1200x700")
        
        # 不设置窗口图标（用户不需要）
        
        # Razer风格配色 - 自动跟随系统深色/浅色模式
        self.colors = get_colors()
        
        self.root.configure(bg=self.colors['bg_main'])
        self.video_files = []
        self.output_dir = None
        self.output_dir_manual = False
        self.processing = False
        
        # 检查ffmpeg是否可用
        self.ffmpeg_available = self.check_ffmpeg()
        
        self.create_widgets()
        self.center_window()
        
    def center_window(self):
        """窗口居中"""
        self.root.update_idletasks()
        width = 1200
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def get_ffmpeg_path(self):
        """获取 ffmpeg 路径（优先使用内嵌版本）"""
        # 尝试内嵌的 ffmpeg（在程序目录下）
        if getattr(sys, 'frozen', False):
            # 打包后的路径
            base_path = Path(sys.executable).parent
        else:
            # 开发环境路径
            base_path = Path(__file__).parent.parent.parent
        
        bundled_ffmpeg = base_path / 'ffmpeg' / 'ffmpeg.exe'
        bundled_ffprobe = base_path / 'ffmpeg' / 'ffprobe.exe'
        
        if bundled_ffmpeg.exists() and bundled_ffprobe.exists():
            return str(bundled_ffmpeg), str(bundled_ffprobe)
        
        # 回退到系统 PATH 中的 ffmpeg
        return 'ffmpeg', 'ffprobe'
    
    def check_ffmpeg(self):
        """检查ffmpeg是否可用"""
        ffmpeg_cmd, _ = self.get_ffmpeg_path()
        try:
            result = subprocess.run(
                [ffmpeg_cmd, '-version'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def create_widgets(self):
        """创建界面组件"""
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
            text="视频处理工具",
            font=("Microsoft YaHei UI", 24, "bold"),
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary']
        )
        title_label.pack()
        
        # FFmpeg状态提示（放在标题下方，不遮挡）
        if not self.ffmpeg_available:
            warning_frame = tk.Frame(self.root, bg='#fff3cd')
            warning_frame.pack(fill=tk.X)
            
            warning_label = tk.Label(
                warning_frame,
                text="⚠ 未检测到 FFmpeg，部分功能不可用（格式转换、压缩、调整尺寸、分组打包需要 FFmpeg）",
                font=("Microsoft YaHei UI", 9),
                bg='#fff3cd',
                fg='#856404',
                padx=15,
                pady=8
            )
            warning_label.pack()
        
        # 主内容区域
        content_frame = tk.Frame(self.root, bg=self.colors['bg_main'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=60, pady=35)
        
        # 左右分栏容器
        columns_container = tk.Frame(content_frame, bg=self.colors['bg_main'])
        columns_container.pack(fill=tk.BOTH, expand=True)
        
        # 左侧区域（2/3宽度）- 操作区
        left_column = tk.Frame(columns_container, bg=self.colors['bg_main'])
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 9))
        
        # 文件选择卡片
        file_card_container, file_card = self.create_card(left_column)
        file_card_container.pack(fill=tk.X, pady=(0, 18))
        self.create_file_section(file_card)
        
        # 处理选项卡片
        options_card_container, options_card = self.create_card(left_column)
        options_card_container.pack(fill=tk.X, pady=(0, 18))
        self.create_options_section(options_card)
        
        # 右侧区域（1/3宽度）- 视频列表
        right_column = tk.Frame(columns_container, bg=self.colors['bg_main'])
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(9, 0))
        right_column.config(width=350)
        right_column.pack_propagate(False)
        
        # 视频列表卡片
        list_card_container, list_card = self.create_card(right_column)
        list_card_container.pack(fill=tk.BOTH, expand=True, pady=(0, 18))
        self.create_video_list(list_card)
    
    def create_card(self, parent):
        """创建Razer 3D拟物化卡片"""
        card_3d = Razer3DCard(parent)
        content = card_3d.get_content()
        
        content_padded = tk.Frame(content, bg=self.colors['bg_card'])
        content_padded.pack(fill=tk.BOTH, expand=True, padx=30, pady=22)
        
        return card_3d, content_padded
    
    def create_file_section(self, parent):
        """创建文件选择区域"""
        # 标题行
        title_row = tk.Frame(parent, bg=self.colors['bg_card'])
        title_row.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            title_row,
            text="添加视频文件",
            font=("Microsoft YaHei UI", 14, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT)
        
        # 右侧输出路径按钮
        output_btn_small = tk.Label(
            title_row,
            text="⚙",
            font=("Microsoft YaHei UI", 12),
            bg=self.colors['bg_card'],
            fg=self.colors['text_muted'],
            cursor="hand2"
        )
        output_btn_small.pack(side=tk.RIGHT)
        output_btn_small.bind("<Button-1>", lambda e: self.select_output_dir())
        output_btn_small.bind("<Enter>", lambda e: output_btn_small.config(fg=self.colors['primary']))
        output_btn_small.bind("<Leave>", lambda e: output_btn_small.config(fg=self.colors['text_muted']))
        
        self.output_path_label = tk.Label(
            title_row,
            text="📁 未选择",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_muted']
        )
        self.output_path_label.pack(side=tk.RIGHT, padx=(0, 5))
        
        # 按钮区域
        button_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        button_frame.pack(fill=tk.X)
        
        # 添加视频按钮（Razer 3D拟物化）
        add_btn = UnifiedButton(
            button_frame,
            text="添加视频",
            command=self.add_videos,
            style="primary",
            width=120,
            height=40
        )
        add_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 添加文件夹按钮（Razer 3D拟物化）
        add_folder_btn = UnifiedButton(
            button_frame,
            text="添加文件夹",
            command=self.add_folder,
            style="primary",
            width=120,
            height=40
        )
        add_folder_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 清空列表按钮（Razer 3D拟物化）
        clear_btn = UnifiedButton(
            button_frame,
            text="清空列表",
            command=self.clear_videos,
            style="secondary",
            width=100,
            height=40
        )
        clear_btn.pack(side=tk.LEFT)
    
    def create_flat_radio(self, parent, text, variable, value):
        """创建Razer 3D拟物化单选框"""
        radio = Razer3DRadio(parent, text, variable, value)
        return radio
    
    def create_options_section(self, parent):
        """创建处理选项区域"""
        tk.Label(
            parent,
            text="处理选项",
            font=("Microsoft YaHei UI", 14, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(anchor='w', pady=(0, 15))
        
        # 第一行：处理类型选择
        row1 = tk.Frame(parent, bg=self.colors['bg_card'])
        row1.pack(fill=tk.X, pady=(0, 15))
        
        type_frame = tk.Frame(row1, bg=self.colors['bg_card'])
        type_frame.pack(side=tk.LEFT)
        
        tk.Label(
            type_frame,
            text="处理类型：",
            font=("Microsoft YaHei UI", 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.operation_var = tk.StringVar(value="rename")
        
        self.create_flat_radio(type_frame, "标题处理", self.operation_var, "rename").pack(side=tk.LEFT, padx=(0, 8))
        self.create_flat_radio(type_frame, "视频归类", self.operation_var, "sort").pack(side=tk.LEFT, padx=(0, 8))
        self.create_flat_radio(type_frame, "视频压缩", self.operation_var, "compress").pack(side=tk.LEFT, padx=(0, 8))
        self.create_flat_radio(type_frame, "视频分组", self.operation_var, "pack").pack(side=tk.LEFT, padx=(0, 8))
        self.create_flat_radio(type_frame, "格式转换", self.operation_var, "convert").pack(side=tk.LEFT, padx=(0, 8))
        self.create_flat_radio(type_frame, "调整尺寸", self.operation_var, "resize").pack(side=tk.LEFT)
        
        # 第二行：格式选择（格式转换时显示）
        self.format_row = tk.Frame(parent, bg=self.colors['bg_card'])
        
        format_frame = tk.Frame(self.format_row, bg=self.colors['bg_card'])
        format_frame.pack(side=tk.LEFT)
        
        tk.Label(
            format_frame,
            text="输出格式：",
            font=("Microsoft YaHei UI", 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.format_var = tk.StringVar(value="mp4")
        
        self.create_flat_radio(format_frame, "MP4", self.format_var, "mp4").pack(side=tk.LEFT, padx=(0, 8))
        self.create_flat_radio(format_frame, "AVI", self.format_var, "avi").pack(side=tk.LEFT, padx=(0, 8))
        self.create_flat_radio(format_frame, "MOV", self.format_var, "mov").pack(side=tk.LEFT, padx=(0, 8))
        self.create_flat_radio(format_frame, "MKV", self.format_var, "mkv").pack(side=tk.LEFT)
        
        # 第三行：压缩设置（压缩时显示）
        self.compress_row = tk.Frame(parent, bg=self.colors['bg_card'])
        
        compress_frame = tk.Frame(self.compress_row, bg=self.colors['bg_card'])
        compress_frame.pack(side=tk.LEFT)
        
        tk.Label(
            compress_frame,
            text="目标大小：",
            font=("Microsoft YaHei UI", 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(
            compress_frame,
            text="压缩到",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.target_size_var = tk.StringVar(value="40")
        entry_border = tk.Frame(compress_frame, bg=self.colors['border_main'])
        entry_border.pack(side=tk.LEFT, padx=(0, 5))
        
        size_entry = tk.Entry(
            entry_border,
            textvariable=self.target_size_var,
            font=("Microsoft YaHei UI", 9),
            width=6,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            relief=tk.FLAT,
            borderwidth=0,
            justify='center'
        )
        size_entry.pack(padx=1, pady=1)
        
        # 单位选择（KB/MB）
        self.size_unit_var = tk.StringVar(value="mb")
        
        tk.Frame(compress_frame, width=5, bg=self.colors['bg_card']).pack(side=tk.LEFT)
        self.create_flat_radio(compress_frame, "KB", self.size_unit_var, "kb").pack(side=tk.LEFT, padx=(0, 4))
        self.create_flat_radio(compress_frame, "MB", self.size_unit_var, "mb").pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Label(
            compress_frame,
            text="以下",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT)
        
        # 监听单位变化，自动换算数值
        def on_unit_change(*args):
            try:
                current_value = float(self.target_size_var.get())
                current_unit = self.size_unit_var.get()
                
                if not hasattr(self, '_last_unit'):
                    self._last_unit = current_unit
                    return
                
                if self._last_unit != current_unit:
                    if current_unit == "mb" and self._last_unit == "kb":
                        new_value = current_value / 1024
                        self.target_size_var.set(f"{new_value:.2f}")
                    elif current_unit == "kb" and self._last_unit == "mb":
                        new_value = current_value * 1024
                        self.target_size_var.set(f"{int(new_value)}")
                    
                    self._last_unit = current_unit
            except ValueError:
                pass
        
        self.size_unit_var.trace_add("write", on_unit_change)
        
        # 第四行：尺寸调整设置（调整尺寸时显示）
        self.resize_row = tk.Frame(parent, bg=self.colors['bg_card'])
        
        resize_frame = tk.Frame(self.resize_row, bg=self.colors['bg_card'])
        resize_frame.pack(side=tk.LEFT)
        
        tk.Label(
            resize_frame,
            text="尺寸预设：",
            font=("Microsoft YaHei UI", 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.resize_preset_var = tk.StringVar(value="1080p")
        
        self.create_flat_radio(resize_frame, "720p (1280x720)", self.resize_preset_var, "720p").pack(side=tk.LEFT, padx=(0, 8))
        self.create_flat_radio(resize_frame, "1080p (1920x1080)", self.resize_preset_var, "1080p").pack(side=tk.LEFT, padx=(0, 8))
        self.create_flat_radio(resize_frame, "仅导出封面", self.resize_preset_var, "cover_only").pack(side=tk.LEFT)
        
        # 第五行：附加选项（提取封面）
        self.extract_row = tk.Frame(parent, bg=self.colors['bg_card'])
        
        extract_frame = tk.Frame(self.extract_row, bg=self.colors['bg_card'])
        extract_frame.pack(side=tk.LEFT)
        
        tk.Label(
            extract_frame,
            text="附加操作：",
            font=("Microsoft YaHei UI", 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # 提取封面复选框
        self.extract_cover_var = tk.IntVar(value=0)
        extract_check = tk.Checkbutton(
            extract_frame,
            text="同时提取视频封面",
            variable=self.extract_cover_var,
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['bg_card'],
            selectcolor=self.colors['bg_card'],
            cursor="hand2"
        )
        extract_check.pack(side=tk.LEFT, padx=(0, 15))
        
        # 封面格式选择
        tk.Label(
            extract_frame,
            text="格式：",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.cover_format_var = tk.StringVar(value="jpg")
        
        self.create_flat_radio(extract_frame, "JPG", self.cover_format_var, "jpg").pack(side=tk.LEFT, padx=(0, 5))
        self.create_flat_radio(extract_frame, "PNG", self.cover_format_var, "png").pack(side=tk.LEFT)
        
        # 第六行：标题处理设置（标题处理时显示）
        self.rename_row = tk.Frame(parent, bg=self.colors['bg_card'])
        
        rename_frame = tk.Frame(self.rename_row, bg=self.colors['bg_card'])
        rename_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            rename_frame,
            text="删除字符：",
            font=("Microsoft YaHei UI", 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # 输入框（默认空值，切换时自动填充）
        self.remove_chars_var = tk.StringVar(value="")
        chars_entry_border = tk.Frame(rename_frame, bg=self.colors['border_main'])
        chars_entry_border.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        chars_entry = tk.Entry(
            chars_entry_border,
            textvariable=self.remove_chars_var,
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            relief=tk.FLAT,
            borderwidth=0
        )
        chars_entry.pack(padx=1, pady=1, fill=tk.X)
        
        # 提示文字
        tk.Label(
            rename_frame,
            text="(多个用逗号分隔)",
            font=("Microsoft YaHei UI", 8),
            bg=self.colors['bg_card'],
            fg=self.colors['text_muted']
        ).pack(side=tk.LEFT)
        
        # 第七行：导出选项
        self.export_row = tk.Frame(parent, bg=self.colors['bg_card'])
        
        export_frame = tk.Frame(self.export_row, bg=self.colors['bg_card'])
        export_frame.pack(side=tk.LEFT)
        
        tk.Label(
            export_frame,
            text="附加操作：",
            font=("Microsoft YaHei UI", 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # 导出切换框（默认选中）
        self.export_titles_var = tk.IntVar(value=1)
        
        # 使用统一的复选框样式（Razer3DCheckbox）
        export_checkbox = Razer3DCheckbox(export_frame, "导出标题到 Excel", self.export_titles_var)
        export_checkbox.pack(side=tk.LEFT)
        
        # 第七行：视频归类设置（视频归类时显示）
        self.sort_row = tk.Frame(parent, bg=self.colors['bg_card'])
        
        sort_frame = tk.Frame(self.sort_row, bg=self.colors['bg_card'])
        sort_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            sort_frame,
            text="Excel 文件：",
            font=("Microsoft YaHei UI", 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Excel 文件状态显示
        self.excel_file_label = tk.Label(
            sort_frame,
            text="未选择",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_main'],
            fg=self.colors['text_muted'],
            anchor=tk.W,
            padx=12,
            pady=6
        )
        self.excel_file_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # 选择 Excel 按钮（Razer 3D拟物化）
        select_excel_btn = UnifiedButton(
            sort_frame,
            text="选择 Excel",
            command=self.select_excel_file,
            style="primary",
            width=110,
            height=32
        )
        select_excel_btn.pack(side=tk.LEFT)
        
        # Excel 文件路径（内部保存）
        self.excel_file_path = None
        
        # 第八行：视频分组设置（视频分组时显示）
        self.pack_row = tk.Frame(parent, bg=self.colors['bg_card'])
        
        pack_frame = tk.Frame(self.pack_row, bg=self.colors['bg_card'])
        pack_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 第一部分：Excel 模板
        tk.Label(
            pack_frame,
            text="Excel 模板：",
            font=("Microsoft YaHei UI", 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.template_file_label = tk.Label(
            pack_frame,
            text="未选择",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_main'],
            fg=self.colors['text_muted'],
            anchor=tk.W,
            padx=12,
            pady=6
        )
        self.template_file_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        select_template_btn = UnifiedButton(
            pack_frame,
            text="选择模板",
            command=self.select_template_file,
            style="primary",
            width=110,
            height=32
        )
        select_template_btn.pack(side=tk.LEFT)
        
        self.template_file_path = None
        
        # 第九行：分组设置
        self.pack_settings_row = tk.Frame(parent, bg=self.colors['bg_card'])
        
        pack_settings_frame = tk.Frame(self.pack_settings_row, bg=self.colors['bg_card'])
        pack_settings_frame.pack(side=tk.LEFT)
        
        tk.Label(
            pack_settings_frame,
            text="分组大小：",
            font=("Microsoft YaHei UI", 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(
            pack_settings_frame,
            text="每组不超过",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.pack_size_var = tk.StringVar(value="399")
        pack_entry_border = tk.Frame(pack_settings_frame, bg=self.colors['border_main'])
        pack_entry_border.pack(side=tk.LEFT, padx=(0, 5))
        
        pack_entry = tk.Entry(
            pack_entry_border,
            textvariable=self.pack_size_var,
            font=("Microsoft YaHei UI", 9),
            width=6,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            relief=tk.FLAT,
            borderwidth=0,
            justify='center'
        )
        pack_entry.pack(padx=1, pady=1)
        
        tk.Label(
            pack_settings_frame,
            text="MB",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        # 匹配列名称
        tk.Label(
            pack_settings_frame,
            text="匹配列：",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.match_column_var = tk.StringVar(value="【必填】视频文件名称")
        match_entry_border = tk.Frame(pack_settings_frame, bg=self.colors['border_main'])
        match_entry_border.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        match_entry = tk.Entry(
            match_entry_border,
            textvariable=self.match_column_var,
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            relief=tk.FLAT,
            borderwidth=0
        )
        match_entry.pack(padx=1, pady=1, fill=tk.X)
        
        # 开始处理按钮（Razer 3D拟物化）
        self.process_btn = UnifiedButton(
            parent,
            text="开始处理",
            command=self.start_processing,
            style="primary",
            width=140,
            height=45
        )
        self.process_btn.pack(anchor='w', pady=(15, 0))
        
        # 进度条
        self.progress_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_muted']
        )
        self.progress_label.pack(pady=(5, 5))
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            maximum=100,
            length=400
        )
        self.progress_bar.pack()
        
        # 监听处理类型变化
        self._current_mode = None
        
        def on_operation_change(*args):
            new_mode = self.operation_var.get()
            
            if self._current_mode == new_mode:
                return
            
            self._current_mode = new_mode
            
            # 隐藏所有选项行
            self.format_row.pack_forget()
            self.compress_row.pack_forget()
            self.resize_row.pack_forget()
            self.extract_row.pack_forget()
            self.rename_row.pack_forget()
            self.export_row.pack_forget()
            self.sort_row.pack_forget()
            self.pack_row.pack_forget()
            self.pack_settings_row.pack_forget()
            
            # 根据模式显示相应选项
            if new_mode == "convert":
                self.format_row.pack(fill=tk.X, pady=(0, 15), before=self.process_btn)
            elif new_mode == "compress":
                self.compress_row.pack(fill=tk.X, pady=(0, 15), before=self.process_btn)
            elif new_mode == "resize":
                self.resize_row.pack(fill=tk.X, pady=(0, 15), before=self.process_btn)
                self.extract_row.pack(fill=tk.X, pady=(0, 15), before=self.process_btn)
            elif new_mode == "sort":
                self.sort_row.pack(fill=tk.X, pady=(0, 15), before=self.process_btn)
            elif new_mode == "pack":
                self.pack_row.pack(fill=tk.X, pady=(0, 15), before=self.process_btn)
                self.pack_settings_row.pack(fill=tk.X, pady=(0, 15), before=self.process_btn)
            elif new_mode == "rename":
                # 切换到标题处理时，自动填充预设值
                if not self.remove_chars_var.get():
                    self.remove_chars_var.set("混剪,hunjian, ,")
                self.rename_row.pack(fill=tk.X, pady=(0, 15), before=self.process_btn)
                self.export_row.pack(fill=tk.X, pady=(0, 15), before=self.process_btn)
        
        self.operation_var.trace_add("write", on_operation_change)
        on_operation_change()
    
    def create_video_list(self, parent):
        """创建视频列表"""
        tk.Label(
            parent,
            text="视频列表",
            font=("Microsoft YaHei UI", 14, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(anchor='w', pady=(0, 15))
        
        # 列表框（带细边框，根据主题选择颜色）
        is_dark = self.colors.get('is_dark', True)
        border_color = '#333333' if is_dark else '#d0d0d0'
        list_border = tk.Frame(parent, bg=border_color)
        list_border.pack(fill=tk.BOTH, expand=True)
        
        list_frame = tk.Frame(list_border, bg=self.colors['bg_input'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 列表框背景根据主题设置
        is_dark = self.colors.get('is_dark', True)
        listbox_bg = '#1e1e1e' if is_dark else '#ffffff'
        
        self.video_listbox = tk.Listbox(
            list_frame,
            font=("Microsoft YaHei UI", 10),
            bg=listbox_bg,
            fg=self.colors['text_primary'],
            selectbackground=self.colors['primary'],
            selectforeground='black',
            yscrollcommand=scrollbar.set,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0
        )
        self.video_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.video_listbox.yview)
    
    def add_videos(self):
        """添加视频"""
        files = filedialog.askopenfilenames(
            title="选择视频",
            filetypes=[
                ("视频文件", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv *.mpg *.mpeg *.m4v"),
                ("所有文件", "*.*")
            ]
        )
        
        if files:
            if not self.output_dir_manual:
                last_file = files[-1]
                self.output_dir = os.path.dirname(last_file)
                self.output_path_label.config(text=f"📁 {os.path.basename(self.output_dir)}")
            
            for file in files:
                if file not in self.video_files:
                    self.video_files.append(file)
                    self.video_listbox.insert(tk.END, Path(file).name)
    
    def add_folder(self):
        """添加文件夹中的所有视频"""
        folder = filedialog.askdirectory(title="选择包含视频的文件夹")
        
        if folder:
            if not self.output_dir_manual:
                self.output_dir = folder
                self.output_path_label.config(text=f"📁 {os.path.basename(self.output_dir)}")
            
            video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.mpg', '.mpeg', '.m4v'}
            
            video_paths = []
            for file_path in Path(folder).rglob('*'):
                if file_path.suffix.lower() in video_extensions:
                    video_paths.append(file_path)
            
            import re
            def natural_sort_key(path):
                parts = re.split(r'(\d+)', str(path.name))
                return [int(part) if part.isdigit() else part.lower() for part in parts]
            
            video_paths.sort(key=natural_sort_key)
            
            added_count = 0
            for file_path in video_paths:
                file_str = str(file_path)
                if file_str not in self.video_files:
                    self.video_files.append(file_str)
                    self.video_listbox.insert(tk.END, file_path.name)
                    added_count += 1
            
            if added_count > 0:
                messagebox.showinfo("成功", f"已添加 {added_count} 个视频")
            else:
                messagebox.showinfo("提示", "文件夹中没有找到视频文件")
    
    def clear_videos(self):
        """清空视频列表"""
        self.video_files.clear()
        self.video_listbox.delete(0, tk.END)
    
    def select_excel_file(self):
        """选择 Excel 文件"""
        file_path = filedialog.askopenfilename(
            title="选择 Excel 文件",
            filetypes=[
                ("Excel 文件", "*.xlsx *.xls"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            self.excel_file_path = file_path
            self.excel_file_label.config(
                text=f"✓ {Path(file_path).name}",
                fg=self.colors['text_primary']
            )
    
    def select_template_file(self):
        """选择 Excel 模板文件"""
        file_path = filedialog.askopenfilename(
            title="选择 Excel 模板文件",
            filetypes=[
                ("Excel 文件", "*.xlsx *.xls"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            self.template_file_path = file_path
            self.template_file_label.config(
                text=f"✓ {Path(file_path).name}",
                fg=self.colors['text_primary']
            )
    
    def select_output_dir(self):
        """选择输出目录"""
        directory = filedialog.askdirectory(
            title="选择输出目录",
            initialdir=self.output_dir if self.output_dir else os.path.expanduser("~")
        )
        
        if directory:
            self.output_dir = directory
            self.output_dir_manual = True
            self.output_path_label.config(text=f"📁 {os.path.basename(self.output_dir)}")
    
    def start_processing(self):
        """开始处理"""
        if not self.ffmpeg_available:
            messagebox.showerror("错误", "FFmpeg 未安装或不可用！\n\n请安装 FFmpeg 后重试。")
            return
        
        if not self.video_files:
            messagebox.showwarning("提示", "请先添加视频")
            return
        
        if not self.output_dir:
            messagebox.showwarning("提示", "请选择输出目录")
            return
        
        if self.processing:
            messagebox.showwarning("提示", "正在处理中，请等待...")
            return
        
        operation = self.operation_var.get()
        
        # 在新线程中处理
        self.processing = True
        self.process_btn.config_state("disabled")
        self.progress_frame.pack(fill=tk.X, pady=(15, 0))
        
        thread = threading.Thread(target=self._do_processing, args=(operation,), daemon=True)
        thread.start()
    
    def _do_processing(self, operation):
        """执行处理（后台线程）"""
        try:
            if operation == "convert":
                self.convert_videos()
            elif operation == "compress":
                self.compress_videos()
            elif operation == "resize":
                self.resize_videos()
            elif operation == "sort":
                self.sort_videos()
            elif operation == "pack":
                self.pack_videos()
            elif operation == "rename":
                self.rename_videos()
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("错误", f"处理失败: {e}"))
        finally:
            self.processing = False
            self.root.after(0, lambda: self.process_btn.config_state("normal"))
            self.root.after(0, lambda: self.progress_frame.pack_forget())
    
    def update_progress(self, current, total, text=""):
        """更新进度"""
        progress = int((current / total) * 100)
        self.root.after(0, lambda: self.progress_bar.config(value=progress))
        if text:
            self.root.after(0, lambda: self.progress_label.config(text=text))
        self.root.after(0, lambda: self.root.update())
    
    def get_video_info(self, video_path):
        """获取视频信息"""
        try:
            _, ffprobe_cmd = self.get_ffmpeg_path()
            cmd = [
                ffprobe_cmd,
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_streams',
                video_path
            ]
            
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            if result.returncode == 0:
                info = json.loads(result.stdout.decode('utf-8'))
                for stream in info.get('streams', []):
                    if stream.get('codec_type') == 'video':
                        return {
                            'width': stream.get('width', 0),
                            'height': stream.get('height', 0),
                            'duration': float(stream.get('duration', 0))
                        }
        except:
            pass
        
        return {'width': 0, 'height': 0, 'duration': 0}
    
    def convert_videos(self):
        """格式转换"""
        format_ext = self.format_var.get()
        output_folder_name = f"格式转换_{format_ext.upper()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        final_output_dir = Path(self.output_dir) / output_folder_name
        final_output_dir.mkdir(parents=True, exist_ok=True)
        
        total = len(self.video_files)
        success_count = 0
        error_count = 0
        
        for idx, video_path in enumerate(self.video_files, 1):
            try:
                self.update_progress(idx - 0.5, total, f"正在转换 {idx}/{total}: {Path(video_path).name}")
                
                output_filename = Path(video_path).stem + f".{format_ext}"
                output_path = final_output_dir / output_filename
                
                ffmpeg_cmd, _ = self.get_ffmpeg_path()
                cmd = [
                    ffmpeg_cmd,
                    '-i', video_path,
                    '-c:v', 'libx264',
                    '-c:a', 'aac',
                    '-y',
                    str(output_path)
                ]
                
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                
                if result.returncode == 0:
                    success_count += 1
                else:
                    error_count += 1
                
                self.update_progress(idx, total)
                
            except Exception as e:
                error_count += 1
                print(f"处理 {video_path} 失败: {e}")
        
        if error_count == 0:
            self.root.after(0, lambda: messagebox.showinfo("成功", 
                f"已成功转换 {success_count} 个视频为 {format_ext.upper()} 格式！\n保存在：{output_folder_name}"))
        else:
            self.root.after(0, lambda: messagebox.showwarning("完成", 
                f"成功: {success_count} 个\n失败: {error_count} 个\n保存在：{output_folder_name}"))
    
    def compress_videos(self):
        """视频压缩"""
        try:
            target_size_value = float(self.target_size_var.get())
            if self.size_unit_var.get() == "kb":
                target_size_bytes = int(target_size_value * 1024)
            else:
                target_size_bytes = int(target_size_value * 1024 * 1024)
        except ValueError:
            self.root.after(0, lambda: messagebox.showerror("错误", "请输入有效的文件大小"))
            return
        
        output_folder_name = f"视频压缩_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        final_output_dir = Path(self.output_dir) / output_folder_name
        final_output_dir.mkdir(parents=True, exist_ok=True)
        
        total = len(self.video_files)
        success_count = 0
        error_count = 0
        skipped_count = 0
        
        for idx, video_path in enumerate(self.video_files, 1):
            try:
                self.update_progress(idx - 0.5, total, f"正在检查 {idx}/{total}: {Path(video_path).name}")
                
                output_filename = Path(video_path).stem + ".mp4"
                output_path = final_output_dir / output_filename
                
                # 检查原视频大小
                original_size = Path(video_path).stat().st_size
                
                # 如果已经小于目标大小，直接复制
                if original_size <= target_size_bytes:
                    self.update_progress(idx - 0.3, total, f"跳过 {idx}/{total}: {Path(video_path).name} (已满足大小)")
                    shutil.copy2(video_path, output_path)
                    skipped_count += 1
                    success_count += 1
                    self.update_progress(idx, total)
                    continue
                
                # 需要压缩
                self.update_progress(idx - 0.5, total, f"正在压缩 {idx}/{total}: {Path(video_path).name}")
                
                # 获取视频时长
                video_info = self.get_video_info(video_path)
                duration = video_info.get('duration', 0)
                
                ffmpeg_cmd, _ = self.get_ffmpeg_path()
                
                if duration > 0:
                    # 计算目标比特率 (bytes * 8 / duration)
                    target_bitrate = int((target_size_bytes * 8) / duration)
                    # 减去音频比特率 (128k)
                    target_video_bitrate = max(target_bitrate - 128000, 128000)
                    
                    cmd = [
                        ffmpeg_cmd,
                        '-i', video_path,
                        '-b:v', str(target_video_bitrate),
                        '-maxrate', str(target_video_bitrate),
                        '-bufsize', str(target_video_bitrate * 2),
                        '-c:v', 'libx264',
                        '-c:a', 'aac',
                        '-b:a', '128k',
                        '-y',
                        str(output_path)
                    ]
                else:
                    # 无法获取时长，使用默认压缩
                    cmd = [
                        ffmpeg_cmd,
                        '-i', video_path,
                        '-c:v', 'libx264',
                        '-crf', '28',
                        '-c:a', 'aac',
                        '-b:a', '128k',
                        '-y',
                        str(output_path)
                    ]
                
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                
                if result.returncode == 0:
                    success_count += 1
                else:
                    error_count += 1
                
                self.update_progress(idx, total)
                
            except Exception as e:
                error_count += 1
                print(f"处理 {video_path} 失败: {e}")
        
        # 显示结果
        msg = f"处理完成！\n\n"
        if success_count - skipped_count > 0:
            msg += f"压缩：{success_count - skipped_count} 个\n"
        if skipped_count > 0:
            msg += f"跳过：{skipped_count} 个（已满足大小）\n"
        if error_count > 0:
            msg += f"失败：{error_count} 个\n"
        msg += f"\n保存在：{output_folder_name}"
        
        if error_count == 0:
            self.root.after(0, lambda: messagebox.showinfo("成功", msg))
        else:
            self.root.after(0, lambda: messagebox.showwarning("完成", msg))
    
    def resize_videos(self):
        """调整视频尺寸"""
        preset = self.resize_preset_var.get()
        
        # 根据预设获取尺寸
        if preset == "720p":
            target_width = 1280
            target_height = 720
            resize_video = True
        elif preset == "1080p":
            target_width = 1920
            target_height = 1080
            resize_video = True
        else:  # cover_only
            resize_video = False
            target_width = 0
            target_height = 0
        
        # 是否提取封面
        extract_cover = self.extract_cover_var.get() == 1
        cover_format = self.cover_format_var.get()
        
        # 如果仅导出封面
        if preset == "cover_only":
            if not extract_cover:
                self.root.after(0, lambda: messagebox.showwarning("提示", "请勾选'同时提取视频封面'选项"))
                return
            
            # 只提取封面
            output_folder_name = f"提取封面_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            final_output_dir = Path(self.output_dir) / output_folder_name
            final_output_dir.mkdir(parents=True, exist_ok=True)
            
            total = len(self.video_files)
            success_count = 0
            error_count = 0
            
            for idx, video_path in enumerate(self.video_files, 1):
                try:
                    self.update_progress(idx - 0.5, total, f"正在提取封面 {idx}/{total}: {Path(video_path).name}")
                    
                    cover_filename = Path(video_path).stem + f"_cover.{cover_format}"
                    cover_path = final_output_dir / cover_filename
                    
                    ffmpeg_cmd, _ = self.get_ffmpeg_path()
                    cover_cmd = [
                        ffmpeg_cmd,
                        '-i', video_path,
                        '-ss', '00:00:01',
                        '-vframes', '1',
                        '-y',
                        str(cover_path)
                    ]
                    
                    result = subprocess.run(
                        cover_cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                    )
                    
                    if result.returncode == 0:
                        success_count += 1
                    else:
                        error_count += 1
                    
                    self.update_progress(idx, total)
                    
                except Exception as e:
                    error_count += 1
                    print(f"处理 {video_path} 失败: {e}")
            
            # 显示结果
            msg = f"成功提取 {success_count} 个封面"
            if error_count > 0:
                msg += f"\n失败 {error_count} 个"
            msg += f"\n保存在：{output_folder_name}"
            
            if error_count == 0:
                self.root.after(0, lambda: messagebox.showinfo("成功", msg))
            else:
                self.root.after(0, lambda: messagebox.showwarning("完成", msg))
            return
        
        # 调整尺寸模式
        output_folder_name = f"调整尺寸_{target_width}x{target_height}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        final_output_dir = Path(self.output_dir) / output_folder_name
        final_output_dir.mkdir(parents=True, exist_ok=True)
        
        total = len(self.video_files)
        success_count = 0
        error_count = 0
        
        for idx, video_path in enumerate(self.video_files, 1):
            try:
                self.update_progress(idx - 0.5, total, f"正在调整尺寸 {idx}/{total}: {Path(video_path).name}")
                
                output_filename = Path(video_path).stem + f"_{target_width}x{target_height}.mp4"
                output_path = final_output_dir / output_filename
                
                # 使用ffmpeg调整尺寸
                ffmpeg_cmd, _ = self.get_ffmpeg_path()
                cmd = [
                    ffmpeg_cmd,
                    '-i', video_path,
                    '-vf', f'scale={target_width}:{target_height}',
                    '-c:a', 'copy',
                    '-y',
                    str(output_path)
                ]
                
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                
                if result.returncode == 0:
                    success_count += 1
                    
                    # 如果需要提取封面
                    if extract_cover:
                        cover_filename = Path(video_path).stem + f"_cover.{cover_format}"
                        cover_path = final_output_dir / cover_filename
                        
                        ffmpeg_cmd, _ = self.get_ffmpeg_path()
                        cover_cmd = [
                            ffmpeg_cmd,
                            '-i', video_path,
                            '-ss', '00:00:01',
                            '-vframes', '1',
                            '-y',
                            str(cover_path)
                        ]
                        
                        subprocess.run(
                            cover_cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                        )
                else:
                    error_count += 1
                
                self.update_progress(idx, total)
                
            except Exception as e:
                error_count += 1
                print(f"处理 {video_path} 失败: {e}")
        
        # 显示结果
        msg = f"成功调整 {success_count} 个视频尺寸"
        if extract_cover:
            msg += f"\n同时提取了 {success_count} 个封面"
        if error_count > 0:
            msg += f"\n失败 {error_count} 个"
        msg += f"\n保存在：{output_folder_name}"
        
        if error_count == 0:
            self.root.after(0, lambda: messagebox.showinfo("成功", msg))
        else:
            self.root.after(0, lambda: messagebox.showwarning("完成", msg))
    
    def extract_covers(self):
        """提取视频封面"""
        cover_format = self.cover_format_var.get()
        
        try:
            min_width = int(self.min_width_var.get())
            min_height = int(self.min_height_var.get())
        except ValueError:
            self.root.after(0, lambda: messagebox.showerror("错误", "请输入有效的尺寸值"))
            return
        
        output_folder_name = f"提取封面_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        final_output_dir = Path(self.output_dir) / output_folder_name
        final_output_dir.mkdir(parents=True, exist_ok=True)
        
        total = len(self.video_files)
        success_count = 0
        error_count = 0
        skipped_count = 0
        
        for idx, video_path in enumerate(self.video_files, 1):
            try:
                self.update_progress(idx - 0.5, total, f"正在提取封面 {idx}/{total}: {Path(video_path).name}")
                
                # 获取视频尺寸
                video_info = self.get_video_info(video_path)
                video_width = video_info.get('width', 0)
                video_height = video_info.get('height', 0)
                
                # 检查尺寸是否满足要求
                if video_width < min_width or video_height < min_height:
                    skipped_count += 1
                    print(f"跳过 {Path(video_path).name}: 尺寸不足 ({video_width}x{video_height})")
                    self.update_progress(idx, total)
                    continue
                
                output_filename = Path(video_path).stem + f"_cover.{cover_format}"
                output_path = final_output_dir / output_filename
                
                # 提取第1秒的帧作为封面
                ffmpeg_cmd, _ = self.get_ffmpeg_path()
                cmd = [
                    ffmpeg_cmd,
                    '-i', video_path,
                    '-ss', '00:00:01',
                    '-vframes', '1',
                    '-y',
                    str(output_path)
                ]
                
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                
                if result.returncode == 0:
                    success_count += 1
                else:
                    error_count += 1
                
                self.update_progress(idx, total)
                
            except Exception as e:
                error_count += 1
                print(f"处理 {video_path} 失败: {e}")
        
        # 显示结果
        msg = f"成功提取 {success_count} 个封面"
        if skipped_count > 0:
            msg += f"\n跳过 {skipped_count} 个（尺寸不足 {min_width}x{min_height}）"
        if error_count > 0:
            msg += f"\n失败 {error_count} 个"
        msg += f"\n保存在：{output_folder_name}"
        
        if error_count == 0:
            self.root.after(0, lambda: messagebox.showinfo("成功", msg))
        else:
            self.root.after(0, lambda: messagebox.showwarning("完成", msg))
    
    def rename_videos(self):
        """标题处理（重命名+导出）"""
        # 获取要删除的字符列表
        remove_chars_str = self.remove_chars_var.get()
        
        # 解析要删除的字符（按逗号分隔）
        remove_chars_list = []
        if remove_chars_str.strip():
            # 不要对每个字符做strip，否则会把空格字符本身去掉
            remove_chars_list = [char for char in remove_chars_str.split(',') if char != '']
        
        total = len(self.video_files)
        success_count = 0
        error_count = 0
        rename_info = []
        processed_titles = []  # 存储处理后的标题
        
        for idx, video_path in enumerate(self.video_files, 1):
            try:
                self.update_progress(idx - 0.5, total, f"正在处理 {idx}/{total}: {Path(video_path).name}")
                
                # 获取原文件名（不含扩展名）和扩展名
                file_path = Path(video_path)
                original_stem = file_path.stem
                extension = file_path.suffix
                
                # 逐个删除指定字符
                new_stem = original_stem
                if remove_chars_list:
                    for remove_char in remove_chars_list:
                        new_stem = new_stem.replace(remove_char, '')
                
                # 如果文件名有变化，进行重命名
                if new_stem != original_stem:
                    # 生成新文件名
                    new_filename = new_stem + extension
                    new_path = file_path.parent / new_filename
                    
                    # 如果新文件名已存在，添加数字后缀
                    counter = 1
                    while new_path.exists():
                        new_filename = f"{new_stem}_{counter}{extension}"
                        new_path = file_path.parent / new_filename
                        counter += 1
                    
                    # 重命名文件
                    file_path.rename(new_path)
                    
                    rename_info.append(f"{original_stem} → {new_stem}")
                    success_count += 1
                    
                    # 更新列表中的路径
                    self.video_files[idx - 1] = str(new_path)
                    
                    # 记录处理后的标题
                    processed_titles.append(new_stem)
                else:
                    # 即使没有重命名，也记录原标题
                    processed_titles.append(original_stem)
                
                self.update_progress(idx, total)
                
            except Exception as e:
                error_count += 1
                print(f"处理 {video_path} 失败: {e}")
                # 记录原标题（即使处理失败）
                processed_titles.append(Path(video_path).stem)
        
        # 更新视频列表显示（确保在主线程中执行）
        def update_list():
            self.video_listbox.delete(0, tk.END)
            for video_path in self.video_files:
                self.video_listbox.insert(tk.END, Path(video_path).name)
        
        self.root.after(0, update_list)
        
        # 如果勾选了导出标题
        if self.export_titles_var.get() == 1:
            try:
                self.update_progress(95, 100, "正在导出标题到 Excel...")
                
                # 创建 Excel 文件
                from openpyxl import Workbook
                wb = Workbook()
                ws = wb.active
                ws.title = "视频标题"
                
                # 写入标题到 A 列
                for i, title in enumerate(processed_titles, start=1):
                    ws[f'A{i}'] = title
                
                # 保存到输出目录
                if self.output_dir:
                    excel_filename = f"视频标题_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                    excel_path = Path(self.output_dir) / excel_filename
                else:
                    # 如果没有输出目录，保存到第一个视频所在目录
                    excel_filename = f"视频标题_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                    excel_path = Path(self.video_files[0]).parent / excel_filename
                
                wb.save(excel_path)
                
                export_msg = f"\n\n已导出标题到：{excel_filename}"
            except ImportError:
                export_msg = "\n\n导出失败：openpyxl 未安装"
            except Exception as e:
                export_msg = f"\n\n导出失败：{e}"
        else:
            export_msg = ""
        
        # 显示结果
        msg = f"处理完成！\n\n"
        if success_count > 0:
            msg += f"重命名：{success_count} 个视频\n"
        if error_count > 0:
            msg += f"失败：{error_count} 个\n"
        if success_count == 0 and error_count == 0:
            msg += "没有需要重命名的视频\n"
        
        # 显示部分重命名信息（最多5条）
        if rename_info:
            msg += "\n重命名示例："
            for info in rename_info[:5]:
                msg += f"\n  {info}"
            if len(rename_info) > 5:
                msg += f"\n  ... 还有 {len(rename_info) - 5} 个"
        
        msg += export_msg
        
        if error_count == 0:
            self.root.after(0, lambda: messagebox.showinfo("成功", msg))
        else:
            self.root.after(0, lambda: messagebox.showwarning("完成", msg))
    
    def refresh_video_list(self):
        """刷新视频列表显示"""
        self.video_listbox.delete(0, tk.END)
        for video_path in self.video_files:
            self.video_listbox.insert(tk.END, Path(video_path).name)
    
    def pack_videos(self):
        """视频分组打包"""
        if not self.template_file_path:
            self.root.after(0, lambda: messagebox.showwarning("提示", "请先选择 Excel 模板"))
            return
        
        try:
            pack_size_mb = int(self.pack_size_var.get())
            if pack_size_mb <= 0:
                self.root.after(0, lambda: messagebox.showerror("错误", "分组大小必须大于0"))
                return
        except ValueError:
            self.root.after(0, lambda: messagebox.showerror("错误", "请输入有效的分组大小"))
            return
        
        pack_size_bytes = pack_size_mb * 1024 * 1024
        match_column = self.match_column_var.get()
        
        self.update_progress(5, 100, "正在预处理视频...")
        
        try:
            # 创建临时目录
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            temp_dir = Path(self.output_dir) / f"_temp_videos_{timestamp}"
            temp_dir.mkdir(exist_ok=True)
            
            # 预处理视频（720p规则）
            processed_videos = []
            total = len(self.video_files)
            
            for idx, video_path in enumerate(self.video_files, 1):
                self.update_progress(5 + (idx / total) * 40, 100, f"预处理 {idx}/{total}: {Path(video_path).name}")
                
                try:
                    # 获取视频尺寸
                    video_info = self.get_video_info(video_path)
                    w = video_info.get('width', 0)
                    h = video_info.get('height', 0)
                    
                    output_path = temp_dir / Path(video_path).name
                    
                    # 判断是否需要缩放
                    scale_expr = self.get_scale_expr(w, h)
                    
                    if scale_expr:
                        # 需要缩放
                        ffmpeg_cmd, _ = self.get_ffmpeg_path()
                        cmd = [
                            ffmpeg_cmd,
                            '-y', '-i', str(video_path),
                            '-vf', scale_expr,
                            '-c:v', 'libx264',
                            '-preset', 'veryfast',
                            '-crf', '23',
                            '-c:a', 'copy',
                            str(output_path)
                        ]
                        
                        subprocess.run(
                            cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                        )
                    else:
                        # 不需要缩放，直接复制
                        shutil.copy2(video_path, output_path)
                    
                    # 获取文件大小
                    if output_path.exists():
                        size = output_path.stat().st_size
                        processed_videos.append((output_path, size))
                except Exception as e:
                    print(f"预处理失败 {Path(video_path).name}: {e}")
            
            if not processed_videos:
                self.root.after(0, lambda: messagebox.showerror("错误", "没有成功预处理的视频"))
                shutil.rmtree(temp_dir, ignore_errors=True)
                return
            
            self.update_progress(50, 100, "正在分组...")
            
            # 使用最佳适应递减算法分组
            groups, group_sizes = self.best_fit_decreasing(processed_videos, pack_size_bytes)
            
            self.update_progress(60, 100, f"分为 {len(groups)} 组，正在打包...")
            
            # 创建输出文件夹
            output_folder_name = f"视频分组打包_{timestamp}"
            final_output_dir = Path(self.output_dir) / output_folder_name
            final_output_dir.mkdir(exist_ok=True)
            
            # 为每组创建ZIP
            for group_idx, (group, group_size) in enumerate(zip(groups, group_sizes), 1):
                self.update_progress(60 + (group_idx / len(groups)) * 35, 100, 
                    f"打包第 {group_idx}/{len(groups)} 组...")
                
                # 获取该组的视频名称
                video_names = {p.name for p, _ in group}
                video_stems = {p.stem for p, _ in group}
                
                # 过滤 Excel 模板
                try:
                    filtered_excel = self.filter_excel_template(
                        self.template_file_path, 
                        video_names, 
                        video_stems,
                        match_column
                    )
                except Exception as e:
                    print(f"Excel 过滤失败: {e}，使用原模板")
                    filtered_excel = None
                
                # 创建 ZIP
                zip_name = f"商品讲解视频打包_{timestamp}_组{group_idx:02d}.zip"
                zip_path = final_output_dir / zip_name
                
                with ZipFile(zip_path, 'w', compression=ZIP_DEFLATED) as zf:
                    # 添加 Excel（使用原文件名）
                    if filtered_excel:
                        zf.write(filtered_excel, arcname=Path(self.template_file_path).name)
                        os.remove(filtered_excel)
                    else:
                        zf.write(self.template_file_path, arcname=Path(self.template_file_path).name)
                    
                    # 添加视频
                    for video_path, _ in group:
                        zf.write(video_path, arcname=video_path.name)
            
            # 清理临时目录
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            self.update_progress(100, 100, "完成！")
            
            # 显示结果
            msg = f"分组打包完成！\n\n共分为 {len(groups)} 组\n"
            for i, sz in enumerate(group_sizes, 1):
                msg += f"组{i}: {self.human_size(sz)}\n"
            msg += f"\n保存在：{output_folder_name}"
            
            self.root.after(0, lambda: messagebox.showinfo("成功", msg))
            
        except ImportError:
            self.root.after(0, lambda: messagebox.showerror("错误", "pandas 模块未安装！\n\n请先安装 pandas：pip install pandas"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("错误", f"读取 Excel 文件失败：{e}"))
    
    def toggle_theme(self):
        """切换主题（尽量保留当前状态）"""
        from theme import get_theme
        current_theme = get_theme()
        new_dark_mode = not current_theme.is_dark

        # 若正在处理，先确认
        if self.processing:
            if not messagebox.askyesno("确认", "当前有任务在执行，切换主题会重启窗口，确定继续吗？"):
                return

        # 保存当前基本状态
        saved_videos = list(self.video_files)
        saved_output_dir = self.output_dir
        saved_output_dir_manual = self.output_dir_manual
        saved_operation = self.operation_var.get() if hasattr(self, 'operation_var') else None

        # 关闭当前窗口并切换全局主题
        self.root.destroy()
        import theme
        theme._global_theme = theme.RazerTheme(dark_mode=new_dark_mode)

        # 重建窗口
        new_root = tk.Tk()
        app = VideoProcessorApp(new_root)

        # 恢复状态
        app.video_files = saved_videos
        app.output_dir = saved_output_dir
        app.output_dir_manual = saved_output_dir_manual
        if saved_operation is not None:
            app.operation_var.set(saved_operation)

        # 恢复列表与输出路径显示
        app.refresh_video_list()
        if app.output_dir:
            app.output_path_label.config(text=f"📁 {os.path.basename(app.output_dir)}")

        new_root.mainloop()

    def open_help(self):
        """显示使用说明（视频处理工具）"""
        try:
            from tkinter import Canvas, Frame

            doc_path = Path(__file__).parent / "视频处理工具使用说明.md"
            if not doc_path.exists():
                messagebox.showinfo("提示", f"未找到使用说明文件：\n{doc_path}")
                return

            raw = doc_path.read_text(encoding="utf-8", errors="ignore")

            help_win = tk.Toplevel(self.root)
            help_win.title("视频处理工具 - 使用说明")
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

    def back_to_launcher(self):
        """返回首页"""
        if self.processing:
            if not messagebox.askyesno("确认", "正在处理中，确定要返回吗？"):
                return
        
        self.root.destroy()
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from launcher import ToolLauncher
        new_root = tk.Tk()
        app = ToolLauncher(new_root)
        new_root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoProcessorApp(root)
    root.mainloop()
