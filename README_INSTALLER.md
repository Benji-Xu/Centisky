# 🎉 Centisky 安装程序和自动更新系统

## 概述

这是一个完整的、生产级别的安装程序和自动更新系统，使用 **Inno Setup 6** 和 **GitHub Releases**。

### 核心特性

- ✅ **一键构建** - 运行脚本自动完成所有步骤
- ✅ **自动更新** - 用户启动时自动检查新版本
- ✅ **后台运行** - 不阻塞主程序
- ✅ **智能提示** - 只在有新版本时提示
- ✅ **用户控制** - 用户决定是否更新
- ✅ **网络容错** - 网络错误时自动跳过
- ✅ **多语言** - 支持中文和英文
- ✅ **完整文档** - 详细的使用说明

---

## 🚀 快速开始（3 分钟）

### 1. 检查环境

```bash
check_setup.bat
```

### 2. 构建安装程序

```bash
build_installer_auto.bat
```

### 3. 发布到 GitHub

1. 更新 `version.txt`
2. 创建 GitHub Release（标签：`v1.0.0`）
3. 上传 `dist/Centisky-Setup-1.0.0.exe`

完成！用户会自动检测到新版本。

---

## 📦 文件清单

### 脚本文件

| 文件 | 说明 |
|------|------|
| `check_setup.bat` | 环境检查脚本 |
| `build_installer_auto.bat` | 一键构建脚本 |
| `build_exe.bat` | 只构建 EXE（不生成安装程序） |

### 配置文件

| 文件 | 说明 |
|------|------|
| `version.txt` | 版本号文件 |
| `installer.iss` | Inno Setup 配置 |
| `program/update_checker.py` | 自动更新检查模块 |

### 文档文件

| 文件 | 说明 |
|------|------|
| `INSTALLER_QUICK_START.md` | 5分钟快速开始 |
| `GITHUB_RELEASE_GUIDE.md` | 完整发布指南 |
| `INSTALLER_SETUP_COMPLETE.md` | 详细设置说明 |
| `SETUP_SUMMARY.md` | 完成总结 |
| `IMPLEMENTATION_CHECKLIST.md` | 实施清单 |
| `QUICK_REFERENCE.txt` | 快速参考卡 |
| `README_INSTALLER.md` | 本文档 |

---

## 🔧 工作流程

```
修改代码
  ↓
更新 version.txt
  ↓
git push
  ↓
build_installer_auto.bat
  ↓
创建 GitHub Release
  ↓
上传安装程序
  ↓
用户自动检测更新
```

---

## 📋 详细步骤

### 第 1 步：准备环境

**必要工具**：
- Python 3.7+
- Inno Setup 6
- PyInstaller

**检查环境**：
```bash
check_setup.bat
```

### 第 2 步：修改代码

编辑你的 Python 代码，进行测试。

### 第 3 步：更新版本号

编辑 `version.txt`：
```
1.0.1
```

### 第 4 步：提交到 Git

```bash
git add .
git commit -m "Release v1.0.1"
git push
```

### 第 5 步：构建安装程序

```bash
build_installer_auto.bat
```

输出：`dist/Centisky-Setup-1.0.1.exe`

### 第 6 步：创建 GitHub Release

1. 打开 https://github.com/Benji-Xu/Centisky/releases
2. 点击 "Create a new release"
3. 填写：
   - **Tag**: `v1.0.1`
   - **Title**: `Centisky v1.0.1`
   - **Description**: 更新说明
4. 上传 `dist/Centisky-Setup-1.0.1.exe`
5. 点击 "Publish release"

### 第 7 步：完成

用户启动应用时会自动检测到新版本，弹窗提示更新。

---

## 🔄 自动更新工作原理

### 用户端流程

```
用户启动应用
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
  │   ├─ 用户点击"是" → 打开浏览器下载
  │   └─ 用户点击"否" → 继续使用
  └─ 本地版本 >= 远程版本
      ↓
      正常启动应用
```

### 技术细节

- **检查方式**：调用 GitHub REST API
- **获取信息**：最新 Release 的 tag_name 和 assets
- **版本比较**：智能版本号比较（支持 1.0.0-beta 格式）
- **下载链接**：优先安装程序，其次便携版本
- **超时处理**：5 秒超时，网络错误自动跳过

---

## ⚙️ 配置说明

### 版本号管理

编辑 `version.txt`：
```
1.0.0
```

格式：`major.minor.patch`

### GitHub 配置

编辑 `program/update_checker.py`：
```python
GITHUB_OWNER = "Benji-Xu"      # 你的 GitHub 用户名
GITHUB_REPO = "Centisky"       # 仓库名
```

### Inno Setup 配置

编辑 `installer.iss` 顶部：
```ini
#define MyAppName "Centisky"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Benji-Xu"
#define MyAppURL "https://github.com/Benji-Xu/Centisky"
```

---

## 🐛 故障排除

### 问题 1：Inno Setup 未找到

