import pandas as pd
import gmbp_common.unittest as ut
from gmbp_quant.dpl.fmp.fmp_stock_market_api import request_historical_sector_performance
pd.set_option('display.max_columns', None)


class TestFMPStockMarketAPI(ut.TestCase):
    def test_request_historical_sector_performance(self):
        # This test might fail because "target" is data of today while benchmark is not.
        target = request_historical_sector_performance()
        benchmark_file = self.get_benchmark_file(basename=f'request_historical_sector_performance.csv')
        benchmark = pd.read_csv(benchmark_file, sep=',', index_col=0)
        pd.testing.assert_frame_equal(benchmark.head(), target.head())
    #
#


if __name__ == '__main__':
    ut.main()
#