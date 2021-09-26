from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import gmbp_quant.dal.mkt_data as dalmd
import gmbp_common.utils.datetime_utils as dtu
import gmbp_common.utils.miscs as mu
import gmbp_quant.dal.sec_master as dalsm
from gmbp_quant.mdpalgo.mdp_algo import max_div_portf, calculate_portfolio_var
import gmbp_quant.dal.bpp as dalbpp

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


def calc_cov_mat_from_adj_closes(adj_closes):
    start_date = adj_closes.index.min()
    end_date = adj_closes.index.max()
    logger.info(f'ADJ_CLOSE for {len(adj_closes)} dates @ start_date={start_date}, end_date={end_date}')

    returns = adj_closes.pct_change()
    returns.dropna(inplace=True)
    logger.info(f'{len(returns)} dates left in returns after NA dropped')

    cov_mat = returns.cov()

    return cov_mat
#


def calc_cov_mat(tickers, start_dateid=None, end_dateid=None,
                 adj_closes_data_source='SMV0'):
    if end_dateid is None:
        end_dateid = dtu.prev_biz_dateid(dateid=dtu.today())
    #
    if start_dateid is None:
        start_date = dtu.dateid_to_datetime(end_dateid) + relativedelta(years=-2)
        start_dateid = dtu.datetime_to_dateid(date=start_date)
        start_dateid = dtu.next_biz_dateid(dateid=start_dateid)
    #
    adj_closes = dalmd.query_adj_closes(symbols=tickers, start_dateid=start_dateid, end_dateid=end_dateid,
                                        data_source=adj_closes_data_source)

    cov_mat = calc_cov_mat_from_adj_closes(adj_closes=adj_closes)

    return cov_mat
#


def filter_tickers(tickers, filters=None):
    all_supported_tickers = dalsm.get_all_tickers()
    tickers = set(mu.iterable_to_tuple(tickers, raw_type='str'))
    unsupported_tickers = tickers.difference(all_supported_tickers)
    if len(unsupported_tickers)>0:
        logger.info(f"Unsupported: {unsupported_tickers}")
    #
    tickers = tickers.intersection(all_supported_tickers)

    if len(tickers)==0:
        return None
    #

    if filters is not None:
        filters = list(mu.iterable_to_tuple(filters, raw_type='str'))
    #
    for filter in filters:
        if isinstance(filter, str):
            if filter=='BPP_UP':
                bpp = dalbpp.query_bpp_moving_window_signal_day_snap(symbols=tickers, cols='TICKER,TIME_X,Is_SetUp')
                bpp_down = bpp[bpp['Is_SetUp']==0]
                if len(bpp_down)>0:
                    logger.info(f"BPP_DOWN: {set(bpp_down['TICKER'])}")
                #
                tickers = set(bpp[bpp['Is_SetUp']==1]['TICKER'])
            #
        else:
            tickers = filter(tickers)
        #
    #

    if tickers is None or len(tickers)==0:
        return None
    #

    return tickers
#


def calc_most_diversified_portfolio(tickers, cov_mat=None,
                                    ticker_filters=None,
                                    equal_weights_divergence_penalty=3):
    if ticker_filters is not None:
        tickers = filter_tickers(tickers=tickers, filters=ticker_filters)
    else:
        tickers = list(mu.iterable_to_tuple(tickers, raw_type='str'))
    #

    if tickers is None or len(tickers)==0:
        msg = f"There are no valid tickers after ticker_filters={ticker_filters}"
        logger.warn(msg)
        return {'Weights': None, 'Volatility': np.nan, 'Msg': msg}
    #

    if cov_mat is None:
        cov_mat = calc_cov_mat(tickers=tickers)
    #

    common_symbols = list()
    common_cov_mat_tickers = list()
    cov_mat_tickers = {ticker.split('.')[0]: ticker for ticker in cov_mat.columns}
    for symbol in tickers:
        if symbol in cov_mat_tickers:
            common_symbols.append(symbol)
            common_cov_mat_tickers.append(cov_mat_tickers[symbol])
        #
    #

    if len(common_symbols)==0:
        msg = f'Skipping since there are no overlapping between "tickers" and "cov_mat.columns"'
        logger.warn(msg)
        return {'Weights': None, 'Volatility': np.nan, 'Msg': msg}
    #

    cov_mat = cov_mat.loc[common_cov_mat_tickers][common_cov_mat_tickers]

    w0 = [1 / len(common_symbols)] * len(common_symbols)
    weights = max_div_portf(w0=w0, v=cov_mat.values, lmd=equal_weights_divergence_penalty)
    return {'Weights': pd.DataFrame({'Weight': weights}, index=common_symbols),
            'Volatility': np.sqrt(calculate_portfolio_var(w=weights, cov_mat=cov_mat)),
            'Msg': 'Success'}
#


