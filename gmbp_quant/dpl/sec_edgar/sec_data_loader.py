import re
import io
import sys
import yaml
import pandas as pd
import lxml.etree as et
from pathlib import Path
from tqdm import tqdm
from bs4 import BeautifulSoup

from gmbp_common.logger import LOG
from gmbp_quant.dpl.base.data_loader import DataLoader
from gmbp_quant.dpl.sec_edgar.sec_schemas import (
    Sec13FHRSchema, Sec13FHRASchema,
    Sec4NonDerivativeSchema, Sec4DerivativeSchema, Sec4ReportingOwnerSchema,
    Sec3NonDerivativeSchema, Sec3DerivativeSchema, Sec3ReportingOwnerSchema,
    SecS3Schema, SecS1Schema, Sec144Schema)

schemas = {
    'Sec13FHRSchema': Sec13FHRSchema,
    'Sec13FHRASchema': Sec13FHRASchema,
    'Sec4NonDerivativeSchema': Sec4NonDerivativeSchema,
    'Sec4DerivativeSchema': Sec4DerivativeSchema,
    'Sec4ReportingOwnerSchema': Sec4ReportingOwnerSchema,
    'Sec3NonDerivativeSchema': Sec3NonDerivativeSchema,
    'Sec3DerivativeSchema': Sec3DerivativeSchema,
    'Sec3ReportingOwnerSchema': Sec3ReportingOwnerSchema,
    'SecS3Schema': SecS3Schema,
    'SecS1Schema': SecS1Schema,
    'Sec144Schema': Sec144Schema
}

logger = LOG.get_logger(__name__)


