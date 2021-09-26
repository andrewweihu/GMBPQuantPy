import requests, math, os
import pandas as pd

import gmbp_quant.env_config as ecfg
import gmbp_common.utils.datetime_utils as dtu
import gmbp_common.utils.miscs as mu
from gmbp_common.utils.endpoint_utils import request_get_as_json

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


# # Query all ticker symbols which are supported by Polygon.io
# # https://polygon.io/docs/get_v2_reference_tickers_anchor
# def request_tickers(sort_field: str = "", ticker_type: str = "", market: str = "", locale: str = "", search: str = "", 
#                     perpage: int = 50, page: int = 0, active: bool = True):
#     key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)
#     params = {"apiKey": key}
#     if sort_field:
#         params["sort"] = sort_field
#     if ticker_type:
#         params["type"] = ticker_type
#     if market:
#         params["market"] = market
#     if locale:
#         params["locale"] = locale
#     if search:
#         params["search"] = search
#     if perpage > 0:
#         params["perpage"] = perpage
#     if page > 0 :
#         params["page"] = page
#     if active:
#         params["active"] = "true"
#     data = requests.get("https://api.polygon.io/v2/reference/tickers", params=params)
#     return pd.Series(data).to_frame().T
# #


# Get a mapping of ticker types to their descriptive names.
# https://polygon.io/docs/get_v2_reference_types_anchor
def request_ticker_types():
    key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)
    url = f"https://api.polygon.io/v2/reference/types?&apiKey={key}"
    data = request_get_as_json(url=url)
    if data is None:
        return None
    #
    sec_types = pd.DataFrame({**data['results']['types'], **data['results']['indexTypes']}.items(),
                             columns=['SecurityTypeCode','SecurityTypeDesc'])
    return sec_types
#


# Get details for a ticker symbol's company/entity.
# https://polygon.io/docs/get_v1_meta_symbols__stocksTicker__news_anchor
def request_ticker_details(symbol: str, separate_tags: bool = True, separate_similars: bool = True):
    key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)
    url = f"https://api.polygon.io/v1/meta/symbols/{symbol}/company?&apiKey={key}"
    data = request_get_as_json(url=url)
    if data is None:
        return None, None, None
    #
    tags = None
    if 'tags' in data and separate_tags:
        tags = pd.DataFrame(data['tags'], columns=['Tag'],
                            index=pd.Index([symbol]*len(data['tags']), name='Ticker'))
        tags.reset_index(inplace=True)
        data.pop('tags', None)
    #
    similars = None
    if 'similar' in data and separate_similars:
        similars = pd.DataFrame(data['similar'], columns=['Similar'],
                                index=pd.Index([symbol]*len(data['similar']), name='Ticker'))
        similars.reset_index(inplace=True)
        data.pop('similar', None)
    #

    ticker_details = pd.Series(data).to_frame().T
    for col in ['listdate', 'updated']:
        ticker_details[col] = pd.to_datetime(ticker_details[col])
    for col in ['cik','sic','employees']:
        ticker_details[col] = ticker_details[col].astype(int)
    #
    ticker_details['marketcap'] = ticker_details['marketcap'].astype(float)
    ticker_details['active'] = ticker_details['active'].astype(bool)

    return ticker_details, tags, similars
#


# # Get the most recent news articles relating to a stock ticker symbol, including a summary of the article and a link to
# # the original source.
# # https://polygon.io/docs/get_v1_meta_symbols__stocksTicker__news_anchor
# def request_ticker_news(symbol: str, perpage: int = 50, page: int = 0):
#     key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)
#     params = {"apiKey": key}
#     if perpage > 0:
#         params["perpage"] = perpage
#     if page > 0:
#         params["page"] = page
#     url = f"https://api.polygon.io/v1/meta/symbols/{symbol}/news"
#     data = requests.get(url, params=params).json()
#     return pd.Series(data).to_frame().T
# #


# Get a list of markets that are currently supported by Polygon.io.
# https://polygon.io/docs/get_v2_reference_markets_anchor
def request_markets():
    key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)
    url = f"https://api.polygon.io/v2/reference/markets?&apiKey={key}"
    data = request_get_as_json(url=url)
    if data is None:
        return None
    #
    return pd.DataFrame(data['results'])
#


# Get a list of locales currently supported by Polygon.io.
# https://polygon.io/docs/get_v2_reference_locales_anchor
def request_locales():
    key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)
    url = f"https://api.polygon.io/v2/reference/locales?&apiKey={key}"
    data = request_get_as_json(url=url)
    if data is None:
        return None
    #
    return pd.DataFrame(data['results'])
#


# Get a list of historical stock splits for a ticker symbol.
# https://polygon.io/docs/get_v2_reference_splits__stocksTicker__anchor
def request_stock_splits(symbol: str):
    key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)
    url = f"https://api.polygon.io/v2/reference/splits/{symbol}?&apiKey={key}"
    data = request_get_as_json(url=url)
    if data is None:
        return None
    #

    stock_splits = pd.DataFrame(data['results'])
    for col in ['exDate','paymentDate','declaredDate']:
        stock_splits[col] = pd.to_datetime(stock_splits[col])
    #
    return stock_splits
