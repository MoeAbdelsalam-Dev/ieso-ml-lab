# ⚡ IESO ML Lab — Forecasting Ontario Electricity Demand

Machine learning on **live** Ontario grid data (IESO) + Toronto weather. Built module-by-module alongside COIS-AIST-3550H (Applied AI & ML, Trent University).

**The problem:** Ontario's grid operator must forecast hourly demand a day ahead. Big industrial users pay peak-based charges (Global Adjustment / ICI), so predicting **peak hours** is worth real money.

## Results so far
| Module | Model | Task | Test metric |
|---|---|---|---|
| 01 | KNN | Peak-hour classification | _fill in_ |
| 02 | KNN + scaling + time split | Peak-hour classification | _fill in_ |
| 03 | Decision tree | Peak-hour classification | _F1: fill in_ |
| 04 | Linear regression (HDD/CDD) | Demand (MW) | _RMSE: fill in_ |
| 05 | MLP neural network | Demand (MW) | _RMSE: fill in_ |

Full run history: [`experiments/runs.csv`](experiments/runs.csv)

## Quick start
```bash
git clone https://github.com/<you>/ieso-ml-lab.git
cd ieso-ml-lab
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/update_data.py      # pulls live IESO + weather data
pytest                             # tests pass?
jupyter notebook notebooks/
```

## Repo structure
```
ieso-ml-lab/
├── src/ieso_lab/        # reusable code (data pulls, features, experiment logging)
├── scripts/             # command-line jobs (update_data.py → later: daily predict)
├── notebooks/           # one notebook per module (learning + experiments)
├── experiments/runs.csv # every model run: params + metrics + git commit
├── tests/               # pytest, run by GitHub Actions on every PR
├── data/                # rebuilt by scripts — NOT in git
├── models/              # saved models — NOT in git
└── docs/                # module map + Git track
```

## Data sources
- **IESO** public hourly demand reports — `reports-public.ieso.ca/public/Demand/`
- **Open-Meteo** historical + forecast weather API (Toronto, no key needed)
