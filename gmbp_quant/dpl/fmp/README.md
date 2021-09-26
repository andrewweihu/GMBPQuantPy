# Instructions of FMP Data Download, Parsing and DB Loading

## Install dependency
pip install -r ./dpl/fmp/requirements.txt

### Download, Parse and load data to DB staging tables
* Example:
```python:
    cd GMBPQuantPy/gmbp_quant
    
    python dpl/fmp/download_fmp.py  --data ./fmp_data --form 13F --report_date 2020-12-31
    python dpl/fmp/load_db_fmp.py  --data ./fmp_data --form 13F --report_date 2020-12-31
   
    python dpl/fmp/download_fmp.py  --data ./fmp_data --form inst_holder
    python dpl/fmp/load_db_fmp.py  --data ./fmp_data --form inst_holder 
    
    python dpl/fmp/download_fmp.py  --data ./fmp_data --form mutual_fund_holder
    python dpl/fmp/load_db_fmp.py  --data ./fmp_data --form mutual_fund_holder
    
    python dpl/fmp/download_fmp.py  --data ./fmp_data --form insider_trading
    python dpl/fmp/load_db_fmp.py  --data ./fmp_data --form insider_trading 
    
    python dpl/fmp/download_fmp.py  --data ./fmp_data --form etf_holder
    python dpl/fmp/load_db_fmp.py  --data ./fmp_data --form etf_holder 
    
    python dpl/fmp/download_fmp.py  --data ./fmp_data --form company_profile
    python dpl/fmp/load_db_fmp.py  --data ./fmp_data --form company_profile 
    
    python dpl/fmp/download_fmp.py  --data ./fmp_data --form enterprise_value
    python dpl/fmp/load_db_fmp.py  --data ./fmp_data --form enterprise_value 

    python dpl/fmp/download_fmp.py  --data ./fmp_data --form stock_split
    python dpl/fmp/load_db_fmp.py  --data ./fmp_data --form stock_split 
    
    python dpl/fmp/download_fmp.py  --data ./fmp_data --form yearly_ratios
    python dpl/fmp/load_db_fmp.py  --data ./fmp_data --form yearly_ratios
    
    python dpl/fmp/download_fmp.py  --data ./fmp_data --form quarterly_ratios
    python dpl/fmp/load_db_fmp.py  --data ./fmp_data --form quarterly_ratios
    
    python dpl/fmp/download_fmp.py  --data ./fmp_data --form ratios_ttm
    python dpl/fmp/load_db_fmp.py  --data ./fmp_data --form ratios_ttm
    
    python dpl/fmp/download_fmp.py  --data ./fmp_data --form yearly_income_statement
    python dpl/fmp/load_db_fmp.py  --data ./fmp_data --form yearly_income_statement
    
    python dpl/fmp/download_fmp.py  --data ./fmp_data --form quarterly_income_statement
    python dpl/fmp/load_db_fmp.py  --data ./fmp_data --form quarterly_income_statement
    
    python dpl/fmp/download_fmp.py  --data ./fmp_data --form etf_list
    python dpl/fmp/load_db_fmp.py  --data ./fmp_data --form etf_list

    python dpl/fmp/download_fmp.py  --data ./fmp_data --form cik_map
    python dpl/fmp/load_db_fmp.py  --data ./fmp_data --form cik_map
    
    python dpl/fmp/load_db_fmp.py  --data ./fmp_data --form cik_sec_map
    
    python dpl/fmp/download_fmp.py  --data ./fmp_data --form sector_performance
    python dpl/fmp/load_db_fmp.py  --data ./fmp_data --form sector_performance
    
    python dpl/fmp/download_fmp.py  --data ./fmp_data --form 10-Q --start_year 2020 --end_year 2020 --quarters Q4
    python dpl/fmp/load_db_fmp.py  --data ./fmp_data --form 10-Q
    
    python dpl/fmp/download_fmp.py  --data ./finnhub_data --form finnhub_sentiment
    python dpl/fmp/load_db_fmp.py  --data ./finnhub_data --form finnhub_sentiment
    
    # The command below can not be used yet, because the Finnhub token has not been authorized.
    python dpl/fmp/download_fmp.py  --data ./finnhub_data --form finnhub_etf_holdings
    python dpl/fmp/load_db_fmp.py  --data ./finnhub_data --form finnhub_etf_holdings
```

Note:
1. cik_sec_map data is downloaded directly from: 
       https://www.sec.gov/Archives/edgar/cik-lookup-data.txt
   Below command is used to convert it into TSV format with manually added header:
       sed -r 's/:([0-9]{10}):/\t\1/g' cik-lookup-data.txt
2. refer to this pull request to learn how to change code base to add a table: 
   https://github.com/GMBPClub/GMBPQuantPy/pull/36/files
   
3. mktdata.calendar_date table is created for Superset dashboard to join/fill in missing dates. It was created by direct SQL query:

    CREATE TABLE mktdata.test('date' DATE);

    INSERT INTO mktdata.test ('date') VALUES ('2020-01-01'); [repeat...]