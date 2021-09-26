import pandas as pd
import gmbp_quant.dpl.finnhub.finnhub_client as fhc

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


def request_stock_symbols(exchange='US'):
    data = fhc.get_finnhub_client().stock_symbols(exchange=exchange)
    if data is None or len(data)==0:
        logger.warn(f'No data found from exchange={exchange} !')
        return None
    #
    data = pd.DataFrame(data)
    inconsistent_symbols = data[data['symbol']!=data['displaySymbol']]
    if len(inconsistent_symbols)==0:
        inconsistent_symbols = None
    else:
        logger.warn(f'Found {len(inconsistent_symbols)} records with inconsistent symbols:\n{inconsistent_symbols.head()}')
    #

    data.drop(columns=['displaySymbol'], inplace=True)
    data.columns = [col.title() for col in data.columns]
    data.rename(columns={'Figi': 'FIGI', 'Mic': 'MIC', 'Type': 'SecurityType'}, inplace=True)

    return data[['FIGI', 'Symbol', 'MIC', 'SecurityType', 'Description', 'Currency']]
#


def request_company_profile(symbol):
    data = fhc.get_finnhub_client().company_profile(symbol=symbol)
    if data is None or len(data)==0:
        logger.warn(f'No data found for symbol={symbol} !')
        return None
    #
    data = pd.DataFrame(data)
    return data
#


def request_news_sentiment(symbol):
    data = fhc.get_finnhub_client().news_sentiment(symbol=symbol)
    if 'sentiment' not in data:
        logger.warn(f'Failed to get data from finnhub for symbol={symbol} !')
        return None
    else:
        data.update(data['sentiment'])
        data.pop('sentiment')
    #
    if 'buzz' in data:
        data.update(data['buzz'])
        data.pop('buzz')
    #

    data = pd.Series(data).to_frame().T
    return data
#


def request_basic_financials(symbol):
    data = fhc.get_finnhub_client().company_basic_financials(symbol=symbol, metric='all')

    metric = None
    if 'metric' in data:
        metric = pd.Series(data['metric']).to_frame().T
    #

    annual_financials = None
    quarterly_financials = None
    if 'series' in data:
        if 'annual' in data['series']:
            financials_list = list()
            for col in data['series']['annual'].keys():
                df = pd.DataFrame(data['series']['annual'][col])
                df.rename(columns={'period':'Date', 'v':col}, inplace=True)
                df.set_index('Date', inplace=True)
                financials_list.append(df)
            #
        #
        annual_financials = pd.concat(financials_list, axis=1, sort=False)
        
        if 'quarterly' in data['series']:
            financials_list = list()
            for col in data['series']['quarterly'].keys():
                df = pd.DataFrame(data['series']['quarterly'][col])
                df.rename(columns={'period': 'Date', 'v': col}, inplace=True)
                df.set_index('Date', inplace=True)
                financials_list.append(df)
            #
        #
        quarterly_financials = pd.concat(financials_list, axis=1, sort=False)
    #

    return metric, annual_financials, quarterly_financials
#
