import os
import sys
import json as json
import pandas as pd
from tqdm import tqdm

sys.path.append('..')
from gmbp_common.logger import LOG
import gmbp_quant.env_config as ecfg
from gmbp_common.utils.endpoint_utils import request_get_as_json
from gmbp_quant.dpl.base.data_loader import DataLoader
from gmbp_quant.dpl.polygon.polygon_schemas import PolygonCompanySchema


logger = LOG.get_logger(__name__)

# Only use it for PROD purpose
polygon_key = ecfg.get_env_config(env='PROD').get(ecfg.Prop.POLYGON_KEY)

class PolygonDataLoader(DataLoader):
    """A :class:`PolygonDataLoader` class

    Args:
        data_dir: folder storing Polygon data
        form_type: Polygon form type, currently support
                    'company'
        report_date: optional
    """

    def __init__(self, data_dir, form_type, report_date=None):
        if report_date is None:
            self.form_dir = data_dir / form_type
            self.tsv_dir = data_dir / 'tsv_files' / form_type
        else:
            self.form_dir = data_dir / form_type / report_date
            self.tsv_dir = data_dir / 'tsv_files' / form_type / report_date
        self.form_list = list(self.form_dir.glob('*.txt'))
        self.report_date = report_date
        schemas = {
            'company': PolygonCompanySchema
        }
        super().__init__(data_dir, form_type, self.tsv_dir, 'mktdata', schemas[form_type])

        self.form_dir.mkdir(parents=True, exist_ok=True)

    def request_company_data(self, ticker):
        if os.path.isfile(self.form_dir / f'{ticker}-json.txt'):
            return None

        data = request_get_as_json(
            url=f'https://api.polygon.io/v1/meta/symbols/{ticker}/company?apikey={polygon_key}')
        if data is None:
            return None
        #

        data['symbol'] = ticker
        del data['tags']
        del data['similar']

        data = [data]
        data_file = self.form_dir / f'{ticker}-json.txt'
        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

        return data
    #


    def parse_company_to_tsv(self):
        """Parse Polygon forms and save to tsv files
        """

        for form in tqdm(self.form_list):
            company = form.stem.split('-')[0]
            with open(form, 'r') as json_file:
                data = json.load(json_file)
                table = pd.DataFrame(data)

                if not table.empty:
                    table_sorted = table
                    table_sorted = table_sorted.drop(columns=['description'])

                    output_path = self.tsv_dir / f'{company}.tsv'
                    table_sorted.to_csv(output_path, sep='\t', index=False)
            #
        #
    #


