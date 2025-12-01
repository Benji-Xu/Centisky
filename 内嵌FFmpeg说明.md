# 内嵌 FFmpeg 到 Workit

## 📋 步骤

### 1. 下载 FFmpeg

访问：https://github.com/BtbN/FFmpeg-Builds/releases

下载文件：`ffmpeg-master-latest-win64-gpl.zip`

### 2. 提取可执行文件

解压下载的 ZIP 文件，找到 `bin` 目录，复制以下文件：
- `ffmpeg.exe`
- `ffprobe.exe`

### 3. 放置文件

将这两个文件放到项目目录：
```
Workit/
└── program/
    └── ffmpeg/          ← 创建这个文件夹
        ├── ffmpeg.exe   ← 放这里
        └── ffprobe.exe  ← 放这里
```

### 4. 代码已自动适配

视频处理工具已经配置为：
1. 优先使用内嵌的 FFmpeg（`program/ffmpeg/`）
2. 如果找不到，再使用系统 PATH 中的 FFmpeg

### 5. 重新打包

运行构建脚本：
```bash
build_exe.bat
```

打包后的程序会自动包含 FFmpeg，用户无需单独安装！

---

## 📦 打包后的结构

```
Workit/
└── _internal/
    └── ffmpeg/
        ├── ffmpeg.exe
        └── ffprobe.exe
```

程序会自动检测并使用内嵌的 FFmpeg。

---

## ⚠️ 注意事项

**文件大小**
- ffmpeg.exe: 约 100 MB
- ffprobe.exe: 约 100 MB
- 总计会增加约 200 MB

**许可证**
- FFmpeg 使用 GPL 许可证
- 确保遵守相关许可协议

---

## ✅ 优势

- ✅ 用户无需手动安装 FFmpeg
- ✅ 开箱即用
- ✅ 避免环境变量配置问题
- ✅ 版本统一，避免兼容性问题


