# CityBike — Bike-Sharing Analytics Platform

A Python-based analytics platform for a fictional city bike-sharing service.
It demonstrates:

- Object-oriented design (inheritance, ABC, properties, validation)
- Pandas data loading/cleaning and analytics
- Custom algorithms (sorting/searching) + benchmarks
- NumPy numerical computing (distance matrix, stats, outliers, vectorized fares)
- Matplotlib visualizations exported to `output/figures/`
- Text + CSV reporting to `output/`

## Project structure

```
citybike/
  main.py
  models.py
  analyzer.py
  algorithms.py
  numerical.py
  visualization.py
  pricing.py
  factories.py
  utils.py
  generate_data.py
  requirements.txt
  data/
  output/
  tests/
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
# .venv\Scripts\activate     # Windows

pip install -r requirements.txt

# Generate sample data into citybike/data/
python generate_data.py

# Run full pipeline (clean, analyze, visualize, report)
python main.py
```

Outputs are written to:

- `data/*_clean.csv`
- `output/summary_report.txt`
- `output/top_stations.csv`
- `output/top_users.csv`
- `output/maintenance_summary.csv`
- `output/search_sort_benchmarks.txt`
- `output/figures/*.png`

## Run tests

```bash
pytest -v
```

## Notes on cleaning strategy

- **Trips**: duplicates removed by `trip_id`; times parsed; numeric fields coerced to float.
  Missing `duration_minutes` or `distance_km` are imputed using the **median** of that column.
  Missing `status` is filled as `"completed"` (most common in this synthetic dataset).
  Invalid rows (end before start, negative distance/duration, unknown categoricals) are removed.
- **Stations**: numeric types coerced; invalid capacities/coords removed.
- **Maintenance**: dates parsed; missing cost imputed with **median cost per bike_type** (fallback overall median).

## Business questions answered

Implements all 14 questions from the handout (Q1–Q14) in `BikeShareSystem`.
