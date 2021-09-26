import gmbp_quant.env_config as ecfg
from gmbp_common.utils.endpoint_utils import request_get_as_json
import pandas as pd


from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


def request_profile(symbol):
    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
    data = request_get_as_json(url=f'https://financialmodelingprep.com/api/v3/profile/{symbol}?'
                                   f'apikey={key}')
    if data is None:
        return None
    #

    profile = pd.DataFrame(data)
    return profile
#


def request_tradable_symbols():
    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
    data = request_get_as_json(url=f'https://financialmodelingprep.com/api/v3/available-traded/list?'
                                   f'apikey={key}')
    if data is None:
        return None
    #

    profile = pd.DataFrame(data)
    return profile
#


def request_company_outlook(symbol):
    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
    data = request_get_as_json(url=f'https://financialmodelingprep.com/api/v4/company-outlook?'
                                   f'symbol={symbol}&apikey={key}')
    if data is None:
        return None
    #

    if 'profile' in data:
        data['profile'] = pd.Series(data['profile']).to_frame().T
    if 'metrics' in data:
        data['metrics'] = pd.Series(data['metrics']).to_frame().T
    if 'insideTrades' in data:
        insider_trades = pd.DataFrame(data['insideTrades'])
        insider_trades['transactionDate'] = pd.to_datetime(insider_trades['transactionDate'])
        data['insideTrades'] = insider_trades
    if 'keyExecutives' in data:
        data['keyExecutives'] = pd.DataFrame(data['keyExecutives'])
    if 'splitHistory' in data:
        split_history = pd.DataFrame(data['splitHistory'])
        split_history['date'] = pd.to_datetime(split_history['date'])
        data['splitHistory'] = split_history
    if 'stockDividend' in data:
        stock_dividens = pd.DataFrame(data['stockDividend'])
        for col in ['date', 'recordDate', 'paymentDate', 'declarationDate']:
            stock_dividens[col] = pd.to_datetime(stock_dividens[col])
        #
        data['stockDividend'] = stock_dividens
    if 'financialsAnnual' in data:
        income = pd.DataFrame(data['financialsAnnual']['income'])
        balance = pd.DataFrame(data['financialsAnnual']['balance'])
        cash = pd.DataFrame(data['financialsAnnual']['cash'])

        for df in [income, balance, cash]:
            for col in ['date', 'fillingDate', 'acceptedDate']:
                df[col] = pd.to_datetime(df[col])
            #
        #
        data['incomeAnnual'] = income
        data['balanceAnnual'] = balance
        data['cashAnnual'] = cash
    if 'financialsQuarter' in data:
        income = pd.DataFrame(data['financialsQuarter']['income'])
        balance = pd.DataFrame(data['financialsQuarter']['balance'])
        cash = pd.DataFrame(data['financialsQuarter']['cash'])

        for df in [income, balance, cash]:
            for col in ['date', 'fillingDate', 'acceptedDate']:
                df[col] = pd.to_datetime(df[col])
            #
        #
        data['incomeQuarter'] = income
        data['balanceQuarter'] = balance
        data['cashQuarter'] = cash
    #

    return data
#


def request_symbols_list_v3():
    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
    data = request_get_as_json(url=f'https://financialmodelingprep.com/api/v3/stock/list?apikey={key}')
    if data is None:
        return None
    #

    return pd.DataFrame(data)
#


def request_tradable_symbols_list_v3():
    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
    data = request_get_as_json(url=f'https://financialmodelingprep.com/api/v3/available-traded/list?apikey={key}')
    if data is None:
        return None
    #

    return pd.DataFrame(data)
#


def request_etf_list_v3():
    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
    data = request_get_as_json(url=f'https://financialmodelingprep.com/api/v3/etf/list?apikey={key}')
    if data is None:
        return None
    #

    return pd.DataFrame(data)
#


def request_symbols_v3():
    symbols = request_symbols_list_v3()
    tradable_symbols = request_tradable_symbols()
    etf_symbols = request_etf_list_v3()

    symbols = pd.concat([symbols, tradable_symbols, etf_symbols], sort=False)
    symbols.drop(columns=['price', ], inplace=True)
    symbols.drop_duplicates(keep='first', inplace=True)
    return symbols
#


def request_financial_statements(symbol, statement_type, period='quarter'):
    if statement_type.lower()=='income':
        statement_type = 'income-statement'
    elif statement_type.lower()=='balance':
        statement_type = 'balance-sheet-statement'
    elif statement_type.lower()=='cash':
        statement_type = 'cash-flow-statement'
    else:
        raise Exception(f"statement_type={statement_type} not in supported [income|balance|cash]")
    #

    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
    url = f'https://financialmodelingprep.com/api/v3/{statement_type}/{symbol}?apikey={key}'
    if period.lower()=='quarter':
        url = f'{url}&period={period}'
    #
    data = request_get_as_json(url=url)
    if data is None:
        return None
    #

    ret = pd.DataFrame(data)
    if len(ret)==0:
        return None
    #

    for col in [col for col in ['date', 'fillingDate', 'acceptedDate'] if col in ret.columns]:
        ret[col] = pd.to_datetime(ret[col])
    #

    return ret
