"""
多选文件夹对话框
支持Ctrl+点击多选文件夹
"""
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from theme import get_colors


class FolderMultiSelectDialog:
    """文件夹多选对话框"""
    
    def __init__(self, parent, initial_dir=None):
        self.result = []
        self.colors = get_colors()
        
        # 创建对话框
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("选择文件夹（可多选）")
        self.dialog.geometry("600x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 设置窗口图标（如果有）
        try:
            icon_path = Path(__file__).parent.parent / "favicon.ico"
            if icon_path.exists():
                self.dialog.iconbitmap(icon_path)
        except:
            pass
        
        self.dialog.configure(bg=self.colors['bg_main'])
        
        # 当前路径
        self.current_path = Path(initial_dir) if initial_dir else Path.home()
        
        self.create_widgets()
        self.load_folders()
        
        # 居中显示
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"600x500+{x}+{y}")
    
    def create_widgets(self):
        """创建界面"""
        # 顶部路径栏
        path_frame = tk.Frame(self.dialog, bg=self.colors['bg_card'], height=50)
        path_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        path_frame.pack_propagate(False)
        
        # 上级按钮
        tk.Button(
            path_frame,
            text="← 上级",
            command=self.go_up,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            cursor="hand2",
            relief=tk.FLAT,
            padx=10,
            pady=8
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # 当前路径显示
        self.path_label = tk.Label(
            path_frame,
            text=str(self.current_path),
            font=("Microsoft YaHei UI", 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            anchor='w'
        )
        self.path_label.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=10)
        
        # 文件夹列表
        list_frame = tk.Frame(self.dialog, bg=self.colors['bg_main'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # 列表框（带边框）
        is_dark = self.colors.get('is_dark', True)
        border_color = '#333333' if is_dark else '#d0d0d0'
        list_border = tk.Frame(list_frame, bg=border_color)
        list_border.pack(fill=tk.BOTH, expand=True)
        
        inner_frame = tk.Frame(list_border, bg=self.colors['bg_input'])
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        scrollbar = tk.Scrollbar(inner_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox_bg = '#1e1e1e' if is_dark else '#ffffff'
        
        self.folder_listbox = tk.Listbox(
            inner_frame,
            font=("Microsoft YaHei UI", 10),
            bg=listbox_bg,
            fg=self.colors['text_primary'],
            selectmode=tk.EXTENDED,  # 支持多选
            selectbackground=self.colors['primary'],
            selectforeground='black',
            yscrollcommand=scrollbar.set,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0
        )
        self.folder_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.folder_listbox.yview)
        
        # 双击进入文件夹
        self.folder_listbox.bind("<Double-Button-1>", self.on_double_click)
        
        # 提示文字
        tip_label = tk.Label(
            self.dialog,
            text="💡 提示：Ctrl+点击可多选文件夹，双击进入子文件夹",
            font=("Microsoft YaHei UI", 9),
            bg=self.colors['bg_main'],
            fg=self.colors['text_muted']
        )
        tip_label.pack(pady=(0, 10))
        
        # 底部按钮
        btn_frame = tk.Frame(self.dialog, bg=self.colors['bg_main'])
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        from unified_button import UnifiedButton
        
        UnifiedButton(
            btn_frame,
            text="确定",
            command=self.on_ok,
            style="primary",
            width=100,
            height=40
        ).pack(side=tk.RIGHT, padx=(10, 0))
        
        UnifiedButton(
            btn_frame,
            text="取消",
            command=self.on_cancel,
            style="secondary",
            width=100,
            height=40
        ).pack(side=tk.RIGHT)
        
        # 已选数量显示
        self.selected_label = tk.Label(
            btn_frame,
            text="已选: 0 个文件夹",
            font=("Microsoft YaHei UI", 10),
            bg=self.colors['bg_main'],
            fg=self.colors['primary']
        )
        self.selected_label.pack(side=tk.LEFT)
        
        # 监听选择变化
        self.folder_listbox.bind("<<ListboxSelect>>", self.on_selection_change)
    
    def load_folders(self):
        """加载当前路径的文件夹"""
        self.folder_listbox.delete(0, tk.END)
        self.path_label.config(text=str(self.current_path))
        
        try:
            # 获取所有子文件夹
            folders = [f for f in self.current_path.iterdir() if f.is_dir()]
            # 排序
            folders.sort(key=lambda x: x.name.lower())
            
            # 添加到列表
            for folder in folders:
                self.folder_listbox.insert(tk.END, f"📁 {folder.name}")
                
        except PermissionError:
            self.folder_listbox.insert(tk.END, "⚠ 无权限访问此目录")
    
    def go_up(self):
        """返回上级目录"""
        if self.current_path.parent != self.current_path:
            self.current_path = self.current_path.parent
            self.load_folders()
    
    def on_double_click(self, event):
        """双击进入文件夹"""
        selection = self.folder_listbox.curselection()
        if selection:
            idx = selection[0]
            folder_name = self.folder_listbox.get(idx).replace("📁 ", "")
            new_path = self.current_path / folder_name
            if new_path.is_dir():
                self.current_path = new_path
                self.load_folders()
    
    def on_selection_change(self, event):
        """选择变化时更新计数"""
        count = len(self.folder_listbox.curselection())
        self.selected_label.config(text=f"已选: {count} 个文件夹")
    
    def on_ok(self):
        """确定"""
        selection = self.folder_listbox.curselection()
        self.result = []
        
        for idx in selection:
            folder_name = self.folder_listbox.get(idx).replace("📁 ", "")
            folder_path = self.current_path / folder_name
            if folder_path.is_dir():
                self.result.append(str(folder_path))
        
        self.dialog.destroy()
    
    def on_cancel(self):
        """取消"""
        self.result = []
        self.dialog.destroy()
    
    def show(self):
        """显示对话框并返回选择结果"""
        self.dialog.wait_window()
        return self.result


def select_folders(parent=None, initial_dir=None):
    """
    显示多选文件夹对话框
    返回: 选择的文件夹路径列表
    """
    if parent is None:
        root = tk.Tk()
        root.withdraw()
        dialog = FolderMultiSelectDialog(root, initial_dir)
        result = dialog.show()
        root.destroy()
        return result
    else:
        dialog = FolderMultiSelectDialog(parent, initial_dir)
        return dialog.show()


# 测试
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    folders = select_folders(root)
    
    if folders:
        print(f"选择了 {len(folders)} 个文件夹:")
        for folder in folders:
            print(f"  - {folder}")
    else:
        print("未选择文件夹")
    
    root.destroy()

