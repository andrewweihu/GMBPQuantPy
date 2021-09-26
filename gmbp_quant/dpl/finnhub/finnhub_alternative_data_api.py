import pandas as pd
import gmbp_quant.dpl.finnhub.finnhub_client as fhc

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


def request_social_sentiment(symbol):
    data = fhc.get_finnhub_client().stock_social_sentiment(symbol=symbol)

    sentiment = list()
    for social in data.keys():
        if social=='symbol':
            continue
        #
        sentiment.append(pd.DataFrame(data[social], index=[social]*len(data[social])))
    #

    return pd.concat(sentiment)
#
