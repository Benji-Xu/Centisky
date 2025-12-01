# Centisky v1.0.0

Centisky 是一个客制化的工具集合，用于日常工作处理和自动化。

## 📋 功能特性

### 🏷️ 标签箱唛处理工具
- 自动生成标签和箱唛文件
- 支持 3C 和玩具两种类型
- 内置丰富的模板库
- Excel 数据批量处理
- 一键导出打印文件

### 🖼️ 图片处理工具
- 图片缩放（按比例/指定宽度，支持格式转换）
- 图片拼接成长图
- 长图智能切片
- 图片压缩优化
- 支持 SVG 格式（高清缩放导出）
- 支持文件夹批量处理
- **注意：SVG 支持需要安装 cairosvg**

### 📊 京准通数据分析
- 快车投流数据周对比分析
- 关键指标可视化展示
- 自动识别周数据
- 支持多种数据格式 （CSV、 Excel）
- 直观的图表对比

### 🎬 视频处理工具
- 标题处理（批量删除指定字符 + 导出标题到 Excel）
- 视频归类（根据 Excel 文件名单自动分类并移动到匹配 / 未匹配文件夹）
- 视频压缩（可指定目标文件大小，默认 40MB，智能跳过已满足大小的视频）
- 视频分组打包（720p 预处理 + 智能分组 + Excel 过滤 + ZIP 打包）
- 格式转换 （MP4、 AVI、 MOV、 MKV）
- 调整尺寸 （720p/1080p 预设，可同时提取封面或仅导出封面）
- 支持文件夹批量处理
- **注意：格式转换、压缩、调整尺寸、分组打包需要安装 FFmpeg**

### 📝 开票信息处理
- 从 Excel 文件生成开票 TXT 格式
- 智能选择工作表（优先 "发票模板"）
- 实时预览生成内容
- 支持统一社会信用代码等字段
- 自动格式化数字 （去除多余 0）

## 🚀 快速开始

### 方式一：直接运行（推荐）
1. 下载最新的 [Release](../../releases) 版本
2. 解压 `Centisky-v1.1.1-win64.zip`
3. 双击 `Workit.exe` 启动程序
4. 无需安装 Python 环境，开箱即用！

### 方式二：从源码运行
```bash
# 1. 克隆仓库
git clone https://github.com/Benji-Xu/Centisky.git
cd Centisky

# 2. 安装依赖
install.bat

# 3. 运行程序
start.bat
```

## 🛠️ 开发构建

### 环境要求
- Python 3.13+
- Windows 10/11
- FFmpeg （仅视频处理工具需要）

### FFmpeg 安装说明
视频处理工具需要 FFmpeg 支持，请按以下步骤安装：

1. 下载 FFmpeg：访问 [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. 下载 Windows 版本并解压到任意目录（如 `C:\ffmpeg`）
3. 将 FFmpeg 的 `bin` 目录添加到系统环境变量 PATH 中
4. 重启命令行 / 程序，验证安装：
```bash
ffmpeg -version
```

如果不使用视频处理工具，可以跳过 FFmpeg 安装。

### 构建可执行文件
```bash
# 安装构建依赖并生成 exe 文件
build_exe.bat
```

生成的可执行文件位于 `program/dist/Workit/` 目录下。

## 📦 项目结构

```
Centisky/
├── program/                    # 主程序目录
│   ├── launcher.py            # 启动器主界面
│   ├── tools/                 # 工具模块
│   │   ├── label_box/        # 标签箱唛工具
│   │   ├── image_processor/  # 图片处理工具
│   │   ├── jzt_analyzer/     # 京准通数据分析工具
│   │   ├── video_processor/  # 视频处理工具
│   │   └── invoice_processor/# 开票信息处理工具
│   ├── favicon.ico           # 程序图标
│   ├── icon-512.png          # Logo图片
│   └── requirements.txt      # Python依赖
├── templates/                 # 模板文件
│   ├── 标签模板 /             # 标签模板库
│   └── 箱唛模板 /             # 箱唛模板库
├── build_exe.bat             # 构建脚本
├── install.bat               # 安装依赖脚本
└── start.bat                 # 启动脚本
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目为私有项目，版权所有。

## 👨‍💻 开发者

Developed by Benjamin ([@Benji-Xu](https://github.com/Benji-Xu)) with Windsurf

---

⭐ 如果这个项目对你有帮助，请给个 Star！
