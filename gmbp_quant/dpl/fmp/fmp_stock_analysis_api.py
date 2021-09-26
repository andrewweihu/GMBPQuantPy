import gmbp_quant.env_config as ecfg
from gmbp_common.utils.endpoint_utils import request_get_as_json
import pandas as pd

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


def request_stock_grade(symbol, limit: int = 500):
    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
    data = request_get_as_json(url=f'https://financialmodelingprep.com/api/v3/grade/{symbol}?'
                                   f'limit={limit}&apikey={key}')
    if data is None:
        return None
    #
    return pd.DataFrame(data)
#