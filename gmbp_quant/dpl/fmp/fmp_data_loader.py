import datetime
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
from gmbp_quant.dpl.fmp.fmp_schemas import Fmp13FSchema, Fmp4Schema, Fmp10KSchema
from gmbp_quant.dpl.fmp.fmp_schemas import FmpInstHolderSchema, FmpEtfHolderSchema, FmpInsiderTradingSchema
from gmbp_quant.dpl.fmp.fmp_schemas import FmpCompanyProfileSchema, FmpEtfSchema, FmpSectorPerformanceSchema
from gmbp_quant.dpl.fmp.fmp_schemas import FmpCikNameMapSchema, FmpSecCikNameMapSchema, FmpEnterpriseValueSchema, \
    FmpStockSplitSchema, FmpMutualFundHolderSchema, FmpYearlyRatiosSchema, FmpQuarterlyRatiosSchema,\
    FmpRatiosTtmSchema, FmpYearlyIncomeStatementSchema, FmpQuarterlyIncomeStatementSchema, Fmp10QSchema, \
    FinnhubSentimentSchema, FinnhubETFHoldings, FmpSharesFloatSchema


logger = LOG.get_logger(__name__)
key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
FINNHUB_API_KEY = ecfg.get_env_config().get(ecfg.Prop.FINNHUB_API_KEY)


