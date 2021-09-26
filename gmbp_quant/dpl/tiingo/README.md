# Instructions of FMP Data Download, Parsing and DB Loading

## Install dependency
pip install -r ./dpl/fmp/requirements.txt

### Download, Parse and load data to DB staging tables
* Example:
```python:
    cd GMBPQuantPy/gmbp_quant
    
    python dpl/tiingo/download_tiingo.py  --data ./tiingo_data --form daily_price --start_date 20200101 --end_date 20210319
    python dpl/tiingo/load_db_tiingo.py  --data ./tiingo_data --form daily_price 
    
```
