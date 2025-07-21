import pandas as pd


def apply_filters(universe: pd.DataFrame) -> pd.DataFrame:
    """Apply liquidity, market cap, sector and seasoning filters."""
    filtered = universe.copy()
    filtered = filtered.dropna(subset=['addv', 'market_cap'])
    filtered = filtered[filtered['addv'] >= 0]
    filtered = filtered[filtered['market_cap'] >= 0]
    filtered = filtered[~filtered['sector'].isin(['Real Estate', 'Financials', 'Health Care'])]
    filtered = filtered[filtered['age'] >= pd.Timedelta(days=0)]
    return filtered


def rank_and_select(df: pd.DataFrame, fscore: pd.Series, max_positions=20, max_sector_weight=0.25) -> pd.DataFrame:
    df = df.join(fscore.rename('fscore'), on='symbol')
    df = df[df['fscore'] >= 7]
    df = df.sort_values('book_to_market', ascending=False)

    selected = []
    sector_counts = {}

    for _, row in df.iterrows():
        sector = row['sector']
        if sector_counts.get(sector, 0) >= int(max_positions * max_sector_weight):
            continue
        selected.append(row)
        sector_counts[sector] = sector_counts.get(sector, 0) + 1
        if len(selected) >= max_positions:
            break

    return pd.DataFrame(selected)
