import pandas as pd
from pathlib import Path
import gmbp_common.unittest as ut
from gmbp_quant.dpl.sec_edgar.sec_data_loader import SecEdgarDataLoader


class TestSecEdgarDataLoader(ut.TestCase):
    def test_parse_forms_to_tsv(self):

        def _test_parse_forms_to_tsv_helper(form_type, form_folder, year,
                                        quarter, document_id):
            data_dir = Path(__file__).parent / 'sec_data'
            sec_loader = SecEdgarDataLoader(data_dir, form_type, year, quarter)
            sec_loader.parse_forms_to_tsv()
            parsed_data_path = (data_dir / 'tsv_files' / form_folder / year /
                                quarter / f'{document_id}.tsv')
            parsed_data = pd.read_csv(parsed_data_path, sep='\t')
            benchmark_path = Path(__file__).parent / 'benchmark' / f'{document_id}.tsv'
            benchmark = pd.read_csv(benchmark_path, sep='\t')
            pd.testing.assert_frame_equal(benchmark, parsed_data)

        _test_parse_forms_to_tsv_helper(
            '13F-HR', '13F-HR', '2019', 'Q4', '0000902219-19-000479')
        _test_parse_forms_to_tsv_helper(
            'S-3', 'S-3', '2020', 'Q4', '0000020286-20-000094')
        _test_parse_forms_to_tsv_helper(
            'S-1', 'S-1', '2020', 'Q4', '0000950103-20-021293')


if __name__ == '__main__':
    ut.main()
