# Module Map: Lectures → Modules → Git Stages

Each session takes about 1 hour. A module takes 2 to 4 sessions.

| Module | Lecture(s) | You build | 🔨 Break-it experiment | Git stage |
|---|---|---|---|---|
| **00 Data** | W1 workflow · W2 tools, X/y, shape | Live data pull, X/y, train/test split | — | 1–3: repo, venv, first PR, project board |
| **01 KNN** | W2 fit/predict · W3 scatter, KNN, Euclidean | Hand-coded distance, KNN peak classifier | k = 1 → 501: memorise vs over-smooth. Accuracy trap | 2: branch per module |
| **02 Scaling** | W4 scaling, confusion matrix | StandardScaler, time split, confusion matrix | Unscaled distances. Random split vs time split (leakage) | 2: read diffs before merging |
| **03 Trees** | W5 metrics, entropy, DT · W6 plot_tree, pruning | Entropy + info gain by hand, tree, P/R/F1 | Depth 1 → 30 overfitting curve. Scaling doesn't affect trees | 2: small commits |
| **04 LinReg** | W6 linear regression, MAE/MSE/R² | Metrics by hand, naive baseline, HDD/CDD features | Straight line through a U-shape | 2: first tag `v0.1` |
| **05 Neural nets** | W7 neuron, ReLU/sigmoid, LR, MLP | Forward pass by hand, MLPRegressor | Learning rate too small/large. No scaling | 6: first merge conflict |
| **06 Pipeline** | — (ahead of lectures) | `scripts/predict.py`: train best model → tomorrow's forecast | — | 7: daily GitHub Action |
| **07 Dashboard** | — | Live page: actual vs forecast, peak alerts | — | 7: auto-deploy |
| **08+** | Upcoming lectures | Each new lecture becomes a module on the same data | — | — |

**How to work through a module:**
1. Create the module Issue on the project board.
2. Create a branch.
3. Run the notebook.
4. Write the TODO cells. These are the core ML code, and they're yours to write.
5. Before each 🔨 cell, write your prediction. Then run it.
6. Answer the "Why questions".
7. Commit, open a PR, merge, and update the README results table.

**When you're stuck:** paste the TODO and your attempt into Claude and ask for a *hint*, not the answer.
