# ✅ Centisky 安装程序和自动更新系统 - 完整设置

## 📋 已完成的工作

### 1. **Inno Setup 配置** ✓
- 现代化的安装程序界面
- 支持中文和英文
- 自动创建开始菜单快捷方式
- 自动创建桌面快捷方式（可选）
- 完整的卸载功能

### 2. **自动更新系统** ✓
- 启动时自动检查 GitHub 最新版本
- 后台运行，不阻塞主程序
- 发现新版本时弹窗提示
- 用户可选择是否更新
- 支持发布说明显示

### 3. **自动化构建脚本** ✓
- `build_installer_auto.bat` - 一键构建安装程序
- `check_setup.bat` - 检查环境配置
- 自动编译 Python 代码
- 自动调用 Inno Setup 生成安装程序

### 4. **文档** ✓
- `INSTALLER_QUICK_START.md` - 快速开始指南
- `GITHUB_RELEASE_GUIDE.md` - 完整发布指南
- 本文档 - 完整设置说明

---

## 🎯 立即开始

### 第 1 步：检查环境

```bash
check_setup.bat
```

这会检查：
- ✓ Python 是否已安装
- ✓ PyInstaller 是否已安装
- ✓ Inno Setup 6 是否已安装
- ✓ 必要文件是否存在

### 第 2 步：构建安装程序

```bash
build_installer_auto.bat
```

这会：
1. 编译 Python 代码为 EXE
2. 使用 Inno Setup 创建安装程序
3. 输出到 `dist/Centisky-Setup-1.0.0.exe`

### 第 3 步：测试安装程序

1. 运行 `dist/Centisky-Setup-1.0.0.exe`
2. 按照向导完成安装
3. 启动应用，验证自动更新功能

### 第 4 步：发布到 GitHub

1. 更新 `version.txt` 中的版本号
2. 提交代码到 Git
3. 创建 GitHub Release（标签格式：`v1.0.0`）
4. 上传安装程序文件
5. 用户会自动检测到新版本

---

## 📁 项目结构

```
Centisky/
├── version.txt                      # 版本号文件
├── installer.iss                    # Inno Setup 配置
├── build_installer_auto.bat         # 自动构建脚本
├── check_setup.bat                  # 环境检查脚本
├── INSTALLER_QUICK_START.md         # 快速开始指南
├── GITHUB_RELEASE_GUIDE.md          # 完整发布指南
├── INSTALLER_SETUP_COMPLETE.md      # 本文档
├── program/
│   ├── launcher.py                  # 主程序启动器
│   ├── update_checker.py            # 自动更新检查模块
│   ├── build_spec.spec              # PyInstaller 配置
│   ├── dist/                        # 编译输出目录
│   └── ...
├── templates/                       # 模板文件
└── dist/                            # 最终安装程序输出
```

---

## 🔧 配置说明

### 版本号管理

编辑 `version.txt`：
```
1.0.0
```

格式：`major.minor.patch`

### Inno Setup 配置

编辑 `installer.iss` 顶部的变量：

```ini
#define MyAppName "Centisky"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Benji-Xu"
#define MyAppURL "https://github.com/Benji-Xu/Centisky"
```

### 自动更新配置

编辑 `program/update_checker.py`：

```python
GITHUB_OWNER = "Benji-Xu"
GITHUB_REPO = "Centisky"
```

如果你 fork 了项目，改为你自己的用户名和仓库名。

---

## 📦 发布工作流程

### 完整发布流程

```bash
# 1. 修改代码
# ... 编辑你的代码 ...

# 2. 更新版本号
echo 1.0.1 > version.txt

# 3. 提交到 Git
git add .
git commit -m "Release v1.0.1"
git push

# 4. 构建安装程序
build_installer_auto.bat

# 5. 创建 GitHub Release
# 打开 https://github.com/Benji-Xu/Centisky/releases
# - 创建新 Release
# - 标签：v1.0.1
# - 标题：Centisky v1.0.1
# - 上传：dist/Centisky-Setup-1.0.1.exe
# - 发布

# 完成！用户会自动检测到新版本
```

### 快速发布（仅更新代码）

如果只是修复 bug，不需要重新构建安装程序：

```bash
# 1. 修改代码
# 2. 更新版本号
# 3. 提交到 Git
# 4. 创建 Release（不上传安装程序）
# 用户下次更新时会获得新版本
```

---

## 🚀 自动更新工作原理

### 用户端流程

```
用户启动 Centisky
    ↓
后台线程启动
    ↓
连接 GitHub API
    ↓
获取最新版本信息
    ↓
比较版本号
    ├─ 本地版本 < 远程版本
    │   ↓
    │   显示更新提示
    │   ├─ 用户点击"是"
    │   │   ↓
    │   │   打开浏览器下载页面
    │   └─ 用户点击"否"
    │       ↓
    │       继续使用当前版本
    └─ 本地版本 >= 远程版本
        ↓
        正常启动应用
```

### 版本比较逻辑

