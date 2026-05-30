# CropGBWater 可复现性评估：2020 年全球四种主要作物蓝绿水消耗复现

## 1. 项目简介

本项目为“数据驱动可重复研究”课程结课项目，围绕 CropGBWater 项目的结果可复现性开展评估。复现对象为发表在 *Nature Food* 的论文：

**Global spatially explicit crop water consumption shows an overall increase of 9% for 46 agricultural crops from 2010 to 2020**

论文链接：https://doi.org/10.1038/s43016-025-01231-x
数据与代码来源：https://doi.org/10.5281/zenodo.13901563

本项目不尝试完整复现全部 46 种作物和所有年份，而是选择一个明确、可检查、可运行的局部复现目标：

> 基于作者公开的 Data_S4 2020 年格点结果文件，复现 Maize、Soybean、Rice 和 Wheat 四种主要作物的全球蓝水与绿水消耗总量，并与论文主文报告值进行对照。

该设计的重点不是重新运行完整 CropGBWater 原始逐日模型，而是检验作者公开的标准结果数据是否能够支持关键作物层面的结果复现。

## 2. 小组成员

* @LingerYU 余玲儿（2025303120004）
* @159368qwe 余明哲（2025303110002）
* @SCD1106 宋晨迪（2025303120167）
* @hewen717478 何文（2025303120003）

## 3. 仓库地址与网页报告

项目仓库：

https://github.com/D2RS-2026spring/CropGBWater-reproducibility

GitHub Pages 网页报告：

https://d2rs-2026spring.github.io/CropGBWater-reproducibility/

## 4. 仓库结构

```text
CropGBWater-reproducibility/
├── code/
│   ├── 00_check_required_data.py
│   ├── 01_prepare_four_crop_data.py
│   ├── 02_calculate_totals.py
│   ├── 03_make_figures.py
│   ├── 04_error_analysis.py
│   ├── 05_reproducibility_check.py
│   └── run_all.py
│
├── data/
│   ├── raw/
│   │   ├── Data_S4_four_crops/
│   │   │   ├── Data_S4_Y2020_WF_Maize_grid_avg.csv
│   │   │   ├── Data_S4_Y2020_WF_Rice_grid_avg.csv
│   │   │   ├── Data_S4_Y2020_WF_Soybean_grid_avg.csv
│   │   │   └── Data_S4_Y2020_WF_Wheat_grid_avg.csv
│   │   └── paper_reported_totals_2020.csv
│   │
│   └── processed/
│       ├── four_crop_2020_water_consumption.csv
│       └── four_crop_2020_water_components_long.csv
│
├── outputs/
│   ├── figures/
│   │   ├── fig1_water_structure.png
│   │   ├── fig2_reproduced_vs_reported.png
│   │   └── fig3_relative_error.png
│   │
│   └── tables/
│       ├── four_crop_reproduction_summary.csv
│       ├── error_analysis_summary.csv
│       └── reproducibility_check.csv
│
├── docs/
├── report/
├── index.qmd
├── README.md
├── requirements.txt
└── _quarto.yml
```

## 5. 数据说明

本项目直接在仓库中提供复现所需的四个原始 Data_S4 格点结果文件，位于：

```text
data/raw/Data_S4_four_crops/
```

四个文件分别对应：

* Maize
* Soybean
* Rice
* Wheat

这些文件来自作者公开的 Data_S4 2020 年作物水消耗格点结果，包含年度尺度的雨养绿水、灌溉绿水、蓝水等变量。Rice 额外包含稻田淹灌附加耗水项。

论文主文报告值整理在：

```text
data/raw/paper_reported_totals_2020.csv
```

该文件用于与本组复现得到的四作物全球总量进行对照。

## 6. 快速复现步骤

克隆仓库：

```bash
git clone https://github.com/D2RS-2026spring/CropGBWater-reproducibility.git
cd CropGBWater-reproducibility
```

安装 Python 依赖：

```bash
pip install -r requirements.txt
```

运行完整复现流程：

```bash
python code/run_all.py
```

该命令会依次完成：

1. 检查原始 Data_S4 文件是否存在；
2. 从四个原始格点 CSV 汇总四作物 2020 年全球蓝绿水消耗；
3. 生成 processed 数据；
4. 计算复现值与论文报告值之间的误差；
5. 生成主要图表；
6. 生成可复现性检查表。

## 7. 复现输出

运行 `python code/run_all.py` 后，将重新生成以下结果。

### 7.1 Processed 数据

```text
data/processed/four_crop_2020_water_consumption.csv
data/processed/four_crop_2020_water_components_long.csv
```

### 7.2 结果表

```text
outputs/tables/four_crop_reproduction_summary.csv
outputs/tables/error_analysis_summary.csv
outputs/tables/reproducibility_check.csv
```

### 7.3 图件

```text
outputs/figures/fig1_water_structure.png
outputs/figures/fig2_reproduced_vs_reported.png
outputs/figures/fig3_relative_error.png
```

## 8. 当前主要结果

本组基于 Data_S4 原始格点结果重新汇总得到的四种作物 2020 年全球总水消耗与论文主文报告值高度一致：

* Maize：复现值约 859.77 km³，论文报告值约 860 km³，相对误差约 -0.027%。
* Soybean：复现值约 520.92 km³，论文报告值约 521 km³，相对误差约 -0.016%。
* Rice：复现值约 1183.47 km³，论文报告值约 1183 km³，相对误差约 0.040%。
* Wheat：复现值约 765.27 km³，论文报告值约 765 km³，相对误差约 0.036%。

四种作物的相对误差均小于 0.05%，说明在 2020 年四种关键作物全球总量这一局部目标上，CropGBWater 公开结果具有较高的结果可复现性。

## 9. 独立复现测试

本组已进行独立 clone 测试：

```bash
git clone https://github.com/D2RS-2026spring/CropGBWater-reproducibility.git
cd CropGBWater-reproducibility
pip install -r requirements.txt
python code/run_all.py
```

测试结果表明，仓库可以从内置的四个 Data_S4 原始 CSV 文件重新生成 processed 数据、结果表和图件。最终运行输出为：

```text
All required files exist.
All reproduction steps completed.
```

## 10. 可复现性评价

从当前局部复现结果看，CropGBWater 项目在关键结果数据公开性方面表现较好。作者公开的 Data_S4 格点结果能够支持四种关键作物 2020 年全球总量的独立汇总与结果校验。

本项目当前实现的是“结果数据层面的局部复现”，即基于作者公开的标准格点输出重新汇总主文关键结果。它不等同于完整运行 CropGBWater 原始逐日模型。

## 11. 局限性

本项目尚未完整复现：

* 全部 46 种作物；
* 2010—2020 年全部年份；
* 完整逐日 CropGBWater 原始模型；
* 所有空间中间变量；
* 原始气象、土壤和作物历输入数据的端到端处理流程。

该设计的目的是在课程项目范围内构建一个小而完整、可检查、可运行的复现工作流。
