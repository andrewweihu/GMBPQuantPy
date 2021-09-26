# Instructions of Polygon Data Download, Parsing and DB Loading

## Install dependency
pip install -r ./dpl/polygon/requirements.txt

### Download, Parse and load data to DB staging tables
* Example:
```python:
    cd GMBPQuantPy/gmbp_quant
    
    python dpl/polygon/download_polygon.py  --data ./polygon_data --form company 
    python dpl/polygon/load_db_polygon.py  --data ./polygon_data --form company  
    
```
