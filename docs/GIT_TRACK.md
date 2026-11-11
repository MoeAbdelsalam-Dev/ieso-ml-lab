# Git & Project Management Track

Every stage has a **Do** step, which you run on this repo, and a **Check** step, which you can only pass if the Do worked.

---

## Stage 1 — Foundations (Module 00, day 1)

**Concepts:** A *repo* is a project folder that Git tracks. A *commit* is a saved snapshot of it. A *remote* is the copy on GitHub. A *venv* is the private set of Python packages for this project.

**Do:**
```bash
# 1. Install Git, then set your identity (one time per computer)
git config --global user.name "Mohammed Abdelsalam"
git config --global user.email "<your GitHub email>"
git config --global init.defaultBranch main

# 2. Unzip ieso-ml-lab, cd into it
python -m venv .venv
source .venv/bin/activate              # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest                                 # 3 passed

# 3. Turn it into a repo
git init
git status                             # see what Git sees. .venv and data are hidden by .gitignore
git add .
git commit -m "Initial project scaffold: pipeline, notebooks, tests, CI"

# 4. Create an EMPTY repo on github.com named ieso-ml-lab (no README), then:
git remote add origin https://github.com/<you>/ieso-ml-lab.git
git push -u origin main
```
In VS Code, select the interpreter `.venv` (Ctrl+Shift+P → "Python: Select Interpreter"). Pick it again as the kernel inside each notebook.

**Check:** Your GitHub repo has *no* `data/processed/dataset.parquet` and no `.venv/`. The **Actions** tab shows a green ✅. If you can explain why both are true, Stage 1 is passed.

**Commit message rule from now on:** use the imperative mood and say what changed. `Add time-split to module 2` ✅ `stuff` ❌ `final final v2` ❌

---

## Stage 2 — Solo pro workflow (every module)

**Concept:** `main` always works. All work happens on a branch and gets back into `main` through a Pull Request.

```bash
git switch main && git pull                 # start from latest
git switch -c module-01-knn                 # new branch
# ...work, then commit in small steps:
git add notebooks/01_knn_peak_classifier.ipynb
git commit -m "Add hand-coded Euclidean distance"
git push -u origin module-01-knn
```
On GitHub, open a PR → read the **Files changed** tab → merge → delete the branch.
```bash
git switch main && git pull                 # get the merged work
git branch -d module-01-knn                 # clean up locally
```

**Commands to own by Module 03:** `git status`, `git log --oneline --graph`, `git diff`, `git restore <file>` (undo uncommitted changes), `git commit --amend` (fix the last message).

**Tags/releases (Module 04):** `git tag v0.1-linreg && git push --tags`. Then on GitHub go to Releases → "Draft new release" and paste the results table.

---

## Stage 3 — Project board (from Module 00)

**Do:**
- On GitHub go to Projects → New → **Board** (columns: Todo / In progress / Done).
- Create one Issue per module, e.g. "Module 01: KNN peak classifier", with the TODO list from `docs/MODULE_MAP.md` as a checklist.
- PR descriptions say `Closes #2`. Merging the PR then closes the Issue automatically.
- Bugs and ideas also get Issues. Example: "Hour should be one-hot encoded (Module 04)".

**Check:** A recruiter opening your repo can see what's done, what's in progress and what's next without asking you.

---

## Stage 4 — Data & model versioning (Module 00 onward)

**Rules:**
| Thing | In Git? | Why |
|---|---|---|
| Code, notebooks, tests | ✅ | It's the source |
| `experiments/runs.csv` | ✅ | Small, and it's the history of your results |
| `data/raw`, `data/processed` | ❌ | Large and rebuildable. `scripts/update_data.py` is the "version" |
| `models/*.joblib` | ❌ | Rebuildable from code + data. Release the best ones as GitHub Release assets |
| `.env` / API keys | ❌ never | Anyone can read public repos. Leaked keys get abused within minutes |

**Later (Module 06):** save a `data/processed/manifest.json` with the date range + row count used for each trained model. That links each model to the exact data it was trained on. DVC is the industry tool for this. You'll know why it exists by then.

**Notebook diffs:** `.ipynb` files are JSON, so diffs look noisy. Before committing, run *Kernel → Restart & Run All* so the outputs are clean and in order.

---

## Stage 5 — Experiment tracking (Module 01 onward)

Every notebook calls `log_run(...)`, which writes one row to `experiments/runs.csv` with the **git commit hash**, parameters and metrics.

**Do:**
- Commit **before** running experiments you want to keep. Otherwise the logged hash points to old code.
- Compare runs with `show_runs("03")` or `show_runs()`.
- After Module 05, upgrade to **MLflow**: `pip install mlflow`, swap `log_run` internals, then run `mlflow ui`. That's the same idea with a UI.

**Check:** For any number in your README results table, you can point at the commit that produced it.

---

## Stage 6 — Team workflow (Module 05)

**Simulated teammate:** In Module 05, ask Claude for a "teammate PR". You'll get a patch that edits the same lines you're editing.

```bash
git switch -c teammate-change
git apply teammate.patch && git commit -am "Teammate: tweak feature list"
git switch main && git merge teammate-change    # merges cleanly
git switch module-05-nn
git merge main                                  # 💥 CONFLICT
```
Open the file. Keep the right parts between `<<<<<<<`, `=======` and `>>>>>>>`, delete the markers, then run `git add` and `git commit`.

**Code review:** Request a review on your PR (paste the diff into Claude as the "reviewer"). Address every comment with a new commit, never by force-pushing over the history.

**Forks:** Fork a public ML repo, fix a typo in its README and open a PR there. That's your first open-source contribution, and it shows on your profile.

**Branch protection:** Settings → Branches → protect `main` and require PRs plus passing checks. Now you *can't* push broken code straight to `main`.

---

## Stage 7 — CI/CD (live from day 1, expanded in Modules 06–07)

- **CI (already on):** `.github/workflows/ci.yml` runs `pytest` on every PR. If you break `parse_ieso_demand`, the PR goes red.
- **Write a test for every bug you fix.** That's the habit that separates projects from portfolios.
- **Module 06:** add `.github/workflows/daily.yml`. It runs on a cron schedule, executes `update_data.py` + `predict.py`, and commits `forecasts/latest.csv`. Your repo then updates itself every morning.
- **Module 07:** the dashboard reads `forecasts/latest.csv` and auto-deploys when it changes.