class FmpDataLoader(DataLoader):
    """A :class:`FMPDataLoader` class

    Args:
        data_dir: folder storing FMP data
        form_type: FMP form type, currently support
                    '13F'
                    '4'
                    'inst_holder'
                    'eft_holder'
                    'company_profile'
                    'enterprise_value'
                    'stock_split'
                    'etf_list'
                    'fmp_sector_performance'
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
        schemas = {  # {form_type: Schema}
            '13F': Fmp13FSchema,
            '4': Fmp4Schema,
            '10-Q': Fmp10QSchema,
            '10-K': Fmp10KSchema,
            'shares_float': FmpSharesFloatSchema,
            'inst_holder': FmpInstHolderSchema,
            "mutual_fund_holder": FmpMutualFundHolderSchema,
            'insider_trading': FmpInsiderTradingSchema,
            'etf_holder': FmpEtfHolderSchema,
            'company_profile': FmpCompanyProfileSchema,
            'enterprise_value': FmpEnterpriseValueSchema,
            'stock_split': FmpStockSplitSchema,
            'yearly_ratios': FmpYearlyRatiosSchema,
            'quarterly_ratios': FmpQuarterlyRatiosSchema,
            'ratios_ttm': FmpRatiosTtmSchema,
            'yearly_income_statement': FmpYearlyIncomeStatementSchema,
            'quarterly_income_statement': FmpQuarterlyIncomeStatementSchema,
            'etf_list': FmpEtfSchema,
            'sector_performance': FmpSectorPerformanceSchema,
            'cik_map': FmpCikNameMapSchema,
            'cik_sec_map': FmpSecCikNameMapSchema,
            'finnhub_sentiment': FinnhubSentimentSchema,
            "finnhub_etf_holdings": FinnhubETFHoldings
        }
        super().__init__(data_dir, form_type, self.tsv_dir, 'mktdata', schemas[form_type])

        self.form_dir.mkdir(parents=True, exist_ok=True)

    def request_form_13_data(self, cik, report_date):
        data_file = self.form_dir / f'{cik}-json.txt'
        if os.path.exists(data_file):
            return None

        data = request_get_as_json(
            url=f'https://financialmodelingprep.com/api/v3/form-thirteen/{cik}?date={report_date}&apikey={key}')
        if data is None:
            return None
        #

        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

        return data
    #

    def request_inst_holder_data(self, ticker):
        data_file = self.form_dir / f'{ticker}-json.txt'
        if os.path.exists(data_file):
            return None

        url = f'https://financialmodelingprep.com/api/v3/institutional-holder/{ticker}?apikey={key}'
        data = request_get_as_json(url)
        if data is None:
            return None
        #

        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

        return data
    #

    def request_mutual_fund_holder_data(self, ticker):
        data_file = self.form_dir / f'{ticker}-json.txt'
        if os.path.exists(data_file):
            return None

        url = f'https://financialmodelingprep.com/api/v3/mutual-fund-holder/{ticker}?apikey={key}'
        data = request_get_as_json(url)
        if data is None:
            return None

        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

        return data

    def request_etf_holder_data(self, ticker):
        data_file = self.form_dir / f'{ticker}-json.txt'
        if os.path.exists(data_file):
            return None

        url =f'https://financialmodelingprep.com/api/v3/etf-holder/{ticker}?apikey={key}'
        data = request_get_as_json(url)
        if data is None:
            return None
        #

        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

        return data
    #

    def request_insider_trading_data(self, ticker):
        data_file = self.form_dir / f'{ticker}-json.txt'
        if os.path.exists(data_file):
            return None

        url =f'https://financialmodelingprep.com/api/v4/insider-trading?symbol={ticker}&apikey={key}'
        data = request_get_as_json(url)
        if data is None:
            return None
        #

        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

        return data
    #

    def request_company_profile_data(self, ticker):
        data_file = self.form_dir / f'{ticker}-json.txt'
        if os.path.exists(data_file):
            return None

        url =f'https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={key}'
        data = request_get_as_json(url)
        if data is None:
            return None
        #

        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

        return data
    #

    def request_enterprise_value_data(self, ticker):
        data_file = self.form_dir / f'{ticker}-json.txt'
        if os.path.exists(data_file):
            return None

        url =f'https://financialmodelingprep.com/api/v3/enterprise-values/{ticker}?limit=40&apikey={key}'
        data = request_get_as_json(url)
        if data is None:
            return None
        #

        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

        return data
    #

    def request_stock_split_data(self, ticker):
        data_file = self.form_dir / f'{ticker}-json.txt'
        if os.path.exists(data_file):
            return None

        url =f'https://financialmodelingprep.com/api/v3/historical-price-full/stock_split/{ticker}?apikey={key}'
        data = request_get_as_json(url)
        if data is None:
            return None
        #

        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

        return data
    #

    def request_yearly_ratios_data(self, ticker):
        data_file = self.form_dir / f'{ticker}-json.txt'
        if os.path.exists(data_file):
            return None

        url = f'https://financialmodelingprep.com/api/v3/ratios/{ticker}?apikey={key}&limit=40'
        data = request_get_as_json(url)
        if data is None:
            return None

        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

        return data

    def request_quarterly_ratios_data(self, ticker):
        data_file = self.form_dir / f'{ticker}-json.txt'
        if os.path.exists(data_file):
            return None

        url = f'https://financialmodelingprep.com/api/v3/ratios/{ticker}?apikey={key}&limit=140&period=quarter'
        data = request_get_as_json(url)
        if data is None:
            return None

        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

        return data

    def request_ratios_ttm_data(self, ticker):
        data_file = self.form_dir / f'{ticker}-json.txt'
        if os.path.exists(data_file):
            return None

        url = f'https://financialmodelingprep.com/api/v3/ratios-ttm/{ticker}?apikey={key}'
        data = request_get_as_json(url)
        if data is None:
            return None

        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

        return data

    def request_yearly_income_statement_data(self, ticker):
        data_file = self.form_dir / f'{ticker}-json.txt'
        if os.path.exists(data_file):
            return None

        url = f'https://financialmodelingprep.com/api/v3/income-statement/{ticker}?apikey={key}&limit=120'
        data = request_get_as_json(url)
        if data is None:
            return None

        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

        return data

    def request_quarterly_income_statement_data(self, ticker):
        data_file = self.form_dir / f'{ticker}-json.txt'
        if os.path.exists(data_file):
            return None

        url = f'https://financialmodelingprep.com/api/v3/income-statement/{ticker}?apikey={key}&limit=400&period=quarter'
        data = request_get_as_json(url)
        if data is None:
            return None

        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

        return data

    def request_10_Q_data(self, ticker, year=2020, quarter="Q4"):
        print("haha", self.form_dir, ticker, year, quarter)
        data_file = self.form_dir / f'{year}-{quarter}-{ticker}-json.txt'
        if os.path.exists(data_file):
            return None

        url = f'https://financialmodelingprep.com/api/v4/financial-reports-json?symbol={ticker}&year={year}&period={quarter}&apikey={key}'
        data = request_get_as_json(url)
        if data is None:
            return None

        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

        return data

    def request_form_10q_data(self, symbol, year=2021, quarter='Q1'):
        data_file = self.form_dir / f'{symbol}-json.txt'
        if os.path.exists(data_file):
            return None

        data = request_get_as_json(
            url=f'https://financialmodelingprep.com/api/v4/financial-reports-json?symbol={symbol}&year={year}&period={quarter}&apikey={key}'
        )

        if data is None:
            return None

        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

    def request_form_10k_data(self, symbol, year=2020):
        data_file = self.form_dir / f'{symbol}-json.txt'
        if os.path.exists(data_file):
            return None

        data = request_get_as_json(
            url=f'https://financialmodelingprep.com/api/v4/financial-reports-json?symbol={symbol}&year={year}&period=FY&apikey={key}'
        )

        if data is None:
            return None

        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

    def request_form_shares_float_data(self, symbol):
        data_file = self.form_dir / f'{symbol}-json.txt'
        if os.path.exists(data_file):
            return None

        data = request_get_as_json(
            url=f'https://financialmodelingprep.com/api/v4/shares_float?symbol={symbol}&apikey={key}'
        )

        if data is None:
            return None

        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

    def request_etf_list_data(self):
        url =f'https://financialmodelingprep.com/api/v3/etf/list?apikey={key}'
        data = request_get_as_json(url)
        if data is None:
            return None
        #

        data_file = self.form_dir / f'etf-json.txt'
        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

        return data
    #

    def request_cik_map_data(self):
        url =f'https://financialmodelingprep.com/api/v4/mapper-cik-name?apikey={key}'
        data = request_get_as_json(url)
        if data is None:
            return None
        #

        data_file = self.form_dir / f'cik-json.txt'
        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

        return data
    #

    def request_sector_performance_data(self):
        data = request_get_as_json(
            url=f'https://financialmodelingprep.com/api/v3/historical-sectors-performance?limit=500&apikey={key}')
        if data is None:
            return None
        #
        data_file = self.form_dir / f'sector_performance-json.txt'
        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)
        return data

    def request_finnhub_sentiment_data(self, ticker):
        data_file = self.form_dir / f'{ticker}-json.txt'
        if os.path.exists(data_file):
            return None

        url = f'https://finnhub.io/api/v1/stock/social-sentiment?symbol={ticker}&token={FINNHUB_API_KEY}'
        data = request_get_as_json(url)
        if data is None:
            return None

        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

        return data

    def request_finnhub_etf_holdings_data(self, ticker):
        data_file = self.form_dir / f'{ticker}-json.txt'
        if os.path.exists(data_file):
            return None

        url = f'https://finnhub.io/api/v1/etf/holdings?symbol={ticker}&token={FINNHUB_API_KEY}'
        data = request_get_as_json(url)
        if data is None:
            return None

        with open(data_file, 'w') as data_file_output:
            json.dump(data, data_file_output)

        return data

    def parse_form_13_to_tsv(self):
        """Parse FMP form 13 and save to tsv files
        """

        for form in tqdm(self.form_list):
            cik = form.stem.split('-')[0]
            with open(form, 'r') as json_file:
                data = json.load(json_file)
                table = pd.DataFrame(data)

                if not table.empty:
                    table_sorted = table
                    table_sorted['report_date'] = table_sorted['date']
                    table_sorted = table_sorted.drop(columns=['date'])

                    output_path = self.tsv_dir / f'{cik}.tsv'
                    table_sorted.to_csv(output_path, sep='\t', index=False)
            #
        #
    #

    def parse_inst_holder_to_tsv(self):
        """Parse FMP forms and save to tsv files
        """

        for form in tqdm(self.form_list):
            ticker = form.stem.split('-')[0]
            with open(form, 'r') as json_file:
                data = json.load(json_file)
                table = pd.DataFrame(data)

                if not table.empty:
                    table_sorted = table
                    table_sorted['ticker'] = ticker
                    table_sorted['sharesChanged'] = table_sorted['change']
                    table_sorted = table_sorted.drop(columns=['change'])

                    output_path = self.tsv_dir / f'{ticker}.tsv'
                    table_sorted.to_csv(output_path, sep='\t', index=False)
            #
        #
    #

    def parse_mutual_fund_holder_to_tsv(self):
        """Parse FMP forms and save to tsv files
        """
        for form in tqdm(self.form_list):
            ticker = form.stem.split('-')[0]
            with open(form, 'r') as json_file:
                data = json.load(json_file)
                table = pd.DataFrame(data)

                if not table.empty:
                    table_sorted = table
                    table_sorted['ticker'] = ticker
                    table_sorted['sharesChanged'] = table_sorted['change']
                    table_sorted = table_sorted.drop(columns=['change'])

                    output_path = self.tsv_dir / f'{ticker}.tsv'
                    table_sorted.to_csv(output_path, sep='\t', index=False)

    def parse_etf_holder_to_tsv(self):
        """Parse FMP forms and save to tsv files
        """

        for form in tqdm(self.form_list):
            holder = form.stem.split('-')[0]
            with open(form, 'r') as json_file:
                data = json.load(json_file)
                table = pd.DataFrame(data)

                if not table.empty:
                    table_sorted = table
                    table_sorted['holder'] = holder

                    output_path = self.tsv_dir / f'{holder}.tsv'
                    table_sorted.to_csv(output_path, sep='\t', index=False)
            #
        #
    #

    def parse_insider_trading_to_tsv(self):
        """Parse FMP forms and save to tsv files
        """

        for form in tqdm(self.form_list):
            holder = form.stem.split('-')[0]
            with open(form, 'r') as json_file:
                data = json.load(json_file)
                table = pd.DataFrame(data)

                if not table.empty:
                    table_sorted = table
                    table_sorted['holder'] = holder

                    output_path = self.tsv_dir / f'{holder}.tsv'
                    table_sorted.to_csv(output_path, sep='\t', index=False)
            #
        #
    #

    def parse_company_profile_to_tsv(self):
        """Parse FMP forms and save to tsv files
        """

        for form in tqdm(self.form_list):
            holder = form.stem.split('-')[0]
            with open(form, 'r') as json_file:
                data = json.load(json_file)
                table = pd.DataFrame(data)

                if not table.empty:
                    table_sorted = table.drop(columns=['description'])
                    table_sorted['holder'] = holder
                    table_sorted['priceRange'] = table_sorted['range']
                    table_sorted = table_sorted.drop(columns='range')

                    output_path = self.tsv_dir / f'{holder}.tsv'
                    table_sorted.to_csv(output_path, sep='\t', index=False)
            #
        #
    #

    def parse_enterprise_value_to_tsv(self):
        """Parse FMP forms and save to tsv files
        """

        for form in tqdm(self.form_list):
            holder = form.stem.split('-')[0]
            with open(form, 'r') as json_file:
                data = json.load(json_file)
                table = pd.DataFrame(data)

                if not table.empty:
                    table_sorted = table
                    table_sorted['report_date'] = table['date']
                    table_sorted = table_sorted.drop(columns=['date'])
                    output_path = self.tsv_dir / f'{holder}.tsv'
                    table_sorted.to_csv(output_path, sep='\t', index=False)
            #
        #
    #

    def parse_stock_split_to_tsv(self):
        """Parse FMP forms and save to tsv files
        """

        for form in tqdm(self.form_list):
            holder = form.stem.split('-')[0]
            with open(form, 'r') as json_file:
                data = json.load(json_file)
                if 'symbol' in data:
                    table = pd.DataFrame(data['historical'])
                    table_sorted = table

                    if not table.empty:
                        table_sorted['report_date'] = table_sorted['date']
                        table_sorted['symbol'] = data['symbol']
                        table_sorted = table_sorted.drop(columns=['date'])
                        output_path = self.tsv_dir / f'{holder}.tsv'
                        table_sorted.to_csv(output_path, sep='\t', index=False)
                    #
                #
            #
        #
    #

    def parse_json_naively_to_tsv(self):
        """
        Transform json to tsv as it is without any change.
        :return:
        """
        for form in tqdm(self.form_list):
            ticker = form.stem.split('-')[0]
            with open(form, 'r') as json_file:
                data = json.load(json_file)
                table = pd.DataFrame(data)

                if not table.empty:
                    output_path = self.tsv_dir / f'{ticker}.tsv'
                    table.to_csv(output_path, sep='\t', index=False)
                else:
                    print(f"The downloaded FMP data for symbol {ticker} is empty.")

    def parse_income_statement_to_tsv(self):
        """
        Transform json to tsv as it is without any change.
        :return:
        """
        for form in tqdm(self.form_list):
            ticker = form.stem.split('-')[0]
            with open(form, 'r') as json_file:
                data = json.load(json_file)
                table = pd.DataFrame(data)
                if table.empty:
                    print(f"The downloaded FMP data for symbol {ticker} is empty.")
                    continue

                table["endDate"] = table['date']  # 'date' is a reserved keyword in db.
                table = table.drop(columns=['date'])

                for i in range(table.shape[0]):
                    # A bug from FMP itself, the last date for September should be 30th
                    _date = table.loc[i, "fillingDate"]
                    if _date and len(_date) > 5 and _date[-5:] == '09-31':
                        table.loc[i, "fillingDate"] = _date[:-5] + "09-30"
                    _date = table.loc[i, "acceptedDate"]
                    if _date and len(_date) > 5 and _date[-5:] == '09-31':
                        table.loc[i, "acceptedDate"] = _date[:-5] + "09-30"

                if not table.empty:
                    output_path = self.tsv_dir / f'{ticker}.tsv'
                    table.to_csv(output_path, sep='\t', index=False)

    def parse_ratios_to_tsv(self):
        """
        Transforms yearly/quarterly ratios json to tsv. Change 'date' to 'endDate'.
        :return:
        """
        for form in tqdm(self.form_list):
            ticker = form.stem.split('-')[0]
            with open(form, 'r') as json_file:
                data = json.load(json_file)
                table = pd.DataFrame(data)

                if table.empty:
                    print(f"The downloaded FMP data for symbol {ticker} is empty.")
                    continue

                table["endDate"] = table['date']  # 'date' is a reserved keyword in db.
                table = table.drop(columns=['date'])

                output_path = self.tsv_dir / f'{ticker}.tsv'
                table.to_csv(output_path, sep='\t', index=False)

    def parse_ratios_ttm_to_tsv(self):
        """
        Transform json to tsv, and add symbol and endDate columns.
        :return:
        """
        for form in tqdm(self.form_list):
            ticker = form.stem.split('-')[0]
            with open(form, 'r') as json_file:
                data = json.load(json_file)
                table = pd.DataFrame(data)

                if not table.empty:
                    table['symbol'] = ticker
                    table['endDate'] = datetime.date.today()
                    output_path = self.tsv_dir / f'{ticker}.tsv'
                    table.to_csv(output_path, sep='\t', index=False)
                else:
                    print(f"The downloaded FMP data for symbol {ticker} is empty.")

    def parse_10_Q_to_tsv(self):
        for form in tqdm(self.form_list):
            year = form.stem[:4]
            quarter = form.stem[5:7]
            ticker = form.stem[8:].split('-')[0]  # the file is in form of YYYY-QQ-ticker-json.txt
            with open(form, 'r') as json_file:
                data = json.load(json_file)

                try:
                    results = {"symbol": [ticker, ticker], "year": [year, year], "period": [quarter, quarter]}
                    for outer_key in data:
                        if "CONDENSED CONSOLIDATED STATEM" not in outer_key:
                            continue
                        elements = data[outer_key]
                        if "CASH FLOWS" not in list(elements[0].keys())[0]:
                            continue
                        nMonthsEnded = list(elements[0].values())[0][0]
                        ending_dates = []
                        numberOfSharesRepurchased = []
                        for element in elements:
                            if "items" in list(element.keys())[0]:
                                endingDate = list(element.values())[0]
                            if "Repurchases of common stock".upper() in list(element.keys())[0].upper():
                                numberOfSharesRepurchased = list(element.values())[0]
                        if len(endingDate) == 2 and len(numberOfSharesRepurchased) == 2:
                            results["nMonthsEnded"] = [nMonthsEnded, nMonthsEnded]
                            results["endingDate"] = endingDate
                            results["numberOfSharesRepurchased"] = numberOfSharesRepurchased
                            break
                    else:
                        print(f"The downloaded FMP data for symbol {ticker} is parsed with failure: the CASH FLOWS table is not found.")
                        continue
                except:
                    print(f"The downloaded FMP data for symbol {ticker} is parsed with failure: encountered exception.")
                    continue

                table = pd.DataFrame(results, columns=["symbol", "year", "period", "nMonthsEnded",
                                                       "endingDate", "numberOfSharesRepurchased"])
                output_path = self.tsv_dir / f'{year}-{quarter}-{ticker}.tsv'
                table.to_csv(output_path, sep='\t', index=False)

    def parse_10q_to_tsv(self):
        """Parse FMP forms and save to tsv files
        """
        # ToDo

        def iterate_json(somejson):

            for key, value in somejson.items():
                if 'entity common stock, shares outstanding' in key.lower():
                    share = (next(item for item in value if item is not None))
                    shares.append(share)
                if type(value) == type(dict()):
                    iterate_json(value)
                elif type(value) == type(list()):
                    for val in value:
                        if type(val) == type(dict()):
                            iterate_json(val)
                        else:
                            pass
            return shares

        def unique_list_3(list_in):
            """
            Return unique first three (or less) unique elements of a list.
            """
            unique_list = []

            for element in list_in:
                if element not in unique_list and len(unique_list) < 3:
                    unique_list.append(element)

            return unique_list

        for form in tqdm(self.form_list):

            ticker = form.stem.split('-')[0]

            with open(form, 'r') as json_file:
                data = json.load(json_file)

                if len(data) > 1: # parse json when it has meaningful data
                    shares = []
                    d = {'symbol': [], 'year': [], 'period': [], 'shares_outstanding': [], 'cls': []}
                    shares = iterate_json(data)
                    shares = unique_list_3(shares)
                    d['symbol'] = [ticker for _ in range(len(shares))]
                    d['year'] = [data['year'] for _ in range(len(shares))]
                    d['period'] = [data['period'] for _ in range(len(shares))]
                    d['shares_outstanding'] = shares
                    d['cls'] = [i for i in range(len(shares))]

                else:
                    d = {'symbol': [ticker], 'year': [''], 'period': [''], 'shares_outstanding': [''], 'cls': ['']}

                table_sorted = pd.DataFrame(d)

                output_path = self.tsv_dir / f'{ticker}_1.tsv'
                table_sorted.to_csv(output_path, sep='\t', index=False)

    def parse_10k_to_tsv(self):
        """Parse FMP forms and save to tsv files
        """

        def iterate_json(somejson):

            for key, value in somejson.items():
                if 'entity common stock, shares outstanding' in key.lower():
                    share = (next(item for item in value if item is not None))
                    shares.append(share)
                if type(value) == type(dict()):
                    iterate_json(value)
                elif type(value) == type(list()):
                    for val in value:
                        if type(val) == type(dict()):
                            iterate_json(val)
                        else:
                            pass
            return shares

        def unique_list_3(list_in):
            """
            Return unique first three (or less) unique elements of a list.
            """
            unique_list = []

            for element in list_in:
                if element not in unique_list and len(unique_list) < 3:
                    unique_list.append(element)

            return unique_list


        for form in tqdm(self.form_list):

            ticker = form.stem.split('-')[0]

            with open(form, 'r') as json_file:
                data = json.load(json_file)

                if len(data) > 1: # parse json when it has meaningful data
                    shares = []
                    d = {'symbol': [], 'year': [], 'shares_outstanding': [], 'cls': []}
                    shares = iterate_json(data)
                    shares = unique_list_3(shares)
                    d['symbol'] = [ticker for _ in range(len(shares))]
                    d['year'] = [data['year'] for _ in range(len(shares))]
                    d['shares_outstanding'] = shares
                    d['cls'] = [i for i in range(len(shares))]

                else:
                    d = {'symbol': [ticker], 'year': [2020], 'shares_outstanding': [''], 'cls': ['']}

                table_sorted = pd.DataFrame(d)

                output_path = self.tsv_dir / f'{ticker}_1.tsv'
                table_sorted.to_csv(output_path, sep='\t', index=False)
            #
        #
    #
    def parse_shares_float_to_tsv(self):
        """Parse FMP forms and save to tsv files
        """

        for form in tqdm(self.form_list):

            ticker = form.stem.split('-json')[0]

            with open(form, 'r') as json_file:
                data = json.load(json_file)

                if data:
                    date_reported = data[0]['date']
                    float_shares = data[0]['floatShares']
                    shares = data[0]['outstandingShares']
                    d = {'symbol': [ticker], 'shares_outstanding': [shares], 'float_shares': [float_shares],
                         'date_reported': [date_reported]}

                    table_sorted = pd.DataFrame(d)
                    output_path = self.tsv_dir / f'{ticker}_1.tsv'
                    table_sorted.to_csv(output_path, sep='\t', index=False)

                else:
                    pass

    def parse_etf_list_to_tsv(self):
        """Parse FMP ETF list and save to tsv files
        """
        for form in tqdm(self.form_list):  # should only have one file "etf-json.txt"
            file_id = form.stem.split('-')[0]
            with open(form, 'r') as json_file:
                data = json.load(json_file)
                table = pd.DataFrame(data)

                if not table.empty:
                    table_sorted = table

                    output_path = self.tsv_dir / f'{file_id}.tsv'
                    table_sorted.to_csv(output_path, sep='\t', index=False)
                    return table_sorted
        return pd.DataFrame()

    def parse_cik_map_to_tsv(self):
        """Parse FMP CIK map and save to tsv files
        """

        for form in tqdm(self.form_list):
            file_id = form.stem.split('-')[0]
            with open(form, 'r') as json_file:
                data = json.load(json_file)
                table = pd.DataFrame(data)

                if not table.empty:
                    table_sorted = table

                    output_path = self.tsv_dir / f'{file_id}.tsv'
                    table_sorted.to_csv(output_path, sep='\t', index=False)
            #
        #
    #

    def parse_sector_performance_to_tsv(self):
        """Parse FMP Sector performance to tsv files
        """
        for form in tqdm(self.form_list):
            file_id = form.stem.split('-')[0]
            with open(form, 'r') as json_file:
                data = json.load(json_file)
                table = pd.DataFrame(data)
                result = []
                for i, row in table.iterrows():
                    d = row['date']
                    for col in table.columns[1:]:
                        s = col.replace('ChangesPercentage', '')
                        c = row[col]
                        result.append([d, s, c])
                
                output_path = self.tsv_dir / f'{file_id}.tsv'
                result_table = pd.DataFrame(result, columns=['currentDate', 'sector', 'changes'])
                result_table.to_csv(output_path, sep='\t', index=False)
            #
        #
    #
    def parse_finnhub_sentiment_to_tsv(self):
        """Parse Finnhub Sentiment data (reddit section) to tsv files
        """

        for form in tqdm(self.form_list):
            file_id = form.stem.split('-')[0]
            with open(form, 'r') as json_file:
                data = json.load(json_file)
                reddit_data = data["reddit"]
                symbol = data["symbol"]
                if len(reddit_data) > 0:
                    cols = ["symbol", "atTime", "mention", "positiveScore", "negativeScore",
                            "positiveMention", "negativeMention", "score"]
                    reddit_data_dict = {col: [] for col in cols}
                    for row in reddit_data:
                        reddit_data_dict["symbol"].append(symbol)
                        for col in cols[1:]:
                            reddit_data_dict[col].append(row[col])

                    reddit_data_dict["atTime"] = list(map(lambda x: pd.Timestamp(x).to_pydatetime(),
                                                     reddit_data_dict["atTime"]))

                    table_output = pd.DataFrame(reddit_data_dict, columns=cols)
                    output_path = self.tsv_dir / f'{file_id}.tsv'
                    table_output.to_csv(output_path, sep='\t', index=False)
            #
        #
    #
    def parse_finnhub_etf_holdings_to_tsv(self):
        for form in tqdm(self.form_list):
            file_id = form.stem.split('-')[0]
            with open(form, 'r') as json_file:
                data = json.load(json_file)
                holdings_data = data["holdings"]
                symbol = data["symbol"]
                atDate = data["atDate"]
                if len(holdings_data) > 0:
                    cols = ["symbol", "atDate", "cusip", "isin", "name",
                            "percent", "share", "value"]
                    holdings_data_dict = {col: [] for col in cols}
                    for row in holdings_data:
                        holdings_data_dict["symbol"].append(symbol)
                        holdings_data_dict["atDate"].append(atDate)
                        for col in cols[2:]:
                            holdings_data_dict[col].append(row[col])

                    holdings_data_dict["marketValue"] = holdings_data_dict["value"]
                    del holdings_data_dict["value"]
                    table_output = pd.DataFrame(holdings_data_dict, columns=cols[:-1]+["marketValue"])
                    output_path = self.tsv_dir / f'{file_id}.tsv'
                    table_output.to_csv(output_path, sep='\t', index=False)
            #
        #
    #

