import gmbp_quant.env_config as ecfg

import finnhub

FINNHUB_CLIENT = None

def get_finnhub_client():
    global FINNHUB_CLIENT
    if FINNHUB_CLIENT is None:
        api_key = ecfg.get_env_config().get(ecfg.Prop.FINNHUB_API_KEY)
        FINNHUB_CLIENT = finnhub.Client(api_key=api_key)
    #
    return FINNHUB_CLIENT
#
