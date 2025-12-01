"""
版本检查和自动更新模块
从 GitHub 检查最新版本，提示用户更新
支持安装程序和便携版本
"""

import os
import sys
import json
import threading
import webbrowser
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import tkinter as tk
from tkinter import messagebox
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# GitHub 仓库信息
GITHUB_OWNER = "Benji-Xu"
GITHUB_REPO = "Centisky"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
GITHUB_RELEASES_PAGE = f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/releases"

# 版本文件路径
VERSION_FILE = Path(__file__).parent.parent / "version.txt"

# 检查间隔（秒）- 避免频繁检查
CHECK_INTERVAL = 3600  # 1小时


def get_local_version():
    """获取本地版本号"""
    try:
        if VERSION_FILE.exists():
            with open(VERSION_FILE, 'r', encoding='utf-8') as f:
                version = f.read().strip()
                if version:
                    return version
    except Exception as e:
        logger.error(f"读取版本文件失败: {e}")
    return "1.0.0"  # 默认版本


def get_github_latest_version():
    """从 GitHub 获取最新版本号和下载信息"""
    try:
        with urlopen(GITHUB_API_URL, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            # 从 tag_name 中提取版本号（如 v1.0.0 -> 1.0.0）
            tag_name = data.get('tag_name', '')
            version = tag_name.lstrip('v')
            
            # 获取发布说明
            release_notes = data.get('body', '').strip()
            
            # 获取下载链接
            assets = data.get('assets', [])
            installer_url = None
            portable_url = None
            
            for asset in assets:
                name = asset['name'].lower()
                url = asset['browser_download_url']
                
                if 'setup' in name or name.endswith('.exe'):
                    if installer_url is None:
                        installer_url = url
                elif 'portable' in name or 'zip' in name:
                    portable_url = url
            
            # 优先返回安装程序，其次返回便携版本
            download_url = installer_url or portable_url or GITHUB_RELEASES_PAGE
            
            return version, download_url, release_notes
    except (URLError, HTTPError, json.JSONDecodeError, Exception) as e:
        logger.error(f"从 GitHub 获取版本失败: {e}")
        return None, None, None


def compare_versions(local_ver, remote_ver):
    """比较版本号，返回是否需要更新"""
    try:
        # 处理版本号中的非数字字符（如 1.0.0-beta）
        def parse_version(ver):
            parts = []
            for part in ver.split('.'):
                # 提取数字部分
                num_str = ''.join(c for c in part if c.isdigit())
                if num_str:
                    parts.append(int(num_str))
            return parts
        
        local_parts = parse_version(local_ver)
        remote_parts = parse_version(remote_ver)
        
        # 补齐版本号长度
        while len(local_parts) < len(remote_parts):
            local_parts.append(0)
        while len(remote_parts) < len(local_parts):
            remote_parts.append(0)
        
        # 逐位比较
        for local, remote in zip(local_parts, remote_parts):
            if remote > local:
                return True  # 需要更新
            elif remote < local:
                return False  # 本地版本更新
        
        return False  # 版本相同
    except Exception as e:
        logger.error(f"版本比较失败: {e}")
        return False


def show_update_dialog(local_version, remote_version, download_url, release_notes=""):
    """显示更新提示对话框"""
    try:
        root = tk.Tk()
        root.withdraw()
        
        message = f"""发现新版本！

当前版本: {local_version}
最新版本: {remote_version}

是否立即下载新版本？
（点击"是"将打开下载页面）"""
        
        if release_notes:
            # 截断过长的发布说明
            notes_preview = release_notes[:200] + "..." if len(release_notes) > 200 else release_notes
            message += f"\n\n更新说明:\n{notes_preview}"
        
        result = messagebox.askyesno("新版本可用", message)
        root.destroy()
        
        if result and download_url:
            logger.info(f"打开下载链接: {download_url}")
            webbrowser.open(download_url)
        
        return result
    except Exception as e:
        logger.error(f"显示更新对话框失败: {e}")
        return False


def check_for_updates(show_dialog=True):
    """检查更新"""
    try:
        local_version = get_local_version()
        remote_version, download_url, release_notes = get_github_latest_version()
        
        if remote_version is None:
            logger.info("无法连接到 GitHub，跳过版本检查")
            return False
        
        logger.info(f"本地版本: {local_version}, GitHub 最新版本: {remote_version}")
        
        if compare_versions(local_version, remote_version):
            logger.info(f"发现新版本: {remote_version}")
            if show_dialog:
                show_update_dialog(local_version, remote_version, download_url, release_notes)
            return True
        else:
            logger.info("已是最新版本")
            return False
    except Exception as e:
        logger.error(f"版本检查异常: {e}")
        return False


def check_for_updates_async(show_dialog=True):
    """异步检查更新（不阻塞主程序）"""
    def _check():
        try:
            check_for_updates(show_dialog=show_dialog)
        except Exception as e:
            logger.error(f"异步检查更新失败: {e}")
    
    thread = threading.Thread(target=_check, daemon=True)
    thread.start()
    return thread


if __name__ == "__main__":
    # 测试版本检查
    print("测试版本检查...")
    check_for_updates(show_dialog=False)
