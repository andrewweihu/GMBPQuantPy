import argparse
import pandas as pd

from yahoo_data_loader  import YahooDataLoader
import gmbp_quant.env_config as ecfg
from gmbp_common.utils.endpoint_utils import request_get_as_json
from pathlib import Path
from yahoo_fin import stock_info

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str, default='./yahoo_data', help='Yahoo data folder')
parser.add_argument('--form', type=str, help='Tiingo form type')
parser.add_argument('--ipo_date', type=str, help='IPO date')
parser.add_argument('--start_date', type=str, help='Start date')
parser.add_argument('--end_date', type=str, help='End date')
opt = parser.parse_args()

fmp_key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)

if __name__ == '__main__':
    ipo_date = opt.ipo_date
    data_dir = Path(opt.data)
    form_type = opt.form

    start_date = opt.start_date
    end_date = opt.end_date

    yahoo_loader = YahooDataLoader(data_dir, form_type)
    if form_type == 'ipo':
        print(f'Downloading yahoo data {ipo_date} to raw file ...')
        yahoo_loader.request_ipo_data(ipo_date)
    elif form_type == 'holders':
        # fmp_stock_list = request_get_as_json(
        #     url=f'https://financialmodelingprep.com/api/v3/stock/list?apikey={fmp_key}')
        # fmp_stock_table = pd.DataFrame(fmp_stock_list)
        
        # use yahoo_fin ticker list 
        symbol_list = set(
        stock_info.tickers_dow() + stock_info.tickers_sp500()
        + stock_info.tickers_nasdaq() + stock_info.tickers_other())
        # uncomment to include tickers from other exchanges
        # + stock_info.tickers_ftse100() + stock_info.tickers_ftse250()
        # + stock_info.tickers_ibovespa() + stock_info.tickers_nifty50()
        # + stock_info.tickers_niftybank() )

        # for symbol in fmp_stock_table.loc[:, 'symbol']:
        for symbol in symbol_list:
            print(f'Downloading yahoo holders for {symbol} to tsv file ...')
            # download and parsing steps have been combined so only parse tsv function is called
            yahoo_loader.parse_holders_to_tsv(symbol)
        #
    elif form_type == 'daily_price':
        fmp_stock_list = request_get_as_json(
            url=f'https://financialmodelingprep.com/api/v3/stock/list?apikey={fmp_key}')

        fmp_stock_table = pd.DataFrame(fmp_stock_list)

        for symbol in fmp_stock_table.loc[:, 'symbol']:
            try:
                print(f'Downloading yahoo daily price for {symbol} to raw file ...')
                yahoo_loader.request_daily_price_data(symbol, start_date, end_date)
            except Exception as e:
                print(f'Fail to download {symbol}')
        #
    #
    elif form_type == 'stats':
        fmp_stock_list = request_get_as_json(
            url=f'https://financialmodelingprep.com/api/v3/stock/list?apikey={fmp_key}')

        fmp_stock_table = pd.DataFrame(fmp_stock_list)

        for symbol in fmp_stock_table.loc[:, 'symbol']:
            try:
                print(f'Downloading yahoo stats for {symbol} to raw file ...')
                yahoo_loader.request_stats_data(symbol)
            except Exception as e:
                print(f'Fail to download {symbol}')
        #
    #
#