# FFmpeg 安装指南

视频处理工具需要 FFmpeg 支持。如果您不使用视频处理功能，可以跳过此安装。

## Windows 安装步骤

### 方法一：使用 Chocolatey（推荐）

如果已安装 Chocolatey 包管理器：

```powershell
choco install ffmpeg
```

### 方法二：手动安装

1. **下载 FFmpeg**
   - 访问官网：https://ffmpeg.org/download.html
   - 或直接访问：https://github.com/BtbN/FFmpeg-Builds/releases
   - 下载 `ffmpeg-master-latest-win64-gpl.zip`

2. **解压文件**
   - 将下载的压缩包解压到任意目录，例如：`C:\ffmpeg`
   - 解压后目录结构应该是：
     ```
     C:\ffmpeg\
     ├── bin\
     │   ├── ffmpeg.exe
     │   ├── ffplay.exe
     │   └── ffprobe.exe
     ├── doc\
     └── presets\
     ```

3. **添加到系统环境变量**
   
   **方式A：通过系统设置（推荐）**
   - 右键点击"此电脑" → "属性"
   - 点击"高级系统设置"
   - 点击"环境变量"
   - 在"系统变量"中找到 `Path`，点击"编辑"
   - 点击"新建"，输入 FFmpeg 的 bin 目录路径：`C:\ffmpeg\bin`
   - 依次点击"确定"保存所有更改
   
   **方式B：使用命令行（需要管理员权限）**
   ```powershell
   # 打开 PowerShell（管理员）
   setx /M PATH "$env:PATH;C:\ffmpeg\bin"
   ```

4. **验证安装**
   - 打开新的命令提示符或 PowerShell 窗口
   - 运行以下命令：
   ```bash
   ffmpeg -version
   ```
   - 如果显示版本信息，说明安装成功！

## 常见问题

### 问题1：命令提示符显示 "ffmpeg 不是内部或外部命令"

**解决方案：**
1. 确认已将 FFmpeg 的 bin 目录添加到环境变量 PATH
2. 重启命令提示符或 PowerShell
3. 如果仍然无效，重启计算机

### 问题 2：Workit 提示未检测到 FFmpeg

**解决方案：**
1. 按上述步骤验证 FFmpeg 是否正确安装
2. 完全关闭 Workit 程序
3. 重新启动 Workit

### 问题3：下载速度慢

**解决方案：**
- 使用国内镜像站下载：
  - 清华大学镜像：https://mirrors.tuna.tsinghua.edu.cn/
  - 阿里云镜像：https://mirrors.aliyun.com/

## 支持的功能

安装 FFmpeg 后，您可以使用以下视频处理功能：

✅ **格式转换**
- MP4、AVI、MOV、MKV 等常见格式互转

✅ **视频压缩**
- 可指定目标文件大小（KB/MB）
- 自动计算最优比特率
- 智能压缩算法

✅ **提取视频封面**
- 支持 JPG、PNG 格式
- 可设置最小尺寸要求（宽度x高度）
- 自动跳过不符合尺寸要求的视频

✅ **批量处理**
- 支持一次处理多个文件
- 支持文件夹批量处理

## 技术支持

如果遇到问题，请访问：
- FFmpeg 官方文档：https://ffmpeg.org/documentation.html
- GitHub Issues：https://github.com/Benji-Xu/Workit/issues

---

**注意：** FFmpeg 是一个开源项目，遵循 GPL/LGPL 许可证。使用时请遵守相关许可协议。

