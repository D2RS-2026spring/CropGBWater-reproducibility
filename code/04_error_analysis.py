from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]

input_file = ROOT / "outputs/tables/four_crop_reproduction_summary.csv"
table_dir = ROOT / "outputs/tables"
fig_dir = ROOT / "outputs/figures"

table_dir.mkdir(parents=True, exist_ok=True)
fig_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(input_file)

error_df = df[
    [
        "crop",
        "reproduced_total_km3",
        "paper_reported_total_km3",
        "difference_km3",
        "absolute_difference_km3",
        "relative_difference_percent",
    ]
].copy()

error_df = error_df.sort_values("absolute_difference_km3", ascending=False)

out_table = table_dir / "error_analysis_summary.csv"
error_df.to_csv(out_table, index=False)

fig, ax = plt.subplots(figsize=(7, 4.5))

ax.bar(
    error_df["crop"],
    error_df["relative_difference_percent"],
)

ax.axhline(0, linewidth=1)
ax.set_ylabel("Relative difference (%)")
ax.set_title("Relative difference between reproduced and reported totals")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

for _, row in error_df.iterrows():
    ax.text(
        row["crop"],
        row["relative_difference_percent"],
        f"{row['relative_difference_percent']:.3f}%",
        ha="center",
        va="bottom" if row["relative_difference_percent"] >= 0 else "top",
        fontsize=9,
    )

plt.tight_layout()

out_fig = fig_dir / "fig3_relative_error.png"
fig.savefig(out_fig, dpi=300)
plt.close(fig)

print("Saved:", out_table)
print("Saved:", out_fig)
print(error_df)
