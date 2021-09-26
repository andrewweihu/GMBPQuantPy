import pandas as pd
import gmbp_quant.dal.sec_master_v0.sec_master as smv0sm
from gmbp_common.utils.miscs import iterable_to_tuple
import gmbp_common.unittest as ut


class TestMktData(ut.TestCase):
    def test_query_security_lookup(self):
        target = smv0sm.query_security_lookup(symbols='AAPL,MSFT')
        benchmark_file = self.get_benchmark_file(basename=f'security_lookup.AAPL_MSFT.csv')
        benchmark = pd.read_csv(benchmark_file, sep=',')
        self.assertEqual(benchmark, target)

        cols = 'ID,TICKER,REGION'
        target = smv0sm.query_security_lookup(symbols='AAPL,MSFT', cols=cols)
        self.assertEqual(benchmark[list(iterable_to_tuple(cols, raw_type='str'))], target)
    #
#


if __name__ == '__main__':
    ut.main()
#
