import pandas as pd
import gmbp_common.utils.datetime_utils as dtu
import gmbp_common.utils.miscs as mu
from gmbp_common.db.mysql_client import get_mysql_client
import gmbp_quant.dal.sec_master_v0.sec_master as smv0sm
import gmbp_quant.env_config as ecfg


def query_bpp_day_ts(symbols, start_dateid=None, end_dateid=None, cols=None):
    start_dateid, end_dateid = dtu.infer_trading_start_dateid_end_dateid(start_date=start_dateid, end_date=end_dateid)
    where_clauses = list()
    where_clauses.append(f"time_X BETWEEN '{dtu.dateid_to_datestr(start_dateid)}' AND '{dtu.dateid_to_datestr(end_dateid)}'")

    # symbols_where_str = mu.iterable_to_db_str(symbols, raw_type='str')
    sids = smv0sm.get_sids(symbols=symbols)
    if len(sids) > 0:
        where_clauses.append(f"SECURITY_LOOKUP_ID IN {mu.iterable_to_db_str(sids, raw_type='int')}")
    #

    query = f'''
        SELECT * FROM mktdata.bpp_day_ts
        WHERE {' AND '.join(where_clauses)}
    '''

    db_config = ecfg.get_env_config().get_db_config(ecfg.DBProp.DB)
    db_client = get_mysql_client(db_config=db_config)
    if cols is not None:
        cols = list(mu.iterable_to_tuple(cols, raw_type='str'))
    #
    bpp_day_ts = pd.read_sql(sql=query, con=db_client.engine, columns=cols, parse_dates=['time_X'])
    return bpp_day_ts
#


def query_bpp_moving_window_signal(symbols, start_dateid=None, end_dateid=None, cols=None,
                                   from_best_fit_model_only=True):
    start_dateid, end_dateid = dtu.infer_trading_start_dateid_end_dateid(start_date=start_dateid, end_date=end_dateid)
    where_clauses = list()
    where_clauses.append(f"time_X BETWEEN '{dtu.dateid_to_datestr(start_dateid)}' AND '{dtu.dateid_to_datestr(end_dateid)}'")

    # symbols_where_str = mu.iterable_to_db_str(symbols, raw_type='str')
    sids = smv0sm.get_sids(symbols=symbols)
    if len(sids) > 0:
        where_clauses.append(f"SECURITY_LOOKUP_ID IN {mu.iterable_to_db_str(sids, raw_type='int')}")
    #

    if from_best_fit_model_only:
        where_clauses.append(f"isBestFit=1")
    #

    query = f'''
        SELECT * FROM mktdata.bpp_moving_window_signal
        WHERE {' AND '.join(where_clauses)}
    '''

    db_config = ecfg.get_env_config().get_db_config(ecfg.DBProp.DB)
    db_client = get_mysql_client(db_config=db_config)
    if cols is not None:
        cols = list(mu.iterable_to_tuple(cols, raw_type='str'))
    #
    bpp_moving_window_signal = pd.read_sql(sql=query, con=db_client.engine, columns=cols, parse_dates=['time_X'])
    return bpp_moving_window_signal
#


def query_bpp_moving_window_signal_day_snap(symbols=None, cols=None,
                                            from_best_fit_model_only=True,
                                            db_prop='RDS_DB'):
    where_clauses = list()
    if symbols is not None:
        sids = smv0sm.get_sids(symbols=symbols)
        if len(sids) > 0:
            where_clauses.append(f"SECURITY_LOOKUP_ID IN {mu.iterable_to_db_str(sids, raw_type='int')}")
        #
    #

    if from_best_fit_model_only:
        where_clauses.append(f"isBestFit=1")
    #

    if len(where_clauses)>0:
        where_str = f"WHERE {' AND '.join(where_clauses)}"
    #

    query = f'''
        SELECT * FROM mktdata.bpp_moving_window_signal_day_snap
        {where_str}
    '''

    if isinstance(db_prop, str):
        db_prop = ecfg.DBProp[db_prop]
    #
    db_config = ecfg.get_env_config().get_db_config(db_prop=db_prop)
    db_client = get_mysql_client(db_config=db_config)
    if cols is not None:
        cols = list(mu.iterable_to_tuple(cols, raw_type='str'))
    #
    bpp_moving_window_signal = pd.read_sql(sql=query, con=db_client.engine, columns=cols, parse_dates=['time_X'])
    return bpp_moving_window_signal
#
