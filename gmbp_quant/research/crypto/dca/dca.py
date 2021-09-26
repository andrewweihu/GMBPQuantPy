import os
import pandas as pd
from gmbp_quant.dpl.fmp.fmp_historical_prices_api import request_historical_daily_prices

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


def get_historical_prices(symbol, data_source=None):
    if data_source=='FMP':
        historical_prices = request_historical_daily_prices(symbol=symbol)
    else:
        if data_source is None:
            data_source = os.path.join(os.path.abspath(os.path.dirname(__file__)), f'{symbol}.daily.csv')
        #
        historical_prices = pd.read_csv(data_source, sep=',', parse_dates=['date'])
        logger.info(f'{symbol} historical prices with shape {historical_prices.shape} loaded from {data_source}')
    #

    historical_prices.sort_values('date', ascending=True, inplace=True)
    return historical_prices
#


def calc_bias(daily_prices, ma_ndays, di_stats_ndays=None,
              close_price_col='adjClose'):
    daily_prices = daily_prices.copy()
    daily_prices['ma'] = daily_prices[close_price_col].rolling(ma_ndays, min_periods=1).mean()
    daily_prices['bias'] = (daily_prices[close_price_col] - daily_prices['ma']) / daily_prices['ma']

    if di_stats_ndays is not None:
        daily_prices['bias_mean'] = daily_prices['bias'].rolling(di_stats_ndays, min_periods=1).mean()
        daily_prices['bias_std'] = daily_prices['bias'].rolling(di_stats_ndays, min_periods=1).std()
        daily_prices['di'] = (daily_prices['bias']-daily_prices['bias_mean']) / daily_prices['bias_std']
    #

    return daily_prices
#


def calc_dca(symbol=None, historical_prices=None, config=None, drop_irrelevant_cols=True):
    if config is None:
        config = dict()
    #

    if historical_prices is None:
        if symbol is None:
            raise Exception(f'Please provide either "symbol" or "historical_prices" !')
        #
        data_source = config.get('data_source', 'FMP')
        dca = get_historical_prices(symbol=symbol, data_source=data_source)
    else:
        dca = historical_prices.copy()
    #
    close_price_col = 'adjClose'

    # start date
    dca['day_of_week'] = dca['date'].dt.dayofweek

    # moving average
    ma_ndays = config.get('ma_ndays', 365)
    di_stats_ndays = config.get('di_stats_ndays', 365)
    dca = calc_bias(daily_prices=dca, ma_ndays=ma_ndays, di_stats_ndays=di_stats_ndays,
                    close_price_col=close_price_col)

    # start_date and end_date
    start_dateid = config.get('start_dateid', 20171215)
    dca = dca[dca['date'] >= pd.to_datetime(str(start_dateid))]
    end_dateid = config.get('end_dateid', None)
    if end_dateid is not None:
        dca = dca[dca['date'] <= pd.to_datetime(str(end_dateid))]
    #

    strategy = config.get('strategy', 'BIAS_GRID_EQUAL_SIZE')
    allow_sell = config.get('allow_sell', True)
    if strategy=='FIXED_AMOUNT':
        dca['investment_ratio'] = 1.0
        allow_sell = False
    elif strategy=='BIAS_GRID_EQUAL_SIZE':
        grid_interval = config.get('grid_interval', 0.1)
        investment_ratio_interval = config.get('investment_ratio_interval', 0.1)
        ngrids = config.get('ngrids', 6)
        # DI Up handling
        for i in range(ngrids-1):
            dca.loc[(dca['bias'] >= i*grid_interval) & (dca['bias'] < (i+1) * grid_interval), 'investment_ratio'] = 1 - (i+1) * investment_ratio_interval
            dca.loc[(dca['bias'] >= -(i+1)*grid_interval) & (dca['bias'] < -i*grid_interval), 'investment_ratio'] = 1 + (i+1) * investment_ratio_interval
        #
        dca.loc[(dca['bias'] >= (ngrids-1) * grid_interval), 'investment_ratio'] = 1 - ngrids * investment_ratio_interval
        dca.loc[(dca['bias'] < -(ngrids-1) * grid_interval), 'investment_ratio'] = 1 + ngrids * investment_ratio_interval

        if not allow_sell:
            dca.loc[(dca['investment_ratio'] < 0), 'investment_ratio'] = 0
        #
    #

    dca_day_of_week = config.get('dca_day_of_week', 0)
    dca_base_amount = config.get('dca_base_amount', 100.0)
    dca.loc[(dca['day_of_week'] == dca_day_of_week), 'amount'] = dca['investment_ratio'] * dca_base_amount

    markup_ratio = config.get('markup_ratio', 0.15/100)
    dca['sided_qty'] = dca['amount'] / (dca[close_price_col] * (1 + markup_ratio))
    dca['cum_sided_qty'] = dca['sided_qty'].cumsum()
    dca.reset_index(drop=True, inplace=True)

    if allow_sell:
        for i in range(len(dca)):
            if dca['cum_sided_qty'][i] < 0:
                dca.loc[i, 'cum_sided_qty'] = 0
                dca.loc[i, 'amount'] = 0
                dca.loc[i, 'sided_qty'] = 0
                if i != 0:
                    dca.loc[i, 'sided_qty'] = -dca['cum_sided_qty'][i-1]
                    dca.loc[i, 'amount'] = dca['sided_qty'][i] * dca[close_price_col][i] * (1 + markup_ratio)
                #
            #
        #
    #

    dca['nmv'] = dca['cum_sided_qty'] * dca[close_price_col]
    dca['cum_amount'] = dca['amount'].cumsum()

    dca['investment_gain_ratio'] = dca['nmv'] / dca['cum_amount']

    dca['ttm'] = [*range(len(dca)-1, -1, -1)]
    growth_rate = config.get('growth_rate', 0.08)
    r = pow(1+growth_rate, 1/365)-1
    dca['fv'] = dca['amount']*[pow(1+r, ttm) for ttm in dca['ttm']]
    dca['cum_fv'] = dca['fv'].cumsum()

    if drop_irrelevant_cols:
        cols = ['open','high','low','close','volume','unadjustedVolume','change','changePercent','vwap']
        cols = [col for col in cols if col in dca.columns]
        dca = dca.drop(columns=cols)
    #

    return dca
#
