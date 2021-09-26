import pandas as pd
from gmbp_common.utils.endpoint_utils import request_get_as_json
import gmbp_common.utils.datetime_utils as dtu
from gmbp_quant import env_config as ecfg

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


def request_historical_daily_prices(symbol, start_dateid=19800101, end_dateid='PTD'):
    """
    >>> from gmbp_quant.dpl.fmp.fmp_historical_prices_api import request_historical_daily_prices
    >>> aapl = request_historical_daily_prices('AAPL')
    >>> aapl.head()
            date    open    high     low   close  adjClose      volume  unadjustedVolume  change  changePercent       vwap
    0 2021-07-02  137.90  140.00  137.75  139.96    139.96  79654531.0        79654531.0    2.06          1.494  139.23667
    1 2021-07-01  136.60  137.33  135.76  137.27    137.27  52555353.0        52555353.0    0.67          0.490  136.78667
    2 2021-06-30  136.17  137.40  135.87  136.96    136.96  63362594.0        63362594.0    0.79          0.580  136.74333
    3 2021-06-29  134.80  136.49  134.36  136.33    136.33  65148265.0        65148265.0    1.53          1.135  135.72667
    4 2021-06-28  133.41  135.25  133.39  134.78    134.78  62283199.0        62283199.0    1.37          1.027  134.47333
    """
    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
    url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={key}'

    start_dateid, end_dateid = dtu.infer_start_dateid_end_dateid(start_date=start_dateid, end_date=end_dateid)
    if start_dateid is not None:
        url += f"&from={dtu.dateid_to_datestr(dateid=start_dateid, sep='-')}"
    if end_dateid is not None:
        url += f"&to={dtu.dateid_to_datestr(dateid=end_dateid, sep='-')}"
    #

    data = request_get_as_json(url=url)
    if data is None:
        return None
    #

    try:
        daily = pd.DataFrame(data['historical'])
    except:
        return None
    #
    cols = [col for col in ['label', 'changeOverTime'] if col in daily.columns]
    daily.drop(columns=cols, inplace=True)
    for col in ['date']:
        daily[col] = pd.to_datetime(daily[col])
    #

    return daily
#
