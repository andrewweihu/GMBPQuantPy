import os
import pandas as pd
from joblib import Parallel, delayed
import gmbp_common.utils.miscs as mu
from gmbp_quant.data_infra.core.security_attributes import infer_symbols

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


def read_secruity_attributes_single_symbol(data_file=None, symbol=None, data_dir=None, cols=None):
    if data_file is None:
        if data_dir is None or symbol is None:
            raise Exception('Please provide either data_file or both (symbol, data_dir) !')
        #
        data_file = os.path.join(data_dir, f'{symbol}.csv')
    #

    try:
        if cols is not None:
            cols = set(mu.iterable_to_tuple(cols, raw_type='str'))
            cols.update({'Symbol', 'DateId'})
            attributes = pd.read_csv(data_file, sep=',', usecols=list(cols))
        else:
            attributes = pd.read_csv(data_file, sep=',')
        #
    except Exception:
        logger.warn(f'Failed to read {data_file} !')
        attributes = None
    #
    return attributes
#


def read_secruity_attributes(universe, data_dir, cols=None):
    symbols = infer_symbols(universe=universe)

    ret = Parallel(n_jobs=-1)(delayed(read_secruity_attributes_single_symbol)(symbol=symbol,
                                                                              data_dir=data_dir,
                                                                              cols=cols)
                              for symbol in symbols)
    ret = pd.concat(ret, sort=False)
    ret.sort_values(['DateId', 'Symbol'])

    return ret
#
