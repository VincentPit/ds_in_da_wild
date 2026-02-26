ds_in_da_wild
For ds class project.

## Data sources (NYC Open Data)

This project uses:

- Traffic Volume Counts (Historical): https://data.cityofnewyork.us/Transportation/Traffic-Volume-Counts-Historical/btm5-ppia
- Motor Vehicle Collisions - Crashes: https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95

### How to download CSV from the website

1. Open a dataset page link above.
2. Click **Export** (top-right).
3. Select **CSV**.
4. Save the file into the `data/` folder.

Direct CSV links:

- Traffic: https://data.cityofnewyork.us/api/views/btm5-ppia/rows.csv?accessType=DOWNLOAD
- Crashes: https://data.cityofnewyork.us/api/views/h9gi-nx95/rows.csv?accessType=DOWNLOAD

See also: [DATA_DOWNLOAD_GUIDE.md](DATA_DOWNLOAD_GUIDE.md)

## Phase I submission artifacts

- Executed feasibility notebook: [two_datasets_analysis.ipynb](two_datasets_analysis.ipynb)
- Analysis-ready export CSV: [analysis_ready_phase1.csv](analysis_ready_phase1.csv)

The notebook includes:
- research question(s)
- raw dataset descriptions
- data loading/cleaning/aggregation/merge steps
- export of final analysis-ready dataframe
- limitations and TA questions

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
