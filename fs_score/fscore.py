import pandas as pd

# Implementation based on Piotroski F-Score using annual data

def compute_fscore(df: pd.DataFrame) -> pd.Series:
    """Compute Piotroski F-Score for each symbol in DataFrame.

    Parameters
    ----------
    df : DataFrame
        Expected columns: symbol, date, roa, operating_cf, long_term_debt,
        current_ratio, shares_outstanding, gross_margin, asset_turnover
    Returns
    -------
    Series mapping symbol to F-Score
    """
    fscore = pd.Series(index=df['symbol'].unique(), dtype=int)
    grouped = df.sort_values('date').groupby('symbol')

    for symbol, g in grouped:
        if len(g) < 2:
            fscore[symbol] = 0
            continue
        latest = g.iloc[-1]
        prev = g.iloc[-2]
        score = 0
        # Profitability
        score += int(latest['roa'] > 0)
        score += int(latest['operating_cf'] > 0)
        score += int(latest['operating_cf'] > latest['roa'])
        score += int(latest['roa'] > prev['roa'])
        # Leverage, Liquidity, Source of Funds
        score += int(latest['long_term_debt'] <= prev['long_term_debt'])
        score += int(latest['current_ratio'] > prev['current_ratio'])
        score += int(latest['shares_outstanding'] <= prev['shares_outstanding'])
        # Operating Efficiency
        score += int(latest['gross_margin'] > prev['gross_margin'])
        score += int(latest['asset_turnover'] > prev['asset_turnover'])
        fscore[symbol] = score
    return fscore
