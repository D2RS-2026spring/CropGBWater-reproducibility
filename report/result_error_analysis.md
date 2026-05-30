---
title: "Untitled"
format: html
---

# 结果误差分析与图表复现说明

本部分由宋晨迪负责，主要补充本项目的结果误差分析和可视化输出检查。

## 1. 分析目标

本项目的核心目标是比较本组复现值与论文主文报告值是否一致。为此，本部分进一步计算四种作物的绝对误差和相对误差，并生成误差分析图。

## 2. 对应脚本

本部分对应脚本为：

code/04_error_analysis.py

该脚本读取：

outputs/tables/four_crop_reproduction_summary.csv

并输出：

outputs/tables/error_analysis_summary.csv

以及：

outputs/figures/fig3_relative_error.png

## 3. 误差指标

误差分析包括三个指标：

- difference_km3：本组复现值减去论文报告值
- absolute_difference_km3：绝对差异
- relative_difference_percent：相对差异百分比

相对差异计算方式为：

relative difference = difference / paper reported total × 100%

## 4. 当前结果解释

当前四种作物的相对误差均小于 0.05%。这说明本组在 2020 年四种主要作物全球总水消耗这一局部目标上，能够较好复现论文主文结果。

从作物层面看：

- Maize 和 Soybean 的复现值略低于论文报告值；
- Rice 和 Wheat 的复现值略高于论文报告值；
- 所有差异均非常小，主要可归因于四舍五入和结果汇总精度差异。

## 5. 图表复现性评价

本项目图表均由 Python 脚本自动生成，而不是手工绘制。运行结果汇总脚本和作图脚本后，可以重新生成主要结果表和图表。因此，本项目在图表层面具有较好的可复现性。

## 6. 小结

误差分析进一步支持本项目的主要判断：CropGBWater 在 2020 年四种关键作物全球总量结果上具有较高结果可复现性。