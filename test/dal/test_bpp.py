import pandas as pd
import gmbp_quant.dal.bpp as dalbpp
import gmbp_common.unittest as ut


class TestBPP(ut.TestCase):
    def test_query_bpp_day_ts(self):
        symbols = 'TSLA,AAPL'
        start_dateid, end_dateid = 20210415, 20210421
        target = dalbpp.query_bpp_day_ts(symbols=symbols, start_dateid=start_dateid, end_dateid=end_dateid)
        benchmark_file = self.get_benchmark_file(basename=f"bpp_day_ts.{symbols.replace(',','_')}.{start_dateid}_{end_dateid}.csv")
        benchmark = pd.read_csv(benchmark_file, sep=',')
        self.assertEqual(benchmark, target)
    #

    def test_bpp_moving_window_signal(self):
        symbols = 'UBS,GME,RLX'
        start_dateid, end_dateid = 20210415, 20210421
        target = dalbpp.query_bpp_moving_window_signal(symbols=symbols, start_dateid=start_dateid, end_dateid=end_dateid)
        benchmark_file = self.get_benchmark_file(basename=f"bpp_moving_window_signal.{symbols.replace(',','_')}.{start_dateid}_{end_dateid}.csv")
        benchmark = pd.read_csv(benchmark_file, sep=',')
        self.assertEqual(benchmark, target)
    #
#


if __name__ == '__main__':
    ut.main()
#
