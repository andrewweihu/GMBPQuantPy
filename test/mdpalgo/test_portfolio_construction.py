import pandas as pd
import numpy as np
import gmbp_quant.mdpalgo.portfolio_construction as pc
from gmbp_common.utils.miscs import iterable_to_tuple
import gmbp_common.unittest as ut


class TestPortfolioConstruction(ut.TestCase):
    def test_calc_cov_mat(self):
        target = pc.calc_cov_mat(tickers='AAPL,MSFT',
                                 start_dateid=20190415, end_dateid=20210413)
        benchmark = np.array([[0.0005756, 0.00041039],
                              [0.00041039, 0.00047059]])
        np.testing.assert_almost_equal(actual=benchmark, desired=target, decimal=8)
    #

    def calc_most_diversified_portfolio(self):
        tickers = 'AMZN,GE,MSFT,CREE'
        cov_mat = pc.calc_cov_mat(tickers=tickers,
                                 start_dateid=20190415, end_dateid=20210413)
        target = pc.calc_most_diversified_portfolio(tickers=tickers, cov_mat=cov_mat,
                                                    equal_weights_divergence_penalty=0)
        np.testing.assert_almost_equal(actual=np.array([0.528271, 0.317784, 0.010000, 0.143945]),
                                       desired=target['Weights'], decimal=6)
        self.assertEqual(0.02006691, np.round(target['Volatility'], 8))
    #
#


if __name__ == '__main__':
    ut.main()
#
