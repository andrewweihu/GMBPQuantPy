import traceback
import pandas as pd
from gmbp_common.db.mysql_client import get_mysql_client
import gmbp_common.utils.miscs as mu

from gmbp_quant import env_config as ecfg


def query_security_lookup(symbols=None, cols=None, db_prop='ADS_DB'):
    schema = ecfg.get_env_config().get(ecfg.Prop.SEC_MASTER_V0_SCHEMA, None)
    query = f"""
        SELECT * FROM {schema}.security_lookup
    """
    if symbols is not None:
        tickers_db_str = mu.iterable_to_db_str(symbols, raw_type='str')
        query = f'{query} WHERE Ticker IN {tickers_db_str}'
    #

    try:
        if isinstance(db_prop, str):
            db_prop = ecfg.DBProp[db_prop]
        #
        db_config = ecfg.get_env_config().get_db_config(db_prop=db_prop)
        db_client = get_mysql_client(db_config=db_config)
        if cols is not None:
            cols = list(mu.iterable_to_tuple(cols, raw_type='str'))
        #
        security_lookup = pd.read_sql(sql=query, con=db_client.engine, columns=cols)
    except Exception as e:
        traceback.print_exc()
        security_lookup = None
    #
    return security_lookup
#


SYMBOL_2_SID = None
def get_symbol_2_sid():
    global SYMBOL_2_SID
    if SYMBOL_2_SID is None:
        SYMBOL_2_SID = query_security_lookup(cols='ID,TICKER')
        SYMBOL_2_SID = SYMBOL_2_SID.set_index('TICKER')['ID'].to_dict()
    #
    return SYMBOL_2_SID
#


def get_sids(symbols):
    symbol_2_sid = get_symbol_2_sid()
    sids = {symbol_2_sid[symbol] for symbol in mu.iterable_to_tuple(symbols, raw_type='str') if symbol in symbol_2_sid}
    return sids
#
