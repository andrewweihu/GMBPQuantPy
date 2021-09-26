import gmbp_quant.env_config as ecfg
from gmbp_common.utils.endpoint_utils import request_get_as_json
import pandas as pd
import numpy as np


from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


def request_financials(symbol):
    key = ecfg.get_env_config().get(ecfg.Prop.GURUFOCUS_TOKEN)
    url = f'https://api.gurufocus.com/public/user/{key}/stock/{symbol}/financials'
    data = request_get_as_json(url=url)
    if data is None:
        return None
    #

    financials = dict()

    for report_type in ['annuals','quarterly']:
        financials[report_type] = dict()
        for financials_type in data['financials'][report_type]:
            if financials_type in ['Fiscal Year','Preliminary']:
                continue
            #
            df = pd.DataFrame(data['financials'][report_type][financials_type],
                              index=data['financials'][report_type]['Fiscal Year'])
            for col in df.columns:
                try:
                    df[col] = df[col].replace(['N/A','-'], np.nan).astype(float)
                except:
                    pass
                #
            #
            df.index.name = 'Period'
            df['IsPreliminary'] = data['financials'][report_type]['Preliminary']
            df['IsPreliminary'] = df['IsPreliminary'].astype(bool)
            financials[report_type][financials_type] = df
        #
    #
    return financials
#
