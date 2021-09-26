import os
import numpy as np
import pandas as pd
from gmbp_quant.dpl.polygon.polygon_reference_api import request_tickers_v3, request_stock_exchanges
from gmbp_quant.dpl.fmp.fmp_company_valuation_api import request_symbols_v3

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


def combine_stocks_basics(sid_mapping_file=None):
    secs_plg = request_tickers_v3()
    secs_plg = secs_plg[secs_plg['market'] == 'stocks']
    secs_plg.drop(columns=['currency_symbol','base_currency_symbol','base_currency_name'], inplace=True)
    secs_plg.columns = ['Symbol', 'Name', 'Market', 'Country', 'MIC',
                        'SecurityType', 'IsActive', 'Currency', 'CIK', 'CompositeFIGI',
                        'ShareClassFIGI', 'LastUpdatedUTC']
    secs_plg.sort_values(['ShareClassFIGI','LastUpdatedUTC'], ascending=True, inplace=True)
    secs_plg_valid = secs_plg[secs_plg['ShareClassFIGI'].notnull()]
    cnt_before = len(secs_plg_valid)
    secs_plg_valid = secs_plg_valid.drop_duplicates(subset=['ShareClassFIGI',], keep='last')
    cnt_after = len(secs_plg_valid)
    logger.info(f"Dropped {cnt_before-cnt_after} records with duplicated 'ShareClassFIGI'. "
                f"The total number of valid 'ShareClassFIGI' is {cnt_after}")
    secs_plg = pd.concat([secs_plg_valid, secs_plg[secs_plg['ShareClassFIGI'].isnull()]], sort=False)

    secs_fmp = request_symbols_v3()
    secs_fmp.columns = ['Symbol', 'Name', 'Exchange']

    secs = pd.merge(secs_plg, secs_fmp, on='Symbol', how='outer', suffixes=('.PLG', '.FMP'))
    secs['Name.PLG'] = np.where(secs['Name.PLG'].isnull(), secs['Name.FMP'], secs['Name.PLG'])
    secs.drop(columns=['Name.FMP'], inplace=True)
    secs.rename(columns={'Name.PLG': 'Name'}, inplace=True)

    in_plg_only = secs[(secs['Market'].notnull()) & (secs['Exchange'].isnull())]
    in_fmp_only = secs[(secs['Market'].isnull()) & (secs['Exchange'].notnull())]
    in_both = secs[(secs['Market'].notnull()) & (secs['Exchange'].notnull())]

    stats = {'#TOTAL': len(secs), '#PLG_ONLY': len(in_plg_only), '#FMP_ONLY': len(in_fmp_only), '#BOTH': len(in_both)}
    logger.info(f"The number of securities are:\n{pd.Series(stats).to_frame().T}")

    exchanges = request_stock_exchanges()
    exchanges = exchanges[['mic','name']].rename(columns={'mic':'MIC','name':'ExchangeName'})
    secs_valid_mic = pd.merge(secs[secs['MIC'].notnull()], exchanges, on='MIC', how='left', sort=False)
    secs_valid_mic['Exchange'] = np.where(secs_valid_mic['Exchange'].isnull(),
                                          secs_valid_mic['ExchangeName'], secs_valid_mic['Exchange'])
    secs_valid_mic.drop(columns=['ExchangeName'], inplace=True)
    secs = pd.concat([secs_valid_mic, secs[secs['MIC'].isnull()]], sort=False)
    # secs.drop(columns=['PrimaryExchange'], inplace=True)

    if sid_mapping_file is not None:
        try:
            sid_mapping = pd.read_csv(sid_mapping_file, sep=',')
            logger.info(f"Loaded {sid_mapping.shape} records from {sid_mapping_file}")
        except:
            os.makedirs(os.path.dirname(sid_mapping_file), exist_ok=True)
            sid_mapping = None
        #

        if sid_mapping is None or len(sid_mapping) == 0:
            logger.warn(f"No existing valid SecurityId Mapping found from {sid_mapping_file}!")
            secs.index.name = 'SID'
            secs.reset_index(inplace=True)
            secs['SID'] += 1
            sid_mapping = secs[['SID', 'Symbol', 'MIC', 'Exchange', 'ShareClassFIGI']]
        else:
            secs = pd.merge(sid_mapping, secs, on=['Symbol','MIC','Exchange'], how='right', sort=False)
            new_secs = secs[secs['SID'].isnull()]
            num_new_secs = len(new_secs)
            if num_new_secs>1:
                next_sid = sid_mapping['SID'].max()+1
                secs.loc[secs['SID'].isnull(), 'SID'] = range(next_sid, next_sid+num_new_secs)
                sid_mapping = pd.concat([sid_mapping, secs[['SID','Symbol','MIC','Exchange']]], sort=False).drop_duplicates(keep='last')
                logger.info(f"{len(new_secs)} NEW sid_mapping added.")
            #
        #
        sid_mapping.to_csv(sid_mapping_file, sep=',', index=False)
        logger.info(f"sid_mapping {sid_mapping.shape} -> {sid_mapping_file} ")
    #

    return secs, secs_plg, secs_fmp
#


