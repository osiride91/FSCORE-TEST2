from fs_score.backtest import Backtester


def main():
    bt = Backtester(start='2021-02-01', end='2021-11-30')
    portfolio = bt.run()
    print(portfolio)


if __name__ == '__main__':
    main()
