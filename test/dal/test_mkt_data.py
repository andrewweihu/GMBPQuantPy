import pandas as pd
import gmbp_quant.dal.mkt_data as dalmd
import gmbp_common.unittest as ut


class TestMktData(ut.TestCase):
    def test_query_adj_closes_smv0(self):
        symbols = 'TSLA,AMZN'
        start_dateid, end_dateid = 20210401, 20210415
        data_source = 'SMV0'
        target = dalmd.query_adj_closes(symbols=symbols, start_dateid=start_dateid, end_dateid=end_dateid,
                                        data_source=data_source)
        benchmark_file = self.get_benchmark_file(basename=f"adj_closes.{data_source}.{symbols.replace(',','_')}.{start_dateid}_{end_dateid}.csv")
        benchmark = pd.read_csv(benchmark_file, sep=',')
        self.assertEqual(benchmark, target)
    #
#


if __name__ == '__main__':
    ut.main()
#
