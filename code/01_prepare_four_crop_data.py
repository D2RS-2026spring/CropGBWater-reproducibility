from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = ROOT / "data/raw/Data_S4_four_crops"
OUT_DIR = ROOT / "data/processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

crop_files = {
    "Maize": RAW_DIR / "Data_S4_Y2020_WF_Maize_grid_avg.csv",
    "Soybean": RAW_DIR / "Data_S4_Y2020_WF_Soybean_grid_avg.csv",
    "Rice": RAW_DIR / "Data_S4_Y2020_WF_Rice_grid_avg.csv",
    "Wheat": RAW_DIR / "Data_S4_Y2020_WF_Wheat_grid_avg.csv",
}

def find_annual_component_column(df: pd.DataFrame, component: str) -> str:
    candidates = []

    for col in df.columns:
        c = str(col).strip().lower()

        if component == "rainfed_green":
            if "wf_gn_rf" in c and c.endswith("_ann"):
                candidates.append(col)

        elif component == "irrigated_green":
            if "wf_gn_ir" in c and c.endswith("_ann"):
                candidates.append(col)

        elif component == "blue_water":
            if "wf_bl" in c and c.endswith("_ann"):
                candidates.append(col)

    if len(candidates) != 1:
        raise ValueError(
            f"Cannot uniquely identify {component} column. "
            f"Candidates found: {candidates}. "
            f"Available columns: {list(df.columns)}"
        )

    return candidates[0]

def find_optional_paddy_column(df: pd.DataFrame):
    for col in df.columns:
        c = str(col).strip().lower()
        if c == "c02_et_paddy" or c == "et_paddy":
            return col
    return None

def sum_numeric(df: pd.DataFrame, col: str) -> float:
    if col is None:
        return 0.0
    return pd.to_numeric(df[col], errors="coerce").sum(skipna=True)

records = []
long_records = []

for crop, file_path in crop_files.items():
    print(f"Reading {crop}: {file_path}")

    if not file_path.exists():
        raise FileNotFoundError(f"Missing raw file: {file_path}")

    df = pd.read_csv(file_path, low_memory=False)

    rainfed_green_col = find_annual_component_column(df, "rainfed_green")
    irrigated_green_col = find_annual_component_column(df, "irrigated_green")
    blue_water_col = find_annual_component_column(df, "blue_water")

    paddy_col = find_optional_paddy_column(df) if crop == "Rice" else None

    rainfed_green_m3 = sum_numeric(df, rainfed_green_col)
    irrigated_green_m3 = sum_numeric(df, irrigated_green_col)
    blue_water_m3 = sum_numeric(df, blue_water_col)
    paddy_flooding_m3 = sum_numeric(df, paddy_col)

    reproduced_total_m3 = (
        rainfed_green_m3
        + irrigated_green_m3
        + blue_water_m3
        + paddy_flooding_m3
    )

    records.append(
        {
            "crop": crop,
            "rainfed_green_km3": rainfed_green_m3 / 1e9,
            "irrigated_green_km3": irrigated_green_m3 / 1e9,
            "blue_water_km3": blue_water_m3 / 1e9,
            "paddy_flooding_km3": paddy_flooding_m3 / 1e9,
            "reproduced_total_km3": reproduced_total_m3 / 1e9,
        }
    )

    long_records.extend(
        [
            {
                "crop": crop,
                "component": "Rainfed green water",
                "water_consumption_km3": rainfed_green_m3 / 1e9,
            },
            {
                "crop": crop,
                "component": "Irrigated green water",
                "water_consumption_km3": irrigated_green_m3 / 1e9,
            },
            {
                "crop": crop,
                "component": "Blue water",
                "water_consumption_km3": blue_water_m3 / 1e9,
            },
            {
                "crop": crop,
                "component": "Paddy flooding",
                "water_consumption_km3": paddy_flooding_m3 / 1e9,
            },
        ]
    )

summary = pd.DataFrame(records)

paper = pd.read_csv(ROOT / "data/raw/paper_reported_totals_2020.csv")
summary = summary.merge(paper, on="crop", how="left")

summary_file = OUT_DIR / "four_crop_2020_water_consumption.csv"
summary.to_csv(summary_file, index=False)

long_file = OUT_DIR / "four_crop_2020_water_components_long.csv"
pd.DataFrame(long_records).to_csv(long_file, index=False)

print("Saved:", summary_file)
print("Saved:", long_file)
print(summary)
