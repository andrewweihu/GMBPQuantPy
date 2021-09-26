import argparse

from fmp_data_loader import FmpDataLoader
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str, default='./fmp_data', help='FMP form data folder')
parser.add_argument('--form', type=str, help='FMP form type')
parser.add_argument('--report_date', type=str, help='FMP data report_date')
opt = parser.parse_args()


if __name__ == '__main__':
    report_date = opt.report_date
    data_dir = Path(opt.data)
    form_type = opt.form

    if form_type == 'inst_holder':
        fmp_loader = FmpDataLoader(data_dir, form_type)

        print(f'Parsing FMP data to tsv files ...')
        fmp_loader.parse_inst_holder_to_tsv()

    if form_type == 'mutual_fund_holder':
        fmp_loader = FmpDataLoader(data_dir, form_type)

        print(f'Parsing FMP data to tsv files ...')
        fmp_loader.parse_mutual_fund_holder_to_tsv()

    elif form_type == 'insider_trading':
        fmp_loader = FmpDataLoader(data_dir, form_type)

        print(f'Parsing FMP data to tsv files ...')
        fmp_loader.parse_insider_trading_to_tsv()

    elif form_type == '10Q':
        fmp_loader = FmpDataLoader(data_dir, form_type)

        print(f'Parsing FMP data to tsv files ...')
        fmp_loader.parse_10q_to_tsv()

    elif form_type == '10-K':
        fmp_loader = FmpDataLoader(data_dir, form_type)

        print(f'Parsing FMP data to tsv files ...')
        fmp_loader.parse_10k_to_tsv()

    elif form_type == 'shares_float':
        fmp_loader = FmpDataLoader(data_dir, form_type)

        print(f'Parsing FMP data to tsv files ...')
        fmp_loader.parse_shares_float_to_tsv()

    elif form_type == 'etf_holder':
        fmp_loader = FmpDataLoader(data_dir, form_type)

        print(f'Parsing FMP data to tsv files ...')
        fmp_loader.parse_etf_holder_to_tsv()

    elif form_type == 'cik_map':
        fmp_loader = FmpDataLoader(data_dir, form_type)

        print(f'Parsing CIK map data to tsv files ...')
        fmp_loader.parse_cik_map_to_tsv()

    elif form_type == 'cik_sec_map':
        fmp_loader = FmpDataLoader(data_dir, form_type)
        # Do nothing

    elif form_type == 'company_profile':
        fmp_loader = FmpDataLoader(data_dir, form_type)

        print(f'Parsing FMP data to tsv files ...')
        fmp_loader.parse_company_profile_to_tsv()

    elif form_type == 'enterprise_value':
        fmp_loader = FmpDataLoader(data_dir, form_type)

        print(f'Parsing FMP data to tsv files ...')
        fmp_loader.parse_enterprise_value_to_tsv()

    elif form_type == 'stock_split':
        fmp_loader = FmpDataLoader(data_dir, form_type)

        print(f'Parsing FMP data to tsv files ...')
        fmp_loader.parse_stock_split_to_tsv()

    elif form_type in ("yearly_income_statement", "quarterly_income_statement"):
        fmp_loader = FmpDataLoader(data_dir, form_type)

        print(f'Parsing FMP data to tsv files ...')
        fmp_loader.parse_income_statement_to_tsv()

    elif form_type == "10-Q":
        fmp_loader = FmpDataLoader(data_dir, form_type)

        print(f'Parsing FMP data to tsv files ...')
        fmp_loader.parse_10_Q_to_tsv()

    elif form_type in ("yearly_ratios", "quarterly_ratios"):
        fmp_loader = FmpDataLoader(data_dir, form_type)

        print(f'Parsing FMP data to tsv files ...')
        fmp_loader.parse_ratios_to_tsv()

    elif form_type == "ratios_ttm":
        fmp_loader = FmpDataLoader(data_dir, form_type)

        print(f'Parsing FMP data to tsv files ...')
        fmp_loader.parse_ratios_ttm_to_tsv()

    elif form_type == 'etf_list':
        fmp_loader = FmpDataLoader(data_dir, form_type)

        print(f'Parsing FMP data to tsv files ...')
        fmp_loader.parse_etf_list_to_tsv()

    elif form_type == 'sector_performance':
        fmp_loader = FmpDataLoader(data_dir, form_type)

        print(f'Parsing FMP sector performance to tsv files ...')
        fmp_loader.parse_sector_performance_to_tsv()

    elif form_type == 'finnhub_sentiment':
        fmp_loader = FmpDataLoader(data_dir, form_type)

        print(f'Parsing Finnhub sentiment to tsv files ...')
        fmp_loader.parse_finnhub_sentiment_to_tsv()

    elif form_type == 'finnhub_etf_holdings':
        fmp_loader = FmpDataLoader(data_dir, form_type)

        print(f'Parsing Finnhub ETF Holdings to tsv files ...')
        fmp_loader.parse_finnhub_etf_holdings_to_tsv()

    else:
        fmp_loader = FmpDataLoader(data_dir, form_type, report_date)

        print(f'Parsing FMP data to tsv files ...')
        fmp_loader.parse_form_13_to_tsv()

    print('Inserting parsed FMP data to DB ...')
    fmp_loader.insert_db()