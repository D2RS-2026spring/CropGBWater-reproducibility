# 环境与运行流程检查说明

本部分由何文负责，主要补充本项目的环境配置、运行流程和可复现性检查。

## 1. 环境依赖

本项目使用 Python 和 Quarto 构建可复现工作流。

Python 依赖记录在：

requirements.txt

主要包括：

- pandas
- numpy
- matplotlib
- seaborn
- plotly
- jupyter

安装依赖的命令为：

pip install -r requirements.txt

## 2. 推荐运行顺序

本项目推荐按以下顺序运行：

第一步，生成 processed 数据表：

python code/01_prepare_four_crop_data.py

第二步，计算四种作物总量和误差：

python code/02_calculate_totals.py

第三步，生成主要图表：

python code/03_make_figures.py

第四步，运行误差分析：

python code/04_error_analysis.py

第五步，运行可复现性检查：

python code/05_reproducibility_check.py

第六步，渲染 Quarto 报告：

quarto render

## 3. 输出文件检查

本部分新增脚本：

code/05_reproducibility_check.py

该脚本会检查 README、Quarto 报告、数据表、代码脚本、输出图表和网页报告是否存在，并生成：

outputs/tables/reproducibility_check.csv

该文件用于辅助判断项目结构是否完整，是否具备课程级可复现性。

## 4. GitHub Pages 报告

本项目已经通过 GitHub Pages 发布网页报告：

https://lingeryu.github.io/CropGBWater-reproducibility/

该网页由 Quarto 渲染生成，源文件为：

index.qmd

渲染输出位于：

docs/index.html

## 5. 环境可复现性评价

当前项目使用轻量级 processed 数据和标准 Python 包，因此比完整运行 CropGBWater 原始模型更容易在不同电脑上复现。该设计符合课程结课项目“小而完整、可检查、可运行”的要求。

需要说明的是，如果未来进行完整模型级复现，还需要进一步固定 Python 版本、原始数据目录结构、数据下载方式和 notebook 执行顺序。

## 6. 小结

从环境与运行流程角度看，本项目已经提供了较清晰的依赖文件、脚本顺序、输出文件和网页报告，具备较好的课程级可复现性。