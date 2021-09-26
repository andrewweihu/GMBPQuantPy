import argparse

from polygon_data_loader import PolygonDataLoader
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str, default='./polygon_data', help='Polygon form data folder')
parser.add_argument('--form', type=str, help='Polygon form type')
parser.add_argument('--report_date', type=str, help='Polygon data report_date')
opt = parser.parse_args()


if __name__ == '__main__':
    report_date = opt.report_date
    data_dir = Path(opt.data)
    form_type = opt.form

    if form_type == 'company':
        polygon_loader = PolygonDataLoader(data_dir, form_type)

        print(f'Parsing Polygon data to tsv files ...')
        polygon_loader.parse_company_to_tsv()

    print('Inserting parsed Polygon data to DB ...')
    polygon_loader.insert_db()