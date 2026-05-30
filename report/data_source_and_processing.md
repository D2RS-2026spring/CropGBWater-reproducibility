本项目复现对象为 CropGBWater 项目。原始论文与数据代码来源如下：

- 论文：Global spatially explicit crop water consumption shows an overall increase of 9% for 46 agricultural crops from 2010 to 2020
- 期刊：Nature Food
- 论文 DOI：https://doi.org/10.1038/s43016-025-01231-x
- 数据与代码仓库：https://doi.org/10.5281/zenodo.13901563

## 2. 本项目的数据处理范围

由于完整 CropGBWater 数据体积较大，本课程项目采用局部复现策略，重点复现 2020 年四种主要作物：

- Maize
- Soybean
- Rice
- Wheat

本项目使用的 processed 数据文件为：

data/processed/four_crop_2020_water_consumption.csv

## 3. 数据字段说明

该 processed 表包括以下字段：

- crop：作物名称
- rainfed_green_km3：雨养绿水消耗，单位为 km³
- irrigated_green_km3：灌溉绿水消耗，单位为 km³
- blue_water_km3：蓝水消耗，单位为 km³
- paddy_flooding_km3：稻田淹灌附加水耗，仅 Rice 使用，单位为 km³
- reproduced_total_km3：本组复现总量，单位为 km³
- paper_reported_total_km3：论文主文报告总量，单位为 km³

## 4. 处理脚本

本部分对应脚本为：

code/01_prepare_four_crop_data.py

该脚本用于生成课程项目使用的轻量级 processed 数据表，使后续总量计算、图表绘制和 Quarto 报告可以在不下载完整原始数据的情况下运行。

## 5. 说明

当前 processed 数据用于课程项目的局部复现和结果校验。若后续开展完整端到端复现，应进一步下载 Zenodo 原始数据，并按作者原始工作流重建所有作物、所有年份和所有空间输出。
