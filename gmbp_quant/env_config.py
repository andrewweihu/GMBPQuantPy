import os, enum
from gmbp_common.env_config import EnvConfig

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


@enum.unique
class Prop(enum.Enum):
    AV_API_KEY = 'av.api_key'
    TIINGO_TOKEN = 'tiingo.token'

    BPII_URL = 'bpii.url'
    BPII_KEY = 'bpii.key'

    POLYGON_KEY = 'polygon.key'
    FMP_KEY = 'fmp.key'
    FINNHUB_TOKEN = 'finnhub.token'
    FINNHUB_API_KEY = 'finnhub.api_key'
    GURUFOCUS_TOKEN = 'gurufocus.token'

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

# @enum.unique
# class CredentialProp(enum.Enum):
#     IB_TWS = 'ib_tws'
# #
#
# @enum.unique
# class ConnectionProp(enum.Enum):
#     IB_TWS = 'ib_tws'
#


def get_env_config(env=None, env_config_file=None, **overrides):
    if env_config_file is None:
        env_config_file = os.path.join(os.path.dirname(__file__), 'env_config.cfg')
    #
    EnvConfig.set_env_config_file(env_config_file=env_config_file)

    return EnvConfig.get_instance(env=env, overrides=overrides)
#
