import pandas as pd
import gmbp_quant.dpl.finnhub.finnhub_client as fhc

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


def request_etfs_profile(symbol):
    data = fhc.get_finnhub_client().etfs_profile(symbol=symbol)

    return pd.Series(data['profile']).to_frame().T
#
