import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

data_file = ROOT / "outputs" / "tables" / "four_crop_reproduction_summary.csv"
fig_dir = ROOT / "outputs" / "figures"
fig_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(data_file)

# ---------- Figure 1: water-consumption structure ----------
components = [
    "rainfed_green_km3",
    "irrigated_green_km3",
    "blue_water_km3",
    "paddy_flooding_km3",
]

labels = [
    "Rainfed green water",
    "Irrigated green water",
    "Blue water",
    "Paddy flooding",
]

plot_df = df.set_index("crop")[components]

ax = plot_df.plot(
    kind="bar",
    stacked=True,
    figsize=(8, 5),
    width=0.72
)

ax.set_xlabel("")
ax.set_ylabel("Water consumption (km³)")
ax.set_title("Water-consumption structure of four major crops in 2020")
ax.legend(labels, frameon=False, loc="upper right")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.xticks(rotation=0)
plt.tight_layout()

fig1 = fig_dir / "fig1_water_structure.png"
plt.savefig(fig1, dpi=300)
plt.close()

# ---------- Figure 2: reproduced vs reported totals ----------
x = range(len(df))
width = 0.36

fig, ax = plt.subplots(figsize=(8, 5))

ax.bar(
    [i - width / 2 for i in x],
    df["paper_reported_total_km3"],
    width=width,
    label="Reported in paper"
)

ax.bar(
    [i + width / 2 for i in x],
    df["reproduced_total_km3"],
    width=width,
    label="Reproduced"
)

ax.set_xticks(list(x))
ax.set_xticklabels(df["crop"])
ax.set_ylabel("Water consumption (km³)")
ax.set_title("Comparison between reported and reproduced totals")
ax.legend(frameon=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

for i, row in df.iterrows():
    y = max(row["paper_reported_total_km3"], row["reproduced_total_km3"])
    ax.text(
        i,
        y + 20,
        f"{row['relative_difference_percent']:.3f}%",
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.tight_layout()

fig2 = fig_dir / "fig2_reproduced_vs_reported.png"
plt.savefig(fig2, dpi=300)
plt.close()

print("Saved:", fig1)
print("Saved:", fig2)
