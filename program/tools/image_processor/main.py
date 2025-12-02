"""
图片综合处理工具
支持批量裁剪、缩放、水印、格式转换等功能
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
from datetime import datetime
import sys

# 添加父目录到路径以导入theme模块
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from theme import get_colors
from razer_ui import Razer3DCard, Razer3DRadio
from unified_button import UnifiedButton
from folder_multi_select import select_folders


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Centisky - 图片处理工具")
        self.root.geometry("1200x700")
        
        # 不设置窗口图标（用户不需要）
        
        # Razer风格配色 - 自动跟随系统深色/浅色模式
        self.colors = get_colors()
        
        self.root.configure(bg=self.colors['bg_main'])
        
        # 使用分组字典存储图片：{组名: [文件列表]}
        self.image_groups = {"默认分组": []}
        # 每个分组的输出路径：{组名: 输出路径}
        self.group_output_dirs = {"默认分组": None}
        self.current_group = "默认分组"
        
        # 全局输出路径（用于手动设置）
        self.output_dir = None
        self.output_dir_manual = False
        
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
        
    def create_widgets(self):
        """创建界面组件"""
        # 主内容区域
        content_frame = tk.Frame(self.root, bg=self.colors['bg_main'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=35)
        
        # 左右分栏容器
        columns_container = tk.Frame(content_frame, bg=self.colors['bg_main'])
        columns_container.pack(fill=tk.BOTH, expand=True)
        
        # 左侧区域（2/3宽度）- 操作区
        left_column = tk.Frame(columns_container, bg=self.colors['bg_main'])
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 9))
        left_column.config(width=500)
        left_column.pack_propagate(False)
        
        # 文件选择卡片
        file_card_container, file_card = self.create_card(left_column)
        file_card_container.pack(fill=tk.X, pady=(0, 18))
        self.create_file_section(file_card)
        
        # 处理选项卡片
        options_card_container, options_card = self.create_card(left_column)
        options_card_container.pack(fill=tk.X, pady=(0, 18))
        self.create_options_section(options_card)
        
        # 右侧区域（1/3宽度）- 图片列表
        right_column = tk.Frame(columns_container, bg=self.colors['bg_main'])
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(9, 0))
        right_column.config(width=350)
        right_column.pack_propagate(False)
        
        # 图片列表卡片（高度自适应，底部留白）
        list_card_container, list_card = self.create_card(right_column)
        list_card_container.pack(fill=tk.BOTH, expand=True, pady=(0, 18))
        self.create_image_list(list_card)
        
    def create_card(self, parent):
        """创建Razer 3D拟物化卡片"""
        card_3d = Razer3DCard(parent)
        content = card_3d.get_content()
        
        # 添加内边距容器
        content_padded = tk.Frame(content, bg=self.colors['bg_card'])
        content_padded.pack(fill=tk.BOTH, expand=True, padx=30, pady=22)
        
        return card_3d, content_padded
    
    def create_file_section(self, parent):
        """创建文件选择区域"""
        # 标题行（包含输出路径按钮）
        title_row = tk.Frame(parent, bg=self.colors['bg_card'])
        title_row.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            title_row,
            text="添加图片文件",
            font=("Microsoft YaHei UI", 14, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT)
        
        # 右侧输出路径按钮（无背景，先pack齿轮再pack文件夹）
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
        
        # 添加图片按钮（统一风格）
        add_btn = UnifiedButton(
            button_frame,
            text="添加图片",
            command=self.add_images,
            style="primary",
            width=100,
            height=40
        )
        add_btn.pack(side=tk.LEFT, padx=(0, 8), pady=(0, 8))
        
        # 添加文件夹按钮（统一风格）
        add_folder_btn = UnifiedButton(
            button_frame,
            text="添加文件夹",
            command=self.add_folder,
            style="primary",
            width=115,
            height=40
        )
        add_folder_btn.pack(side=tk.LEFT, padx=(0, 8), pady=(0, 8))
        
        # 清空列表按钮（统一风格）
        clear_btn = UnifiedButton(
            button_frame,
            text="清空列表",
            command=self.clear_images,
            style="secondary",
            width=100,
            height=40
        )
        clear_btn.pack(side=tk.LEFT, padx=(0, 8), pady=(0, 8))
        
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
        
        self.operation_var = tk.StringVar(value="convert")
        
        # 处理类型选项
        self.create_flat_radio(type_frame, "格式转换", self.operation_var, "convert").pack(side=tk.LEFT, padx=(0, 8))
        self.create_flat_radio(type_frame, "拼长图", self.operation_var, "stitch").pack(side=tk.LEFT, padx=(0, 8))
        self.create_flat_radio(type_frame, "切片", self.operation_var, "slice").pack(side=tk.LEFT, padx=(0, 8))
        self.create_flat_radio(type_frame, "抠图", self.operation_var, "remove_bg").pack(side=tk.LEFT)
        
        # 第二行：输出格式选择
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
        
        self.format_var = tk.StringVar(value="jpg")
        
        self.create_flat_radio(format_frame, "JPG", self.format_var, "jpg").pack(side=tk.LEFT, padx=(0, 8))
        self.create_flat_radio(format_frame, "PNG", self.format_var, "png").pack(side=tk.LEFT)
        
        # 第三行：拼长图宽度设置（仅拼长图时显示）
        self.stitch_row = tk.Frame(parent, bg=self.colors['bg_card'])
        
        stitch_frame = tk.Frame(self.stitch_row, bg=self.colors['bg_card'])
        stitch_frame.pack(side=tk.LEFT)
        
        tk.Label(
            stitch_frame,
            text="输出宽度：",
            font=("Microsoft YaHei UI", 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # 宽度选项
        self.width_mode_var = tk.StringVar(value="auto")
        
        self.create_flat_radio(stitch_frame, "自动（第一张）", self.width_mode_var, "auto").pack(side=tk.LEFT, padx=(0, 8))
        self.create_flat_radio(stitch_frame, "自定义", self.width_mode_var, "custom").pack(side=tk.LEFT, padx=(0, 15))
        
        # 自定义宽度输入框
        self.width_input_frame = tk.Frame(stitch_frame, bg=self.colors['bg_card'])
        
        self.custom_width_var = tk.StringVar(value="1920")
        width_entry_border = tk.Frame(self.width_input_frame, bg=self.colors['border_main'])
        width_entry_border.pack(side=tk.LEFT, padx=(0, 5))
        
        width_entry = tk.Entry(
            width_entry_border,
            textvariable=self.custom_width_var,
            font=("Microsoft YaHei UI", 9),
            width=8,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            relief=tk.FLAT,
            borderwidth=0,
            justify='center'
        )
        width_entry.pack(padx=1, pady=1)
        
        tk.Label(
            self.width_input_frame,
            text="像素",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT)
        
        # 监听宽度模式变化
        def on_width_mode_change(*args):
            if self.width_mode_var.get() == "custom":
                self.width_input_frame.pack(side=tk.LEFT)
            else:
                self.width_input_frame.pack_forget()
        
        self.width_mode_var.trace_add("write", on_width_mode_change)
        on_width_mode_change()
        
        # 第三行2：切片设置（仅切片时显示）
        self.slice_row = tk.Frame(parent, bg=self.colors['bg_card'])
        
        slice_frame = tk.Frame(self.slice_row, bg=self.colors['bg_card'])
        slice_frame.pack(side=tk.LEFT)
        
        tk.Label(
            slice_frame,
            text="切片方式：",
            font=("Microsoft YaHei UI", 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # 切片方式选项
        self.slice_mode_var = tk.StringVar(value="px")
        
        self.create_flat_radio(slice_frame, "按像素", self.slice_mode_var, "px").pack(side=tk.LEFT, padx=(0, 8))
        self.create_flat_radio(slice_frame, "平均切", self.slice_mode_var, "avg").pack(side=tk.LEFT, padx=(0, 15))
        
        # 按像素输入框
        self.px_input_frame = tk.Frame(slice_frame, bg=self.colors['bg_card'])
        
        tk.Label(
            self.px_input_frame,
            text="每",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.slice_px_var = tk.StringVar(value="1000")
        px_entry_border = tk.Frame(self.px_input_frame, bg=self.colors['border_main'])
        px_entry_border.pack(side=tk.LEFT, padx=(0, 5))
        
        px_entry = tk.Entry(
            px_entry_border,
            textvariable=self.slice_px_var,
            font=("Microsoft YaHei UI", 9),
            width=8,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            relief=tk.FLAT,
            borderwidth=0,
            justify='center'
        )
        px_entry.pack(padx=1, pady=1)
        
        tk.Label(
            self.px_input_frame,
            text="像素切一张",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT)
        
        # 平均切输入框
        self.avg_input_frame = tk.Frame(slice_frame, bg=self.colors['bg_card'])
        
        tk.Label(
            self.avg_input_frame,
            text="平均切",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.slice_count_var = tk.StringVar(value="5")
        count_entry_border = tk.Frame(self.avg_input_frame, bg=self.colors['border_main'])
        count_entry_border.pack(side=tk.LEFT, padx=(0, 5))
        
        count_entry = tk.Entry(
            count_entry_border,
            textvariable=self.slice_count_var,
            font=("Microsoft YaHei UI", 9),
            width=6,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            relief=tk.FLAT,
            borderwidth=0,
            justify='center'
        )
        count_entry.pack(padx=1, pady=1)
        
        tk.Label(
            self.avg_input_frame,
            text="张",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # 预览信息
        self.slice_preview_label = tk.Label(
            self.avg_input_frame,
            text="",
            font=("Microsoft YaHei UI", 8),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary']
        )
        self.slice_preview_label.pack(side=tk.LEFT)
        
        # 监听切片模式变化
        def on_slice_mode_change(*args):
            if self.slice_mode_var.get() == "px":
                self.px_input_frame.pack(side=tk.LEFT)
                self.avg_input_frame.pack_forget()
            else:
                self.px_input_frame.pack_forget()
                self.avg_input_frame.pack(side=tk.LEFT)
                update_slice_preview()
        
        # 更新切片预览
        def update_slice_preview(*args):
            if self.slice_mode_var.get() == "avg" and self.image_files:
                try:
                    count = int(self.slice_count_var.get())
                    # 假设第一张图是要切片的图
                    img = Image.open(self.image_files[0])
                    height = img.height
                    per_height = height // count
                    remainder = height % count
                    self.slice_preview_label.config(
                        text=f"(每张约{per_height}px，最后一张{per_height + remainder}px)"
                    )
                except:
                    self.slice_preview_label.config(text="")
            else:
                self.slice_preview_label.config(text="")
        
        self.slice_mode_var.trace_add("write", on_slice_mode_change)
        self.slice_count_var.trace_add("write", update_slice_preview)
        on_slice_mode_change()
        
        # 第四行：压缩设置（PNG和JPG都支持）
        self.compress_row = tk.Frame(parent, bg=self.colors['bg_card'])
        
        compress_frame = tk.Frame(self.compress_row, bg=self.colors['bg_card'])
        compress_frame.pack(side=tk.LEFT)
        
        tk.Label(
            compress_frame,
            text="压缩设置：",
            font=("Microsoft YaHei UI", 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # 压缩选项
        self.compress_var = tk.StringVar(value="no")
        
        self.create_flat_radio(compress_frame, "不压缩", self.compress_var, "no").pack(side=tk.LEFT, padx=(0, 8))
        self.create_flat_radio(compress_frame, "压缩", self.compress_var, "yes").pack(side=tk.LEFT, padx=(0, 15))
        
        # 压缩目标大小输入框（仅压缩时显示，样式统一为扁平按钮样式）
        self.size_input_frame = tk.Frame(compress_frame, bg=self.colors['bg_card'])
        
        tk.Label(
            self.size_input_frame,
            text="压缩到",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        # 使用和选框一样的边框样式
        self.target_size_var = tk.StringVar(value="500")
        entry_border = tk.Frame(self.size_input_frame, bg=self.colors['border_main'])
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
        self.size_unit_var = tk.StringVar(value="kb")
        
        tk.Frame(self.size_input_frame, width=5, bg=self.colors['bg_card']).pack(side=tk.LEFT)  # 间距
        self.create_flat_radio(self.size_input_frame, "KB", self.size_unit_var, "kb").pack(side=tk.LEFT, padx=(0, 4))
        self.create_flat_radio(self.size_input_frame, "MB", self.size_unit_var, "mb").pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Label(
            self.size_input_frame,
            text="以下",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT)
        
        # 监听压缩选项变化
        def on_compress_change(*args):
            if self.compress_var.get() == "yes":
                self.size_input_frame.pack(side=tk.LEFT)
            else:
                self.size_input_frame.pack_forget()
        
        # 监听单位变化，自动换算数值
        def on_unit_change(*args):
            try:
                current_value = float(self.target_size_var.get())
                current_unit = self.size_unit_var.get()
                
                # 检查是否是从另一个单位切换过来的
                if not hasattr(self, '_last_unit'):
                    self._last_unit = current_unit
                    return
                
                if self._last_unit != current_unit:
                    # 进行换算
                    if current_unit == "mb" and self._last_unit == "kb":
                        # KB -> MB
                        new_value = current_value / 1024
                        self.target_size_var.set(f"{new_value:.2f}")
                    elif current_unit == "kb" and self._last_unit == "mb":
                        # MB -> KB
                        new_value = current_value * 1024
                        self.target_size_var.set(f"{int(new_value)}")
                    
                    self._last_unit = current_unit
            except ValueError:
                # 如果输入的不是有效数字，忽略
                pass
        
        self.compress_var.trace_add("write", on_compress_change)
        self.size_unit_var.trace_add("write", on_unit_change)
        on_compress_change()  # 初始化
        
        # 第五行：抠图选项
        self.remove_bg_row = tk.Frame(parent, bg=self.colors['bg_card'])
        
        remove_bg_frame = tk.Frame(self.remove_bg_row, bg=self.colors['bg_card'])
        remove_bg_frame.pack(side=tk.LEFT)
        
        tk.Label(
            remove_bg_frame,
            text="抠图方式：",
            font=("Microsoft YaHei UI", 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.remove_bg_mode_var = tk.StringVar(value="both")
        
        self.create_flat_radio(remove_bg_frame, "抠图+白底图", self.remove_bg_mode_var, "both").pack(side=tk.LEFT, padx=(0, 8))
        self.create_flat_radio(remove_bg_frame, "仅抠图", self.remove_bg_mode_var, "only_remove").pack(side=tk.LEFT, padx=(0, 8))
        self.create_flat_radio(remove_bg_frame, "仅白底图", self.remove_bg_mode_var, "only_white").pack(side=tk.LEFT)
        
        # 创建开始处理按钮（统一风格）
        self.process_btn = UnifiedButton(
            parent,
            text="开始处理",
            command=self.start_processing,
            style="primary",
            width=120,
            height=40
        )
        self.process_btn.pack(anchor='w')
        
        # 监听处理类型变化，动态显示/隐藏选项行（在按钮之前插入）
        self._current_mode = None  # 记录当前模式，避免重复pack
        
        def on_operation_change(*args):
            new_mode = self.operation_var.get()
            
            # 如果模式没变，不做任何操作
            if self._current_mode == new_mode:
                return
            
            self._current_mode = new_mode
            
            # 清空所有选项行
            self.format_row.pack_forget()
            self.stitch_row.pack_forget()
            self.compress_row.pack_forget()
            self.remove_bg_row.pack_forget()
            
            # 按顺序重新pack（在开始处理按钮之前）
            if new_mode == "stitch":
                # 拼长图模式：输出格式 → 输出宽度 → 压缩设置
                self.format_row.pack(fill=tk.X, pady=(0, 15), before=self.process_btn)
                self.stitch_row.pack(fill=tk.X, pady=(0, 15), before=self.process_btn)
                self.compress_row.pack(fill=tk.X, pady=(0, 15), before=self.process_btn)
            elif new_mode == "slice":
                # 切片模式：输出格式 → 切片设置 → 压缩设置
                self.format_row.pack(fill=tk.X, pady=(0, 15), before=self.process_btn)
                self.slice_row.pack(fill=tk.X, pady=(0, 15), before=self.process_btn)
                self.compress_row.pack(fill=tk.X, pady=(0, 15), before=self.process_btn)
            elif new_mode == "remove_bg":
                # 抠图模式：抠图方式
                self.remove_bg_row.pack(fill=tk.X, pady=(0, 15), before=self.process_btn)
            else:
                # 格式转换模式：输出格式 → 压缩设置
                self.format_row.pack(fill=tk.X, pady=(0, 15), before=self.process_btn)
                self.compress_row.pack(fill=tk.X, pady=(0, 15), before=self.process_btn)
        
        self.operation_var.trace_add("write", on_operation_change)
        on_operation_change()  # 初始化
        
    def create_image_list(self, parent):
        """创建图片列表（树形显示分组）"""
        # 标题和分组管理按钮
        header_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            header_frame,
            text="图片列表",
            font=("Microsoft YaHei UI", 14, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT)
        
        # 分组管理按钮
        group_btn_frame = tk.Frame(header_frame, bg=self.colors['bg_card'])
        group_btn_frame.pack(side=tk.RIGHT)
        
        UnifiedButton(
            group_btn_frame,
            text="新建组",
            command=self.create_new_group,
            style="secondary",
            width=65,
            height=28
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        UnifiedButton(
            group_btn_frame,
            text="合并组",
            command=self.merge_groups,
            style="secondary",
            width=65,
            height=28
        ).pack(side=tk.LEFT)
        
        # 树形列表（带细边框）
        is_dark = self.colors.get('is_dark', True)
        border_color = '#333333' if is_dark else '#d0d0d0'
        tree_border = tk.Frame(parent, bg=border_color)
        tree_border.pack(fill=tk.BOTH, expand=True)
        
        tree_frame = tk.Frame(tree_border, bg=self.colors['bg_input'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # 导入ttk
        from tkinter import ttk
        
        # 滚动条
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 树形视图
        listbox_bg = '#1e1e1e' if is_dark else '#ffffff'
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
                       background=listbox_bg,
                       foreground=self.colors['text_primary'],
                       fieldbackground=listbox_bg,
                       borderwidth=0)
        style.configure("Treeview.Heading",
                       background=self.colors['bg_card'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1)
        style.map('Treeview',
                 background=[('selected', self.colors['primary'])],
                 foreground=[('selected', 'black')])
        
        self.image_tree = ttk.Treeview(
            tree_frame,
            columns=('count',),
            displaycolumns=('count',),
            yscrollcommand=scrollbar.set,
            show='tree',  # 只显示树，不显示列标题
            selectmode='extended'
        )
        self.image_tree.column('#0', width=340, minwidth=200)
        self.image_tree.column('count', width=60, minwidth=40, anchor='center')
        
        self.image_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.image_tree.yview)
        
        # 绑定右键菜单
        self.image_tree.bind("<Button-3>", self.show_context_menu)
        
        # 绑定拖拽事件
        self.dragged_item = None
        self.image_tree.bind("<ButtonPress-1>", self.on_drag_start)
        self.image_tree.bind("<B1-Motion>", self.on_drag_motion)
        self.image_tree.bind("<ButtonRelease-1>", self.on_drag_release)
        
        # 初始化分组
        self.refresh_tree()
        
    def refresh_tree(self):
        """刷新树形列表"""
        # 清空树
        for item in self.image_tree.get_children():
            self.image_tree.delete(item)
        
        # 添加分组和文件
        for group_name, files in self.image_groups.items():
            # 添加分组节点（显示数量）
            group_id = self.image_tree.insert('', 'end', 
                                              text=f"📁 {group_name} ({len(files)})", 
                                              values=('',), 
                                              tags=('group',))
            
            # 添加文件节点
            for file_path in files:
                self.image_tree.insert(group_id, 'end', 
                                      text=Path(file_path).name,
                                      values=('',), 
                                      tags=('file',))
        
        # 展开所有分组
        for item in self.image_tree.get_children():
            self.image_tree.item(item, open=True)
        
    def add_images(self):
        """添加图片到当前分组"""
        files = filedialog.askopenfilenames(
            title="选择图片",
            filetypes=[
                ("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif *.webp"),
                ("所有文件", "*.*")
            ]
        )
        
        if files:
            # 设置当前分组的输出路径
            if not self.group_output_dirs.get(self.current_group):
                self.group_output_dirs[self.current_group] = os.path.dirname(files[0])
            
            # 添加到当前分组
            for file in files:
                if file not in self.image_groups[self.current_group]:
                    self.image_groups[self.current_group].append(file)
            
            # 更新显示（显示当前分组的输出路径）
            if self.group_output_dirs[self.current_group]:
                self.output_path_label.config(text=f"📁 {os.path.basename(self.group_output_dirs[self.current_group])}")
            
            self.refresh_tree()
                    
    def add_folder(self):
        """添加文件夹（选完后询问是否继续）"""
        # 鏀寔鐨勫浘鐗囨墿灞曞悕
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'}

        import re
        def natural_sort_key(path):
            parts = re.split(r'(\d+)', str(path.name))
            return [int(part) if part.isdigit() else part.lower() for part in parts]

        folders_added = 0
        
        while True:
            # 选择一个文件夹
            folder = filedialog.askdirectory(title="选择文件夹添加为分组")
            
            if not folder:
                # 用户取消
                break
            
            # 收集图片文件
            image_paths = []
            for file_path in Path(folder).rglob('*'):
                if file_path.suffix.lower() in image_extensions:
                    image_paths.append(file_path)
            
            # 自然排序
            image_paths.sort(key=natural_sort_key)
            
            if not image_paths:
                # 文件夹为空，询问是否继续
                result = messagebox.askyesno("提示", f"文件夹'{Path(folder).name}'中没有图片\n\n是否继续添加其他文件夹？")
                if not result:
                    break
                continue
            
            # 创建新分组
            group_name = Path(folder).name
            original_name = group_name
            counter = 1
            while group_name in self.image_groups:
                group_name = f"{original_name}_{counter}"
                counter += 1
            
            self.image_groups[group_name] = [str(p) for p in image_paths]
            self.group_output_dirs[group_name] = folder
            self.current_group = group_name
            folders_added += 1
            
            # 刷新显示
            self.refresh_tree()
            
            # 询问是否继续添加
            result = messagebox.askyesno("成功", 
                f"已创建分组'{group_name}'，添加了 {len(image_paths)} 张图片\n\n是否继续添加其他文件夹？")
            
            if not result:
                # 用户选择"否"，结束
                break
                    
    def clear_images(self):
        """清空所有分组和图片"""
        if messagebox.askyesno("确认", "确定要清空所有分组和图片吗？"):
            self.image_groups = {"默认分组": []}
            self.group_output_dirs = {"默认分组": None}
            self.current_group = "默认分组"
            self.refresh_tree()
    
    def on_drag_start(self, event):
        """开始拖拽"""
        item = self.image_tree.identify_row(event.y)
        if item:
            tags = self.image_tree.item(item, 'tags')
            # 只有文件可以拖拽
            if 'file' in tags:
                self.dragged_item = item
                self.image_tree.selection_set(item)
    
    def on_drag_motion(self, event):
        """拖拽中"""
        if self.dragged_item:
            # 高亮目标位置
            target = self.image_tree.identify_row(event.y)
            if target:
                self.image_tree.selection_set(target)
    
    def on_drag_release(self, event):
        """释放拖拽"""
        if not self.dragged_item:
            return
        
        target = self.image_tree.identify_row(event.y)
        if not target:
            self.dragged_item = None
            return
        
        target_tags = self.image_tree.item(target, 'tags')
        
        # 如果拖到分组上
        if 'group' in target_tags:
            target_group = self.image_tree.item(target, 'text').replace("📁 ", "")
            
            # 获取源文件信息
            parent_item = self.image_tree.parent(self.dragged_item)
            source_group = self.image_tree.item(parent_item, 'text').replace("📁 ", "")
            filename = self.image_tree.item(self.dragged_item, 'text').strip()
            
            # 如果不是同一个组，执行移动
            if source_group != target_group:
                # 找到文件路径
                for fp in self.image_groups[source_group]:
                    if Path(fp).name == filename:
                        self.image_groups[source_group].remove(fp)
                        self.image_groups[target_group].append(fp)
                        self.refresh_tree()
                        break
        
        self.dragged_item = None
    
    def create_new_group(self):
        """创建新分组"""
        # 简单对话框获取组名
        from tkinter import simpledialog
        group_name = simpledialog.askstring("新建分组", "请输入分组名称：")
        
        if group_name:
            if group_name in self.image_groups:
                messagebox.showwarning("提示", f"分组'{group_name}'已存在")
            else:
                self.image_groups[group_name] = []
                self.group_output_dirs[group_name] = None
                self.current_group = group_name
                self.refresh_tree()
                messagebox.showinfo("成功", f"已创建分组'{group_name}'")
    
    def merge_groups(self):
        """合并选中的分组"""
        # 获取选中的分组
        selected = self.image_tree.selection()
        groups_to_merge = []
        
        for item in selected:
            if 'group' in self.image_tree.item(item, 'tags'):
                group_text = self.image_tree.item(item, 'text')
                group_name = group_text.replace("📁 ", "")
                groups_to_merge.append(group_name)
        
        if len(groups_to_merge) < 2:
            messagebox.showwarning("提示", "请至少选择两个分组进行合并")
            return
        
        # 询问合并后的组名
        from tkinter import simpledialog
        new_name = simpledialog.askstring("合并分组", 
                                          f"将 {', '.join(groups_to_merge)} 合并为：",
                                          initialvalue=groups_to_merge[0])
        
        if new_name:
            # 合并所有文件
            merged_files = []
            for group_name in groups_to_merge:
                merged_files.extend(self.image_groups[group_name])
                if group_name != new_name:
                    del self.image_groups[group_name]
            
            # 去重
            self.image_groups[new_name] = list(dict.fromkeys(merged_files))
            self.current_group = new_name
            self.refresh_tree()
            messagebox.showinfo("成功", f"已合并为'{new_name}'，共 {len(self.image_groups[new_name])} 个文件")
    
    def show_context_menu(self, event):
        """显示右键菜单"""
        # 获取点击位置的项
        item = self.image_tree.identify_row(event.y)
        if not item:
            return
        
        # 选中该项
        self.image_tree.selection_set(item)
        
        # 创建右键菜单
        menu = tk.Menu(self.root, tearoff=0,
                      bg=self.colors['bg_card'],
                      fg=self.colors['text_primary'],
                      activebackground=self.colors['primary'],
                      activeforeground='black')
        
        tags = self.image_tree.item(item, 'tags')
        
        if 'group' in tags:
            # 分组菜单
            menu.add_command(label="重命名分组", command=lambda: self.rename_group(item))
            menu.add_command(label="并入其他分组", command=lambda: self.merge_into_other(item))
            menu.add_separator()
            menu.add_command(label="删除分组", command=lambda: self.delete_group(item))
        else:
            # 文件菜单
            menu.add_command(label="移动到其他组", command=lambda: self.move_file_to_group(item))
            menu.add_command(label="从分组移除", command=lambda: self.remove_file_from_group(item))
        
        menu.post(event.x_root, event.y_root)
    
    def rename_group(self, item):
        """重命名分组"""
        old_name = self.image_tree.item(item, 'text').replace("📁 ", "")
        from tkinter import simpledialog
        new_name = simpledialog.askstring("重命名分组", "新的分组名称：", initialvalue=old_name)
        
        if new_name and new_name != old_name:
            if new_name in self.image_groups:
                messagebox.showwarning("提示", f"分组'{new_name}'已存在")
            else:
                self.image_groups[new_name] = self.image_groups.pop(old_name)
                if self.current_group == old_name:
                    self.current_group = new_name
                self.refresh_tree()
    
    def merge_into_other(self, item):
        """将分组并入其他分组"""
        source_group = self.image_tree.item(item, 'text').replace("📁 ", "")
        
        # 获取其他分组列表
        other_groups = [g for g in self.image_groups.keys() if g != source_group]
        
        if not other_groups:
            messagebox.showinfo("提示", "没有其他分组可以并入")
            return
        
        # 选择目标分组
        from tkinter import simpledialog
        target_group = simpledialog.askstring(
            "并入分组", 
            f"将'{source_group}'并入到：\n\n可选分组：{', '.join(other_groups)}",
            initialvalue=other_groups[0]
        )
        
        if target_group and target_group in self.image_groups and target_group != source_group:
            # 合并文件
            self.image_groups[target_group].extend(self.image_groups[source_group])
            # 去重
            self.image_groups[target_group] = list(dict.fromkeys(self.image_groups[target_group]))
            
            # 删除源分组
            del self.image_groups[source_group]
            if source_group in self.group_output_dirs:
                del self.group_output_dirs[source_group]
            
            # 更新当前分组
            if self.current_group == source_group:
                self.current_group = target_group
            
            self.refresh_tree()
            messagebox.showinfo("成功", f"已将'{source_group}'并入'{target_group}'")
    
    def delete_group(self, item):
        """删除分组"""
        group_name = self.image_tree.item(item, 'text').replace("📁 ", "")
        
        if len(self.image_groups) <= 1:
            messagebox.showwarning("提示", "至少需要保留一个分组")
            return
        
        if messagebox.askyesno("确认", f"确定要删除分组'{group_name}'吗？"):
            del self.image_groups[group_name]
            if group_name in self.group_output_dirs:
                del self.group_output_dirs[group_name]
            if self.current_group == group_name:
                self.current_group = list(self.image_groups.keys())[0]
            self.refresh_tree()
    
    def move_file_to_group(self, item):
        """移动文件到其他组"""
        # 获取文件信息
        parent_item = self.image_tree.parent(item)
        old_group = self.image_tree.item(parent_item, 'text').replace("📁 ", "")
        filename = self.image_tree.item(item, 'text').strip()
        
        # 找到完整路径
        file_path = None
        for fp in self.image_groups[old_group]:
            if Path(fp).name == filename:
                file_path = fp
                break
        
        if not file_path:
            return
        
        # 选择目标分组
        from tkinter import simpledialog
        groups = list(self.image_groups.keys())
        groups.remove(old_group)
        
        if not groups:
            messagebox.showinfo("提示", "没有其他分组可以移动")
            return
        
        target_group = simpledialog.askstring("移动文件", 
                                             f"移动到分组（可选：{', '.join(groups)}）：",
                                             initialvalue=groups[0])
        
        if target_group and target_group in self.image_groups:
            self.image_groups[old_group].remove(file_path)
            self.image_groups[target_group].append(file_path)
            self.refresh_tree()
    
    def remove_file_from_group(self, item):
        """从分组移除文件"""
        parent_item = self.image_tree.parent(item)
        group_name = self.image_tree.item(parent_item, 'text').replace("📁 ", "")
        filename = self.image_tree.item(item, 'text').strip()
        
        # 找到完整路径
        for fp in self.image_groups[group_name]:
            if Path(fp).name == filename:
                self.image_groups[group_name].remove(fp)
                self.refresh_tree()
                break
        
    def select_output_dir(self):
        """选择输出目录"""
        directory = filedialog.askdirectory(
            title="选择输出目录",
            initialdir=self.output_dir if self.output_dir else os.path.expanduser("~")
        )
        
        if directory:
            self.output_dir = directory
            self.output_dir_manual = True  # 标记为手动设置
            self.output_path_label.config(text=f"📁 {os.path.basename(self.output_dir)}")
            
    def start_processing(self):
        """开始处理（支持分组导出）"""
        # 检查是否有图片
        total_files = sum(len(files) for files in self.image_groups.values())
        if total_files == 0:
            messagebox.showwarning("提示", "请先添加图片")
            return
            
        # 不再检查全局output_dir，每个分组有自己的输出路径
        operation = self.operation_var.get()
        
        try:
            if operation == "convert":
                self.batch_convert()
            elif operation == "stitch":
                self.stitch_images()
            elif operation == "slice":
                self.slice_image()
            elif operation == "remove_bg":
                self.remove_background()
            else:
                messagebox.showinfo("提示", "该功能开发中...")
                
        except Exception as e:
            messagebox.showerror("错误", f"处理失败: {e}")
            
    def batch_convert(self):
        """批量格式转换（每个分组导出到各自路径）"""
        format_ext = self.format_var.get().lower()
        
        format_map = {
            'jpg': 'JPEG',
            'png': 'PNG'
        }
        
        target_format = format_map.get(format_ext)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        success_count = 0
        error_count = 0
        
        # 按分组处理，每个分组导出到各自路径
        for group_name, image_files in self.image_groups.items():
            if not image_files:
                continue
            
            # 获取该分组的输出路径
            group_base_dir = self.group_output_dirs.get(group_name)
            if not group_base_dir:
                group_base_dir = os.path.dirname(image_files[0])
            
            # 在该分组路径下创建输出文件夹
            output_folder_name = f"格式转换_{format_ext.upper()}_{timestamp}"
            group_output_dir = Path(group_base_dir) / output_folder_name
            group_output_dir.mkdir(parents=True, exist_ok=True)
            
            for img_path in image_files:
                try:
                    img = Image.open(img_path)
                
                    # 如果是RGBA模式且目标格式是JPEG，需要转换为RGB
                    if target_format == "JPEG" and img.mode in ("RGBA", "LA", "P"):
                        # 创建白色背景
                        bg = Image.new("RGB", img.size, (255, 255, 255))
                        if img.mode == "P":
                            img = img.convert("RGBA")
                        bg.paste(img, mask=img.split()[-1] if len(img.split()) > 3 else None)
                        img = bg
                    
                    # 生成输出文件名
                    output_filename = Path(img_path).stem + f".{format_ext}"
                    output_path = group_output_dir / output_filename
                    
                    # 保存（根据压缩设置）
                    if self.compress_var.get() == "no":
                        # 不压缩
                        if target_format == "JPEG":
                            img.save(output_path, target_format, quality=95)
                        else:  # PNG
                            img.save(output_path, target_format, optimize=False)
                    else:
                        # 压缩到指定大小
                        try:
                            target_size_value = float(self.target_size_var.get())
                            # 根据单位计算字节数
                            if self.size_unit_var.get() == "kb":
                                target_size_bytes = int(target_size_value * 1024)
                            else:  # mb
                                target_size_bytes = int(target_size_value * 1024 * 1024)
                            self.compress_to_size(img, output_path, target_format, target_size_bytes, format_ext)
                        except ValueError:
                            messagebox.showerror("错误", "请输入有效的文件大小（数字）")
                            return
                            
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    print(f"处理 {img_path} 失败: {e}")
        
        # 显示结果
        if error_count == 0:
            messagebox.showinfo("成功", f"已成功转换 {success_count} 张图片为 {format_ext.upper()} 格式！\n\n每个分组已保存到各自文件夹")
        else:
            messagebox.showwarning("完成", f"成功: {success_count} 张\n失败: {error_count} 张\n\n每个分组已保存到各自文件夹")
    
    def compress_to_size(self, img, output_path, format_name, target_size_bytes, format_ext):
        """将图片压缩到指定大小以下"""
        import io
        
        if format_name == "JPEG":
            # JPG使用quality参数压缩
            min_quality = 10
            max_quality = 95
            
            while min_quality < max_quality:
                mid_quality = (min_quality + max_quality + 1) // 2
                
                # 测试这个质量
                buffer = io.BytesIO()
                img.save(buffer, format_name, quality=mid_quality)
                size = buffer.tell()
                
                if size <= target_size_bytes:
                    min_quality = mid_quality
                else:
                    max_quality = mid_quality - 1
            
            # 使用最终质量保存
            img.save(output_path, format_name, quality=min_quality)
            
        else:  # PNG
            # PNG先尝试优化，如果还是太大，降低颜色数量
            buffer = io.BytesIO()
            img.save(buffer, format_name, optimize=True)
            
            if buffer.tell() <= target_size_bytes:
                # 优化后已满足要求
                img.save(output_path, format_name, optimize=True)
            else:
                # 需要更激进的压缩，转换为调色板模式
                if img.mode == "RGBA":
                    # 保留透明度
                    img_rgb = img.convert("RGB")
                    img_p = img_rgb.convert("P", palette=Image.ADAPTIVE, colors=256)
                else:
                    img_p = img.convert("P", palette=Image.ADAPTIVE, colors=256)
                
                # 尝试不同的颜色数量
                for colors in [256, 128, 64, 32, 16]:
                    buffer = io.BytesIO()
                    temp_img = img.convert("P", palette=Image.ADAPTIVE, colors=colors) if img.mode != "P" else img_p
                    temp_img.save(buffer, format_name, optimize=True)
                    
                    if buffer.tell() <= target_size_bytes:
                        temp_img.save(output_path, format_name, optimize=True)
                        break
                else:
                    # 即使16色还是太大，直接保存
                    img_p.save(output_path, format_name, optimize=True)
    
    def stitch_images(self):
        """拼接长图（支持分组）"""
        # 获取所有图片
        all_files = []
        for files in self.image_groups.values():
            all_files.extend(files)
        
        if len(all_files) < 2:
            messagebox.showwarning("提示", "拼长图至少需要2张图片")
            return
        
        # 加载所有图片
        images = []
        for img_path in all_files:
            img = Image.open(img_path)
            images.append(img)
        
        # 确定目标宽度
        if self.width_mode_var.get() == "auto":
            target_width = images[0].width
        else:
            try:
                target_width = int(self.custom_width_var.get())
            except ValueError:
                messagebox.showerror("错误", "请输入有效的宽度值")
                return
        
        # 调整所有图片宽度并计算总高度
        resized_images = []
        total_height = 0
        
        for img in images:
            if img.width != target_width:
                # 按比例缩放
                ratio = target_width / img.width
                new_height = int(img.height * ratio)
                resized_img = img.resize((target_width, new_height), Image.Resampling.LANCZOS)
                resized_images.append(resized_img)
                total_height += new_height
            else:
                resized_images.append(img)
                total_height += img.height
        
        # 创建长图画布
        long_img = Image.new('RGB', (target_width, total_height), (255, 255, 255))
        
        # 拼接图片
        current_y = 0
        for img in resized_images:
            # 如果是透明图，需要转换
            if img.mode in ('RGBA', 'LA'):
                bg = Image.new('RGB', img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[-1] if len(img.split()) > 3 else None)
                img = bg
            elif img.mode == 'P':
                img = img.convert('RGB')
            
            long_img.paste(img, (0, current_y))
            current_y += img.height
        
        # 创建输出子文件夹并生成文件名
        format_ext = self.format_var.get().lower()
        output_folder_name = f"拼长图_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        final_output_dir = Path(self.output_dir) / output_folder_name
        final_output_dir.mkdir(parents=True, exist_ok=True)
        
        output_filename = f"拼接长图.{format_ext}"
        output_path = final_output_dir / output_filename
        
        # 保存（根据格式和压缩设置）
        format_map = {'jpg': 'JPEG', 'png': 'PNG'}
        target_format = format_map.get(format_ext)
        
        if self.compress_var.get() == "no":
            # 不压缩
            if target_format == "JPEG":
                long_img.save(output_path, target_format, quality=95)
            else:
                long_img.save(output_path, target_format, optimize=False)
        else:
            # 压缩到指定大小
            try:
                target_size_value = float(self.target_size_var.get())
                if self.size_unit_var.get() == "kb":
                    target_size_bytes = int(target_size_value * 1024)
                else:
                    target_size_bytes = int(target_size_value * 1024 * 1024)
                self.compress_to_size(long_img, output_path, target_format, target_size_bytes, format_ext)
            except ValueError:
                messagebox.showerror("错误", "请输入有效的文件大小")
                return
        
        messagebox.showinfo("成功", f"已成功拼接 {len(images)} 张图片！\n保存在：{output_folder_name}\n文件名：{output_filename}")
    
    def slice_image(self):
        """切片长图（支持分组）"""
        # 获取所有图片
        all_files = []
        for files in self.image_groups.values():
            all_files.extend(files)
        
        if len(all_files) != 1:
            messagebox.showwarning("提示", "切片功能只能处理一张图片，请只添加一张长图")
            return
        
        # 加载图片
        img_path = all_files[0]
        img = Image.open(img_path)
        img_width = img.width
        img_height = img.height
        
        # 创建输出子文件夹
        format_ext = self.format_var.get().lower()
        output_folder_name = f"切片_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        final_output_dir = Path(self.output_dir) / output_folder_name
        final_output_dir.mkdir(parents=True, exist_ok=True)
        
        # 根据切片模式计算切片信息
        slices = []
        
        if self.slice_mode_var.get() == "px":
            # 按像素切割
            try:
                slice_height = int(self.slice_px_var.get())
            except ValueError:
                messagebox.showerror("错误", "请输入有效的像素值")
                return
            
            current_y = 0
            slice_index = 1
            
            while current_y < img_height:
                end_y = min(current_y + slice_height, img_height)
                slices.append((current_y, end_y, slice_index))
                current_y = end_y
                slice_index += 1
        else:
            # 平均切
            try:
                slice_count = int(self.slice_count_var.get())
            except ValueError:
                messagebox.showerror("错误", "请输入有效的切片数量")
                return
            
            if slice_count <= 0:
                messagebox.showerror("错误", "切片数量必须大于0")
                return
            
            per_height = img_height // slice_count
            remainder = img_height % slice_count
            
            current_y = 0
            for i in range(slice_count):
                # 最后一张包含余数
                if i == slice_count - 1:
                    end_y = img_height
                else:
                    end_y = current_y + per_height
                
                slices.append((current_y, end_y, i + 1))
                current_y = end_y
        
        # 执行切片
        format_map = {'jpg': 'JPEG', 'png': 'PNG'}
        target_format = format_map.get(format_ext)
        
        for start_y, end_y, index in slices:
            # 裁剪图片
            cropped = img.crop((0, start_y, img_width, end_y))
            
            # 如果是RGBA且目标格式是JPEG，转换
            if target_format == "JPEG" and cropped.mode in ("RGBA", "LA", "P"):
                bg = Image.new("RGB", cropped.size, (255, 255, 255))
                if cropped.mode == "P":
                    cropped = cropped.convert("RGBA")
                bg.paste(cropped, mask=cropped.split()[-1] if len(cropped.split()) > 3 else None)
                cropped = bg
            
            # 生成文件名
            output_filename = f"切片_{index:03d}.{format_ext}"
            output_path = final_output_dir / output_filename
            
            # 保存（根据压缩设置）
            if self.compress_var.get() == "no":
                if target_format == "JPEG":
                    cropped.save(output_path, target_format, quality=95)
                else:
                    cropped.save(output_path, target_format, optimize=False)
            else:
                try:
                    target_size_value = float(self.target_size_var.get())
                    if self.size_unit_var.get() == "kb":
                        target_size_bytes = int(target_size_value * 1024)
                    else:
                        target_size_bytes = int(target_size_value * 1024 * 1024)
                    self.compress_to_size(cropped, output_path, target_format, target_size_bytes, format_ext)
                except ValueError:
                    messagebox.showerror("错误", "请输入有效的文件大小")
                    return
        
        messagebox.showinfo("成功", f"已成功切片为 {len(slices)} 张图片！\n保存在：{output_folder_name}")
        
    def remove_background(self):
        """抠图处理（支持分组）"""
        # 检查是否有图片
        total_files = sum(len(files) for files in self.image_groups.values())
        if total_files == 0:
            messagebox.showwarning("提示", "请先添加图片")
            return
        
        remove_bg_mode = self.remove_bg_mode_var.get()
        
        # 检查是否安装rembg
        try:
            from rembg import remove
        except ImportError:
            result = messagebox.askyesno(
                "缺少依赖", 
                "抠图功能需要安装 rembg 库。\n\n是否现在安装？\n\n安装命令：pip install rembg"
            )
            if result:
                messagebox.showinfo("提示", "请在命令行运行：pip install rembg")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        success_count = 0
        
        # 按分组处理，每个分组导出到各自路径
        for group_name, image_files in self.image_groups.items():
            if not image_files:
                continue
            
            # 获取该分组的输出路径
            group_base_dir = self.group_output_dirs.get(group_name)
            if not group_base_dir:
                group_base_dir = os.path.dirname(image_files[0])
            
            # 根据模式在分组路径下创建文件夹
            if remove_bg_mode == "both":
                remove_bg_dir = os.path.join(group_base_dir, f"抠图_{timestamp}")
                white_bg_dir = os.path.join(group_base_dir, f"白底图_{timestamp}")
                os.makedirs(remove_bg_dir, exist_ok=True)
                os.makedirs(white_bg_dir, exist_ok=True)
            elif remove_bg_mode == "only_remove":
                remove_bg_dir = os.path.join(group_base_dir, f"抠图_{timestamp}")
                os.makedirs(remove_bg_dir, exist_ok=True)
                white_bg_dir = None
            else:  # only_white
                white_bg_dir = os.path.join(group_base_dir, f"白底图_{timestamp}")
                os.makedirs(white_bg_dir, exist_ok=True)
                remove_bg_dir = None
            
            for img_path in image_files:
                try:
                    # 读取图片
                    input_img = Image.open(img_path)
                    
                    # 抠图
                    if remove_bg_mode in ["both", "only_remove"]:
                        # 使用rembg去除背景
                        output_img = remove(input_img)
                        
                        # 保存抠图PNG
                        filename = Path(img_path).stem
                        output_path = os.path.join(remove_bg_dir, f"{filename}.png")
                        output_img.save(output_path, "PNG")
                    
                    # 生成白底图
                    if remove_bg_mode in ["both", "only_white"]:
                        # 如果是both模式，使用已抠图的；如果是only_white，先抠图
                        if remove_bg_mode == "only_white":
                            output_img = remove(input_img)
                        
                        # 创建白色背景
                        white_bg = Image.new("RGB", output_img.size, (255, 255, 255))
                        
                        # 合成（如果有透明通道）
                        if output_img.mode == 'RGBA':
                            white_bg.paste(output_img, (0, 0), output_img)
                        else:
                            white_bg.paste(output_img, (0, 0))
                        
                        # 保存为JPG
                        filename = Path(img_path).stem
                        output_path = os.path.join(white_bg_dir, f"{filename}.jpg")
                        white_bg.save(output_path, "JPEG", quality=95)
                    
                    success_count += 1
                    
                except Exception as e:
                    print(f"处理 {Path(img_path).name} 失败：{e}")
                    continue
        
        # 显示结果
        result_msg = f"成功处理 {success_count}/{total_files} 张图片！\n\n按分组保存在：\n"
        if remove_bg_mode in ["both", "only_remove"]:
            result_msg += f"抠图_{timestamp}/\n"
        if remove_bg_mode in ["both", "only_white"]:
            result_msg += f"白底图_{timestamp}/"
        
        messagebox.showinfo("完成", result_msg)
        
    def open_help(self):
        """显示使用说明（图片处理工具）"""
        try:
            from tkinter import Canvas, Frame

            doc_path = Path(__file__).parent / "图片处理工具使用说明.md"
            if not doc_path.exists():
                messagebox.showinfo("提示", f"未找到使用说明文件：\n{doc_path}")
                return

            raw = doc_path.read_text(encoding="utf-8", errors="ignore")

            help_win = tk.Toplevel(self.root)
            help_win.title("图片处理工具 - 使用说明")
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

    def toggle_theme(self):
        """切换主题（保留数据）"""
        from theme import get_theme
        current_theme = get_theme()
        new_dark_mode = not current_theme.is_dark
        
        # 保存当前数据
        saved_groups = self.image_groups.copy()
        saved_group_dirs = self.group_output_dirs.copy()
        saved_current_group = self.current_group
        saved_output_dir = self.output_dir
        saved_output_dir_manual = self.output_dir_manual
        
        # 重启应用
        self.root.destroy()
        import theme
        theme._global_theme = theme.RazerTheme(dark_mode=new_dark_mode)
        
        new_root = tk.Tk()
        app = ImageProcessorApp(new_root)
        
        # 恢复数据
        app.image_groups = saved_groups
        app.group_output_dirs = saved_group_dirs
        app.current_group = saved_current_group
        app.output_dir = saved_output_dir
        app.output_dir_manual = saved_output_dir_manual
        if app.group_output_dirs.get(app.current_group):
            app.output_path_label.config(text=f"📁 {os.path.basename(app.group_output_dirs[app.current_group])}")
        app.refresh_tree()
        
        new_root.mainloop()
        
    def back_to_launcher(self):
        """返回首页"""
        self.root.destroy()
        # 重新打开launcher
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from launcher import ToolLauncher
        new_root = tk.Tk()
        app = ToolLauncher(new_root)
        new_root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()