#


# Get a list of historical dividends for a stock, including the relevant dates and the amount of the dividend.
# https://polygon.io/docs/get_v2_reference_dividends__stocksTicker__anchor
def request_stock_dividends(symbol: str):
    key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)
    url = f"https://api.polygon.io/v2/reference/dividends/{symbol}?&apiKey={key}"
    data = request_get_as_json(url=url)
    if data is None:
        return None
    #

    stock_dividends = pd.DataFrame(data['results'])
    for col in ['exDate','paymentDate','recordDate','declaredDate']:
        stock_dividends[col] = pd.to_datetime(stock_dividends[col])
    #
    return stock_dividends
#


# Get historical financial data for a stock ticker.
# https://polygon.io/docs/get_v2_reference_financials__stocksTicker__anchor
def request_stock_financials(symbol: str, limit: int = 5, report_type: str = 'Y', sort_field: str = 'reportPeriod'):
    key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)
    # params = {"apiKey": key}
    params = dict()
    if limit > 0:
        params["limit"] = limit
    if report_type:
        params["type"] = report_type
    if sort_field:
        params["sort"] = sort_field
    url = f"https://api.polygon.io/v2/reference/financials/{symbol}?&apiKey={key}"
    data = request_get_as_json(url=url, params=params)
    if data is None:
        return None
    #

    stock_financials = pd.DataFrame(data['results'])
    for col in ['calendarDate','reportPeriod','updated','dateKey']:
        stock_financials[col] = pd.to_datetime(stock_financials[col])
    #
    return stock_financials
#


# Get upcoming market holidays and their open/close times.
# https://polygon.io/docs/get_v1_marketstatus_upcoming_anchor
def request_upcoming_market_holidays():
    key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)
    url = f"https://api.polygon.io/v1/marketstatus/upcoming?&apiKey={key}"
    data = request_get_as_json(url=url)
    if data is None:
        return None
    #

    market_holidays = pd.DataFrame(data['results'])
    for col in ['date','open','close']:
        if col in market_holidays.columns:
            market_holidays[col] = pd.to_datetime(market_holidays[col])
        #
    #
    return market_holidays
#


# Get the current trading status of the exchanges and overall financial markets.
# https://polygon.io/docs/get_v1_marketstatus_now_anchor
def request_current_market_status():
    key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)
    url = f"https://api.polygon.io/v1/marketstatus/now?&apiKey={key}"
    data = request_get_as_json(url=url)
    if data is None:
        return None
    #

    for section in ['exchanges','currencies']:
        if section in data:
            data.update(data[section])
            data.pop(section, None)
        #
    #
    data['serverTime'] = dtu.parse_datetime(data['serverTime'])
    return pd.Series(data)
#


# Get a list of stock exchanges which are supported by Polygon.io.
# https://polygon.io/docs/get_v1_meta_exchanges_anchor
def request_stock_exchanges():
    key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)
    url = f"https://api.polygon.io/v1/meta/exchanges?&apiKey={key}"
    data = request_get_as_json(url=url)
    if data is None:
        return None
    #

    return pd.DataFrame(data)
#

# Get a unified numerical mapping for conditions on trades and quotes.
# https://polygon.io/docs/get_v1_meta_conditions__ticktype__anchor
def request_tick_condition_mappings(ticktype: str = "trades"):
    key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)
    url = f"https://api.polygon.io/v1/meta/conditions/{ticktype}?&apiKey={key}"
    data = request_get_as_json(url=url)
    if data is None:
        return None
    #

    return data
#


# Get a list of cryptocurrency exchanges which are supported by Polygon.io.
# https://polygon.io/docs/get_v1_meta_crypto-exchanges_anchor
def request_crypto_exchanges():
    key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)
    url = f"https://api.polygon.io/v1/meta/crypto-exchanges?&apiKey={key}"
    data = request_get_as_json(url=url)
    if data is None:
        return None
    #

    return pd.DataFrame(data)
#


##### Belows are the functions to handle looping, concating, etc. #####
def request_tick_conditions(ticktypes: str = 'trades,quotes'):
    ticktypes = mu.iterable_to_tuple(ticktypes, raw_type='str')
    ret = list()
    for ticktype in ticktypes:
        cm = request_tick_condition_mappings(ticktype=ticktype)
        cm = pd.Series(cm).to_frame('Condition')
        cm.index.name = 'ConditionCode'
        cm.reset_index(inplace=True)
        cm['TickType'] = ticktype
        ret.append(cm)
    #
    ret = pd.concat(ret, ignore_index=True, sort=False)

    return ret
#


