# Centisky 安装程序和自动更新使用指南

## 概述

Centisky 现在支持：
1. **安装程序** - 用户可自定义安装路径
2. **版本检查** - 启动时自动检查 GitHub 最新版本
3. **自动更新提示** - 发现新版本时弹窗提示

## 安装前准备

### 系统要求
- Windows 7 或更高版本
- Python 3.7 或更高版本（可选，如果已安装）

### 需要安装的工具
1. **Inno Setup 6**（用于生成安装程序）
   - 下载地址：https://jrsoftware.org/isdl.php
   - 选择 "Inno Setup 6.x.x" 版本
   - 安装到默认位置（C:\Program Files (x86)\Inno Setup 6）

## 生成安装程序

### 步骤 1：准备代码
确保所有代码都已提交并保存。

### 步骤 2：运行构建脚本
双击 `build_installer.bat` 脚本：
```
d:\Centisky\build_installer.bat
```

### 步骤 3：等待构建完成
脚本会：
1. 检查 Python 环境
2. 安装必要的构建工具
3. 编译 Python 代码为 EXE
4. 使用 Inno Setup 生成安装程序

### 步骤 4：获取安装程序
构建完成后，安装程序位于：
```
d:\Centisky\dist\Centisky-Setup-1.0.0.exe
```

## 分发安装程序

### 给用户分发
1. 将 `Centisky-Setup-1.0.0.exe` 发送给用户
2. 用户双击运行安装程序
3. 选择安装路径（默认为 `C:\Program Files\Centisky`）
4. 完成安装

### 安装程序功能
- ✓ 自定义安装路径
- ✓ 创建开始菜单快捷方式
- ✓ 创建桌面快捷方式
- ✓ 自动检测 Python
- ✓ 支持卸载

## 版本检查和自动更新

### 工作原理
1. **启动时检查** - 用户打开 Centisky 时，程序会异步检查 GitHub 最新版本
2. **版本比较** - 将本地版本与 GitHub 最新版本比较
3. **提示更新** - 如果有新版本，弹窗提示用户
4. **下载更新** - 用户可点击"是"打开下载页面

### 版本文件
- **本地版本** - 存储在 `d:\Centisky\version.txt`
- **GitHub 版本** - 从 GitHub Releases API 获取

### 版本号格式
- 格式：`主版本.次版本.修订版本`
- 例如：`1.0.0`, `1.1.2`, `2.0.0`

## 发布新版本到 GitHub

### 步骤 1：更新版本号
编辑 `d:\Centisky\version.txt`：
```
1.0.1
```

### 步骤 2：提交代码
```bash
git add .
git commit -m "Release v1.0.1"
git push
```

### 步骤 3：创建 GitHub Release
1. 打开 GitHub 仓库：https://github.com/Benji-Xu/Centisky
2. 点击 "Releases" → "Create a new release"
3. 填写信息：
   - Tag version: `v1.0.1`
   - Release title: `Centisky v1.0.1`
   - Description: 更新说明
4. 上传安装程序文件：`Centisky-Setup-1.0.1.exe`
5. 点击 "Publish release"

### 步骤 4：用户更新
用户启动 Centisky 时，会自动检测到新版本并弹窗提示。

## 故障排除

### 问题 1：Inno Setup 未找到
**错误信息**：`ERROR: Inno Setup not found!`

**解决方案**：
1. 从 https://jrsoftware.org/isdl.php 下载 Inno Setup 6
2. 安装到默认位置
3. 重新运行 `build_installer.bat`

### 问题 2：Python 未找到
**错误信息**：`ERROR: Python not found!`

**解决方案**：
1. 从 https://www.python.org 下载 Python 3.7+
2. 安装时勾选 "Add Python to PATH"
3. 重新运行 `build_installer.bat`

### 问题 3：版本检查失败
**现象**：启动时没有版本检查提示

**原因**：
- 网络连接问题
- GitHub 无法访问
- GitHub API 速率限制

**解决方案**：
- 检查网络连接
- 稍后重试
- 程序会继续正常运行，不会因为版本检查失败而中断

### 问题 4：安装程序损坏
**错误信息**：`This installation package could not be opened`

**解决方案**：
1. 重新运行 `build_installer.bat` 生成新的安装程序
2. 确保 `program\dist\Centisky\Workit.exe` 存在

## 技术细节

### 版本检查模块
- 文件：`d:\Centisky\program\update_checker.py`
- 功能：
  - 从 GitHub API 获取最新版本
  - 比较版本号
  - 显示更新提示
  - 打开下载链接

### 启动器集成
- 文件：`d:\Centisky\program\launcher.py`
- 修改：在 `__init__` 中调用 `check_for_updates_async()`
- 特点：异步检查，不阻塞主程序

### Inno Setup 配置
- 文件：`d:\Centisky\installer.iss`
- 功能：
  - 定义安装程序属性
  - 配置文件复制
  - 创建快捷方式
  - 检查 Python

## 常见问题

**Q: 用户可以自定义安装路径吗？**
A: 可以。安装程序会在第一步显示安装路径选择。

**Q: 可以卸载吗？**
A: 可以。通过 Windows 控制面板 → 程序和功能 → Centisky → 卸载。

**Q: 版本检查会影响启动速度吗？**
A: 不会。版本检查是异步进行的，不会阻塞主程序启动。

**Q: 如果没有网络连接会怎样？**
A: 版本检查会失败，但程序会继续正常运行。

**Q: 可以禁用版本检查吗？**
A: 目前不支持，但可以修改 `update_checker.py` 来禁用。

## 后续改进

- [ ] 实现自动下载和安装更新
- [ ] 添加更新日志显示
- [ ] 支持 Beta 版本检查
- [ ] 添加更新检查频率控制
- [ ] 支持离线更新

## 相关文件

- `version.txt` - 版本号文件
- `program/update_checker.py` - 版本检查模块
- `program/launcher.py` - 启动器（已集成版本检查）
- `installer.iss` - Inno Setup 配置
- `build_installer.bat` - 安装程序构建脚本
- `build_exe.bat` - EXE 构建脚本（已更新）

## 支持

如有问题，请提交 Issue 到：
https://github.com/Benji-Xu/Centisky/issues
