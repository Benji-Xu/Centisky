# GitHub 发布和自动更新指南

## 概述

本指南说明如何使用 GitHub Releases 发布新版本，以及如何通过自动更新功能让用户获取最新版本。

## 工作流程

```
修改代码 → 更新版本号 → 构建安装程序 → 创建 GitHub Release → 用户自动检测更新
```

## 步骤 1：更新版本号

编辑 `version.txt` 文件，更新版本号：

```
1.0.1
```

版本号格式：`major.minor.patch`

## 步骤 2：构建安装程序

运行自动化构建脚本：

```bash
build_installer_auto.bat
```

这会自动：
1. 编译 Python 代码为 EXE
2. 使用 Inno Setup 创建安装程序
3. 输出文件到 `dist/Centisky-Setup-1.0.1.exe`

## 步骤 3：创建 GitHub Release

### 方法 A：使用 GitHub Web 界面

1. 打开 https://github.com/Benji-Xu/Centisky/releases
2. 点击 "Create a new release"
3. 填写以下信息：

   - **Tag version**: `v1.0.1` (必须以 `v` 开头)
   - **Release title**: `Centisky v1.0.1`
   - **Description**: 
     ```
     ## 新功能
     - 功能 1
     - 功能 2

     ## 修复
     - 修复 1
     - 修复 2

     ## 下载
     - Windows 安装程序：Centisky-Setup-1.0.1.exe
     ```

4. 上传文件：
   - 点击 "Attach binaries by dropping them here or selecting them"
   - 选择 `dist/Centisky-Setup-1.0.1.exe`

5. 点击 "Publish release"

### 方法 B：使用 GitHub CLI

```bash
# 安装 GitHub CLI (如果还没安装)
# https://cli.github.com/

# 创建 Release
gh release create v1.0.1 \
  --title "Centisky v1.0.1" \
  --notes "## 新功能\n- 功能 1\n\n## 修复\n- 修复 1" \
  dist/Centisky-Setup-1.0.1.exe
```

## 步骤 4：用户自动检测更新

### 工作原理

1. **启动检测**：用户打开应用时，会自动检查 GitHub 最新版本
2. **后台检查**：检查在后台进行，不会阻塞主程序
3. **提示更新**：如果发现新版本，弹窗提示用户
4. **下载更新**：用户点击"是"后，自动打开下载页面

### 配置

更新检查配置在 `program/update_checker.py`：

```python
GITHUB_OWNER = "Benji-Xu"
GITHUB_REPO = "Centisky"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
```

如果你 fork 了这个项目，需要修改这些值为你自己的 GitHub 用户名和仓库名。

## 版本号格式规范

### 标签格式

- 必须以 `v` 开头：`v1.0.0`
- 支持预发布版本：`v1.0.0-beta`, `v1.0.0-rc1`
- 自动去掉 `v` 前缀进行比较

### 版本比较

- `1.0.0` < `1.0.1` < `1.1.0` < `2.0.0`
- 支持任意位数：`1.0.0.1` 等
- 自动处理版本号中的非数字字符

## 发布清单

发布新版本前检查：

- [ ] 代码已提交到 Git
- [ ] 版本号已更新到 `version.txt`
- [ ] 构建脚本成功运行
- [ ] 安装程序已测试
- [ ] 发布说明已准备
- [ ] GitHub Release 已创建
- [ ] 安装程序已上传

## 故障排除

### 问题：用户没有收到更新提示

**原因**：
- 网络连接问题
- GitHub API 超时
- 版本号格式不正确

**解决**：
- 检查网络连接
- 查看应用日志
- 确保 tag 格式为 `v1.0.0`

### 问题：安装程序无法运行

**原因**：
- Python 依赖缺失
- 构建过程中出错

**解决**：
- 重新运行 `build_installer_auto.bat`
- 检查 PyInstaller 输出
- 验证 `program/dist/Workit/` 目录

### 问题：Inno Setup 编译失败

**原因**：
- Inno Setup 未安装
- 路径不正确
- 文件权限问题

**解决**：
- 安装 Inno Setup 6：https://jrsoftware.org/isdl.php
- 检查安装路径：`C:\Program Files (x86)\Inno Setup 6\`
- 以管理员身份运行构建脚本

## 自定义更新检查

### 修改检查间隔

编辑 `program/update_checker.py`：

```python
CHECK_INTERVAL = 3600  # 改为你想要的秒数
```

### 禁用自动检查

在 `program/launcher.py` 中注释掉：

```python
# check_for_updates_async()
```

### 手动检查更新

```python
from update_checker import check_for_updates
check_for_updates(show_dialog=True)
```

## 高级配置

### 支持多个下载源

修改 `get_github_latest_version()` 函数以支持多个下载链接：

```python
# 返回多个下载选项
return version, {
    'installer': installer_url,
    'portable': portable_url,
    'zip': zip_url
}, release_notes
```

### 自定义更新检查逻辑

创建自己的检查函数并替换 `check_for_updates()`。

## 参考资源

- [GitHub Releases 文档](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- [GitHub CLI 文档](https://cli.github.com/manual/)
- [Inno Setup 文档](https://jrsoftware.org/isinfo.php)
- [PyInstaller 文档](https://pyinstaller.org/)

## 常见问题

**Q: 如何回滚到旧版本？**
A: 用户可以从 GitHub Releases 页面下载任何历史版本。

**Q: 如何强制用户更新？**
A: 修改 `update_checker.py` 中的 `show_update_dialog()` 函数，使用 `messagebox.showwarning()` 代替 `askyesno()`。

**Q: 如何支持自动安装更新？**
A: 需要额外的更新器程序。可以使用 Squirrel.Windows 或类似工具。

**Q: 如何处理网络错误？**
A: 已在 `get_github_latest_version()` 中处理，会自动跳过检查。

---

**最后更新**：2024年12月
**维护者**：Benji-Xu
