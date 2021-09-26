from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
import pandas as pd

import gmbp_quant.env_config as ecfg
import gmbp_common.utils.datetime_utils as dtu
from gmbp_common.utils.endpoint_utils import request_get_as_json

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


BARS_COLS_MAP = {'T': 'Ticker',
                 'o': 'Open',
                 'h': 'High',
                 'l': 'Low',
                 'c': 'Close',
                 'v': 'Volume',
                 'vw': 'VWAP',
                 't': 'DateTime',
                 'n': 'NumberTransactions',
                 'av': 'AccumulatedVolume'}
QUOTES_COLS_MAP = {'p': 'Bid',
                   's': 'BidSize',
                   'P': 'Ask',
                   'S': 'AskSize',
                   't': 'DateTime'}
TRADES_COLS_MAP = {'c': 'Condition',
                   'i': 'TradeID',
                   'p': 'Price',
                   's': 'Size',
                   't': 'DateTime',
                   'x': 'ExchangeID'}


def request_open_close(symbol: str, dateid: int, adjusted=True):
    key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)
    url = f"https://api.polygon.io/v1/open-close/{symbol}/{dtu.dateid_to_datestr(dateid=dateid, sep='-')}" \
          f"?unadjusted={not adjusted}&apiKey={key}"
    data = requests.get(url).json()

    status = data['status']
    if status != 'OK':
        logger.error(f'Failed with status={status} on url={url}')
        return None
    #

    data = pd.Series(data).to_frame().T
    return data
#


def request_grouped_daily(dateid, adjusted=True):
    key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)
    url = f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{dtu.dateid_to_datestr(dateid=dateid, sep='-')}" \
          f"?unadjusted={not adjusted}&apiKey={key}"
    data = request_get_as_json(url=url)
    # 'results' will be missing if markets are closed
    if data is None or 'results' not in data:
        return None
    #
    daily = pd.DataFrame(data['results'])
    daily.rename(columns=BARS_COLS_MAP, inplace=True)
    local_timezone = datetime.now().astimezone().tzinfo
    for col in ['DateTime']:
        daily[col] = pd.to_datetime(daily[col].astype(int), unit='ms', utc=True).dt.tz_convert(local_timezone)
    #
    return daily
#


def request_aggregates(symbol, start_dateid=None, end_dateid=None,
                       multiplier=1, timespan='minute', adjusted=True):
    """
    >>> from gmbp_quant.dpl.polygon.polygon_stock_api import request_aggregates
    >>> aapl = request_aggregates(symbol='AAPL', start_dateid=19800101, timespan='day')
            Volume    VWAP    Open   Close    High     Low                  DateTime  NumberTransactions
    0  237916000.0  0.3687  0.3698  0.3713  0.3768  0.3606 2003-10-01 00:00:00-04:00                9710
    1  205946608.0  0.3658  0.3715  0.3673  0.3715  0.3622 2003-10-02 00:00:00-04:00                9672
    2  299651520.0  0.3829  0.3748  0.3873  0.3903  0.3729 2003-10-03 00:00:00-04:00               13466
    3  268328088.0  0.3941  0.3870  0.3981  0.3988  0.3854 2003-10-06 00:00:00-04:00                8637
    4  417483584.0  0.4051  0.3938  0.4147  0.4181  0.3913 2003-10-07 00:00:00-04:00               15233
    """

    timespan = timespan.lower()
    if timespan not in ['minute', 'hour', 'day', 'week', 'month', 'quarter', 'year']:
        logger.error(f'Invalid timespan={timespan}. The only supported resolutions are minute|hour|day|week|month|quarter|year')
        return None
    #

    key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)

    start_dateid, end_dateid = dtu.infer_start_dateid_end_dateid(start_date=start_dateid, end_date=end_dateid)
    start_date = dtu.dateid_to_datestr(dateid=start_dateid, sep='-')
    end_date = dtu.dateid_to_datestr(dateid=end_dateid, sep='-')

    url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/{multiplier}/{timespan}/{start_date}/{end_date}?' \
          f'unadjusted={not adjusted}&sort=asc&limit=50000&apiKey={key}'

    data = request_get_as_json(url=url)
    if data is None:
        return None
    #

    bars = pd.DataFrame(data['results'])
    bars.rename(columns=BARS_COLS_MAP, inplace=True)
    local_timezone = datetime.now().astimezone().tzinfo
    for col in ['DateTime']:
        bars[col] = pd.to_datetime(bars[col].astype(int), unit='ms', utc=True).dt.tz_convert(local_timezone)
    #
    return bars