def _post_process_tickers(tickers):
    drop_cols = ['url']
    if 'codes' in tickers.columns:
        codes = pd.DataFrame([(d if isinstance(d, dict) else dict()) for d in tickers['codes']])
        drop_cols.append('codes')
        tickers = pd.concat([tickers, codes], axis=1, ignore_index=False, sort=False)
    #
    if 'cik' in tickers.columns:
        tickers['cik'] = pd.Series([(int(cik) if isinstance(cik, str) else cik) for cik in tickers['cik']],
                                   dtype='Int64')
    #
    for col in [col for col in ['updated'] if col in tickers.columns]:
        tickers[col] = pd.to_datetime(tickers[col])
    #

    drop_cols = [col for col in ['url'] if col in tickers.columns]
    if len(drop_cols) > 0:
        tickers.drop(columns=drop_cols, inplace=True)
    #

    return tickers
#

def _dump_tickers_on_page(tickers, page_no, output_dir):
    dateid = dtu.today()
    output_file = os.path.join(output_dir, str(dateid), f'tickers.page{page_no:04}.{dateid}.csv')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    tickers.to_csv(output_file, sep=',', index=False)
    logger.info(f'polygon tickers on page {page_no} -> {output_file}')
#


def request_tickers_single_page_v2(page_no, session=None):
    key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)
    data = request_get_as_json(url=f'https://api.polygon.io/v2/reference/tickers?'
                                   f'apiKey={key}&page={page_no}',
                               session=session)
    if data is None:
        logger.warn(f'Skipping Tickers Page {page_no} !')
        return None
    #
    tickers = pd.DataFrame(data['tickers'])
    tickers = _post_process_tickers(tickers=tickers)

    return tickers
#


# Get the list of all supported tickers from Polygon.io
def request_tickers_v2(num_pages=None, output_dir=None):
    url = 'https://api.polygon.io/v2/reference/tickers'
    key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)

    session = requests.Session()
    data = request_get_as_json(url=f'{url}?apiKey={key}&page=1&perPage=1', session=session)
    if data is None:
        return None
    #
    # This is to figure out how many pages to run pagination
    count = data['count']
    if num_pages is None:
        num_pages = math.ceil(count / data['perPage'])
    #
    logger.info(f'Total number of supported tickers is {count} and there are {num_pages} pages to scrape!')

    tickers = list()
    # Pull in all the pages of tickers
    for page_no in range(1, num_pages+1):
        tickers_this_page = request_tickers_single_page_v2(page_no=page_no, session=session)
        if tickers_this_page is None:
            continue
        #
        if output_dir is not None:
            _dump_tickers_on_page(tickers=tickers_this_page, page_no=page_no, output_dir=output_dir)
        #

        tickers.append(tickers_this_page)
        # df.to_csv('data/tickers/{}.csv'.format(page), index=False)
        logger.info(f'Tickers Page {page_no} processed')
    #
    tickers = pd.concat(tickers, sort=False, ignore_index=True)

    return tickers
#


def request_tickers_single_page_v3(cursor=None, session=None):
    key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)
    url = f'https://api.polygon.io/v3/reference/tickers?apiKey={key}&limit=1000'
    if cursor is not None:
        url = f'{url}&{cursor}'
    #
    data = request_get_as_json(url=url, session=session)
    if data is None:
        logger.warn(f'No data for {url} !')
        return None
    #

    tickers = pd.DataFrame(data['results'])
    tickers = _post_process_tickers(tickers=tickers)
    next_url = data.get('next_url', None)

    return tickers, next_url
#


def request_tickers_v3(output_dir=None):
    session = requests.Session()

    tickers = list()
    # Pull in all the pages of tickers
    page_no = 1
    cursor = None
    while True:
        tickers_this_page, next_url = request_tickers_single_page_v3(cursor=cursor, session=session)
        if tickers_this_page is None:
            break
        #
        if output_dir is not None:
            _dump_tickers_on_page(tickers=tickers_this_page, page_no=page_no, output_dir=output_dir)
        #
        tickers.append(tickers_this_page)
        logger.info(f'Tickers Page {page_no} processed')

        if next_url is None:
            break
        #
        cursor = next_url.split('?')[1]
        page_no += 1
    #
    tickers = pd.concat(tickers, sort=False, ignore_index=True)

    return tickers
#


def request_stock_financials_vX(symbol: str, limit: int = 5, report_type: str = 'Y', sort_field: str = 'reportPeriod'):
    key = ecfg.get_env_config().get(ecfg.Prop.POLYGON_KEY)
    # params = {"apiKey": key}
    params = dict()
    if limit > 0:
        params["limit"] = limit
    if report_type:
        params["type"] = report_type
    if sort_field:
        params["sort"] = sort_field
    url = f"https://api.polygon.io/vX/reference/financials/{symbol}?&apiKey={key}"
    data = request_get_as_json(url=url, params=params)
    if data is None:
        return None
    #

    # stock_financials = pd.DataFrame(data['results'])
    # for col in ['calendarDate', 'reportPeriod', 'updated', 'dateKey']:
    #     stock_financials[col] = pd.to_datetime(stock_financials[col])
    # #
    # return stock_financials
    return data
#