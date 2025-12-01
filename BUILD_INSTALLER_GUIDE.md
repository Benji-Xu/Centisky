# 📦 Centisky 打包安装包完整指南

**指南日期**：2024年12月1日  
**作者**：Benjamin  
**版本**：1.0.0

---

## 🎯 打包流程概览

```
准备工作 → 更新版本号 → 提交代码 → 构建安装程序 → 创建 Release → 用户自动更新
```

---

## 📋 完整打包步骤

### 第 1 步：准备工作

#### 1.1 检查环境
```bash
check_setup.bat
```

确保以下工具已安装：
- ✅ Python 3.7+
- ✅ PyInstaller
- ✅ Inno Setup 6

#### 1.2 测试应用
```bash
start.bat
```

验证应用功能正常，特别是：
- ✅ 主应用启动正常
- ✅ 各个工具可以打开
- ✅ 自动更新检查正常工作

---

### 第 2 步：更新版本号

#### 2.1 编辑版本文件
打开 `version.txt`，更新版本号：

```
1.0.1
```

**版本号规范**：
- `major.minor.patch` 格式
- 例如：`1.0.0`, `1.0.1`, `1.1.0`, `2.0.0`

#### 2.2 更新 Inno Setup 配置
打开 `installer.iss`，确保版本号一致：

```ini
#define MyAppVersion "1.0.1"
```

---

### 第 3 步：提交代码到 Git

#### 3.1 添加所有改动
```bash
git add .
```

#### 3.2 提交代码
```bash
git commit -m "Release v1.0.1

- 改进 1
- 改进 2
- 改进 3"
```

#### 3.3 推送到 GitHub
```bash
git push
```

**重要**：确保代码已推送到 GitHub，这样用户才能检查到更新。

---

### 第 4 步：构建安装程序

#### 4.1 运行构建脚本
```bash
build_installer_auto.bat
```

这个脚本会自动：
1. ✅ 检查 Python 环境
2. ✅ 编译 Python 代码为 EXE
3. ✅ 调用 Inno Setup 生成安装程序
4. ✅ 打开输出文件夹

#### 4.2 验证输出文件
构建完成后，检查 `dist/` 文件夹：
- ✅ `Centisky-Setup-1.0.1.exe` - 安装程序文件

**文件大小**：通常 50-100MB（取决于依赖项）

---

### 第 5 步：测试安装程序

#### 5.1 在干净的系统上测试（推荐）
1. 在虚拟机或其他电脑上测试
2. 运行 `Centisky-Setup-1.0.1.exe`
3. 按照向导完成安装
4. 启动应用，验证功能正常

#### 5.2 验证自动更新功能
1. 启动已安装的应用
2. 等待 5-10 秒
3. 如果有新版本，会弹窗提示更新
4. 点击"是"应该打开下载页面

#### 5.3 检查关键功能
- ✅ 主应用启动正常
- ✅ 各个工具可以打开
- ✅ 没有显示窗口图标
- ✅ 自动更新检查正常

---

### 第 6 步：创建 GitHub Release

#### 6.1 打开 GitHub Releases 页面
访问：https://github.com/Benji-Xu/Centisky/releases

#### 6.2 创建新 Release
点击 "Create a new release"

#### 6.3 填写 Release 信息

**Tag version**：`v1.0.1`
- 必须以 `v` 开头
- 格式：`v主版本.次版本.补丁版本`

**Release title**：`Centisky v1.0.1`

**Description**：
```markdown
## 🎉 新版本发布

### ✨ 新功能
- 功能 1
- 功能 2

### 🐛 修复
- 修复 1
- 修复 2

### 🔧 改进
- 改进 1
- 改进 2

### 📥 下载
- Windows 安装程序：Centisky-Setup-1.0.1.exe

### 📝 更新说明
详见 [更新日志](../../blob/main/CHANGES_SUMMARY.txt)

### 🙏 感谢
感谢所有用户的支持和反馈！
```

#### 6.4 上传安装程序文件
1. 点击 "Attach binaries by dropping them here or selecting them"
2. 选择 `dist/Centisky-Setup-1.0.1.exe`
3. 等待上传完成

#### 6.5 发布 Release
点击 "Publish release"

