import os, sys
import gmbp_quant.env_config as ecfg
import gmbp_common.utils.datetime_utils as dtu
from gmbp_quant.dpl.polygon.polygon_reference_api import request_tickers_v2, request_tickers_v3

from gmbp_common.logger import LOG
logger = LOG.get_logger(__name__)


def setup_cli_options(parser=None):
    if parser is None:
        from optparse import OptionParser, IndentedHelpFormatter
        parser = OptionParser(formatter=IndentedHelpFormatter(width=200), epilog='\n')
    #

    parser.add_option('-o', '--output_dir',
                      dest='output_dir', default=None,
                      help='Output tickers file directory. If provided, the output file(s) will be "{OUTPUT_DIR}/polygon_tickers.page[page_no].[TODAY].csv" .')
    parser.add_option('-C', '--connection_env',
                      dest='connection_env', default='RESEARCH',
                      help=f'Default: %default .')
    parser.add_option('-v', '--polygon_tickers_api_version',
                      dest='polygon_tickers_api_version', default='v3',
                      help=f'Default: %default .')

    return parser
#


if __name__ == '__main__':
    logger.info(' '.join(sys.argv))

    options, args = setup_cli_options().parse_args()

    connection_env = options.connection_env
    ecfg.get_env_config(env=connection_env)
    logger.info(f'connection environment is {ecfg.get_env_config().env}')

    output_dir = options.output_dir
    if options.polygon_tickers_api_version.lower()=='v2':
        tickers = request_tickers_v2(output_dir=output_dir)
    elif options.polygon_tickers_api_version.lower()=='v3':
        tickers = request_tickers_v3(output_dir=output_dir)
    else:
        raise Exception(f"polygon_tickers_api_version={options.polygon_tickers_api_version} is not supported in [v2|v3] !")
    #

    if output_dir is not None:
        dateid = dtu.today()
        output_file = os.path.join(output_dir, f'polygon_tickers.{dateid}.pkl.gz')
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        tickers.to_pickle(output_file, compression='gzip')
        logger.info(f'All polygon tickers -> {output_file}')
    #
#
