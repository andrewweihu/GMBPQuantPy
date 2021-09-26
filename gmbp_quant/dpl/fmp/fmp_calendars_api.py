import gmbp_quant.env_config as ecfg
from gmbp_common.utils.endpoint_utils import request_get_as_json
import pandas as pd

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


def request_historical_earnings_calendar(symbol, limit: int=80):
    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
    data = request_get_as_json(url=f'https://financialmodelingprep.com/api/v3/historical/earning_calendar/{symbol}?'
                                   f'limit={limit}&apikey={key}')
    if data is None:
        return None
    #
    return pd.DataFrame(data)
#


def request_earnings_calendar(start_dateid=None, end_dateid=None):
    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
    data = request_get_as_json(url=f'https://financialmodelingprep.com/api/v3/earning_calendar?'
                                   f'apikey={key}')
    if data is None:
        return None
    #
    return pd.DataFrame(data)
#
