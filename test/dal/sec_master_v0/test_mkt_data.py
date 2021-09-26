import pandas as pd
import gmbp_quant.dal.sec_master_v0.mkt_data as smv0md
from gmbp_common.utils.miscs import iterable_to_tuple
import gmbp_common.unittest as ut


class TestMktData(ut.TestCase):
    def test_query_security_day_price(self):
        # dateid = 20210105
        # target = dalsd.query_security_day_price(end_dateid=dateid)
        # benchmark_file = self.get_benchmark_file(basename=f'security_day_price.20210105.csv')
        # benchmark = pd.read_csv(benchmark_file, sep=',')
        # self.assertEqual(benchmark, target)

        symbols = 'TSLA'
        start_dateid, end_dateid = 20101001, 20101231
        target = smv0md.query_security_day_price(symbols=symbols, start_dateid=start_dateid, end_dateid=end_dateid)
        benchmark_file = self.get_benchmark_file(basename=f'security_day_price.{symbols}.{start_dateid}.{end_dateid}.csv')
        benchmark = pd.read_csv(benchmark_file, sep=',')
        self.assertEqual(benchmark, target)

        cols = 'SECURITY_LOOKUP_ID,TICKER,time_x,ADJ_CLOSE'
        target = smv0md.query_security_day_price(symbols=symbols, start_dateid=start_dateid, end_dateid=end_dateid,
                                                 cols=cols)
        self.assertEqual(benchmark[list(iterable_to_tuple(cols, raw_type='str'))], target)
    #
#


if __name__ == '__main__':
    ut.main()
#