class SecEdgarDataLoader(DataLoader):
    """A :class:`SecEdgarDataLoader` class

    Args:
        data_dir: folder storing SEC EDGAR data
        form_type: SEC form type, currently support
                    '13F-HR'
                    '13F-HRA'
                    '4-NonDerivative'
                    '4-Derivative'
                    '3-NonDerivative'
                    '3-Derivative'
                    'S-3'
        year: year of SEC reporting
        quarter: quarter of SEC reporting
    """

    def __init__(self, data_dir, form_type, year, quarter):

        self.data_dir = Path(data_dir)
        self.form_type = form_type
        # xsl_file is optional depending on form_type
        self.xsl_file = Path(__file__).parent / 'xsl_files' / f'{form_type}.xsl'

        sec_yml_path = Path(__file__).parent / 'sec_forms.yml'
        with open(sec_yml_path, 'r') as yamlfile:
            self.sec_yml = yaml.load(yamlfile, Loader=yaml.FullLoader)

        self.form_dir = self.data_dir / self.sec_yml[form_type]['form_folder'] / year / quarter
        self.form_list = list(self.form_dir.glob('*.txt'))
        self.tsv_dir = self.data_dir / 'tsv_files' / form_type / year / quarter
        self.tsv_dir.mkdir(parents=True, exist_ok=True)
        self.year, self.quarter = year, quarter

        self._db_name = 'mktdata'
        self._schema = schemas[self.sec_yml[form_type]['schema']]
        self.table_keyword = self.sec_yml[form_type].get('table_keyword', "")

        super().__init__(data_dir, form_type, self.tsv_dir, self._db_name, self._schema)

    def get_essentials_from_txt(self, xml_txt, document_id):
        """Get essential fields from xml text.
        """
        rows = xml_txt.split('\n')
        cik_regex = re.compile(self.sec_yml['cik'], re.I)
        essentials_regex = {}
        for k, v in self.sec_yml[self.form_type]['essentials'].items():
            essentials_regex[k] = re.compile(v, re.I)  # re.I means ignore case

        # get regex dict by form type
        essentials = {}
        num_essentials = len(essentials_regex) + 1  # the extra 1 is for "cik"
        for row in rows:
            for k, v in essentials_regex.items():
                if k not in essentials and v.search(row):
                    essentials[k] = v.search(row).group(1).strip()
                    num_essentials -= 1
            if 'cik' not in essentials and cik_regex.search(row):
                essentials['cik'] = cik_regex.search(row).group(1)
                num_essentials -= 1
            # check if we get all essential fields
            if num_essentials == 0:
                return essentials
        if num_essentials != 0:
            print("Encountered a parsing problem in document_id = {}.".format(document_id))
            print("{} essential fields are not found compared to the sec_forms.yml file plus cik! \
            We only found essentials = {}".format(num_essentials, essentials))
        
        # assign `NA` to missing fields           
        essentials = {
            k: essentials[k] if k in essentials else 'NA' for k in list(essentials_regex.keys()) + ['cik']}
        return essentials

    def _extract_body_by_xsl(self, soup, output_path):
        """
        Extract data from xml_data and write it to file output_path.

        :return: bool. False means this sec file should be skipped
                 and the file output_path is not written.
        """
        table_re = re.compile(f'^{self.table_keyword}', re.I)
        if soup.find(table_re):
            soup.find(table_re).attrs = {}
        else:
            return False

        data_table = soup.find(table_re)
        # check if table is empty
        if data_table is None:
            return False

        with open(self.xsl_file, 'r') as f:
            xslt = et.parse(f)

        dom = et.parse(io.StringIO(data_table.prettify()))
        transform = et.XSLT(xslt)
        tsv_data = transform(dom)

        with open(output_path, 'w') as f:
            f.write(str(tsv_data))
        return True

    def _extract_body_table_by_bs(
            self, soup, output_path,
            columns=(),
            must_contain_words=()):
        """
        Extract data from the nth_table (0-indexed) in xml_data.
        The column names are columns.

        :param xml_data: str. The downloaded sec file.
        :param output_path: str representing path of .tsv format, saving the extracted data.
        :param columns: tuple of str, columns names of the table
        :param must_contain_words: tuple of str, the words that must exist in the table. We use word one by one to filter the tables
                                    until only one table is left
        :return: bool. False means we should drop this file.
        """
        tables = soup.findAll("table")
        for word in must_contain_words:
            word = word.lower()
            if len(tables) == 0:
                return False
            if len(tables) == 1:
                break
            tables = [table for table in tables if word in table.text.lower()]
        if len(tables) != 1:
            # Failure: there are more than 1 table that meet the requirement.
            return False
        table = tables[0]
        values = []
        for row in table.findAll("tr"):
            cur_values = []
            cells = row.findAll("td")

            for cell in cells:
                if cell.text.strip():
                    cur_values.append(cell.text.strip())
            if len(cur_values) != len(columns):
                # Row skipped because length of this row and size of columns are inconsistent
                continue
            values.append(cur_values)
        values = values[1:]  # skip the first row of table names
        if not values:  # extraction failure
            return False
        values = list(zip(*values))
        values_dict = {columns[i]: values[i] for i in range(len(columns))}
        df = pd.DataFrame(values_dict, columns=columns)
        df.to_csv(output_path, sep='\t', index=False)
        return True

    def _extract_body(self, soup, output_path):
        """
        :return: bool. False means we should drop this file.
        """
        if self.form_type in ("13F-HR", "13F-HRA", "4-NonDerivative", "4-Derivative", "4-ReportingOwner",
                              "3-NonDerivative", "3-Derivative", '3-ReportingOwner'):  # xsl
            return self._extract_body_by_xsl(soup, output_path)
        elif self.form_type in ("S-1", "S-3"):
            # TODO(weimin): move columns and must_contain_words to yml files,
            #  so that users don't have to change code when those keywords changed.
            return self._extract_body_table_by_bs(
                soup, output_path,
                columns=("title_of_each_class", "amount_of_each_class", "max_offering_price",
                         "max_aggregate_price", "registration_fee"),
                must_contain_words=("each class", "register", "fee", "amount", "price",
                                    "offering price", "registration fee"))
        elif self.form_type == "144":
            return True
        print("The form type of {} can not be handled by sec_data_loader.py.".format(self.form_type))
        return False

    def parse_forms_to_tsv(self):
        """Parse SEC forms and save to tsv files.
        Parsed data is stored in TSV format as comma is often used in field value.
        """
        for form in tqdm(self.form_list):
            with open(form, 'r') as f:
                xml_data = f.read()

            # Get CIK and dates by scanning line by line
            essentials = self.get_essentials_from_txt(xml_data, form.stem)
            output_path = self.tsv_dir / f'{form.stem}.tsv'

            # Group all namespace tag
            soup = BeautifulSoup(xml_data, 'lxml')
            namespace_re = re.compile('^.+\:.+$', re.I)
            tag_name_re = re.compile('^.+\:(.+)$', re.I)
            for tag in soup.find_all(namespace_re):
                tag.name = tag_name_re.match(tag.name).group(1)

            # Extract information from the body of the forms
            if not self._extract_body(soup, output_path):
                # TODO(weimin): don't skip this form,
                #  still inject this form into db with "NA".
                continue

            # Fill in essential fields
            if Path(output_path).exists():
                tsv_data = pd.read_csv(output_path, sep='\t')
                for k, v in essentials.items():
                    tsv_data[k] = v
            else:
                # In case extraction by .yml will be enough,
                # or the main body has missing data
                tsv_data = pd.DataFrame(essentials, index=[0])

            tsv_data['document_id'] = form.stem
            tsv_data.to_csv(output_path, sep='\t', index=False)
