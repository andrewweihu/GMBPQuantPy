import pytz
from datetime import datetime, timedelta
import gmbp_quant.env_config as ecfg
import gmbp_common.utils.datetime_utils as dtu
from gmbp_common.db.mysql_client import get_mysql_client
import pandas as pd


# def query_bpii(start_dt, end_dt, timezone='America/New_York'):
#     start_dt = dtu.parse_datetime(dt=start_dt)
#     if start_dt.hour == 0 and start_dt.minute == 0 and start_dt.second == 0:
#         start_dt = start_dt.replace(second=1)
#     #
#     end_dt = dtu.parse_datetime(dt=end_dt)
#     if end_dt.hour == 0 and end_dt.minute == 0 and end_dt.second == 0:
#         end_dt = end_dt.replace(hour=23, minute=59, second=59)
#     #
#
#     query = f'''
#         SELECT * FROM quant.bpii
#         WHERE Signal_Time BETWEEN '{start_dt.strftime('%Y-%m-%d %H:%M:%S')}' AND '{end_dt.strftime('%Y-%m-%d %H:%M:%S')}'
#     '''
#
#     db_config = ecfg.get_env_config().get_db_config(ecfg.DBProp.DB)
#     db_client = get_mysql_client(db_config=db_config)
#     bpii = pd.read_sql(sql=query, con=db_client.engine, parse_dates=['Signal_Time'])
#     bpii['Signal_Time'] = bpii['Signal_Time'].dt.tz_localize(pytz.timezone(timezone))
#     return bpii
# #

def query_bpii_realtime(top_cnt=1):
    TZ_NY = pytz.timezone('America/New_York')
    now = datetime.now(TZ_NY)

    # query = f'''
    #     SELECT * FROM bpii.bpii_us_realtime_grandtotal
    #     # WHERE time_x BETWEEN '{(now-timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S')}' AND '{now.strftime('%Y-%m-%d %H:%M:%S')}'
    # '''

    query = f'''
        SELECT * FROM bpii.bpii_us_realtime_grandtotal
        ORDER BY time_X DESC LIMIT {top_cnt};
    '''

    db_config = ecfg.get_env_config().get_db_config(ecfg.DBProp.DB)
    db_client = get_mysql_client(db_config=db_config)
    bpii = pd.read_sql(sql=query, con=db_client.engine, parse_dates=['time_x'])
    bpii['time_x'] = bpii['time_x'].dt.tz_localize(TZ_NY)

    return bpii.head(1)
#
