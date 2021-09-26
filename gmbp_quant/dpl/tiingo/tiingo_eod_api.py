import gmbp_quant.env_config as ecfg
import gmbp_common.utils.datetime_utils as dtu
from gmbp_common.utils.endpoint_utils import request_get_as_json
import pandas as pd

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


def request_historical_daily_prices(symbol, start_dateid=19800101, end_dateid='PTD'):
    """
    >>> from gmbp_quant.dpl.tiingo.tiingo_eod_api import request_historical_daily_prices
    >>> aapl = request_historical_daily_prices(symbol='AAPL')
                           date  close   high    low   open   volume  adjClose   adjHigh    adjLow   adjOpen  adjVolume  divCash  splitFactor
    0 1980-12-12 00:00:00+00:00  28.75  28.87  28.75  28.75  2093900  0.101001  0.101423  0.101001  0.101001  469034069      0.0          1.0
    1 1980-12-15 00:00:00+00:00  27.25  27.38  27.25  27.38   785200  0.095732  0.096188  0.095732  0.096188  175884975      0.0          1.0
    2 1980-12-16 00:00:00+00:00  25.25  25.37  25.25  25.37   472000  0.088706  0.089127  0.088706  0.089127  105728105      0.0          1.0
    3 1980-12-17 00:00:00+00:00  25.87  26.00  25.87  25.87   385900  0.090884  0.091340  0.090884  0.090884   86441686      0.0          1.0
    4 1980-12-18 00:00:00+00:00  26.63  26.75  26.63  26.63   327900  0.093554  0.093975  0.093554  0.093554   73449673      0.0          1.0
    """

    token = ecfg.get_env_config().get(ecfg.Prop.TIINGO_TOKEN)
    url = f'https://api.tiingo.com/tiingo/daily/{symbol}/prices?token={token}'

    start_dateid, end_dateid = dtu.infer_start_dateid_end_dateid(start_date=start_dateid, end_date=end_dateid)
    if start_dateid is not None:
        url += f"&startDate={dtu.dateid_to_datestr(dateid=start_dateid, sep='-')}"
    if end_dateid is not None:
        url += f"&endDate={dtu.dateid_to_datestr(dateid=end_dateid, sep='-')}"
    #

    data = request_get_as_json(url=url)
    if data is None:
        return None
    #
    daily = pd.DataFrame(data)
    for col in ['date']:
        daily[col] = pd.to_datetime(daily[col])
    #

    return daily
#
