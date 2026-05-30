from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]

input_file = ROOT / "outputs/tables/four_crop_reproduction_summary.csv"
fig_dir = ROOT / "outputs/figures"
fig_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(input_file)

components = [
    "rainfed_green_km3",
    "irrigated_green_km3",
    "blue_water_km3",
    "paddy_flooding_km3",
]

fig, ax = plt.subplots(figsize=(8, 5))

bottom = None

for comp in components:
    values = df[comp]
    if bottom is None:
        ax.bar(df["crop"], values, label=comp)
        bottom = values.copy()
    else:
        ax.bar(df["crop"], values, bottom=bottom, label=comp)
        bottom = bottom + values

ax.set_ylabel("Water consumption (km³)")
ax.set_title("2020 water consumption structure of four major crops")
ax.legend(frameon=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()

fig1 = fig_dir / "fig1_water_structure.png"
fig.savefig(fig1, dpi=300)
plt.close(fig)

x = list(range(len(df)))
width = 0.36

fig, ax = plt.subplots(figsize=(8, 5))

ax.bar(
    [i - width / 2 for i in x],
    df["paper_reported_total_km3"],
    width,
    label="Paper reported",
)

ax.bar(
    [i + width / 2 for i in x],
    df["reproduced_total_km3"],
    width,
    label="Reproduced",
)

ax.set_xticks(x)
ax.set_xticklabels(df["crop"])
ax.set_ylabel("Water consumption (km³)")
ax.set_title("Reproduced vs paper-reported 2020 totals")
ax.legend(frameon=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()

fig2 = fig_dir / "fig2_reproduced_vs_reported.png"
fig.savefig(fig2, dpi=300)
plt.close(fig)

print("Saved:", fig1)
print("Saved:", fig2)
