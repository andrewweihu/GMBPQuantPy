import pandas as pd
import gmbp_common.unittest as ut
import gmbp_quant.dpl.yahoo.earnings as dplye


class TestEarnings(ut.TestCase):
    def test_query_earnings_multi_symbols(self):
        target = dplye.query_earnings_multi_symbols(symbols='AAPL,TSLA')
        benchmark_file = self.get_benchmark_file(basename=f'earnings.AAPL_TSLA.upto_20210421.csv')
        benchmark = pd.read_csv(benchmark_file, sep=',')
        self.assertEqual(benchmark[benchmark['startdatetime']<='2021-04-21'], target[target['startdatetime']<='2021-04-21'])
    #

    def test_query_earnings_multi_dates(self):
        start_dateid = 20201026
        end_dateid = 20201030
        target = dplye.query_earnings_multi_dates(start_dateid=start_dateid, end_dateid=end_dateid)
        benchmark_file = self.get_benchmark_file(basename=f'earnings.{start_dateid}_{end_dateid}.csv')
        benchmark = pd.read_csv(benchmark_file, sep=',')
        self.assertEqual(benchmark, target)
    #

    # def test_query_next_earning_date(self):
    #     self.assertEqual(20210427, dplye.query_next_earning_date(symbol='AAPL'))
    # #
#


if __name__ == '__main__':
    ut.main()
#
