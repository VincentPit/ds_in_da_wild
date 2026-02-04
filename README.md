ds_in_da_wild
For ds class project.

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
