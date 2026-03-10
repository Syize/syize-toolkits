# syize/一个简单好用的工具箱

syize 是一个集合了多种实用工具的 Python 包，主要用于处理字符串、图片、PDF、Fortran 代码、NetCDF 数据以及电视节目管理等任务。这些工具是为了简化日常开发、数据分析和处理工作而设计的。

## 功能模块

### 1. 字符串处理 (`syize.string`)
- **格式化字符串**：`format_string` - 自动格式化字符串，去除冗余换行符
- **去除冗余换行**：`remove_redundant_linebreak` - 智能处理文本中的换行符

### 2. 图片处理 (`syize.picture`)
- **图片转文字**：`picture_to_string` - 使用 OCR 技术从图片中提取文本（支持中文和英文）
- **PDF转图片**：`pdf_to_picture` - 将 PDF 文件转换为图片（PNG格式）

### 3. 代码处理 (`syize.fortran`)
- **Fortran代码解析**：`entry_parse_fortran` - 解析和格式化 Fortran 代码
- **代码格式化**：包含对 Fortran 代码的格式化和处理工具

### 4. 数据处理 (`syize.nc`)
- **NetCDF数据查看**：`NCView` - 提供交互式界面查看 NetCDF 数据文件
- **数据交互**：支持查看数据集属性、坐标、变量和数据内容

### 5. 可视化 (`syize.plot`)
- **地图绘制**：包含地图可视化相关工具（基于 Cartopy）
- **绘图辅助**：提供颜色条制备和图表调整功能

### 6. 电视节目管理 (`syize.tv_show_manage`)
- **节目排序**：`entry_sort_episode` - 识别并排序剧集文件
- **重命名**：`entry_rename_episode_file` - 重命名剧集文件
- **文件识别**：支持多种剧集编号格式

### 7. Qt 界面 (`syize.qt`)
- **下载器**：`Downloader` - 提供下载文件的图形界面
- **下载管理**：支持下载参数配置和进度监控

## 安装

使用 pip 安装：

```bash
pip install syize
```

或者通过源码安装：

```bash
git clone <repository_url>
cd syize-toolkits
pip install .
```

## 命令行使用

syize 提供了两个主要的命令行工具：

### 1. `syize` - 通用工具箱

```bash
syize -h  # 显示帮助信息
syize list  # 列出当前目录所有文件
syize ocr -i image.png -o output.txt  # 图片转文字
syize pdf -i document.pdf -o ./images  # PDF转图片
syize str -i input.txt -o output.txt  # 格式化字符串
syize nc -i data.nc  # 查看NetCDF数据
syize ft -i code.f90 -o formatted_code.f90  # 格式化Fortran代码
```

### 2. `tvsm` - 电视节目管理工具

```bash
tvsm -h  # 显示帮助信息
tvsm sort "Episode %%d"  # 排序剧集文件
tvsm rename "MyShow S01E"  # 重命名剧集文件
```

## 依赖

项目依赖以下 Python 包：
- Pillow, pytesseract (图片处理)
- pdf2image (PDF处理)
- rich (终端美化)
- matplotlib, Cartopy (可视化)
- haversine (地理计算)
- pyside6 (GUI界面)
- prompt-toolkit (交互式命令)
- xarray, netcdf4, numpy (数据处理)
- requests (网络请求)

## 开发

项目使用 Meson 构建系统：

```bash
meson setup build
cd build
ninja
```

## 文档

完整的 API 文档可以在 `docs/` 目录中找到，使用 Sphinx 生成。

## 许可证

本项目采用 GPL-3.0-or-later 许可证。