#


def request_financial_ratios(symbol, period='quarter'):
    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
    period = period.lower()
    if period=='ttm':
        period_type = 'ratios-ttm'
    elif period in ['quarter','annual']:
        period_type = 'ratios'
    else:
        raise Exception(f"period={period} is not supported in [ttm|quarter]")
    #

    url = f'https://financialmodelingprep.com/api/v3/{period_type}/{symbol}?apikey={key}&limit=1000'
    if period in ['quarter','annual']:
        url = f'{url}&period={period}'
    #
    data = request_get_as_json(url=url)
    if data is None:
        return None
    #

    ret = pd.DataFrame(data)
    if len(ret)==0:
        return None
    #

    ret['date'] = pd.to_datetime(ret['date'])
    ret['dividendPaidAndCapexCoverageRatio'] = ret['dividendPaidAndCapexCoverageRatio'].astype(float)
    for col in ['dividendPayoutRatio','dividendYield']:
        ret[col] = ret[col].astype(float)
    #

    return ret
#


def request_enterprise_value(symbol, period='quarter'):
    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
    url = f'https://financialmodelingprep.com/api/v3/enterprise-values/{symbol}?apikey={key}&limit=1000'
    if period.lower()=='quarter':
        url = f'{url}&period={period}'
    #
    data = request_get_as_json(url=url)
    if data is None:
        return None
    #

    ret = pd.DataFrame(data)
    if len(ret)==0:
        return None
    #

    ret['date'] = pd.to_datetime(ret['date'])
    for col in ['minusCashAndCashEquivalents']:
        ret[col] = ret[col].astype(float)
    #

    return ret
#


def request_key_metrics(symbol, period='quarter'):
    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
    period = period.lower()
    if period=='ttm':
        period_type = 'key-metrics-ttm'
    elif period in ['quarter','annual']:
        period_type = 'key-metrics'
    else:
        raise Exception(f"period={period} is not supported in [ttm|quarter]")
    #

    url = f'https://financialmodelingprep.com/api/v3/{period_type}/{symbol}?apikey={key}&limit=1000'
    if period in ['quarter','annual']:
        url = f'{url}&period={period}'
    #
    data = request_get_as_json(url=url)
    if data is None:
        return None
    #

    ret = pd.DataFrame(data)
    if len(ret)==0:
        return None
    #

    ret['date'] = pd.to_datetime(ret['date'])
    for col in ['workingCapital','netCurrentAssetValue','averageReceivables','averagePayables','averageInventory']:
        ret[col] = ret[col].astype(float)
    #

    return ret
#


def request_financial_growth(symbol, period='quarter'):
    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
    url = f'https://financialmodelingprep.com/api/v3/financial-growth/{symbol}?apikey={key}&limit=1000'
    if period.lower()=='quarter':
        url = f'{url}&period={period}'
    #
    data = request_get_as_json(url=url)
    if data is None:
        return None
    #

    ret = pd.DataFrame(data)
    if len(ret)==0:
        return None
    #

    ret['date'] = pd.to_datetime(ret['date'])
    return ret
#


def request_rating_historical(symbol):
    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
    url = f'https://financialmodelingprep.com/api/v3/historical-rating/{symbol}?apikey={key}'
    data = request_get_as_json(url=url)
    if data is None:
        return None
    #

    ret = pd.DataFrame(data)
    if len(ret)==0:
        return None
    #

    ret['date'] = pd.to_datetime(ret['date'])
    return ret
#


def request_dcf_historical(symbol):
    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
    url = f'https://financialmodelingprep.com/api/v3/historical-daily-discounted-cash-flow/{symbol}?apikey={key}'
    data = request_get_as_json(url=url)
    if data is None:
        return None
    #

    ret = pd.DataFrame(data)
    if len(ret)==0:
        return None
    #

    ret['date'] = pd.to_datetime(ret['date'])
    return ret
#


def request_mktcap_historical(symbol):
    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
    url = f'https://financialmodelingprep.com/api/v3/historical-market-capitalization/{symbol}?apikey={key}'
    data = request_get_as_json(url=url)
    if data is None:
        return None
    #

    ret = pd.DataFrame(data)
    if len(ret)==0:
        return None
    #

    ret['date'] = pd.to_datetime(ret['date'])
    return ret
#


def request_balance_sheet(symbol, period='annual'):
    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
    url = f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{symbol}?apikey={key}'
    if period=='quarter':
        url += '&period=quarter'
    #
    data = request_get_as_json(url=url)
    if data is None:
        return None
    #

    ret = pd.DataFrame(data)
    if len(ret)==0:
        return None
    #

    for col in ['date','fillingDate','acceptedDate']:
        ret[col] = pd.to_datetime(ret[col])
    #
    return ret
#
