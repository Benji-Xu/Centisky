"""
多选文件夹对话框
Windows系统使用Shell对话框实现多选
"""
import sys
import os


def select_multiple_folders(title="选择文件夹"):
    """
    选择多个文件夹
    返回: 文件夹路径列表，如果取消返回空列表
    """
    if sys.platform == "win32":
        try:
            # Windows系统使用win32com
            import win32com.client
            
            shell = win32com.client.Dispatch("Shell.Application")
            # BrowseForFolder的参数：
            # 0 = 桌面
            # 0x200 = 允许多选 (BIF_NEWDIALOGSTYLE)
            folder = shell.BrowseForFolder(0, title, 0x200, 0)
            
            if folder:
                # 获取选中的项
                items = folder.Items()
                folders = []
                for item in items:
                    path = item.Path
                    if os.path.isdir(path):
                        folders.append(path)
                return folders
            return []
            
        except ImportError:
            # 如果win32com不可用，使用简单的对话框
            import tkinter as tk
            from tkinter import filedialog, messagebox
            
            root = tk.Tk()
            root.withdraw()
            
            folders = []
            messagebox.showinfo("多选文件夹", "请逐个选择文件夹，点击取消结束选择")
            
            while True:
                folder = filedialog.askdirectory(title=f"{title}（已选{len(folders)}个，取消结束）")
                if folder:
                    folders.append(folder)
                else:
                    break
            
            root.destroy()
            return folders
    else:
        # 非Windows系统，使用循环选择
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()
        
        folders = []
        while True:
            folder = filedialog.askdirectory(title=f"{title}（已选{len(folders)}个，取消结束）")
            if folder:
                folders.append(folder)
            else:
                break
        
        root.destroy()
        return folders


if __name__ == "__main__":
    # 测试
    folders = select_multiple_folders("测试多选文件夹")
    print(f"选择了 {len(folders)} 个文件夹:")
    for folder in folders:
        print(f"  - {folder}")

