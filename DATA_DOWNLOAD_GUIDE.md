# NYC Open Data Download Guide

This project uses four public datasets from NYC Open Data:

1. **Traffic Volume Counts (Historical)**  
   - Dataset page: https://data.cityofnewyork.us/Transportation/Traffic-Volume-Counts-Historical/btm5-ppia
   - Dataset ID: `btm5-ppia`
   - Direct CSV: https://data.cityofnewyork.us/api/views/btm5-ppia/rows.csv?accessType=DOWNLOAD

2. **Motor Vehicle Collisions - Crashes**  
   - Dataset page: https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95
   - Dataset ID: `h9gi-nx95`
   - Direct CSV: https://data.cityofnewyork.us/api/views/h9gi-nx95/rows.csv?accessType=DOWNLOAD

3. **New York City Climate Projections: Temperature and Precipitation**  
   - Dataset page: https://data.cityofnewyork.us/Environment/New-York-City-Climate-Projections-Temperature-and/hmdk-eidg
   - Dataset ID: `hmdk-eidg`
   - Direct CSV: https://data.cityofnewyork.us/api/views/hmdk-eidg/rows.csv?accessType=DOWNLOAD

4. **Hyperlocal Temperature Monitoring**  
   - Dataset page: https://data.cityofnewyork.us/Environment/Hyperlocal-Temperature-Monitoring/qdq3-9eqn
   - Dataset ID: `qdq3-9eqn`
   - Direct CSV: https://data.cityofnewyork.us/api/views/qdq3-9eqn/rows.csv?accessType=DOWNLOAD

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
- `data/New_York_City_Climate_Projections__Temperature_and_Precipitation_YYYYMMDD.csv`
- `data/Hyperlocal_Temperature_Monitoring_YYYYMMDD.csv`

(Example date suffix: `20260225`)

## Notes

- NYC Open Data updates these datasets over time, so row counts can change.
- If you need reproducibility, record the download date in your analysis notes.