---

### 第 7 步：验证发布

#### 7.1 检查 Release 页面
访问：https://github.com/Benji-Xu/Centisky/releases
- ✅ 新 Release 已显示
- ✅ 版本号正确
- ✅ 安装程序文件已上传
- ✅ 下载链接可用

#### 7.2 测试用户更新
1. 在已安装旧版本的电脑上测试
2. 启动应用
3. 等待自动更新检查
4. 应该弹窗提示新版本
5. 点击"是"应该打开下载页面

---

## 🔍 自动更新工作原理

### 用户端流程

```
用户启动应用
    ↓
后台线程启动
    ↓
读取本地版本 (version.txt)
    ↓
连接 GitHub API
    ↓
获取最新 Release 信息
    ↓
比较版本号
    ├─ 本地版本 < 远程版本 → 显示更新提示
    └─ 本地版本 >= 远程版本 → 正常启动
```

### 关键配置

**本地版本文件**：`version.txt`
```
1.0.1
```

**GitHub 配置**：`program/update_checker.py`
```python
GITHUB_OWNER = "Benji-Xu"
GITHUB_REPO = "Centisky"
GITHUB_API_URL = "https://api.github.com/repos/Benji-Xu/Centisky/releases/latest"
```

**版本检查逻辑**：
1. 从 GitHub API 获取最新 Release
2. 提取 tag_name（如 `v1.0.1`）
3. 去掉 `v` 前缀，得到版本号 `1.0.1`
4. 与本地版本号比较
5. 如果远程版本更新，显示提示

---

## ✅ 打包检查清单

### 代码准备
- [ ] 所有代码已测试
- [ ] 所有 bug 已修复
- [ ] 代码已提交到 Git
- [ ] 代码已推送到 GitHub

### 版本管理
- [ ] `version.txt` 已更新
- [ ] `installer.iss` 版本号已更新
- [ ] 版本号格式正确（`major.minor.patch`）
- [ ] 版本号大于当前版本

### 构建验证
- [ ] 运行 `check_setup.bat` 成功
- [ ] 运行 `build_installer_auto.bat` 成功
- [ ] 安装程序文件已生成
- [ ] 文件大小合理（50-100MB）

### 安装测试
- [ ] 在干净系统上测试安装
- [ ] 应用启动正常
- [ ] 各个工具可以打开
- [ ] 自动更新检查正常

### GitHub 发布
- [ ] Release 标签格式正确（`v1.0.1`）
- [ ] Release 标题正确
- [ ] Release 说明完整
- [ ] 安装程序文件已上传
- [ ] Release 已发布

### 用户更新验证
- [ ] 旧版本用户收到更新提示
- [ ] 点击"是"打开下载页面
- [ ] 新安装程序可以下载
- [ ] 新版本安装正常

---

## 🚀 快速打包流程（总结）

```bash
# 1. 检查环境
check_setup.bat

# 2. 更新版本号
# 编辑 version.txt，例如：1.0.1

# 3. 提交代码
git add .
git commit -m "Release v1.0.1"
git push

# 4. 构建安装程序
build_installer_auto.bat

# 5. 测试安装程序
# 运行 dist/Centisky-Setup-1.0.1.exe

# 6. 创建 GitHub Release
# 打开 https://github.com/Benji-Xu/Centisky/releases
# 创建新 Release，标签：v1.0.1
# 上传：dist/Centisky-Setup-1.0.1.exe
# 发布

# 完成！用户会自动检测到新版本
```

---

## 📊 版本号管理

### 版本号规范

| 版本 | 用途 | 例子 |
|------|------|------|
| 主版本 | 大功能更新 | 1.0.0 → 2.0.0 |
| 次版本 | 新功能 | 1.0.0 → 1.1.0 |
| 补丁版本 | bug 修复 | 1.0.0 → 1.0.1 |

### 版本号示例

```
1.0.0  初始版本
1.0.1  修复 bug
1.1.0  添加新功能
1.1.1  修复 bug
2.0.0  大版本更新
```

---

## 🔐 安全考虑

### GitHub 仓库要求
- ✅ 仓库必须是**公开的**
- ✅ 自动更新才能正常工作
- ✅ 用户可以访问 Release 页面

