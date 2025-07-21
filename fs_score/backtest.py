import pandas as pd
from pandas.tseries.offsets import BDay
from pandas.tseries.holiday import USFederalHolidayCalendar

from .data_loader import load_financials, load_prices
from .fscore import compute_fscore
from .strategy import apply_filters, rank_and_select


class Backtester:
    def __init__(self, start, end):
        self.start = pd.Timestamp(start)
        self.end = pd.Timestamp(end)
        self.cal = USFederalHolidayCalendar()

    def run(self):
        # Load sample data
        financials = load_financials()
        prices = load_prices()
        universe = self.prepare_universe(prices, financials)

        portfolio_history = []

        for rebalance_date in self.rebalance_dates():
            # filter universe as of rebalance date
            universe_slice = universe[universe['date'] == rebalance_date]
            filt = apply_filters(universe_slice)
            # In this example we use all fundamental data for scoring
            fscore = compute_fscore(financials)
            selection = rank_and_select(filt, fscore)
            selection['weight'] = 1.0 / len(selection) if len(selection) else 0
            selection['rebalance_date'] = rebalance_date
            portfolio_history.append(selection)

        return pd.concat(portfolio_history, ignore_index=True)

    def rebalance_dates(self):
        months = [2, 5, 8, 11]
        dates = []
        for year in range(self.start.year, self.end.year + 1):
            for month in months:
                # second Friday of month
                date = pd.Timestamp(year=year, month=month, day=1)
                date += pd.offsets.WeekOfMonth(week=1, weekday=4)  # 0=Mon
                if date < self.start or date > self.end:
                    continue
                dates.append(date)
        return dates

    def prepare_universe(self, prices, financials):
        """Create universe DataFrame used for screening and ranking."""
        prices = prices.copy()
        prices['addv'] = prices['close'] * prices['volume']
        prices['market_cap'] = prices['close'] * prices['shares_outstanding']
        prices['age'] = prices['date'] - prices.groupby('symbol')['date'].transform('min')

        # Compute book-to-market using latest available book equity
        latest_book = (financials.sort_values('date')
                                   .groupby('symbol')['book_equity']
                                   .last())
        prices = prices.join(latest_book, on='symbol')
        prices['book_to_market'] = prices['book_equity'] / prices['market_cap']
        return prices