**解决**：
1. 下载 Inno Setup 6：https://jrsoftware.org/isdl.php
2. 安装到默认位置：`C:\Program Files (x86)\Inno Setup 6\`
3. 重新运行 `build_installer_auto.bat`

### 问题 2：用户没有收到更新提示

**检查**：
- 网络连接是否正常
- GitHub 仓库是否公开
- Release 标签格式是否正确（必须是 `v1.0.0`）
- 远程版本号是否大于本地版本号

**调试**：
```bash
python program/update_checker.py
```

### 问题 3：安装程序无法运行

**解决**：
- 重新运行 `build_installer_auto.bat`
- 检查 `program/dist/Workit/` 目录
- 查看 PyInstaller 输出日志

---

## 📚 文档导航

### 快速开始

- **5分钟快速开始**：[INSTALLER_QUICK_START.md](INSTALLER_QUICK_START.md)
- **快速参考卡**：[QUICK_REFERENCE.txt](QUICK_REFERENCE.txt)

### 完整指南

- **完整发布指南**：[GITHUB_RELEASE_GUIDE.md](GITHUB_RELEASE_GUIDE.md)
- **详细设置说明**：[INSTALLER_SETUP_COMPLETE.md](INSTALLER_SETUP_COMPLETE.md)

### 实施和维护

- **实施清单**：[IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md)
- **完成总结**：[SETUP_SUMMARY.md](SETUP_SUMMARY.md)

---

## 💡 最佳实践

### 版本号规范

- **主版本号**：大功能更新（如 1.0.0 → 2.0.0）
- **次版本号**：新功能（如 1.0.0 → 1.1.0）
- **补丁版本号**：bug 修复（如 1.0.0 → 1.0.1）

### 发布清单

发布新版本前检查：

- [ ] 代码已测试
- [ ] 版本号已更新
- [ ] 构建脚本成功运行
- [ ] 安装程序已测试
- [ ] 发布说明已准备
- [ ] GitHub Release 已创建
- [ ] 安装程序已上传

### 测试步骤

1. 在干净系统上测试安装程序
2. 测试升级流程（从旧版本升级）
3. 验证自动更新功能
4. 检查快捷方式
5. 检查卸载功能

---

## 🎓 高级功能

### 自定义更新检查间隔

编辑 `program/update_checker.py`：
```python
CHECK_INTERVAL = 86400  # 改为 24 小时
```

### 强制更新

修改 `show_update_dialog()` 函数以使用 `showwarning()` 代替 `askyesno()`。

### 支持多个下载源

修改 `get_github_latest_version()` 函数以返回多个下载链接。

### 自定义安装程序界面

编辑 `installer.iss` 的 `[Setup]` 部分。

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

## 🎯 常见问题

**Q: 如何支持自动安装更新？**
A: 需要额外的更新器程序。可以使用 Squirrel.Windows 或 Wix Toolset。

**Q: 如何签名安装程序？**
A: 在 Inno Setup 中配置代码签名证书。

**Q: 如何支持静默安装？**
A: 用户可以使用 `/SILENT` 参数运行安装程序。

**Q: 如何处理依赖项？**
A: 在 Inno Setup 中添加 `[Files]` 部分来包含依赖项。

**Q: 如何回滚到旧版本？**
A: 用户可以从 GitHub Releases 页面下载任何历史版本。

---

## 🚀 下一步

1. ✅ 运行 `check_setup.bat` 检查环境
2. ✅ 运行 `build_installer_auto.bat` 构建安装程序
3. ✅ 测试安装程序
4. ✅ 创建第一个 GitHub Release
5. ✅ 验证自动更新功能

---

## 📞 支持

### 文档

- 快速开始：[INSTALLER_QUICK_START.md](INSTALLER_QUICK_START.md)
- 完整指南：[GITHUB_RELEASE_GUIDE.md](GITHUB_RELEASE_GUIDE.md)
- 快速参考：[QUICK_REFERENCE.txt](QUICK_REFERENCE.txt)

### 外部资源

- [Inno Setup 文档](https://jrsoftware.org/isinfo.php)
- [PyInstaller 文档](https://pyinstaller.org/)
- [GitHub Releases 文档](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)

---

## 📝 更新日志

### v1.0.0 (2024-12-01)

- ✨ 初始版本
- ✨ Inno Setup 6 配置
- ✨ 自动更新系统
- ✨ 自动化构建脚本
- ✨ 完整文档

---

## 📄 许可证

MIT License

---

## 👤 维护者

**Benji-Xu**

- GitHub: https://github.com/Benji-Xu
- 项目：https://github.com/Benji-Xu/Centisky

---

## 🙏 致谢

感谢以下项目的支持：
- [Inno Setup](https://jrsoftware.org/)
- [PyInstaller](https://pyinstaller.org/)
- [GitHub](https://github.com/)

---

**最后更新**：2024年12月  
**版本**：1.0.0  
**状态**：✅ 生产就绪
