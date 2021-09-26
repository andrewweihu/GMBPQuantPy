import argparse

from yahoo_data_loader import YahooDataLoader
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str, default='./yahoo_data', help='Yahoo data folder')
parser.add_argument('--form', type=str, help='Yahoo form type')
opt = parser.parse_args()


if __name__ == '__main__':
    data_dir = Path(opt.data)
    form_type = opt.form

    yahoo_loader = YahooDataLoader(data_dir, form_type)

    if form_type == 'ipo':
        print(f'Parsing Yahoo IPO data to tsv files ...')
        yahoo_loader.parse_ipo_to_tsv()
    elif form_type == 'holders':
        print(f'Yahoo holder data have been parsed to tsv in download step ...')
    elif form_type == 'daily_price':
        print(f'Parsing Yahoo Daily Price data to tsv files ...')
        yahoo_loader.parse_daily_price_to_tsv()
    elif form_type == 'stats':
         print(f'Parsing Yahoo Stats data to tsv files ...')
         yahoo_loader.parse_stats_to_tsv()

    print(f'Inserting parsed Yahoo {form_type} data to DB ...')
    yahoo_loader.insert_db()