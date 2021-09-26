import gmbp_quant.dal.sec_master_v0.sec_master as smv0sm

def get_all_tickers(data_source='SMV0'):
    if data_source == 'SMV0':
        return set(smv0sm.get_symbol_2_sid().keys())
    #

    raise ValueError(f'"data_source"={data_source} is not supported in [SMV0] !')
#
