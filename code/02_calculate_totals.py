from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

input_file = ROOT / "data/processed/four_crop_2020_water_consumption.csv"
out_dir = ROOT / "outputs/tables"
out_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(input_file)

required_cols = [
    "crop",
    "rainfed_green_km3",
    "irrigated_green_km3",
    "blue_water_km3",
    "paddy_flooding_km3",
    "reproduced_total_km3",
    "paper_reported_total_km3",
]

missing = [c for c in required_cols if c not in df.columns]
if missing:
    raise ValueError(f"Missing columns in processed file: {missing}")

df["difference_km3"] = (
    df["reproduced_total_km3"]
    - df["paper_reported_total_km3"]
)

df["absolute_difference_km3"] = df["difference_km3"].abs()

df["relative_difference_percent"] = (
    df["difference_km3"]
    / df["paper_reported_total_km3"]
    * 100
)

out = df[
    [
        "crop",
        "rainfed_green_km3",
        "irrigated_green_km3",
        "blue_water_km3",
        "paddy_flooding_km3",
        "reproduced_total_km3",
        "paper_reported_total_km3",
        "difference_km3",
        "absolute_difference_km3",
        "relative_difference_percent",
    ]
].copy()

out_file = out_dir / "four_crop_reproduction_summary.csv"
out.to_csv(out_file, index=False)

print("Saved:", out_file)
print(out)
