# LA weather & AQI (MLWeatherProject)

End-to-end notebooks for exploring Los Angeles air quality and weather data, engineering features, training an **XGBoost** model, and generating predictions.

## Notebooks (order)

1. `01_eda.ipynb` — exploratory analysis  
2. `02_features.ipynb` — feature table  
3. `03_modeling.ipynb` — train / evaluate (`models/la_xgboost.pkl`)  
4. `04_predictions.ipynb` — forecasts and checks  

Supporting code lives in `epa_loader.py`.

## Data

- **`data/processed/`** — merged weather + AQI and feature matrices (committed; small enough for GitHub).
- **`data/raw/`** — daily EPA Air Quality System (AQS) CSVs are **not** in this repo (each year is hundreds of MB). Download the daily files you need (this project uses the `daily_88101_*.csv` PM2.5 series for LA) into `data/raw/`, then re-run the early notebooks if you want to rebuild processed files from scratch.

## Requirements

Python 3.10+ with `pandas`, `numpy`, `scikit-learn`, `xgboost`, `matplotlib`, `jupyter`, and notebook-specific imports as cells import them.
