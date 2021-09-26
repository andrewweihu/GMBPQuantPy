import gmbp_quant.env_config as ecfg
from gmbp_common.utils.endpoint_utils import request_get_as_json
import pandas as pd

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


def get_top_holders(df, num_holders=10):
    df = df.sort_values('shares', ascending=False)
    df = df.head(num_holders)
    df.index = [f'R{i}' for i in range(min(num_holders,len(df)))]
    df.index.name = 'Rank'
    df['shares'] /= 1e6
    df['change'] /= 1e6
    df.drop(columns=['dateReported'], inplace=True)
    return df.T
#


def request_institutional_holders(symbol):
    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
    data = request_get_as_json(url=f'https://financialmodelingprep.com/api/v3/institutional-holder/{symbol}?'
                                   f'apikey={key}')
    if data is None:
        return None
    #
    return pd.DataFrame(data)
#


def request_mutual_fund_holders(symbol):
    key = ecfg.get_env_config().get(ecfg.Prop.FMP_KEY)
    data = request_get_as_json(url=f'https://financialmodelingprep.com/api/v3/mutual-fund-holder/{symbol}?'
                                   f'apikey={key}')
    if data is None:
        return None
    #
    return pd.DataFrame(data)
#
