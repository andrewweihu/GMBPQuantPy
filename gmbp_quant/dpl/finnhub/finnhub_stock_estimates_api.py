import pandas as pd
import gmbp_quant.dpl.finnhub.finnhub_client as fhc

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


def request_recommendation_trends(symbol):
    data = fhc.get_finnhub_client().recommendation_trends(symbol=symbol)

    data = pd.DataFrame(data)
    data.drop(columns='symbol', inplace=True)
    data.rename(columns={'period':'Date'}, inplace=True)

    return data[['Date', 'strongBuy', 'buy', 'hold', 'sell', 'strongSell']]
#


def request_price_target(symbol): # Premium Required
    data = fhc.get_finnhub_client().price_target(symbol=symbol)

    return pd.Series(data).to_frame().T
#