- 从 GitHub API 获取最新 Release
- 提取 tag_name（如 `v1.0.1`）
- 去掉 `v` 前缀，得到版本号 `1.0.1`
- 与本地 `version.txt` 中的版本号比较
- 如果远程版本更新，显示提示

### 下载链接优先级

1. 首先查找 `setup` 或 `.exe` 文件（安装程序）
2. 其次查找 `portable` 或 `.zip` 文件（便携版）
3. 最后回退到 Releases 页面

---

## 🔐 安全考虑

### 版本检查的安全性

- ✓ 使用 HTTPS 连接 GitHub API
- ✓ 5 秒超时防止卡顿
- ✓ 网络错误时自动跳过
- ✓ 不下载或执行任何文件
- ✓ 用户完全控制是否更新

### 发布的安全性

- ✓ 使用 Inno Setup 的 LZMA 压缩
- ✓ 支持代码签名（可选）
- ✓ GitHub Releases 自动验证文件完整性

---

## 🐛 故障排除

### 问题 1：Inno Setup 未找到

**症状**：`build_installer_auto.bat` 报错找不到 ISCC.exe

**解决**：
1. 下载 Inno Setup 6：https://jrsoftware.org/isdl.php
2. 安装到默认位置：`C:\Program Files (x86)\Inno Setup 6\`
3. 重新运行脚本

### 问题 2：PyInstaller 构建失败

**症状**：`build_installer_auto.bat` 在编译 EXE 时失败

**解决**：
```bash
pip install --upgrade pyinstaller
python -m PyInstaller --version
```

### 问题 3：用户没有收到更新提示

**症状**：用户启动应用，但没有看到更新提示

**检查**：
- [ ] 网络连接正常
- [ ] GitHub 仓库是公开的
- [ ] Release 标签格式正确（`v1.0.0`）
- [ ] 远程版本号 > 本地版本号
- [ ] 查看应用日志

**调试**：
```bash
python program/update_checker.py
```

### 问题 4：安装程序无法运行

**症状**：用户运行安装程序时出错

**解决**：
- 检查 `program/dist/Workit/` 目录是否存在
- 重新运行 `build_installer_auto.bat`
- 检查 PyInstaller 输出日志

---

## 📊 监控和统计

### 查看下载统计

GitHub Releases 页面会显示每个文件的下载次数。

### 收集用户反馈

在 Release 说明中添加反馈链接：

```markdown
## 反馈
- 报告 Bug：https://github.com/Benji-Xu/Centisky/issues
- 功能请求：https://github.com/Benji-Xu/Centisky/discussions
```

---

## 🎓 高级用法

### 自定义更新检查间隔

编辑 `program/update_checker.py`：

```python
CHECK_INTERVAL = 86400  # 改为 24 小时
```

### 强制更新

修改 `show_update_dialog()` 函数：

```python
# 改为 showwarning 而不是 askyesno
messagebox.showwarning("必须更新", "请更新到最新版本")
```

### 支持 Beta 版本

修改版本比较逻辑以支持 `1.0.0-beta` 格式。

### 集成其他更新源

修改 `get_github_latest_version()` 以支持多个源。

---

## 📞 支持和帮助

### 文档

- 快速开始：[INSTALLER_QUICK_START.md](INSTALLER_QUICK_START.md)
- 完整指南：[GITHUB_RELEASE_GUIDE.md](GITHUB_RELEASE_GUIDE.md)

### 外部资源

- [Inno Setup 文档](https://jrsoftware.org/isinfo.php)
- [PyInstaller 文档](https://pyinstaller.org/)
- [GitHub Releases 文档](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)

### 常见问题

**Q: 如何支持自动安装更新？**
A: 需要额外的更新器程序。可以使用 Squirrel.Windows 或 Wix Toolset。

**Q: 如何签名安装程序？**
A: 在 Inno Setup 中配置代码签名证书。

**Q: 如何支持静默安装？**
A: 用户可以使用 `/SILENT` 参数运行安装程序。

**Q: 如何处理依赖项？**
A: 在 Inno Setup 中添加 `[Files]` 部分来包含依赖项。

---

## ✨ 最佳实践

1. **版本号规范**
   - 始终使用 `major.minor.patch` 格式
   - 主版本号用于大功能更新
   - 次版本号用于新功能
   - 补丁版本号用于 bug 修复

2. **发布说明**
   - 清晰列出新功能和修复
   - 包含已知问题
   - 提供升级说明

3. **测试**
   - 在发布前在干净系统上测试
   - 测试升级流程
   - 验证自动更新功能

4. **备份**
   - 保留所有历史版本
   - 定期备份 GitHub 仓库
   - 保存发布说明

---

## 🎉 总结

你现在拥有一个完整的、专业的安装程序和自动更新系统：

✅ 一键构建安装程序  
✅ 自动版本检查  
✅ 用户友好的更新提示  
✅ GitHub 集成  
✅ 完整的文档  

**下一步**：
1. 运行 `check_setup.bat` 检查环境
2. 运行 `build_installer_auto.bat` 构建安装程序
3. 测试安装程序
4. 创建第一个 GitHub Release

---

**创建时间**：2024年12月  
**维护者**：Benji-Xu  
**许可证**：MIT
