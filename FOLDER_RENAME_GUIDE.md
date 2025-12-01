# 文件夹重命名指南：Workit → Centisky

## 方式一：自动重命名（推荐）

### 步骤 1：关闭所有程序
确保没有任何程序正在使用 Workit 文件夹中的文件：
- 关闭 IDE（VS Code、PyCharm 等）
- 关闭文件浏览器中打开的 Workit 文件夹
- 关闭任何正在运行的 Python 程序

### 步骤 2：运行重命名脚本
1. 打开命令提示符（CMD）
2. 导航到 Workit 文件夹的**父目录**：
   ```bash
   cd D:\
   ```
3. 运行重命名脚本：
   ```bash
   Workit\rename_folder.bat
   ```

### 步骤 3：确认重命名
脚本会显示确认信息，按任意键继续。

### 步骤 4：验证结果
- 检查 `D:\Centisky` 文件夹是否存在
- 检查 `D:\Workit` 文件夹是否已删除

## 方式二：手动重命名

### 步骤 1：关闭所有程序
同上

### 步骤 2：打开文件浏览器
1. 按 `Win + E` 打开文件浏览器
2. 导航到 `D:\` 驱动器

### 步骤 3：重命名文件夹
1. 右键点击 `Workit` 文件夹
2. 选择 "重命名"
3. 输入 `Centisky`
4. 按 Enter 确认

### 步骤 4：验证结果
确保文件夹已成功重命名为 `Centisky`

## 方式三：命令行手动重命名

### 步骤 1：打开命令提示符
按 `Win + R`，输入 `cmd`，按 Enter

### 步骤 2：导航到父目录
```bash
cd D:\
```

### 步骤 3：重命名文件夹
```bash
ren Workit Centisky
```

### 步骤 4：验证结果
```bash
dir
```
确保看到 `Centisky` 文件夹

## 重命名后的操作

### 更新快捷方式
如果你有指向 Workit 的快捷方式，需要更新它们：
1. 右键点击快捷方式
2. 选择 "属性"
3. 更新目标路径：`D:\Centisky\...`

### 更新 IDE 项目路径
如果在 IDE 中打开了 Workit 项目：
1. 关闭项目
2. 打开新的 `D:\Centisky` 项目

### 更新环境变量（如果有）
如果设置了指向 Workit 的环境变量，需要更新：
1. 打开系统属性
2. 编辑环境变量
3. 更新路径为 `D:\Centisky`

## 常见问题

### Q: 重命名失败，显示"文件被占用"
**A**: 
1. 关闭所有打开的程序
2. 重启计算机
3. 再次运行重命名脚本

### Q: 重命名后程序无法启动
**A**:
1. 检查 `start.bat` 中的路径是否正确
2. 更新任何硬编码的路径
3. 重新生成安装程序

### Q: 如何撤销重命名
**A**:
1. 右键点击 `Centisky` 文件夹
2. 选择 "重命名"
3. 改回 `Workit`

### Q: 重命名后 GitHub 仓库怎么办
**A**:
1. 在 GitHub 上将仓库从 `Workit` 重命名为 `Centisky`
2. 或创建新的 `Centisky` 仓库
3. 更新本地仓库的远程地址：
   ```bash
   git remote set-url origin https://github.com/Benji-Xu/Centisky.git
   ```

## 重命名前的检查清单

- [ ] 关闭所有 IDE 和编辑器
- [ ] 关闭所有文件浏览器窗口
- [ ] 关闭所有正在运行的 Python 程序
- [ ] 备份重要文件（可选）
- [ ] 记下当前路径 `D:\Workit`

## 重命名后的验证清单

- [ ] `D:\Centisky` 文件夹存在
- [ ] `D:\Workit` 文件夹已删除
- [ ] 所有文件和子文件夹都在 `D:\Centisky` 中
- [ ] `start.bat` 可以正常运行
- [ ] 应用可以正常启动

## 相关文件

- `rename_folder.bat` - 自动重命名脚本
- `start.bat` - 启动脚本（已更新路径）
- `build_installer.bat` - 安装程序构建脚本
- `build_exe.bat` - EXE 构建脚本

## 支持

如有问题，请提交 Issue 到：
https://github.com/Benji-Xu/WeKit/issues

---

**重要**: 重命名后，所有指向 `D:\Workit` 的路径都需要更新为 `D:\Centisky`。
