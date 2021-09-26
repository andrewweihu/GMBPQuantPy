import pandas as pd
import gmbp_common.unittest as ut
from gmbp_quant.dpl.polygon.polygon_stock_api import request_open_close, request_minute_bars, request_hour_bars, request_aggregates_over_all_tickers

COLUMN_CUTOFF = 15

class TestPolygonStockAPI(ut.TestCase):
    def test_request_open_close(self):
        dateid = 20210302
        symbol = 'AAPL'
        target = request_open_close(symbol=symbol, dateid=dateid, adjusted=False)
        benchmark_file = self.get_benchmark_file(basename=f'open_close.{symbol}.{dateid}.csv')
        benchmark = pd.read_csv(benchmark_file, sep=',')
        self.assertEqual(benchmark, target)
    #

    def test_request_minute_bars(self):
        start_dateid, end_dateid = 20210324, 20210324
        symbol = 'TSLA'
        target = request_minute_bars(symbol=symbol, start_dateid=start_dateid, end_dateid=end_dateid, adjusted=False)
        benchmark_file = self.get_benchmark_file(basename=f'minute_bars.{symbol}.{start_dateid}_{end_dateid}.csv')
        benchmark = pd.read_csv(benchmark_file, sep=',')
        self.assertEqual(benchmark, target)
    #

    def test_request_hour_bars(self):
        start_dateid, end_dateid = 20210324, 20210324
        symbol = 'GOOG'
        target = request_hour_bars(symbol=symbol, start_dateid=start_dateid, end_dateid=end_dateid, adjusted=False)
        benchmark_file = self.get_benchmark_file(basename=f'hour_bars.{symbol}.{start_dateid}_{end_dateid}.csv')
        benchmark = pd.read_csv(benchmark_file, sep=',')
        self.assertEqual(benchmark, target)
    #

    def test_aggregates_over_all_tickers(self):
        start_dateid, end_dateid = 20210310, 20210313
        fields = ["Open", "High", "Low", "Close", "Volume", "VWAP", "NumberTransactions"]
        aggregates = request_aggregates_over_all_tickers(start_dateid=start_dateid, end_dateid=end_dateid)
        for f in fields:
            # we store only COLUMN_CUTOFF columns in
            # the test fixtures to enhance readability
            target = aggregates[f].iloc[:, :COLUMN_CUTOFF]
            benchmark_file = self.get_benchmark_file(basename=f'aggregates_over_all_tickers.{f}.{start_dateid}_{end_dateid}.csv')
            benchmark = pd.read_csv(benchmark_file, sep=',')
            self.assertEqual(benchmark, target)
    #
#


if __name__ == '__main__':
    ut.main()
#
