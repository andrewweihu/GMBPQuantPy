import numpy as np

from gmbp_quant.mdpalgo.mdp_algo import max_div_portf
from py_datasource.DataTable import get_multi_daily_close_px
from py_helper.py_helper import get_nonzero_array
from py_security.security import Security



# tickers = sys.argv[1].split(",")
# print(tickers)
tickers = [
"MSFT.US",
"AAPL.US"
           ]

security = Security()
start = "2020-04-07 00:00:00"
end = "2021-04-07 00:00:00"

px = get_multi_daily_close_px(security, start=start, end=end, ticker=tickers, inv=1)  # get px
px = get_nonzero_array(px)

weights = [1 / len(tickers)] * len(tickers)  # weights

# run mdp
rtn = np.array([np.diff(np.log(x)) for x in px])  # get log rtn
v = np.cov(rtn)  # get cov matrix
w = max_div_portf(weights, v, lmd=3)  # optimized weight
print(w)