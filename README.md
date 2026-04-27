# ds_in_da_wild

DS class project — **How is daily roadway traffic volume associated with motor-vehicle collision frequency and injury severity in NYC?**

**Group:** Qiaohao Hu (qh252), Jinyue Wang (jw2796), Junyi Li (jl4724), Wenzhuo Zhang (wz475)

## Phase IV — final submission

The Phase IV deliverable is a single executed notebook plus a standalone cleaning script:

- **Final notebook:** [phase4_final.ipynb](phase4_final.ipynb) — introduction, data description, cleaning summary, preregistration, three preregistered analyses (NegBin GLM, HC3-OLS, chi-square), supplemental analyses, conclusions, limitations, bibliography.
- **Cleaning script:** [phase4_clean.py](phase4_clean.py) — reads cached inputs from `data/` and writes the two analysis-ready CSVs the notebook imports.
- **Analysis-ready CSVs (committed):**
  - [data/phase4_borough_day.csv](data/phase4_borough_day.csv) — 18,693 rows (5 boroughs × 3,739 dates), used for H1.
  - [data/phase4_city_day.csv](data/phase4_city_day.csv) — 3,739 city-days, used for H2 and H3.
- **Pre-fetched ERA5 weather:** [data/era5_nyc_daily.csv](data/era5_nyc_daily.csv) — Open-Meteo daily mean temperature (°F) and total precipitation (mm) for NYC, 2012-01-01 to 2025-12-31. Cached so the cleaner has no network dependency.

### Reproduce Phase IV end-to-end

From the repo root, with the project venv active:

```bash
python phase4_clean.py                                                # writes data/phase4_*.csv
python build_phase4_notebook.py                                       # writes phase4_final.ipynb
jupyter nbconvert --to notebook --execute phase4_final.ipynb --inplace \
    --ExecutePreprocessor.kernel_name=ds-wild                          # executes all cells
```

`build_phase4_notebook.py` regenerates the notebook from inline cell definitions; edit it (not the `.ipynb`) when changing prose or analysis. The `ds-wild` kernel is registered with `python -m ipykernel install --user --name ds-wild` from the project venv.

## Earlier phases

- **Phase I — feasibility:** [two_datasets_analysis.ipynb](two_datasets_analysis.ipynb), exported as [analysis_ready_phase1.csv](analysis_ready_phase1.csv).
- **Phase II — full EDA:** [phase2_eda.ipynb](phase2_eda.ipynb).
- **Phase III — preregistration:** the three hypotheses are reproduced verbatim in the §4 of the Phase IV notebook.

## Data sources

| Dataset | Source | Used in |
|---|---|---|
| Automated Traffic Volume Counts (ATVC) | NYC Open Data, Socrata `7ym2-wayt` | Phase IV exposure variable (`vol_M`) |
| Motor Vehicle Collisions – Crashes | NYC Open Data, `h9gi-nx95` | Outcome — crash counts and victim-type injuries |
| Traffic Volume Counts (Historical) | NYC Open Data, `btm5-ppia` | Phase II hourly profiling only |
| Hyperlocal Temperature Monitoring | NYC Open Data, `qdq3-9eqn` | Phase I; superseded by ERA5 in Phases II+ |
| NYC Climate Projections | NYC Open Data, `hmdk-eidg` | Not used (decadal granularity) |
| Open-Meteo ERA5 reanalysis | `archive-api.open-meteo.com` | Daily NYC weather (temp, precip) for the full panel |

Direct CSV download links and per-dataset notes: [DATA_DOWNLOAD_GUIDE.md](DATA_DOWNLOAD_GUIDE.md).

## How to work on this repo
- Clone: `git clone https://github.com/VincentPit/ds_in_da_wild.git`
- Enter folder: `cd ds_in_da_wild`
- Create your branch (replace `feature-name`): `git checkout -b feature-name`
- Make changes and commit: `git add <files> && git commit -m "Your message"`
- Push your branch: `git push origin feature-name`

## How to open a pull request (PR)
- On GitHub, open a PR from your branch into `main`.
- Keep PRs small and focused; add a clear summary of changes.
- Request a teammate to review before merging.

## How to update your branch before merging
- Fetch and rebase onto latest main: `git fetch origin && git rebase origin/main`
- Resolve any conflicts locally, then continue the rebase: `git rebase --continue`
- Push updated branch (force push because of rebase): `git push -f origin feature-name`

## How to merge
- After approvals and passing checks, use GitHub to merge the PR into `main`.
- Clean up: delete your branch on GitHub and locally (`git branch -d feature-name`).
