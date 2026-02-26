# NYC Open Data Download Guide

This project uses two public datasets from NYC Open Data:

1. **Traffic Volume Counts (Historical)**  
   - Dataset page: https://data.cityofnewyork.us/Transportation/Traffic-Volume-Counts-Historical/btm5-ppia
   - Dataset ID: `btm5-ppia`
   - Direct CSV: https://data.cityofnewyork.us/api/views/btm5-ppia/rows.csv?accessType=DOWNLOAD

2. **Motor Vehicle Collisions - Crashes**  
   - Dataset page: https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95
   - Dataset ID: `h9gi-nx95`
   - Direct CSV: https://data.cityofnewyork.us/api/views/h9gi-nx95/rows.csv?accessType=DOWNLOAD

## Download CSV from the website (UI)

For each dataset page:

1. Open the dataset page URL.
2. Click **Export** (top-right).
3. Select **CSV**.
4. Save the file to the `data/` folder in this repo.

## Optional: keep filenames used in this project

To match the notebook’s current naming convention, save as:

- `data/Traffic_Volume_Counts_(Historical)_YYYYMMDD.csv`
- `data/Motor_Vehicle_Collisions_-_Crashes_YYYYMMDD.csv`

(Example date suffix: `20260225`)

## Notes

- NYC Open Data updates these datasets over time, so row counts can change.
- If you need reproducibility, record the download date in your analysis notes.
