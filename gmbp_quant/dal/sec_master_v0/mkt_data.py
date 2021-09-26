import traceback
import pandas as pd
import gmbp_quant.env_config as ecfg
import gmbp_common.utils.datetime_utils as dtu
from gmbp_common.utils.miscs import iterable_to_db_str, iterable_to_tuple
from gmbp_common.db.mysql_client import get_mysql_client
import gmbp_quant.dal.sec_master_v0.sec_master as smv0sm

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


def query_security_day_price(symbols=None, start_dateid=None, end_dateid=None, cols=None, db_prop='ADS_DB'):
    where_clauses = list()
    if symbols is None:
        if end_dateid is None:
            end_dateid = dtu.today()
            logger.warn(f'"tickers" and "end_dateid" found both None! Set "end_dateid" to be CTD={end_dateid}')
        #
    else:
        # sec_id_ticker = query_security_lookup(symbols=symbols, cols='ID,TICKER')
        sids = smv0sm.get_sids(symbols=symbols)
        where_clauses.append(f"SECURITY_LOOKUP_ID IN {iterable_to_db_str(sids, raw_type='int')}")
    #

    # if start_dateid is not None:
    #     if end_dateid is None:
    #         end_dateid = start_dateid
    #         logger.warn(f'"start_dateid"={start_dateid} but "end_dateid" is None! Set "end_dateid" to be "start_dateid"')
    #     #
    # else:
    #     if end_dateid is not None:
    #         start_dateid, end_dateid = dtu.infer_start_dateid_end_dateid(start_date=start_dateid, end_date=end_dateid,
    #                                                                      date_range_mode='SINGLE_DATE')
    #     #
    # #

    if start_dateid is not None and end_dateid is not None:
        start_dateid, end_dateid = dtu.infer_start_dateid_end_dateid(start_date=start_dateid, end_date=end_dateid,
                                                                     date_range_mode='SINGLE_DATE')
        where_clauses.append(f"time_X BETWEEN '{dtu.dateid_to_datestr(start_dateid)}' AND '{dtu.dateid_to_datestr(end_dateid)}'")
    #

    schema = ecfg.get_env_config().get(ecfg.Prop.SEC_MASTER_V0_SCHEMA, None)
    query = f"""
            SELECT * FROM {schema}.security_day_price
            WHERE {' AND '.join(where_clauses)}
        """
    logger.debug(query)

    try:
        if isinstance(db_prop, str):
            db_prop = ecfg.DBProp[db_prop]
        #
        db_config = ecfg.get_env_config().get_db_config(db_prop=db_prop)
        db_client = get_mysql_client(db_config=db_config)
        if cols is not None:
            cols = list(iterable_to_tuple(cols, raw_type='str'))
        #
        security_day_price = pd.read_sql(sql=query, con=db_client.engine, columns=cols)
    except Exception as e:
        traceback.print_exc()
        security_day_price = None
    #
    return security_day_price
#

