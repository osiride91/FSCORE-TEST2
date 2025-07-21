import pandas as pd
from fs_score.fscore import compute_fscore


def test_compute_fscore():
    data = pd.DataFrame([
        {'symbol': 'AAA', 'date': '2020-12-31', 'roa': 0.02, 'operating_cf': 1,
         'long_term_debt': 50, 'current_ratio': 1.2, 'shares_outstanding': 100,
         'gross_margin': 0.3, 'asset_turnover': 1.1},
        {'symbol': 'AAA', 'date': '2021-12-31', 'roa': 0.05, 'operating_cf': 2,
         'long_term_debt': 40, 'current_ratio': 1.3, 'shares_outstanding': 100,
         'gross_margin': 0.35, 'asset_turnover': 1.2},
    ])
    data['date'] = pd.to_datetime(data['date'])
    fscore = compute_fscore(data)
    assert fscore['AAA'] == 9
