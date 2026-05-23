import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

input_file = ROOT / "data" / "processed" / "four_crop_2020_water_consumption.csv"
output_dir = ROOT / "outputs" / "tables"
output_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(input_file)

component_cols = [
    "rainfed_green_km3",
    "irrigated_green_km3",
    "blue_water_km3",
    "paddy_flooding_km3",
]

df["calculated_total_km3"] = df[component_cols].sum(axis=1)
df["difference_km3"] = df["reproduced_total_km3"] - df["paper_reported_total_km3"]
df["absolute_difference_km3"] = df["difference_km3"].abs()
df["relative_difference_percent"] = (
    df["difference_km3"] / df["paper_reported_total_km3"] * 100
)

output_file = output_dir / "four_crop_reproduction_summary.csv"
df.to_csv(output_file, index=False)

print("Saved:", output_file)
print(df[[
    "crop",
    "reproduced_total_km3",
    "paper_reported_total_km3",
    "difference_km3",
    "relative_difference_percent"
]])
