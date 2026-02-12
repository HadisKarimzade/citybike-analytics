# CityBike — Bike-Sharing Analytics Platform

A Python-based analytics platform for a fictional city bike-sharing service.


## Setup

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



