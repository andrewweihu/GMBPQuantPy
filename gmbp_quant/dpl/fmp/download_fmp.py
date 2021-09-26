import argparse
import pandas as pd

from fmp_data_loader import FmpDataLoader
import gmbp_quant.env_config as ecfg
from gmbp_common.utils.endpoint_utils import request_get_as_json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str, default='./fmp_data', help='FMP form data folder')
parser.add_argument('--form', type=str, help='FMP form type')
parser.add_argument('--report_date', type=str, help='FMP data report_date')
parser.add_argument('--start_year', type=int, help='Download start year')
parser.add_argument('--end_year', type=int, help='Download end year')
parser.add_argument('--quarters', default=["Q4"], nargs='+', type=str, choices=["Q1", "Q2", "Q3", "Q4"],
                    help='Quarters of documents to download')
args = parser.parse_args()


if __name__ == '__main__':
    report_date = args.report_date
    start_year = args.start_year
    end_year = args.end_year
    quarters = args.quarters
    data_dir = Path(args.data)
    form_type = args.form

    if report_date is None:
        list_file_dir = data_dir / form_type
    else:
        list_file_dir = data_dir / form_type / report_date

    list_file_dir.mkdir(parents=True, exist_ok=True)

    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)

    def get_symbols_in_NASDAQ100():
        file_path = "./dpl/fmp/NASDAQ100.csv"
        try:
            symbols_data = request_get_as_json(
                url=f'https://financialmodelingprep.com/api/v3/etf-holder/QQQ?apikey={key}')
            symbols_table = pd.DataFrame(symbols_data)
            symbols_table.sort_values(by=["weightPercentage", "asset"], ascending=False)
            symbols_table.to_csv(file_path, index=False)
        except Exception as e:
            symbols_table = pd.read_csv(file_path)
        if symbols_table.empty:  # in case of some kind of failure
            symbols_table = pd.read_csv(file_path)
        return list(pd.DataFrame(symbols_table)['asset'])

    def get_symbols_in_SP500():
        file_path = "./dpl/fmp/SP500.csv"
        try:
            symbols_data = request_get_as_json(
                url=f'https://financialmodelingprep.com/api/v3/etf-holder/SPY?apikey={key}')
            symbols_table = pd.DataFrame(symbols_data)
            symbols_table.sort_values(by=["weightPercentage", "asset"], ascending=False)
            symbols_table.to_csv(file_path, index=False)
        except Exception as e:
            symbols_table = pd.read_csv(file_path)
        if symbols_table.empty:
            symbols_table = pd.read_csv(file_path)
        return list(pd.DataFrame(symbols_table)['asset'])

    def get_symbols_list_supported_by_fmp():
        """
        :return: list of symbols, such as AAPL.US, containing all the symbols supported by FMP
        """
        symbols_data = request_get_as_json(
            url=f'https://financialmodelingprep.com/api/v3/available-traded/list?apikey={key}')

        symbols_table_raw = pd.DataFrame(symbols_data)
        symbols_table = pd.concat([
            symbols_table_raw.loc[symbols_table_raw['exchange'] == 'NASDAQ'],
            symbols_table_raw.loc[symbols_table_raw['exchange'] == 'Nasdaq'],
            symbols_table_raw.loc[symbols_table_raw['exchange'] == 'Nasdaq Capital Market'],
            symbols_table_raw.loc[symbols_table_raw['exchange'] == 'NASDAQ Global Market'],
            symbols_table_raw.loc[symbols_table_raw['exchange'] == 'Nasdaq Global Market'],
            symbols_table_raw.loc[symbols_table_raw['exchange'] == 'Nasdaq Global Select'],
            symbols_table_raw.loc[symbols_table_raw['exchange'] == 'NYSE American'],
            symbols_table_raw.loc[symbols_table_raw['exchange'] == 'NYSEArca'],
            symbols_table_raw.loc[symbols_table_raw['exchange'] == 'New York Stock Exchange'],
            symbols_table_raw.loc[symbols_table_raw['exchange'] == 'New York Stock Exchange Arca'],
            ])

        symbols_list_file = list_file_dir / f'download.list'
        symbols_table.to_csv(symbols_list_file, sep='\t', index=False)
        symbols_list = list(symbols_table.loc[:, 'symbol'])

        def get_key(symbol):
            if "." in symbol:
                return tuple(symbol.split('.')[::-1])
            else:
                return "", symbol

        return sorted(symbols_list, key=lambda x: get_key(x))

    def get_priority_companies():
        nasdaq100 = get_symbols_in_NASDAQ100()
        sp500 = get_symbols_in_SP500()
        return nasdaq100 + sp500

    def get_all_companies():
        return get_priority_companies() + get_symbols_list_supported_by_fmp()

    def get_all_ETFs():
        # TODO(weimin): rank ETF by its AUM when AUM is available
        _fmp_loader = FmpDataLoader(data_dir, "etf_list")
        _fmp_loader.request_etf_list_data()
        df = _fmp_loader.parse_etf_list_to_tsv()
        return list(df["symbol"])

    def dedup(all_symbols):
        visited = set()
        symbols = []
        for symbol in all_symbols:
            if symbol not in visited:
                symbols.append(symbol)
                visited.add(symbol)
        return symbols

    def download_with_FmpDataLoader_function(func, is_etf=False):
        """
        This function downloads and saves data for all symbols available in FMP
        using FmpDataLoader's method func.

        :param func: str, a method of the class FmpDataLoader to download data
                        which must take a parameter of ticker.
        :return: None.
        """
        if is_etf:
            all_symbols = get_all_ETFs()
        else:
            all_symbols = get_all_companies()
        symbols = dedup(all_symbols)

        fmp_data_loader = FmpDataLoader(data_dir, form_type)
        download_method = getattr(fmp_data_loader, func)
        for i, ticker in enumerate(symbols):
            print('Downloading FMP data of the symbol {:>10} to json file by {}(). {:7d}/{:7d} ...'
                  .format(ticker, func, i, len(symbols)))
            download_method(ticker)  # equivalent to fmp_data_loader.func(ticker)

    if form_type == 'inst_holder':
        download_with_FmpDataLoader_function("request_inst_holder_data")
    elif form_type == "mutual_fund_holder":
        download_with_FmpDataLoader_function("request_mutual_fund_holder_data")
    elif form_type == 'insider_trading':
        download_with_FmpDataLoader_function("request_insider_trading_data")
    elif form_type == 'etf_holder':
        download_with_FmpDataLoader_function("request_etf_holder_data")
    elif form_type == 'company_profile':
        download_with_FmpDataLoader_function("request_company_profile_data")
    elif form_type == 'enterprise_value':
        download_with_FmpDataLoader_function("request_enterprise_value_data")
    elif form_type == 'stock_split':
        download_with_FmpDataLoader_function("request_stock_split_data")
    elif form_type == "yearly_ratios":
        download_with_FmpDataLoader_function("request_yearly_ratios_data")
    elif form_type == "quarterly_ratios":
        download_with_FmpDataLoader_function("request_quarterly_ratios_data")
    elif form_type == "ratios_ttm":
        download_with_FmpDataLoader_function("request_ratios_ttm_data")
    elif form_type == "yearly_income_statement":
        download_with_FmpDataLoader_function("request_yearly_income_statement_data")
    elif form_type == "quarterly_income_statement":
        download_with_FmpDataLoader_function("request_quarterly_income_statement_data")
    elif form_type == "10-Q":
        symbols = get_symbols_list_supported_by_fmp()
        fmp_data_loader = FmpDataLoader(data_dir, form_type)
        for year in range(start_year, end_year+1):
            for quarter in quarters:
                for i, ticker in enumerate(symbols):
                    print('Downloading FMP data of the ticker {:>10} to json file for {}-{}. {:7d}/{:7d} ...'
                          .format(ticker, year, quarter, i, len(symbols)))
                    fmp_data_loader.request_10_Q_data(ticker, year, quarter)
    elif form_type == "10-K":
        download_with_FmpDataLoader_function("request_form_10k_data")
    elif form_type == 'shares_float':
        download_with_FmpDataLoader_function("request_form_shares_float_data")
    elif form_type == 'etf_list':
        fmp_loader = FmpDataLoader(data_dir, form_type)
        print(f'Downloading ETF list to json file ...')
        fmp_loader.request_etf_list_data()
    #
    elif form_type == 'cik_map':
        fmp_loader = FmpDataLoader(data_dir, form_type)
        print(f'Downloading CIK map to json file ...')
        fmp_loader.request_cik_map_data()
    #
    elif form_type == 'sector_performance':
        fmp_loader = FmpDataLoader(data_dir, form_type)
        fmp_loader.request_sector_performance_data()       
    #
    elif form_type == 'finnhub_sentiment':
        download_with_FmpDataLoader_function("request_finnhub_sentiment_data")

    elif form_type == 'finnhub_etf_holdings':
        download_with_FmpDataLoader_function("request_finnhub_etf_holdings_data", is_etf=True)

    else:
        data = request_get_as_json(
            url=f'https://financialmodelingprep.com/api/v3/cik_list?apikey={key}')

        table = pd.DataFrame(data)

        list_file = list_file_dir / f'download.list'
        table.to_csv(list_file, sep='\t', index=False)

        fmp_loader = FmpDataLoader(data_dir, form_type, report_date)
        for cik in table.loc[:, 'cik']:
            print(f'Downloading FMP data {cik} to json file ...')
            fmp_loader.request_form_13_data(cik, report_date)
        #

#