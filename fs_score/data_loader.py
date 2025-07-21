import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / '..' / 'data'


def load_financials():
    """Load sample fundamental data for demonstration."""
    fpath = DATA_DIR / 'sample_financials.csv'
    return pd.read_csv(fpath, parse_dates=['date'])


def load_prices():
    """Load sample price data for demonstration."""
    fpath = DATA_DIR / 'sample_prices.csv'
    return pd.read_csv(fpath, parse_dates=['date'])
