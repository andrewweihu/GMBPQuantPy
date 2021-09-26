# Instructions of Yahoo Data Download, Parsing and DB Loading

## Install dependency
pip install -r ./dpl/fmp/requirements.txt

### Download, Parse and load data to DB staging tables
* Example:
```python:
    cd GMBPQuantPy/gmbp_quant
    
    python dpl/yahoo/download_yahoo.py  --data ./yahoo_data --form ipo --ipo_date 20201209 
    python dpl/yahoo/load_db_yahoo.py  --data ./yahoo_data --form ipo 
    
    python dpl/yahoo/download_yahoo.py  --data ./yahoo_data --form holders
    python dpl/yahoo/load_db_yahoo.py  --data ./yahoo_data --form holders 
    
    python dpl/yahoo/download_yahoo.py  --data ./yahoo_data --form daily_price --start_date 01/01/2020 --end_date 03/09/2021
    python dpl/yahoo/load_db_yahoo.py  --data ./yahoo_data --form daily_price 
    
    python dpl/yahoo/download_yahoo.py  --data ./yahoo_data --form stats
    python dpl/yahoo/load_db_yahoo.py  --data ./yahoo_data --form stats 
```