### 版本检查安全性
- ✅ 使用 HTTPS 连接 GitHub API
- ✅ 5 秒超时防止卡顿
- ✅ 网络错误时自动跳过
- ✅ 不下载或执行任何文件
- ✅ 用户完全控制是否更新

### 安装程序安全性
- ✅ 使用 Inno Setup 的 LZMA 压缩
- ✅ 支持代码签名（可选）
- ✅ GitHub Releases 自动验证文件完整性

---

## 🐛 常见问题

### Q1: 用户没有收到更新提示
**检查**：
- [ ] GitHub 仓库是否公开
- [ ] Release 标签格式是否正确（必须是 `v1.0.0`）
- [ ] 远程版本号是否大于本地版本号
- [ ] 用户网络连接是否正常

### Q2: 安装程序无法运行
**解决**：
- [ ] 重新运行 `build_installer_auto.bat`
- [ ] 检查 `program/dist/Workit/` 目录
- [ ] 查看 PyInstaller 输出日志

### Q3: Inno Setup 编译失败
**解决**：
- [ ] 确认 Inno Setup 6 已安装
- [ ] 检查安装路径：`C:\Program Files (x86)\Inno Setup 6\`
- [ ] 以管理员身份运行构建脚本

### Q4: 如何支持自动安装更新？
**答**：需要额外的更新器程序，可以使用 Squirrel.Windows 或 Wix Toolset。

---

## 📝 发布清单模板

```markdown
## 🎉 Centisky v1.0.1 发布

### ✨ 新功能
- [ ] 功能 1
- [ ] 功能 2

### 🐛 修复
- [ ] 修复 1
- [ ] 修复 2

### 🔧 改进
- [ ] 改进 1
- [ ] 改进 2

### 📥 下载
- Windows 安装程序：Centisky-Setup-1.0.1.exe

### 🙏 感谢
感谢所有用户的支持和反馈！
```

---

## 🎯 后续维护

### 每次发布前
1. ✅ 运行 `check_setup.bat` 检查环境
2. ✅ 在干净系统上测试安装程序
3. ✅ 测试升级流程（从旧版本升级）
4. ✅ 验证自动更新功能

### 每个月
1. ✅ 检查 GitHub Issues
2. ✅ 回复用户反馈
3. ✅ 检查下载统计

### 定期
1. ✅ 审查更新日志
2. ✅ 计划下一个版本
3. ✅ 备份 GitHub 仓库

---

## 📞 获取帮助

### 查看相关文档
- `INSTALLER_QUICK_START.md` - 快速开始指南
- `GITHUB_RELEASE_GUIDE.md` - 完整发布指南
- `INSTALLER_SETUP_COMPLETE.md` - 详细设置说明
- `QUICK_REFERENCE.txt` - 快速参考卡

### 运行相关脚本
- `check_setup.bat` - 检查环境
- `build_installer_auto.bat` - 构建安装程序
- `verify_improvements.bat` - 验证改进

### 查看源代码
- `installer.iss` - Inno Setup 配置
- `program/update_checker.py` - 自动更新模块
- `version.txt` - 版本号文件

---

## 🎊 总结

### 打包流程
1. ✅ 准备工作 - 检查环境和测试应用
2. ✅ 更新版本号 - 更新 `version.txt` 和 `installer.iss`
3. ✅ 提交代码 - Git 提交和推送
4. ✅ 构建安装程序 - 运行 `build_installer_auto.bat`
5. ✅ 测试安装程序 - 在干净系统上测试
6. ✅ 创建 GitHub Release - 上传安装程序
7. ✅ 验证发布 - 测试用户更新

### 自动更新保证
- ✅ 本地版本号在 `version.txt` 中
- ✅ GitHub Release 标签格式正确
- ✅ 自动更新检查代码正常工作
- ✅ 用户网络连接正常

### 立即开始
```bash
check_setup.bat              # 检查环境
build_installer_auto.bat     # 构建安装程序
# 然后创建 GitHub Release
```

---

**指南完成日期**：2024年12月1日  
**作者**：Benjamin  
**版本**：1.0.0  
**状态**：✅ 完成
