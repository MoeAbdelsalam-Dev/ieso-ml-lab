from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
EXPERIMENTS_FILE = ROOT / "experiments" / "runs.csv"
MODELS_DIR = ROOT / "models"

for d in (RAW_DIR, PROCESSED_DIR, MODELS_DIR, EXPERIMENTS_FILE.parent):
    d.mkdir(parents=True, exist_ok=True)

DATASET_FILE = PROCESSED_DIR / "dataset.parquet"
