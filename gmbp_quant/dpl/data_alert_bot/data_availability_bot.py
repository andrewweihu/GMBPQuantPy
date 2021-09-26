import datetime as dt
import os
import sys
import yaml
import slack_bot
import schedule, time

import env_config as ecfg
# import gmbp_quant.env_config as ecfg
from gmbp_common.db.db_client import DBClient
from sqlalchemy.orm import sessionmaker

# workaround of not finding GMBPQuantPy path. To Be fixed.
# sys.path.insert(0, r'C:\Users\Vince\OneDrive\Documents\Python\GitHub\GMBPQuantPy')


def run_date_check():
    """Run check latest date, write the result with slack bot."""
    # Load table list from forms_to_check.yml file
    yaml_file = 'forms_to_check.yml'
    with open(os.path.join(sys.path[0], yaml_file)) as f:
        sec_yml = yaml.load(f, Loader=yaml.FullLoader)

    prefix = 'Data availability check {today}\n'.format(today=dt.datetime.now().strftime('%Y-%m-%d, %H:%M:%S'))
    prefix += '(schema.table, last update)\n'
    msgs = ''

    # check the latest date from each table, raise alert and record number of days last data is available.
    for form, attr in sec_yml.items():
        alert, num_days = CheckDate(schema=attr['schema'],
                                    table=attr['table'],
                                    dt_col=attr['dt_col']).check_days_delta(attr['days'])

        # Slack bot raises alert if data available date not recent.
        if alert == 1:
            msgs += '{table},  {num}-day ago\n'.format(
                num=num_days, table=attr['schema'] + '.' + attr['table'])

    if not msgs:
        msgs = 'Data availability check passed!'

    # send to slack channel
    slack_bot.text_bot(msg=prefix + msgs)


def get_conn_to_database():
    """Return connection (conn) to the database, for conn.execute(sql)"""
    db_config = ecfg.get_env_config().get_db_config(ecfg.DBProp.DB)
    db_client = DBClient(db_config=db_config, client_type='mysql')

    return db_client.engine


def get_raw_conn_to_database():
    """Return raw connection (conn) to the database, for pd.read_sql(sql, conn)."""
    db_config = ecfg.get_env_config().get_db_config(ecfg.DBProp.DB)
    db_client = DBClient(db_config=db_config, client_type='mysql')

    db_session = sessionmaker(bind=db_client.engine)
    sess = db_session()

    return sess.bind.raw_connection()


class CheckDate:
    """
    Check data availability by its report date. Report anomaly when data is unavailable.
    Including: bpii
    """
    def __init__(self, schema, table, dt_col):

        self.schema = schema
        self.table = table
        self.dt_col = dt_col

    def get_latest_date(self):
        """Return latest datetime object that data is acquired"""

        conn = get_conn_to_database()
        sql = """SELECT max({dt}) FROM {schema}.{table}""".format(
            dt=self.dt_col, schema=self.schema, table=self.table)

        latest_date = conn.execute(sql).fetchall()[0][0]

        if isinstance(latest_date, dt.datetime):
            return latest_date.date()
        elif isinstance(latest_date, dt.date):
            return latest_date
        else:
            raise TypeError('Column specified is not datetime or date object')

    def check_days_delta(self, days=1):
        """Return missing data alert (1/0) and number of days between today and last data reported date"""

        num_days = (dt.date.today() - self.get_latest_date()).days
        # number of days between today and last data reported
        alert = 1 if num_days > days else 0
        return alert, num_days



if __name__ == '__main__':
    run_date_check()
    # scheduler
    # #schedule.every(60).seconds.do(run_date_check)
    #schedule.every().day.at("07:00").do(run_date_check)
    #
    # while True:
    #     print('Running...{}'.format(dt.datetime.now()))
    #     schedule.run_pending()
    #     time.sleep(60)
