import pandas as pd
import gmbp_common.unittest as ut
from gmbp_quant.research.signal_mining.event_analysis import summarize_event_details


class TestEventAnalysis(ut.TestCase):
    def test_summarize_event_details(self):
        event_details_file = self.get_benchmark_file(basename='event_details.DIA-QQQ_lt_3sigma.csv')
        event_details = pd.read_csv(event_details_file, sep=',')
        return_cols = [f'CumReturn.QQQ.{num_days}D' for num_days in ['01', '03', '05', '10', '21']]
        target = summarize_event_details(event_details=event_details, return_cols=return_cols)
        benchmark_file = self.get_benchmark_file(basename='event_summary.DIA-QQQ_lt_3sigma.csv')
        benchmark = pd.read_csv(benchmark_file, sep=',', index_col='Item')

        pd.testing.assert_frame_equal(benchmark, target)
    #
#


if __name__ == '__main__':
    ut.main()
#