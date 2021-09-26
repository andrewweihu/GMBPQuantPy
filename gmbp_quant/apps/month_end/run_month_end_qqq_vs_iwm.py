import sys
import pandas as pd
import pandas_datareader.data as web
from pandas.tseries.offsets import MonthEnd
import gmbp_common.utils.datetime_utils as dtu

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


def infer_dates(num_days_till_me):
    dateid = dtu.today()
    month_end = dtu.dateid_to_datetime(dateid) + MonthEnd(1)
    if not dtu.is_trading_session(date=month_end):
        month_end_dateid = dtu.datetime_to_dateid(date=month_end)
        month_end_dateid = dtu.prev_trading_dateid(dateid=month_end_dateid)
    else:
        month_end_dateid = dtu.datetime_to_dateid(date=month_end)
    #

    num_days_offset = int(num_days_till_me) + 2
    start_dateid = dtu.shift_trading_dates(dateid=month_end_dateid, offset_days=-num_days_offset)

    return dateid, start_dateid, month_end_dateid
#


def get_returns(symbol, start_dateid, end_dateid):
    data = web.DataReader(symbol, 'yahoo',
                          start=dtu.dateid_to_datestr(dateid=start_dateid, sep='-'),
                          end=dtu.dateid_to_datestr(dateid=end_dateid, sep='-'))
    data.rename(columns={'Adj Close': 'AdjClose'}, inplace=True)
    data['Return'] = data['AdjClose'].pct_change()

    return data
#


def infer_me_signals(start_dateid, month_end_dateid):
    qqq = get_returns(symbol='QQQ', start_dateid=start_dateid, end_dateid=month_end_dateid)
    iwm = get_returns(symbol='IWM', start_dateid=start_dateid, end_dateid=month_end_dateid)
    logger.info('QQQ and IWM data loaded .')

    me_signals = pd.merge(qqq[['AdjClose', 'Return']], iwm[['AdjClose', 'Return']],
                          left_index=True, right_index=True, suffixes=('.QQQ', '.IWM'))
    me_signals['Return.{QQQ-IWM}'] = me_signals['Return.QQQ'] - me_signals['Return.IWM']
    me_signals['D(Return.{QQQ-IWM})'] = me_signals['Return.{QQQ-IWM}'].diff()
    for col in me_signals.columns:
        if 'Return' in col:
            me_signals[col] *= 100.0
        #
    #
    me_signals['IWMStrongerPTD'] = (me_signals['Return.{QQQ-IWM}'] < 0).shift().astype(bool)
    me_signals.columns = [col + '%' if 'Return' in col else col for col in me_signals.columns]
    me_signals['Signal'] = ((me_signals['IWMStrongerPTD']) & (me_signals['D(Return.{QQQ-IWM})%'] > 0)).astype(bool)

    dates = dtu.infer_trading_dateids(start_dateid=start_dateid, end_dateid=month_end_dateid)
    dates = pd.to_datetime(dates, format='%Y%m%d')
    missing_dates = [date for date in dates if date not in me_signals.index]
    if len(missing_dates) > 0:
        me_signals = pd.concat([me_signals, pd.DataFrame(index=missing_dates)])
    #

    me_signals['DaysTillME'] = range(-(len(me_signals)-1), 1)
    me_signals.fillna('', inplace=True)

    return me_signals
#


def setup_cli_options(parser=None):
    if parser is None:
        from optparse import OptionParser, IndentedHelpFormatter
        parser = OptionParser(formatter=IndentedHelpFormatter(width=200), epilog='\n')
    #

    parser.add_option('-n', '--num_days_till_me',
                      dest='num_days_till_me', default=5,
                      help=f'Default: %default .')

    return parser
#


if __name__ == '__main__':
    logger.info(' '.join(sys.argv))

    options, args = setup_cli_options().parse_args()

    dateid, start_dateid, month_end_dateid = infer_dates(num_days_till_me=options.num_days_till_me)

    if dateid <= start_dateid:
        logger.warn(f'Skipping since today({dateid})<=start_date({start_dateid}), far from month_end({month_end_dateid}) !')
        exit(0)
    #

    logger.info(f'===== [START] today({dateid})>start_date({start_dateid}) close to month_end({month_end_dateid}) =====')

    me_signals = infer_me_signals(start_dateid=start_dateid, month_end_dateid=month_end_dateid)

    logger.info(f'\n{me_signals}')

    logger.info('===== [END] =====')
#
