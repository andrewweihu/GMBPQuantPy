import os
import sys
import pandas as pd
from tqdm import tqdm
from datetime import datetime
import yahoo_fin.stock_info as yahoo_si

sys.path.append('..')
from gmbp_common.utils.datetime_utils import dateid_to_datestr
from gmbp_quant.dpl.base.data_loader import DataLoader
from gmbp_quant.dpl.yahoo.yahoo_schemas import (
    YahooIpoSchema, YahooMajorHolderSchema,
    YahooDirectHolderSchema, YahooInstitutionHolderSchema,
    YahooDailyPriceSchema, YahooStatsSchema)

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


class YahooDataLoader(DataLoader):
    """A :class:`YahooDataLoader` class

    Args:
        data_dir: folder storing Yahoo data
        form_type: Yahoo data type, currently support
                    'ipo'
    """

    def __init__(self, data_dir, form_type):
        self.form_dir = data_dir / form_type
        self.tsv_dir = data_dir / 'tsv_files' / form_type
        self.form_list = list(self.form_dir.glob('*.txt'))
        schemas = {
            'ipo': YahooIpoSchema,
            # 3 sub forms under holders
            'holders': {
                'major': YahooMajorHolderSchema,
                'direct': YahooDirectHolderSchema,
                'institution': YahooInstitutionHolderSchema
            },
            'daily_price': YahooDailyPriceSchema,
            'stats': {'stats': YahooStatsSchema}
        }

        super().__init__(data_dir, form_type, self.tsv_dir, 'mktdata', schemas[form_type])

        self.form_dir.mkdir(parents=True, exist_ok=True)

    def request_ipo_data(self, dateid=None):
        datestr = dateid_to_datestr(dateid=dateid)
        url = f'https://finance.yahoo.com/calendar/ipo?day={datestr}'

        print (url)
        ipo_data_raw = pd.read_html(url)

        if len(ipo_data_raw) == 0:
            logger.info(f'No IPO data found for date={dateid}')
            return None
        if len(ipo_data_raw) > 2:
            logger.warn(f'len(ipo_data)={len(ipo_data_raw)} is not expected !')
        #

        data_file = self.form_dir / f'{datestr}-tsv.txt'
        pd.concat(ipo_data_raw).to_csv(data_file, sep='\t', index=False)

        return ipo_data_raw
    #

    def parse_ipo_to_tsv(self):
        """Parse Yahoo IPO data and save to tsv files
        """

        print(f'File count {len(self.form_list)}')
        for form in tqdm(self.form_list):
            file_id = form.stem.split('-')[0]
            print(f'Processing {form}...')
            table = pd.read_csv(form, sep='\t')

            table_sorted = table
            table_sorted['PriceRange'] = table_sorted['Price Range']
            table_sorted['IpoDate'] = pd.to_datetime(table_sorted['Date']).dt.tz_localize(None)
            table_sorted = table_sorted.drop(columns=['Price Range', 'Date'])

            output_path = self.tsv_dir / f'{file_id}.tsv'
            table_sorted.to_csv(output_path, sep='\t', index=False)
            #
        #
    #

    def parse_holders_to_tsv(self, ticker):
        """Download holder data and save to tsv files.
        """
        ts = pd.Timestamp(datetime.today())
        year_quarter = f'{ts.year}Q{ts.quarter}'
        major_file = self.tsv_dir / f'{ticker}_{year_quarter}_major.tsv'
        direct_file = self.tsv_dir / f'{ticker}_{year_quarter}_direct.tsv'
        institution_file = self.tsv_dir / f'{ticker}_{year_quarter}_institution.tsv'

        try:
            holders = yahoo_si.get_holders(ticker)
        except Exception as e:
            print(f'Error {e} occured during download {ticker}')
            return None
        
        # Major holders
        if 'Major Holders' in holders.keys():
            top_row = holders['Major Holders'].columns.to_list()
            # if symbol is not a stock or doesn't conform table structure
            if len(top_row) != 2:
                return None

            holders['Major Holders'].loc[-1] = top_row
            holders['Major Holders'] = holders['Major Holders'].sort_index().reset_index(drop=True)
            holders['Major Holders'].columns = ['Numbers', 'HolderCategory']
            
            holders['Major Holders']['DownloadYearQuarter'] = year_quarter
            holders['Major Holders']['Symbol'] = ticker
            holders['Major Holders']['row_num'] = holders['Major Holders'].index

            cols = ['DownloadYearQuarter', 'Symbol', 'row_num', 'Numbers', 'HolderCategory']
            holders['Major Holders'] = holders['Major Holders'][cols]
            holders['Major Holders'].to_csv(major_file, sep='\t', index=False)
        
        # Direct holders
        if 'Direct Holders (Forms 3 and 4)' in holders.keys():
            if len(holders['Direct Holders (Forms 3 and 4)'].columns) != 5:
                return None

            holders['Direct Holders (Forms 3 and 4)'].columns = [
                'Holder', 'Shares', 'DateReported', 'PercentOut', 'Value']
            
            holders['Direct Holders (Forms 3 and 4)']['DateReported'] = pd.to_datetime(
                holders['Direct Holders (Forms 3 and 4)']['DateReported']).dt.tz_localize(None)
            
            holders['Direct Holders (Forms 3 and 4)']['DownloadYearQuarter'] = year_quarter
            holders['Direct Holders (Forms 3 and 4)']['Symbol'] = ticker
            holders['Direct Holders (Forms 3 and 4)']['row_num'] = holders['Direct Holders (Forms 3 and 4)'].index
            
            cols = ['DownloadYearQuarter', 'Symbol', 'row_num', 'Holder',
                'DateReported', 'PercentOut', 'Shares', 'Value']
            holders['Direct Holders (Forms 3 and 4)'] = holders['Direct Holders (Forms 3 and 4)'][cols]
            holders['Direct Holders (Forms 3 and 4)'].to_csv(direct_file, sep='\t', index=False)

        # Institutional Holders
        if 'Top Institutional Holders' in holders.keys():
            if len(holders['Top Institutional Holders'].columns) != 5:
                return None

            holders['Top Institutional Holders'].columns = [
                'Holder', 'Shares', 'DateReported', 'PercentOut', 'Value']
            
            holders['Top Institutional Holders']['DateReported'] = pd.to_datetime(
                holders['Top Institutional Holders']['DateReported']).dt.tz_localize(None)
            
            holders['Top Institutional Holders']['DownloadYearQuarter'] = year_quarter
            holders['Top Institutional Holders']['Symbol'] = ticker
            holders['Top Institutional Holders']['row_num'] = holders['Top Institutional Holders'].index
            
            cols = ['DownloadYearQuarter', 'Symbol', 'row_num', 'Holder',
                'DateReported', 'PercentOut', 'Shares', 'Value']
            holders['Top Institutional Holders'] = holders['Top Institutional Holders'][cols]
            holders['Top Institutional Holders'].to_csv(institution_file, sep='\t', index=False)
    
        return holders
    #

    def request_daily_price_data(self, ticker, start_date, end_date):
        data_file = self.form_dir / f'{ticker}-tsv.txt'
        if os.path.exists(data_file):
            return None

        daily_price_date = yahoo_si.get_data(ticker, start_date, end_date)
        daily_price_date['report_date'] = daily_price_date.index

        daily_price_date.to_csv(data_file, sep='\t', index=False)

        return daily_price_date
    #

    def parse_daily_price_to_tsv(self):
        """Parse Yahoo Daily Price data and save to tsv files
        """

        print(f'File count {len(self.form_list)}')
        for form in tqdm(self.form_list):
            file_id = form.stem.split('-')[0]
            print(f'Processing {form}...')
            table = pd.read_csv(form, sep='\t')

            output_path = self.tsv_dir / f'{file_id}.tsv'
            table.to_csv(output_path, sep='\t', index=False)
            #
        #
    #

    def request_stats_data(self, ticker):
        data_file = self.form_dir / f'{ticker}-tsv.txt'
        if os.path.exists(data_file):
            return None

        stats_data = yahoo_si.get_stats(ticker)
        stats_data['Symbol'] = ticker

        stats_data.to_csv(data_file, sep='\t', index=False)

        return stats_data
    #

    def parse_stats_to_tsv(self):
        """Parse Yahoo stats data and save to tsv files
        """

        print(f'File count {len(self.form_list)}')
        for form in tqdm(self.form_list):
            file_id = form.stem.split('-tsv')[0]

            print(f'Processing {form}...')
            table = pd.read_csv(form, sep='\t')

            try:
                cols = ['Shares Outstanding 5', 'Float', '% Held by Insiders 1', '% Held by Institutions 1']
                df = table.pivot_table(columns='Attribute', values='Value', aggfunc='first')[cols]
                df.columns = ['shares_outstanding', 'shares_float', 'insider_holding', 'institution_holding']
                df.insert(0, 'symbol', file_id)
            except:
                print(f'fail to parse {file_id}')

            output_path = self.tsv_dir / f'{file_id}-stats.tsv'
            df.to_csv(output_path, sep='\t', index=False)
            #
        #
    #