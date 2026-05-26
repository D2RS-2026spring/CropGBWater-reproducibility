# 数据来源与 processed 数据构建说明

本部分由余明哲负责，主要补充本项目的数据来源、数据处理口径和 processed 数据表构建过程。

## 1. 原始数据来源

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