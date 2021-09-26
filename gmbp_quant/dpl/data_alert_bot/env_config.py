import os, enum
from gmbp_common.env_config import EnvConfig


@enum.unique
class Prop(enum.Enum):
    IB_TWS_HOST = 'ib_tws.host'
    IB_TWS_PORT = 'ib_tws.port'
    IB_TWS_CLIENT_ID = 'ib_tws.client_id'

    AV_API_KEY = 'av.api_key'
    TIINGO_TOKEN = 'tiingo.token'

    BPII_URL = 'bpii.url'
    BPII_KEY = 'bpii.key'

    POLYGON_KEY = 'polygon.key'
    FMP_KEY = 'fmp.key'

    SEC_MASTER_V0_SCHEMA = 'sec_master_v0.schema'

    EQUITY_DAILY_PRICING_SERVICE = 'equity_daily_pricing_svc'

    SLACK_BOT_TOKEN = 'SLACK_BOT_TOKEN'
#


@enum.unique
class DBProp(enum.Enum):
    DB = 'db'
    RDS_DB = 'rds_db'
    ADS_DB = 'ads_db'
#


def get_env_config(env=None, env_config_file=None, **overrides):
    if env_config_file is None:
        env_config_file = os.path.join(os.path.dirname(__file__), 'env_config.cfg')
    #
    EnvConfig.set_env_config_file(env_config_file=env_config_file)

    return EnvConfig.get_instance(env=env, overrides=overrides)
#
