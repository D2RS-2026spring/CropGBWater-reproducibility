from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

required_files = [
    ROOT / "data/raw/Data_S4_four_crops/Data_S4_Y2020_WF_Maize_grid_avg.csv",
    ROOT / "data/raw/Data_S4_four_crops/Data_S4_Y2020_WF_Rice_grid_avg.csv",
    ROOT / "data/raw/Data_S4_four_crops/Data_S4_Y2020_WF_Soybean_grid_avg.csv",
    ROOT / "data/raw/Data_S4_four_crops/Data_S4_Y2020_WF_Wheat_grid_avg.csv",
    ROOT / "data/raw/paper_reported_totals_2020.csv",
]

missing = [str(p.relative_to(ROOT)) for p in required_files if not p.exists()]

if missing:
    print("Missing required files:")
    for item in missing:
        print("-", item)
    raise SystemExit(1)

print("All required raw data files exist.")
