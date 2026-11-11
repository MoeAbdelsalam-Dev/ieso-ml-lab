from .paths import DATASET_FILE


def load_dataset():
    """Load the processed dataset built by scripts/update_data.py."""
    import pandas as pd

    if not DATASET_FILE.exists():
        raise FileNotFoundError(
            "No dataset yet. Run:  python scripts/update_data.py"
        )
    return pd.read_parquet(DATASET_FILE)
