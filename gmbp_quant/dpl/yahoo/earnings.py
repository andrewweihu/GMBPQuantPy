import time
import requests
import json
import pandas as pd
from datetime import datetime
from joblib import Parallel, delayed
import gmbp_common.utils.datetime_utils as dtu
import gmbp_common.utils.miscs as mu

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)

BASE_URL = 'https://finance.yahoo.com/calendar/earnings'
BASE_STOCK_URL = 'https://finance.yahoo.com/quote'
RATE_LIMIT = 2000.0
SLEEP_BETWEEN_REQUESTS_S = 60 * 60 / RATE_LIMIT
OFFSET_STEP = 100


def _get_data_dict(url):
    time.sleep(SLEEP_BETWEEN_REQUESTS_S)
    page = requests.get(url)
    page_content = page.content.decode(encoding='utf-8', errors='strict')
    try:
        page_data_string = [row for row in page_content.split('\n') if row.startswith('root.App.main = ')][0][:-1]
    except IndexError:
        logger.warn(f'Skipping since no valid records found: {url}')
        return None
    #
    page_data_string = page_data_string.split('root.App.main = ', 1)[1]
    return json.loads(page_data_string)
#


def _query_earnings_single_symbol(symbol, offset=0):
    url = f'{BASE_URL}?symbol={symbol}&offset={offset}&size={OFFSET_STEP}'
    logger.debug(f'Fetching Yahoo earnings data {url}')
    page_data_dict = _get_data_dict(url)
    if page_data_dict is None:
        return None
    #
    try:
        earnings = page_data_dict['context']['dispatcher']['stores']['ScreenerResultsStore']['results']['rows']
        earnings = pd.DataFrame(earnings)
        if len(earnings)<OFFSET_STEP:
            return earnings
        #
        more_earnings = _query_earnings_single_symbol(symbol=symbol, offset=offset+OFFSET_STEP)
        return pd.concat([earnings, more_earnings], sort=False)
    except:
        logger.debug(f'Skipping since no valid records found: {url}')
        return None
    #
#


def query_earnings_single_symbol(symbol):
    url = f'{BASE_URL}?symbol={symbol}'

    earnings = _query_earnings_single_symbol(symbol=symbol)
    if earnings is None:
        logger.error(f'Skipping since no valid records found: {url}')
        return None
    #

    logger.info(f'{symbol} earnings with shape {earnings.shape} from {url}')
    return earnings
#


def query_earnings_multi_symbols(symbols):
    symbols = mu.iterable_to_tuple(symbols, raw_type='str')
    earnings = Parallel(n_jobs=2)(delayed(query_earnings_single_symbol)(symbol=symbol)
                                  for symbol in symbols)
    return pd.concat(earnings, sort=False)
#


def _query_earnings_single_date(dateid, offset=0):
    date_str = dtu.dateid_to_datestr(dateid=dateid, sep='-')
    url = f'{BASE_URL}?day={date_str}&offset={offset}&size={OFFSET_STEP}'
    logger.debug(f'Fetching Yahoo earnings data {url}')
    page_data_dict = _get_data_dict(url)


    try:
        earnings = page_data_dict['context']['dispatcher']['stores']['ScreenerResultsStore']['results']['rows']
        earnings = pd.DataFrame(earnings)
        if len(earnings) < OFFSET_STEP:
            return earnings
        #
        more_earnings = _query_earnings_single_date(dateid=dateid, offset=offset+OFFSET_STEP)
        return pd.concat([earnings, more_earnings], sort=False)
    except:
        logger.debug(f'Skipping since no valid records found: {url}')
        return None
    #
#


def query_earnings_single_date(dateid):
    date_str = dtu.dateid_to_datestr(dateid=dateid, sep='-')
    url = url = f'{BASE_URL}?day={date_str}'

    earnings = _query_earnings_single_date(dateid=dateid)
    if earnings is None:
        logger.error(f'Skipping since no valid records found: {url}')
        return None
    #

    logger.info(f'{dateid} earnings with shape {earnings.shape} from {url}')
    return earnings
#


def query_earnings_multi_dates(start_dateid=None, end_dateid=None, date_range_mode='SINGLE_DATE', mic='XNYS'):
    start_dateid, end_dateid = dtu.infer_trading_start_dateid_end_dateid(start_date=start_dateid, end_date=end_dateid,
                                                                         date_range_mode=date_range_mode, mic=mic)
    dateids = dtu.infer_trading_dateids(start_dateid=start_dateid, end_dateid=end_dateid, mic=mic)
    earnings = Parallel(n_jobs=2)(delayed(query_earnings_single_date)(dateid=dateid)
                                  for dateid in dateids)
    return pd.concat(earnings, sort=False)
#


def query_next_earning_date(symbol):
    url = f'{BASE_STOCK_URL}/{symbol}'
    try:
        page_data_dict = _get_data_dict(url)
        next_earning_date = page_data_dict['context']['dispatcher']['stores']['QuoteSummaryStore']['calendarEvents']['earnings']['earningsDate'][0]['raw']
        next_earning_date = datetime.fromtimestamp(next_earning_date)
        return dtu.datetime_to_dateid(date=next_earning_date)
    except:
        logger.warn(f'No earnings records from {url}')
        return None
    #
#
