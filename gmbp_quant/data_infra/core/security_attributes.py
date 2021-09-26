import os
import traceback
from enum import Enum
import pandas as pd
from gmbp_common.utils import miscs as mu
from gmbp_common.data import indexes as cdi
from gmbp_quant.dpl.fmp.fmp_company_valuation_api import request_mktcap_historical, request_dcf_historical, request_rating_historical

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


class Universe(Enum):
    SP_500 = 'S&P 500'
    RUSSELL_3000 = 'RUSSELL 3000'
#


def infer_symbols(universe):
    universe = set(mu.iterable_to_tuple(universe, raw_type='str'))

    def get_symbols(mnemonic):
        try:
            mnemonic = Universe[mnemonic.upper()]
        except:
            pass
        #
        if mnemonic == Universe.SP_500:
            symbols = set(cdi.get_sp500_instruments()['Symbol'].tolist())
        elif mnemonic == Universe.RUSSELL_3000:
            alive, delisted = cdi.get_russell_3000_instruments()
            symbols = set(alive['Symbol'].tolist()).union(set(delisted['Symbol'].tolist()))
        else:
            symbols = set(mu.iterable_to_tuple(mnemonic, raw_type='str'))
        #
        return symbols
    #

    symbols = set()
    for mnemonic in universe:
        symbols.update(get_symbols(mnemonic=mnemonic))
    #
    symbols = sorted(symbols)

    return symbols
#


def request_secruity_attributes_historical(universe, output_dir=None):
    symbols = infer_symbols(universe=universe)

    attributes_univese = list()
    for symbol in symbols:
        mktcap = request_mktcap_historical(symbol=symbol)
        mktcap.rename(columns={'symbol': 'Symbol', 'date': 'Date', 'marketCap': 'MktCap'}, inplace=True)

        dcf = request_dcf_historical(symbol=symbol)
        dcf.rename(columns={'symbol': 'Symbol', 'date': 'Date', 'dcf': 'DCF'}, inplace=True)

        rating = request_rating_historical(symbol=symbol)
        cols = ['symbol','date','ratingScore','ratingDetailsDCFScore','ratingDetailsROEScore',
                'ratingDetailsROAScore','ratingDetailsDEScore','ratingDetailsPEScore','ratingDetailsPBScore']
        cols = [col for col in cols if col in rating.columns]
        rating = rating[cols]
        rating.columns = [col.capitalize() for col in cols]

        try:
            attributes = pd.merge(mktcap, dcf, on=['Symbol','Date'], how='outer', sort=False)
            attributes = pd.merge(attributes, rating, on=['Symbol', 'Date'], how='outer', sort=False)
            attributes['Date'] = attributes['Date'].dt.strftime('%Y%m%d').astype(int)
            attributes.rename(columns={'Date':'DateId'}, inplace=True)
            attributes.sort_values(['Symbol','DateId'], ascending=True, inplace=True)
        except:
            logger.warn(f"Failed to get attributes for symbol={symbol} !")
            traceback.print_exc()
            attributes = None
        #

        if attributes is None:
            continue
        #

        if output_dir is not None:
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f'{symbol}.csv')
            attributes.to_csv(output_file, sep=',', index=False)
        else:
            attributes_univese.append(attributes)
        #
    #

    attributes_univese = pd.concat(attributes_univese, sort=False) if output_dir is None else None
    return attributes_univese
#