#


def request_minute_bars(symbol, start_dateid, end_dateid, adjusted=True):
    start_date = dtu.dateid_to_datetime(dateid=start_dateid)
    end_date = dtu.dateid_to_datetime(dateid=end_dateid)
    if end_date <= start_date+relativedelta(months=3):
        logger.info(f"Requesting minute bars for symbol={symbol}, start_dateid={start_dateid}, end_dateid={end_dateid}")
        return request_aggregates(symbol=symbol, start_dateid=start_dateid, end_dateid=end_dateid,
                                  multiplier=1, timespan='minute', adjusted=adjusted)
    #

    ret = list()
    while start_date<=end_date:
        next_end_date = min(start_date + relativedelta(months=3), end_date)
        ret.append(request_minute_bars(symbol=symbol,
                                       start_dateid=dtu.datetime_to_dateid(date=start_date),
                                       end_dateid=dtu.datetime_to_dateid(date=next_end_date),
                                       adjusted=adjusted))
        start_date = next_end_date + relativedelta(days=1)
    #

    return pd.concat(ret, sort=False)
#


def request_hour_bars(symbol, start_dateid, end_dateid, adjusted=True):
    return request_aggregates(symbol=symbol, start_dateid=start_dateid, end_dateid=end_dateid,
                              multiplier=1, timespan='hour', adjusted=adjusted)
#


def request_aggregates_over_all_tickers(start_dateid, end_dateid, adjusted=True):
    """Returns a dictionary containing a mapping
    from each field within BARS_COLS_MAP to the respective
    dataframe, which holds information over all available 
    tickers for the requested date range.
    """
    aggregated_data = {}
    col_idx = 0
    # "Ticker", "DateTime" are used as indices
    fields = [v for _,v in BARS_COLS_MAP.items() if v not in ("Ticker", "DateTime")]
    for f in fields:
        aggregated_data[f] = pd.DataFrame()
    #

    for dateid in range(start_dateid, end_dateid):
        data = request_grouped_daily(dateid=dateid, adjusted=True)
        # skip days when markets are closed
        if data is None:
            continue
        data_indexed_by_ticker = data.set_index('Ticker')
        for f in fields:
            aggregated_data[f].insert(col_idx, f"{dateid}", data_indexed_by_ticker[f])
        #
        col_idx += 1
    #

    # take transpose --> now columns are tickers, rows are dateids
    for f in aggregated_data:
        aggregated_data[f] = aggregated_data[f].T
        aggregated_data[f].index.name = 'DateId'
    #
    return aggregated_data
#


def request_snapshot_ticker(ticker):
    key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)
    url = f"https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers/{ticker}?&apiKey={key}"
    data = request_get_as_json(url=url)
    if data is None or 'ticker' not in data:
        return None
    #

    data = data['ticker']

    ctd_bar = pd.Series(data['day']).to_frame().T
    ctd_bar.rename(columns=BARS_COLS_MAP, inplace=True)

    last_quote = pd.Series(data['lastQuote']).to_frame().T
    last_quote.rename(columns=QUOTES_COLS_MAP, inplace=True)

    last_trade = pd.Series(data['lastTrade']).to_frame().T
    last_trade.rename(columns=TRADES_COLS_MAP, inplace=True)

    last_min_bar = pd.Series(data['min']).to_frame().T
    last_min_bar.rename(columns=BARS_COLS_MAP, inplace=True)

    ptd_bar = pd.Series(data['prevDay']).to_frame().T
    ptd_bar.rename(columns=BARS_COLS_MAP, inplace=True)

    return_data = pd.Series({'Ticker':data['ticker'], 'Change':data['todaysChange'], 'Return':data['todaysChangePerc'], 'DateTime':data['updated']}).to_frame().T
    return_data['Return'] /= 100.0

    local_timezone = datetime.now().astimezone().tzinfo
    for data in [ctd_bar, last_quote, last_trade, last_min_bar, ptd_bar, return_data]:
        for col in ['DateTime']:
            if col in data.columns:
                try:
                    data[col] = pd.to_datetime(data[col].astype(int), unit='ns', utc=True).dt.tz_convert(local_timezone)
                except:
                    logger.error(f"Failed to handle data:\n{data}")
            #
        #
    #

    return ctd_bar, last_quote, last_trade, last_min_bar, ptd_bar, return_data
#
