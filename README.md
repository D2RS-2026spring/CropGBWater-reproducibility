# CropGBWater 可复现性评估：2020 年全球四种主粮作物蓝绿水消耗复现

## 1. 项目简介

本项目为数据驱动可重复研究课程结课项目，围绕 CropGBWater 项目的可复现性开展评估。复现对象为发表在 Nature Food 的论文：Global spatially explicit crop water consumption shows an overall increase of 9% for 46 agricultural crops from 2010 to 2020。

论文链接：https://doi.org/10.1038/s43016-025-01231-x

数据与代码来源：https://doi.org/10.5281/zenodo.13901563

本项目不尝试完整复现全部 46 种作物和所有年份，而是选择一个明确、可检查、可运行的局部复现目标：复现 2020 年全球 Maize、Soybean、Rice 和 Wheat 四种主要作物的蓝水与绿水消耗结果。

## 2. 小组成员

- @LingerYU 余玲儿（2025303120004）
- @159368qwe 余明哲（2025303110002）
- @SCD1106 宋晨迪（2025303120167）
- @hewen717478 何文（2025303120003）

## 3. 仓库结构

- code：数据汇总和作图脚本
- data/raw：原始数据来源说明
- data/processed：课程项目使用的轻量级 processed 数据
- outputs/figures：复现生成的图表
- outputs/tables：复现生成的结果表
- docs：Quarto 渲染生成的网页报告
- index.qmd：Quarto 主报告
- requirements.txt：Python 依赖包

## 4. 数据说明

原始数据来自作者公开的 Zenodo 仓库。由于原始数据体积较大，本课程项目不直接上传完整原始数据，而是提供整理后的四作物 2020 年结果表，用于复现主要图表和结果对照。

核心 processed 数据文件为：

data/processed/four_crop_2020_water_consumption.csv

## 5. 复现步骤

克隆仓库后，进入项目目录：

git clone https://github.com/LingerYU/CropGBWater-reproducibility.git
cd CropGBWater-reproducibility

安装 Python 依赖：

pip install -r requirements.txt

运行结果汇总脚本：

python code/02_calculate_totals.py

运行作图脚本：

python code/03_make_figures.py

渲染 Quarto 报告：

quarto render

渲染完成后，打开以下文件查看网页报告：

docs/index.html

## 6. 当前主要结果

本组复现结果与论文主文报告值高度一致：

- Maize：复现值约 859.8 km³，论文报告值约 860 km³。
- Soybean：复现值约 520.9 km³，论文报告值约 521 km³。
- Rice：复现值约 1183.5 km³，论文报告值约 1183 km³。
- Wheat：复现值约 765.3 km³，论文报告值约 765 km³。

四种作物的相对误差均小于 0.05%，说明在 2020 年四种关键作物全球总量这一局部目标上，CropGBWater 项目具有较高的结果可复现性。

## 7. 可复现性评价

从当前局部复现结果看，CropGBWater 项目的数据公开性较高，作者提供的输出结果能够支持关键作物层面的结果校验。代码层面具备进一步复现基础，但完整端到端复现仍可能受到数据体积、运行环境、路径设置和 notebook 执行顺序的影响。

## 8. 局限性

本项目属于局部复现，尚未完整复现全部 46 种作物、2010—2020 年全部年度结果和所有空间中间变量。该设计的目的是在课程项目范围内构建一个小而完整、可检查、可运行的可复现工作流。
