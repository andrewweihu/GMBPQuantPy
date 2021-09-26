import gmbp_quant.dal.sec_master_v0.mkt_data as smv0md


def query_security_day_price(symbols=None, start_dateid=None, end_dateid=None,
                             cols=None, data_source='SMV0'):
    if data_source == 'SMV0':
        return smv0md.query_security_day_price(symbols=symbols, start_dateid=start_dateid, end_dateid=end_dateid, cols=cols)
    #

    raise ValueError(f'"data_source"={data_source} is not supported in [SMV0] !')
#


def query_adj_closes(symbols=None, start_dateid=None, end_dateid=None,
                     data_source='SMV0'):
    if data_source == 'SMV0':
        adj_closes = smv0md.query_security_day_price(symbols=symbols,
                                                     start_dateid=start_dateid, end_dateid=end_dateid,
                                                     cols='time_x,TICKER,ADJ_CLOSE')
        adj_closes = adj_closes.pivot(index='time_x', columns='TICKER', values='ADJ_CLOSE')
        
        return adj_closes
    #

    raise ValueError(f'"data_source"={data_source} is not supported in [SMV0] !')
#
