import os
import pandas as pd
import gmbp_common.utils.miscs as mu

# url = "http://old.nasdaq.com/screening/companies-by-industry.aspx?&render=download"

# NASDAQ sectors, not the same as Morningstar
NASDAQ_SECTORS = ['Basic Industries', 'Capital Goods', 'Consumer Durables', 'Consumer Non-Durables', 'Consumer Services',
                  'Energy', 'Finance', 'Health Care', 'Miscellaneous', 'Public Utilities',
                  'Technology', 'Transportation', 'n/a']


def read_nasdaq_screener(data_file=None, data_dir=None, cols=None):
    if data_file is None:
        data_file = os.path.join(data_dir, 'nasdaq_screener.csv')
    #

    if cols is None:
        return pd.read_csv(data_file, sep=',')
    #

    cols = set(mu.iterable_to_tuple(cols, raw_type='str'))
    cols.update({'Symbol',})

    return pd.read_csv(data_file, sep=',', usecols=list(cols))
#


def read_symbol_nasdaq_sectors(data_file=None, data_dir=None, attach_sector_id=False):
    symbol_sectors = read_nasdaq_screener(data_file=data_file, data_dir=data_dir,
                                          cols=['Symbol', 'Sector'])

    if attach_sector_id:
        nasdaq_sector_name_to_id_map = {name:i for i,name in enumerate(NASDAQ_SECTORS)}
        symbol_sectors['SectorId'] = symbol_sectors['Sector'].map(nasdaq_sector_name_to_id_map).fillna(-1).astype(int)
    #

    return symbol_sectors
#
