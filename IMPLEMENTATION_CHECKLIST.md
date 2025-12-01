# ✅ Centisky 安装程序实施清单

## 🎯 环境准备

### 必要工具检查

- [ ] **Python 3.7+** 已安装
  - 验证：运行 `python --version`
  - 下载：https://www.python.org

- [ ] **Inno Setup 6** 已安装
  - 验证：`C:\Program Files (x86)\Inno Setup 6\ISCC.exe` 存在
  - 下载：https://jrsoftware.org/isdl.php
  - 安装位置：必须是默认位置

- [ ] **PyInstaller** 已安装
  - 验证：运行 `pip show pyinstaller`
  - 安装：`pip install pyinstaller`

### 快速检查

```bash
check_setup.bat
```

---

## 📦 第一次构建

### 步骤 1：验证文件

- [ ] `version.txt` 存在且包含版本号（如 `1.0.0`）
- [ ] `installer.iss` 存在
- [ ] `program/launcher.py` 存在
- [ ] `program/update_checker.py` 存在
- [ ] `program/build_spec.spec` 存在

### 步骤 2：构建安装程序

```bash
build_installer_auto.bat
```

- [ ] 脚本运行成功
- [ ] 没有错误信息
- [ ] `dist/Centisky-Setup-1.0.0.exe` 已生成

### 步骤 3：测试安装程序

- [ ] 运行 `dist/Centisky-Setup-1.0.0.exe`
- [ ] 按照向导完成安装
- [ ] 应用成功启动
- [ ] 检查开始菜单快捷方式
- [ ] 检查桌面快捷方式（如果选择）

### 步骤 4：测试自动更新

- [ ] 启动应用
- [ ] 等待 5-10 秒
- [ ] 检查是否有更新提示（如果有新版本）
- [ ] 查看应用日志（如果有）

---

## 🚀 发布新版本

### 步骤 1：准备代码

- [ ] 所有代码已测试
- [ ] 所有 bug 已修复
- [ ] 代码已提交到 Git

### 步骤 2：更新版本号

编辑 `version.txt`：

```
1.0.1
```

- [ ] 版本号已更新
- [ ] 格式正确（`major.minor.patch`）
- [ ] 版本号大于当前版本

### 步骤 3：提交到 Git

```bash
git add version.txt
git commit -m "Release v1.0.1"
git push
```

- [ ] 代码已推送到 GitHub

### 步骤 4：构建安装程序

```bash
build_installer_auto.bat
```

- [ ] 构建成功
- [ ] 输出文件：`dist/Centisky-Setup-1.0.1.exe`

### 步骤 5：创建 GitHub Release

打开 https://github.com/Benji-Xu/Centisky/releases

- [ ] 点击 "Create a new release"
- [ ] **Tag version**：`v1.0.1`（必须以 `v` 开头）
- [ ] **Release title**：`Centisky v1.0.1`
- [ ] **Description**：
  ```markdown
  ## 新功能
  - 功能 1
  - 功能 2

  ## 修复
  - 修复 1
  - 修复 2

  ## 下载
  - Windows 安装程序：Centisky-Setup-1.0.1.exe
  ```

### 步骤 6：上传安装程序

- [ ] 点击 "Attach binaries by dropping them here or selecting them"
- [ ] 选择 `dist/Centisky-Setup-1.0.1.exe`
- [ ] 文件已上传

### 步骤 7：发布

- [ ] 点击 "Publish release"
- [ ] Release 已发布

### 步骤 8：验证

- [ ] 访问 https://github.com/Benji-Xu/Centisky/releases
- [ ] 新 Release 已显示
- [ ] 安装程序文件已显示
- [ ] 下载链接可用

---

## 🔄 用户更新流程

### 用户端

- [ ] 用户启动应用
- [ ] 后台自动检查 GitHub
- [ ] 发现新版本时弹窗提示
- [ ] 用户点击"是"打开下载页面
- [ ] 用户下载新版本安装程序
- [ ] 用户运行安装程序
- [ ] 应用自动更新

---

## 📋 定期维护

### 每周

- [ ] 检查 GitHub Issues
- [ ] 回复用户反馈
- [ ] 检查下载统计

### 每月

- [ ] 审查更新日志
- [ ] 计划下一个版本
- [ ] 备份 GitHub 仓库

### 每个版本发布前

- [ ] 运行 `check_setup.bat` 验证环境
- [ ] 在干净系统上测试安装程序
- [ ] 测试升级流程（从旧版本升级）
- [ ] 验证自动更新功能
- [ ] 准备发布说明

---

## 🐛 常见问题排查

### 问题：安装程序无法生成

**检查清单**：
- [ ] Inno Setup 6 已安装在正确位置
- [ ] PyInstaller 已安装
- [ ] `program/dist/Workit/` 目录存在
- [ ] 运行 `build_installer_auto.bat` 查看错误信息

### 问题：用户没有收到更新提示

**检查清单**：
- [ ] GitHub 仓库是公开的
- [ ] Release 标签格式正确（`v1.0.0`）
- [ ] 远程版本号 > 本地版本号
- [ ] 用户网络连接正常
- [ ] 查看应用日志

### 问题：安装程序运行时出错

**检查清单**：
- [ ] Python 依赖已安装
- [ ] 所有必要文件已包含
- [ ] 在干净系统上测试
- [ ] 查看 PyInstaller 输出日志

---

## 📚 文档参考

| 文档 | 用途 |
|------|------|
| `INSTALLER_QUICK_START.md` | 5分钟快速开始 |
| `GITHUB_RELEASE_GUIDE.md` | 完整发布指南 |
| `INSTALLER_SETUP_COMPLETE.md` | 详细设置说明 |
| `SETUP_SUMMARY.md` | 完成总结 |
| `IMPLEMENTATION_CHECKLIST.md` | 本清单 |

---

## 🎯 快速参考

### 常用命令

```bash
# 检查环境
check_setup.bat

# 构建安装程序
build_installer_auto.bat

# 只构建 EXE（不生成安装程序）
build_exe.bat

# 测试更新检查
python program/update_checker.py
```

### 关键文件位置

```
version.txt                    # 版本号
installer.iss                  # Inno Setup 配置
program/update_checker.py      # 更新检查模块
program/launcher.py            # 主程序启动器
dist/                          # 输出目录
```

### 版本号格式

```
1.0.0          # 标准版本
1.0.1          # 补丁版本
1.1.0          # 次版本
2.0.0          # 主版本
v1.0.0         # GitHub Release 标签（必须以 v 开头）
```

---

## ✨ 成功标志

✅ 安装程序成功生成  
✅ 安装程序可以运行  
✅ 应用成功启动  
✅ 自动更新功能正常  
✅ GitHub Release 已发布  
✅ 用户可以下载安装程序  

---

## 🎉 完成！

你现在已经拥有一个完整的、专业的安装程序和自动更新系统。

**下一步**：
1. 运行 `check_setup.bat` 验证环境
2. 运行 `build_installer_auto.bat` 构建安装程序
3. 测试安装程序
4. 创建第一个 GitHub Release

**需要帮助**？查看相关文档或运行 `check_setup.bat`。

---

**最后更新**：2024年12月  
**维护者**：Benji-Xu
