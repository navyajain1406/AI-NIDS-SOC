
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


def save_detection_results(results, filename="detection_results.csv"):
    """
    Save detection results as a CSV report.
    """
    if not isinstance(results, pd.DataFrame):
        raise TypeError("Results must be a pandas DataFrame.")

    output_path = REPORT_DIR / filename

    results.to_csv(output_path, index=False)

    print(f"Detection report saved successfully: {output_path}")

    return output_path
