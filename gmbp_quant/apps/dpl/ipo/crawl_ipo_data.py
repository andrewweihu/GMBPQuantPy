import os, sys
import pandas as pd
import gmbp_common.utils.datetime_utils as dtu

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


def crawl_ipo_data_single_date(dateid, source='YAHOO'):
    datestr = dtu.dateid_to_datestr(dateid=dateid)

    if source == 'YAHOO':
        url = f'https://finance.yahoo.com/calendar/ipo?day={datestr}'
    else:
        raise ValueError(f'source={source} is not supported in [YAHOO] !')
    #

    ipo_data_raw = pd.read_html(url)
    
    if len(ipo_data_raw) == 0:
        logger.info(f'No IPO data found for date={dateid}')
        return None
    if len(ipo_data_raw) > 2:
        logger.warn(f'len(ipo_data)={len(ipo_data_raw)} is not expected !')
    #
    
    ipo_types = ['Pricings', 'Filings']
    ipo_data = list()
    for i, data in enumerate(ipo_data_raw):
        data['IPOType'] = ipo_types[i]
        ipo_data.append(data)
    #
    ipo_data = pd.concat(ipo_data, sort=False)
    ipo_data.columns = [col.replace(' ', '') for col in ipo_data.columns]

    ipo_data['Date'] = pd.to_datetime(ipo_data['Date'])
    ipo_data.replace(to_replace={'-': None}, inplace=True)
    ipo_data['Price'] = ipo_data['Price'].astype(float)
    ipo_data['Shares'] = ipo_data['Shares'].astype(float)
    ipo_data['PriceRange'] = ipo_data['PriceRange'].astype(str)
    
    return ipo_data
#


def setup_cli_options(parser=None):
    if parser is None:
        from optparse import OptionParser, IndentedHelpFormatter
        parser = OptionParser(formatter=IndentedHelpFormatter(width=200), epilog='\n')
    #

    today = dtu.today()
    parser.add_option('-E', '--end_date',
                      dest='end_date', default=today,
                      help=f'Default: Current Trading Date {today} .')
    parser.add_option('-S', '--start_date',
                      dest='start_date', default=None,
                      help=f'Default: If not provided, it will get inferred according to "date_range_mode" .')
    parser.add_option('-R', '--date_range_mode',
                      dest='date_range_mode', default='SINGLE_DATE',
                      help=f'Default: %default. Supported values are [SINGLE_DATE|ROLLING_WEEK|ROLLING_MONTH] .')
    parser.add_option('-f', '--output_file',
                      dest='output_file', default=None,
                      help='Output IPO file. If not provided, then the output file will be inferred from "output_dir" .')
    parser.add_option('-o', '--output_dir',
                      dest='output_dir', default=None,
                      help='Output IPO file directory. If provided, the output file(s) will be inferred as "ipo.YYYYMMDD.csv" .')

    return parser
#


if __name__ == '__main__':
    logger.info(' '.join(sys.argv))

    options, args = setup_cli_options().parse_args()

    output_file = options.output_file
    if output_file is None:
        if options.output_dir is None:
            raise Exception(f'Please provide either "output_file" or "output_dir" !')
        #
    #

    start_dateid, end_dateid = dtu.infer_start_dateid_end_dateid(start_date=options.start_date, end_date=options.end_date,
                                                                 date_range_mode=options.date_range_mode)
    dateids = dtu.infer_biz_dateids(start_dateid=start_dateid, end_dateid=end_dateid)

    for dateid in dateids:
        ipo_data = crawl_ipo_data_single_date(dateid=dateid, source='YAHOO')
        if ipo_data is None:
            continue
        #
        if output_file is None:
            output_file = os.path.join(options.output_dir, f'ipo.{dateid}.csv')
        #
        ipo_data.to_csv(output_file, sep=',', index=False)
        logger.info(f'ipo_data on date={dateid} -> {output_file}')
    #
#
