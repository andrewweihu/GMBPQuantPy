import argparse
import pandas as pd

from polygon_data_loader import PolygonDataLoader
import gmbp_quant.env_config as ecfg
from gmbp_common.utils.endpoint_utils import request_get_as_json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str, default='./polygon_data', help='Polygon form data folder')
parser.add_argument('--form', type=str, help='Polygon form type')
parser.add_argument('--report_date', type=str, help='Polygon data report_date')
opt = parser.parse_args()


if __name__ == '__main__':
    report_date = opt.report_date
    data_dir = Path(opt.data)
    form_type = opt.form

    list_file_dir = data_dir / form_type
    list_file_dir.mkdir(parents=True, exist_ok=True)
    
    fmp_key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)

    if form_type == 'company':
        url=f'https://financialmodelingprep.com/api/v3/stock/list?apikey={fmp_key}'
        data = request_get_as_json(url)

        table = pd.DataFrame(data)

        list_file = list_file_dir / f'download.list'
        table.to_csv(list_file, sep='\t', index=False)

        polygon_loader = PolygonDataLoader(data_dir, form_type)
        print(f'Start to download {len(table.loc[:, "symbol"])} tickers')
        for ticker in table.loc[:, 'symbol']:
            print(f'Downloading company profile {ticker} to json file ...')
            polygon_loader.request_company_data(ticker)
        #
    #