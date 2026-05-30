from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

required_files = [
    "README.md",
    "_quarto.yml",
    "index.qmd",
    "requirements.txt",
    "data/raw/paper_reported_totals_2020.csv",
    "data/raw/Data_S4_four_crops/Data_S4_Y2020_WF_Maize_grid_avg.csv",
    "data/raw/Data_S4_four_crops/Data_S4_Y2020_WF_Rice_grid_avg.csv",
    "data/raw/Data_S4_four_crops/Data_S4_Y2020_WF_Soybean_grid_avg.csv",
    "data/raw/Data_S4_four_crops/Data_S4_Y2020_WF_Wheat_grid_avg.csv",
    "data/processed/four_crop_2020_water_consumption.csv",
    "data/processed/four_crop_2020_water_components_long.csv",
    "code/00_check_required_data.py",
    "code/01_prepare_four_crop_data.py",
    "code/02_calculate_totals.py",
    "code/03_make_figures.py",
    "code/04_error_analysis.py",
    "code/05_reproducibility_check.py",
    "code/run_all.py",
    "outputs/tables/four_crop_reproduction_summary.csv",
    "outputs/tables/error_analysis_summary.csv",
    "outputs/figures/fig1_water_structure.png",
    "outputs/figures/fig2_reproduced_vs_reported.png",
    "outputs/figures/fig3_relative_error.png",
    "docs/index.html",
]

records = []

for item in required_files:
    path = ROOT / item
    records.append(
        {
            "file": item,
            "exists": path.exists(),
            "size_bytes": path.stat().st_size if path.exists() else 0,
        }
    )

check_df = pd.DataFrame(records)

output_dir = ROOT / "outputs/tables"
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "reproducibility_check.csv"
check_df.to_csv(output_file, index=False)

print("Saved:", output_file)
print(check_df)

missing = check_df.loc[~check_df["exists"], "file"].tolist()

if missing:
    print("Missing files:")
    for item in missing:
        print("-", item)
    raise SystemExit(1)

print("All required files exist.")
