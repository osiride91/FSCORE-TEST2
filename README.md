# FSCORE-TEST2

This repository contains a simplified example of a fundamental equity backtest
that combines value and quality factors. The strategy selects up to 20 stocks
from a sample universe each quarter using high book-to-market ratios and strong
Piotroski F-Scores.

The code in `fs_score` demonstrates how one might structure the data loading,
filtering, ranking, and backtest mechanics. Sample CSV files in the `data`
folder provide minimal data so the example can run without external data
providers.

## Running the Example

Install dependencies and run the simulation:

```bash
pip install -r requirements.txt
python simulate.py
```

Unit tests can be executed with `pytest`:

```bash
pytest
```
