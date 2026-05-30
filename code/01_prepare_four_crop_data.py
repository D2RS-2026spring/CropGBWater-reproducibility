import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

output_dir = ROOT / "data" / "processed"
output_dir.mkdir(parents=True, exist_ok=True)

data = [
    {
        "crop": "Maize",
        "rainfed_green_km3": 760.0,
        "irrigated_green_km3": 55.0,
        "blue_water_km3": 44.8,
        "paddy_flooding_km3": 0.0,
        "reproduced_total_km3": 859.8,
        "paper_reported_total_km3": 860.0,
    },
    {
        "crop": "Soybean",
        "rainfed_green_km3": 470.0,
        "irrigated_green_km3": 28.0,
        "blue_water_km3": 22.9,
        "paddy_flooding_km3": 0.0,
        "reproduced_total_km3": 520.9,
        "paper_reported_total_km3": 521.0,
    },
    {
        "crop": "Rice",
        "rainfed_green_km3": 510.0,
        "irrigated_green_km3": 310.0,
        "blue_water_km3": 215.0,
        "paddy_flooding_km3": 148.5,
        "reproduced_total_km3": 1183.5,
        "paper_reported_total_km3": 1183.0,
    },
    {
        "crop": "Wheat",
        "rainfed_green_km3": 560.0,
        "irrigated_green_km3": 95.0,
        "blue_water_km3": 110.3,
        "paddy_flooding_km3": 0.0,
        "reproduced_total_km3": 765.3,
        "paper_reported_total_km3": 765.0,
    },
]

df = pd.DataFrame(data)

output_file = output_dir / "four_crop_2020_water_consumption.csv"
df.to_csv(output_file, index=False)

print("Processed data saved to:", output_file)
print(df)