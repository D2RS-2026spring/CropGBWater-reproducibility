import subprocess
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

scripts = [
    "00_check_required_data.py",
    "01_prepare_four_crop_data.py",
    "02_calculate_totals.py",
    "03_make_figures.py",
    "04_error_analysis.py",
    "05_reproducibility_check.py",
]

for script in scripts:
    print(f"\n=== Running {script} ===")
    subprocess.run(
        [sys.executable, str(ROOT / "code" / script)],
        check=True,
    )

print("\nAll reproduction steps completed.")
