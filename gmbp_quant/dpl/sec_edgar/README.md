# Instructions of SEC Data Download, Parsing and DB Loading

## Install dependency
```pip install -r ./requirements.txt```

check the root README.md to get more details.

## Patch secutils edgar.py
Because the original edgar.py in the `secutils` package does not specify header info in `urlretrieve`, it sometimes trigger "HTTP 403 Forbidden" error when SEC Edgar server enforces header information. I added a patch to fix it, but it requires a manual patch as follows:
* CD into gmbp_quant/dpl/sec_edgar/secutils_patch folder
* Run `python patch_secutils.py`

## In daily or monthly operation
### Step 1: Download form data from SEC EDGAR
* Modify the variables of start_year, end_year, quarters and form_types in `download_forms.sh` to specify what forms you want to download. For example, if you want to download "form 4", set `--form_types 4`; if you want to download "form 13F-HR", set `--form_types 13F-HR`, etc.
* `sec-utils` supports downloading multiple years/quarters at the same time.
* Run `download_forms.sh`
### Step 2: Parse and load data to DB staging tables
* load_db.py does parsing and data injection to database. To use the script, follow examples below. Note: Pass in data folder that holds SEC data downloaded by `sec-utils`. Separate year/quarter with `,` and no space.
Example:
```python:
# Get into GMBPQuantPy repo folder and assume SEC data are in gmbp_quant/dpl/sec_edgar/sec_data
# Parse 13F-HR data for all year 2019, 2020, and load data to database
python gmbp_quant/dpl/sec_edgar/load_db.py --form 13F-HR --year 2019,2020 --quarter Q1,Q2,Q3,Q4 --data gmbp_quant/dpl/sec_edgar/sec_data

# Parse form 3 tables, and load data to database
python gmbp_quant/dpl/sec_edgar/load_db.py --form 3-NonDerivative --year 2019,2020 --quarter Q1,Q2,Q3,Q4 --data gmbp_quant/dpl/sec_edgar/sec_data
python gmbp_quant/dpl/sec_edgar/load_db.py --form 3-Derivative --year 2019,2020 --quarter Q1,Q2,Q3,Q4 --data gmbp_quant/dpl/sec_edgar/sec_data
python gmbp_quant/dpl/sec_edgar/load_db.py --form 3-ReportingOwner --year 2019,2020 --quarter Q1,Q2,Q3,Q4 --data gmbp_quant/dpl/sec_edgar/sec_data

# Parse form 4 tables, and load data to database
python gmbp_quant/dpl/sec_edgar/load_db.py --form 4-NonDerivative --year 2019,2020 --quarter Q1,Q2,Q3,Q4 --data gmbp_quant/dpl/sec_edgar/sec_data
python gmbp_quant/dpl/sec_edgar/load_db.py --form 4-Derivative --year 2019,2020 --quarter Q1,Q2,Q3,Q4 --data gmbp_quant/dpl/sec_edgar/sec_data
python gmbp_quant/dpl/sec_edgar/load_db.py --form 4-ReportingOwner --year 2019,2020 --quarter Q1,Q2,Q3,Q4 --data gmbp_quant/dpl/sec_edgar/sec_data

# Parse sec form 144, and load data to database
python gmbp_quant/dpl/sec_edgar/load_db.py --form 144 --year 2019,2020 --quarter Q1,Q2,Q3,Q4 --data gmbp_quant/dpl/sec_edgar/sec_data
```

### Step 3: Automate data moving to save time
* `sec-utils` minimum download unit is one quarter. However, it automatically checks existing downloaded files for an ongoing quarter.
* One way to minimize operation cost is to move data that is already processed out of the `sec_data` folder so that the same data will not be parsed and injected again, run the `load_db.py` script, and then move the data back to the `sec_data` folder (so next day when we run `download_forms.sh`, `sec-utils` will skip existing files).